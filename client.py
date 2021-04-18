import time
import multiprocessing
import multiprocessing.managers
import numpy as np
from pprint import pprint

from streaming_kmppti.constant import *
from kmppti.constant import *
from kmppti.grid import Grid
from kmppti.rtree import RTree
from kmppti.skyline import dynamic_skyline, reverse_skyline


class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("streaming_server")

def main():
    # connect client to the server 
    manager = MyListManager(address=('/tmp/mypipe'), authkey=b"")
    manager.connect()
    data = manager.streaming_server()

    # get information from data 
    k_size = data[K_SIZE]
    grid_size = data[GRID_SIZE]
    max_boundary = data[MAX_BOUNDARY]
    max_val = max([d[1] for d in max_boundary])
    dim_size = len(max_boundary)
    history = {}                                    # save updated/last dsl result {p1: {c1: 0.67, c2: 0.1} }
    product_name = {}

    print("k size: ", k_size)
    print("Grid size: ", grid_size)
    print("Max boundary: ", max_boundary)
    print("Max value: ", max_val)
    print("Queue: ", data[QUEUE:])

    # initialization instance of class
    grid = Grid(grid_size, dim_size, max_val)
    rtree = RTree(dim_size, max_boundary)

    while True:
        if data[QUEUE:]:
            obj = data.pop(QUEUE)
            print("=============================")
            print("OBJ: ", obj)

            if customer_insertion(obj[TYPE], obj[ACT]):
                # insert to grid 
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                # get search space 
                space = grid.search_space(obj[ID], obj[VALUE])
                # get products on the search space
                products = grid.get_data(PRODUCT, space=space)
                # compute dynamic skyline 
                dsl_result, dominance_boundary = dynamic_skyline(obj[ID], obj[VALUE], products)
                # insert to R-Tree 
                node_id = rtree.insert(obj[ID], obj[VALUE], dsl_result)
                # save dsl result in the grid 
                grid.update_customer(obj[ID], dsl_result, dominance_boundary, node_id)
                # update history of market contribution 
                for p_data in dsl_result:
                    score = 1/len(dsl_result)
                    update_history(history, p_data[0], obj[ID], score)

            elif customer_deletion(obj[TYPE], obj[ACT]):
                # remove from grid
                c_data = grid.remove(obj[ID], obj[TYPE])
                # remove from tree 
                rtree.delete(c_data["node_id"])
                for p_data in c_data["dsl_result"]:
                    # remove from all p's rsl result 
                    grid.remove_rsl_result(p_data[0], obj[ID])
                    # update history of market contribution 
                    history[p_data[0]].pop(obj[ID], None)

            elif product_insertion(obj[TYPE], obj[ACT]):
                # insert to grid 
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                # search candidate - not dominated by dominance boundaries  
                c_id = rtree.search(p_id=obj[ID], p_val=obj[VALUE])     # return [c_id, c_id, c_id]
                # get customers data based on candidate id                      
                customers = grid.get_data(CUSTOMER, obj_id=c_id)
                # compute reverse skyline 
                rsl_result = reverse_skyline(obj[ID], obj[VALUE], customers)   # return value formatnya sama kayak dari grid
                # for each c in rsl result 
                for c_id, c_data in rsl_result.items():
                    # update dsl result
                    curent_dsl_result = grid.get_dsl_result(c_id)
                    update_dsl_result(grid, rtree, c_id, c_data["value"], curent_dsl_result, c_data["dsl_result"], c_data["dominance_boundary"], c_data["node_id"])
                    # update history of market contribution 
                    score = 1/len(c_data["dsl_result"])
                    update_history(history, obj[ID], c_id, score)
                # save rsl result in the grid 
                grid.update_product(obj[ID], list(rsl_result.keys()))
                # add product name 
                product_name[obj[ID]] = obj[NAME]

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
                            dsl_result = get_unique_list(dsl_result + c_dsl_result)
                            # recompute dsl skyline 
                            products = {c_data[0]: {"value": c_data[1]} for c_data in dsl_result}
                            dsl_result, dominance_boundary = dynamic_skyline(c_id, c_value, products)
                            # update dsl result
                            update_dsl_result(grid, rtree, c_id, c_value, c_dsl_result, dsl_result, dominance_boundary, node_id)
                            # update history of market contribution 
                            for p_data in dsl_result:
                                score = 1/len(dsl_result)
                                update_history(history, p_data[0], c_id, score)
                # delete product from history of market contribution 
                history.pop(obj[ID])
                # delete product name 
                product_name.pop(obj[ID])

            # calculate market contribution 
            score = [tuple([key, calc_score(val)]) for key, val in history.items()]
            dtype = [("product", int), ("score", float)]
            market_contribution = np.array(score, dtype=dtype)
            # reverse sorting
            market_contribution[::-1].sort(order="score")
            result = [[product_name[d[0]], d[1]] for d in market_contribution[:k_size].tolist()]
            print("RESULT")
            for res in result:
                print(res)

""" Helper Function """

def customer_insertion(obj_type, act):
    return obj_type == CUSTOMER and act == INSERTION

def customer_deletion(obj_type, act):
    return obj_type == CUSTOMER and act == DELETION

def product_insertion(obj_type, act):
    return obj_type == PRODUCT and act == INSERTION

def product_deletion(obj_type, act):
    return obj_type == PRODUCT and act == DELETION

def is_product(data_type):
    return data_type == PRODUCT

def update_history(history, p_id, c_id, score):
    if not p_id in history:
        history[p_id] = {}
    history[p_id][c_id] = score

def update_dsl_result(grid, rtree, c_id, c_value, current_dsl_result, new_dsl_result, dominance_boundary, node_id):
    # remove c_id from p's rsl result in the current dsl result
    if current_dsl_result:
        for p_data in current_dsl_result:
            grid.remove_rsl_result(p_data[0], c_id)       # p_data= [p_id, p_value]
    # update R-Tree 
    rtree.update(c_id, c_value, new_dsl_result, node_id)
    # save dsl result in the grid 
    grid.update_customer(c_id, new_dsl_result, dominance_boundary, node_id)

def get_unique_list(mylist):
    # get unique value between current dsl result and new dsl result
    new_arr = []
    for arr in mylist:
        if not arr in new_arr:
            new_arr.append(arr)
    return new_arr

def calc_score(c_data):
    score = 0
    for key, val in c_data.items():
        score += val
    return score

if __name__ == '__main__':
    main()