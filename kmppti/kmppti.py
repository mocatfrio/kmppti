# standard library
import sys 
import os
import json
from collections import Counter

# 3rd party packages 
from prettyprinter import pprint

# local source
from kmppti.grid import Grid
from kmppti.rtree import RTree
from kmppti.pandora_box import PandoraBox
from kmppti.skyline import dynamic_skyline, reverse_skyline
from kmppti.constant import *


# constant variables 
INSERTION = 0
DELETION = 1
TS = 0
ID = 1
TYPE = 2
ACT = 3
NAME = 4
VALUE = -1

""" Precomputing function """

def process(queue, grid_size, history_file=None, history_file_editable=None):
    # get information from data 
    max_ts = queue.get_max_ts()
    max_val = queue.get_max_val()
    dim_size = queue.get_dim_size()
    product_size = queue.get_product_size()
    max_boundary = queue.get_max_boundary()
    queue_size = queue.get_queue_size()

    # initialization
    grid = Grid(grid_size, dim_size, max_val)
    rtree = RTree(dim_size, max_boundary)
    pbox = PandoraBox(max_ts, product_size)

    # import history file 
    history = {}
    if history_file:
        if os.path.exists(history_file):
            history = import_history(history_file)
    history_counter = 0 

    # start processing 
    counter = 0
    now_ts = 0
    while now_ts <= max_ts:
        objs = queue.pop(now_ts)
        for obj in objs:
            progress(counter, queue_size)
            id_data = "_".join([str(obj[0])] + [str(o) for o in obj[2:]])
            if customer_insertion(obj[TYPE], obj[ACT]):
                # insert to grid 
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                # get dynamic skyline
                if use_history(history, id_data):
                    dsl_result = history[id_data]["dsl_result"]
                    dominance_boundary = history[id_data]["dominance_boundary"]
                else:
                    # get search space 
                    space = grid.search_space(obj[ID], obj[VALUE])
                    # get products on the search space
                    products = grid.get_data(PRODUCT, space=space)
                    # compute dynamic skyline 
                    dsl_result, dominance_boundary = dynamic_skyline(obj[ID], obj[VALUE], products)
                    # simpan 
                    history[id_data] = {
                        "dsl_result": dsl_result,
                        "dominance_boundary": dominance_boundary
                    }
                # insert to R-Tree 
                node_id = rtree.insert(obj[ID], obj[VALUE], dsl_result)
                # save dsl result in the grid 
                grid.update_customer(obj[ID], dsl_result, dominance_boundary, node_id)

            elif customer_deletion(obj[TYPE], obj[ACT]):
                # remove from grid
                c_data = grid.remove(obj[ID], obj[TYPE])
                # remove from tree 
                rtree.delete(c_data["node_id"])
                # remove from all p's rsl result 
                for p_id in c_data["dsl_result"]:
                    grid.remove_rsl_result(p_id[0], obj[ID])

            elif product_insertion(obj[TYPE], obj[ACT]):
                # insert to grid 
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                # get reverse skyline 
                if use_history(history, id_data):
                    rsl_result = {int(key):val for key,val in history[id_data]["rsl_result"].items()}
                else:
                    # search candidate - not dominated by dominance boundaries  
                    c_id = rtree.search(p_id=obj[ID], p_val=obj[VALUE])     # return [c_id, c_id, c_id]
                    # get customers data based on candidate id                      
                    customers = grid.get_data(CUSTOMER, obj_id=c_id)
                    # compute reverse skyline 
                    rsl_result = reverse_skyline(obj[ID], obj[VALUE], customers)   # return value formatnya sama kayak dari grid
                    # simpan 
                    history[id_data] = {
                        "rsl_result": rsl_result,
                    }
                # for each c in rsl result 
                for c_id, c_data in rsl_result.items():
                    # update dsl result
                    curent_dsl_result = grid.get_dsl_result(c_id)
                    update_dsl_result(grid, rtree, c_id, c_data["value"], curent_dsl_result, c_data["dsl_result"], c_data["dominance_boundary"], c_data["node_id"])
                # save rsl result in the grid 
                grid.update_product(obj[ID], list(rsl_result.keys()))

            elif product_deletion(obj[TYPE], obj[ACT]):
                # remove from grid
                p_data = grid.remove(obj[ID], obj[TYPE])
                # remove from tree
                if p_data["rsl_result"]:
                    for c_id in p_data["rsl_result"]:
                        # get all customer neighbors in the same branch
                        node_id = grid.get_node_id(c_id)
                        neighbors_id = rtree.search(node_id=node_id)                           # [c_id, c_id, c_id]
                        customers = grid.get_data(CUSTOMER, obj_id=neighbors_id)
                        # get all dsl result of the neighbors - to get potential products if this product is deleted
                        dsl_result = [item for sublist in [val["dsl_result"] for key, val in customers.items()] for item in sublist]
                        # get current dsl result of c_id
                        c_dsl_result = grid.get_dsl_result(c_id)
                        c_value = grid.get_value(c_id, CUSTOMER)
                        # if current dsl result and neighbor's dsl result are not same
                        if Counter([dsl[0] for dsl in dsl_result]) != Counter([dsl[0] for dsl in c_dsl_result]):
                            sub_id_data = "_".join([str(c_id), str(c_value)])
                            if use_history(history, id_data, sub_id_data):
                                dsl_result = history[id_data][sub_id_data]["dsl_result"]
                                dominance_boundary = history[id_data][sub_id_data]["dominance_boundary"]
                            else:
                                dsl_result = get_unique_list(dsl_result + c_dsl_result)
                                # recompute dsl skyline 
                                products = {c_data[0]: {"value": c_data[1]} for c_data in dsl_result}
                                dsl_result, dominance_boundary = dynamic_skyline(c_id, c_value, products)
                                # simpan 
                                if not id_data in history:
                                    history[id_data] = {}
                                history[id_data][sub_id_data] = {
                                    "dsl_result": dsl_result,
                                    "dominance_boundary": dominance_boundary
                                }
                            # update dsl result
                            update_dsl_result(grid, rtree, c_id, c_value, c_dsl_result, dsl_result, dominance_boundary, node_id)
            counter += 1
            history_counter += 1
            if history_counter == 1000:
                # export history data 
                if history_file_editable:
                    export_history(history_file, history)
                    print("Export", history_file)
                history_counter = 0
        # get all customers
        customers = grid.get_data(CUSTOMER)
        # update pbox 
        pbox.update(now_ts, customers)
        now_ts += 1
    return pbox.get()

""" Helper Function """

def customer_insertion(obj_type, act):
    return obj_type == CUSTOMER and act == INSERTION

def customer_deletion(obj_type, act):
    return obj_type == CUSTOMER and act == DELETION

def product_insertion(obj_type, act):
    return obj_type == PRODUCT and act == INSERTION

def product_deletion(obj_type, act):
    return obj_type == PRODUCT and act == DELETION

def get_unique_list(mylist):
    # get unique value between current dsl result and new dsl result
    new_arr = []
    for arr in mylist:
        if not arr in new_arr:
            new_arr.append(arr)
    return new_arr

def update_dsl_result(grid, rtree, c_id, c_value, current_dsl_result, new_dsl_result, dominance_boundary, node_id):
    # remove c_id from p's rsl result in the current dsl result
    if current_dsl_result:
        for p_data in current_dsl_result:
            grid.remove_rsl_result(p_data[0], c_id)       # p_data= [p_id, p_value]
    # update R-Tree 
    rtree.update(c_id, c_value, new_dsl_result, node_id)
    # save dsl result in the grid 
    grid.update_customer(c_id, new_dsl_result, dominance_boundary, node_id)

def use_history(history, id_data, sub_id_data=None):
    result = history and id_data in history
    if sub_id_data:
        result = result and sub_id_data in history[id_data]
    return result
    
def progress(counter, queue_size):
    # progress notif
    if counter == 0:
        print("================================")
        print("Progress 0%")
    elif counter == round(5/100 * queue_size):
        print("================================")
        print("Progress 5%")
    elif counter == round(10/100 * queue_size):
        print("================================")
        print("Progress 10%")
    elif counter == round(15/100 * queue_size):
        print("================================")
        print("Progress 15%")
    elif counter == round(20/100 * queue_size):
        print("================================")
        print("Progress 20%")
    elif counter == round(25/100 * queue_size):
        print("================================")
        print("Progress 25%")
    elif counter == round(30/100 * queue_size):
        print("================================")
        print("Progress 30%")
    elif counter == round(35/100 * queue_size):
        print("================================")
        print("Progress 35%")
    elif counter == round(40/100 * queue_size):
        print("================================")
        print("Progress 40%")
    elif counter == round(45/100 * queue_size):
        print("================================")
        print("Progress 45%")
    elif counter == round(50/100 * queue_size):
        print("================================")
        print("Progress 50%")
    elif counter == round(55/100 * queue_size):
        print("================================")
        print("Progress 55%")
    elif counter == round(60/100 * queue_size):
        print("================================")
        print("Progress 60%")
    elif counter == round(65/100 * queue_size):
        print("================================")
        print("Progress 65%")
    elif counter == round(70/100 * queue_size):
        print("================================")
        print("Progress 70%")
    elif counter == round(75/100 * queue_size):
        print("================================")
        print("Progress 75%")
    elif counter == round(80/100 * queue_size):
        print("================================")
        print("Progress 80%")
    elif counter == round(85/100 * queue_size):
        print("================================")
        print("Progress 85%")
    elif counter == round(90/100 * queue_size):
        print("================================")
        print("Progress 90%")
    elif counter == round(95/100 * queue_size):
        print("================================")
        print("Progress 95%")
    elif counter == queue_size:
        print("================================")
        print("Progress 100%")

def import_history(history_file):
    with open(history_file) as json_file:
        history = json.load(json_file)
    return history

def export_history(history_file, history):
    with open(history_file, 'w') as json_file:
        json.dump(history, json_file)
