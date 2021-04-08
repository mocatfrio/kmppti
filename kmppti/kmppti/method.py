# standard library
import os
import csv
import sys

# 3rd party packages 
import numpy as np
from dotenv import load_dotenv
from prettyprinter import pprint

# local source
from kmppti.Queue import Queue
from kmppti.Grid import Grid
from kmppti.RTree import RTree
from kmppti.PandoraBox import PandoraBox
from kmppti.Skyline import dynamic_skyline, reverse_skyline
from kmppti.Constant import PRODUCT, CUSTOMER

load_dotenv()

# constant function 
INSERTION = 0
DELETION = 1
TS = 0
ID = 1
TYPE = 2
ACT = 3
NAME = 4
VALUE = -1

""" Public Function """

def kmppti(p_file, c_file, k, grid_size, time_start, time_end):
    # generate pbox filename 
    filename = generate_pbox_filename(p_file, c_file)
    pbox_file = os.getenv("PBOX_PATH") + filename
    # precompute first
    if not exist(pbox_file):
        queue = Queue(p_file, c_file)
        pbox_data = process(queue, grid_size)
        with open(pbox_file, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(pbox_data)
        csv_file.close()
    # import pbox data 
    pbox_data = np.genfromtxt(pbox_file, delimiter=',')
    pbox_data = pbox_data[0 : len(pbox_data), time_start - 1 : time_end - 1]
    result = sort(np.sum(pbox_data, axis = 1), k)
    label = get_products(p_file)
    return reshape_result(pbox_data, label) 

""" Main Function """

def process(queue, grid_size):
    # get information from data 
    max_ts = queue.get_max_ts()
    max_val = queue.get_max_val()
    dim_size = queue.get_dim_size()
    product_size = queue.get_product_size()
    max_boundary = queue.get_max_boundary()
    # initialization
    grid = Grid(grid_size, dim_size, max_val)
    rtree = RTree(dim_size, max_boundary)
    pbox = PandoraBox(max_ts, product_size)
    # start processing 
    now_ts = 0
    while now_ts <= max_ts:
        print("=============================================")
        print("TS", now_ts)
        objs = queue.pop(now_ts)
        for obj in objs:
            print("")
            print(obj)
            if customer_insertion(obj[TYPE], obj[ACT]):
                # insert to grid 
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                # get search space 
                space = grid.search_space(obj[ID], obj[VALUE])
                # get products on the search space
                products = grid.get_data(PRODUCT, space=space)
                # get dynamic skyline
                dsl_result, dominance_boundary = dynamic_skyline(obj[ID], obj[VALUE], products)
                # insert to R-Tree 
                node_id = rtree.insert(obj[ID], obj[VALUE], dsl_result)
                # save dsl result in the grid 
                grid.update_customer(obj[ID], dsl_result, dominance_boundary, node_id)

            elif customer_deletion(obj[TYPE], obj[ACT]):
                # remove from grid
                c_data = grid.remove(obj[ID], obj[TYPE])
                # remove from tree 
                rtree.delete(c_data["node_id"])

            elif product_insertion(obj[TYPE], obj[ACT]):
                # insert to grid 
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                # search candidate - not dominated by dominance boundaries 
                c_id = rtree.search(obj[ID], obj[VALUE])                           # [c_id, c_id, c_id]
                customers = grid.get_data(CUSTOMER, obj_id=c_id)
                # get reverse skyline 
                rsl_result = reverse_skyline(obj[ID], obj[VALUE], customers)      # return value formatnya sama kayak dari grid
                print("")
                print("Update to RTree")
                for key, val in rsl_result.items():
                    # update R-Tree 
                    rtree.update(key, val["value"], val["dsl_result"], val["node_id"])
                    # save dsl result in the grid 
                    grid.update_customer(obj[ID], all_data=val)
                # save rsl result in the grid 
                grid.update_product(obj[ID], list(rsl_result.keys()))

            elif product_deletion(obj[TYPE], obj[ACT]):
                pass
                # # remove from grid
                # p_data = grid.remove(obj[ID], obj[TYPE])
                # # remove from tree                 
                # rtree.delete_product(obj[ID])
        # get all customers
        customers = grid.get_data(CUSTOMER)
        # update pbox 
        pbox.update(now_ts, customers)
        now_ts += 1
    # return pbox.get()
    pbox.print()
    sys.exit()

""" Helper Function """

def sort(pbox_data, k):
    # restructure
    score = [tuple([i, pbox_data[i]]) for i in range(len(pbox_data))]
    dtype = [("p_id", int), ("score", float)]
    market_contribution = np.array(score, dtype=dtype)
    # reverse sorting
    market_contribution[::-1].sort(order="score")
    return market_contribution[:k].tolist()

def exist(filename):
    return os.path.exists(filename)

def reshape_result(result, label):
    return [
        {
            "label": label[result[i][0]], 
            "market_contribution": result[i][1]
        } for i in range(len(result))
    ]

def generate_pbox_filename(p_file, c_file):
    connector = "_"
    filename = [c_file.split("/")[-1].split(".")[0], p_file.split("/")[-1].split(".")[0]]
    return connector.join(filename) + ".csv"

def get_products(p_file):
    # can be more effective 
    with open(p_file) as csv_file:
        products = []
        first_row = True
        for row in csv_file:
            if first_row: first_row = False; continue
            products.append(row.split(',')[1])
    return products

def customer_insertion(obj_type, act):
    return obj_type == CUSTOMER and act == INSERTION

def customer_deletion(obj_type, act):
    return obj_type == CUSTOMER and act == DELETION

def product_insertion(obj_type, act):
    return obj_type == PRODUCT and act == INSERTION

def product_deletion(obj_type, act):
    return obj_type == PRODUCT and act == DELETION