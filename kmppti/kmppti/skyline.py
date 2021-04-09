import copy
import operator
import numpy as np
from prettyprinter import pprint
from collections import Counter

from kmppti.Constant import PRODUCT, CUSTOMER

ID = 0
DIFF = 1
DOMINATED = 2

def dynamic_skyline(c_id, c_val, products):
    result = []
    if products: 
        # calculate diff from the first 
        result = [[key, calculate_diff(c_val, val["value"]), False] for key, val in products.items()]
        compare(result)
    # get data that is not dominated 
    result = [[res[ID], res[DIFF]] for res in result if not res[DOMINATED]]
    # calculate dominance boundary 
    dominance_boundary = calculate_dominance_boundary(c_val, result)
    # get actual data value
    result = [[res[ID], products[res[ID]]["value"]] for res in result]
    return result, dominance_boundary

def reverse_skyline(p_id, p_val, customers):
    candidate = []
    for key, val in customers.items():
        p_diff = calculate_diff(val["value"], p_val)
        # check using dominance boundary
        if is_candidate(p_diff, val["dominance_boundary"]):
            candidate.append(key)
    rsl_result = {}
    for c_id in candidate:
        # current dsl result
        products = {}
        curr_dsl_id = []
        if customers[c_id]["dsl_result"]:
            products = {c_data[0]: {"value": c_data[1]} for c_data in customers[c_id]["dsl_result"]}
            curr_dsl_id = [dsl[0] for dsl in customers[c_id]["dsl_result"]]
        # add new product 
        products[p_id] = {"value": p_val}
        # recompute dsl result 
        dsl_result, dominance_boundary = dynamic_skyline(c_id, customers[c_id]["value"], products)
        new_dsl_id = [dsl[0] for dsl in dsl_result]
        # if current and new dsl result is not same 
        if Counter(new_dsl_id) != Counter(curr_dsl_id):
            rsl_result[c_id] = {
                "value": customers[c_id]["value"],
                "dsl_result": dsl_result,
                "dominance_boundary": dominance_boundary,
                "node_id": customers[c_id]["node_id"]
            }
    return rsl_result

def calculate_diff(arr1, arr2):
    return [abs(arr1[i] - arr2[i]) for i in range(len(arr1))]

def calculate_dominance_boundary(c_val, result):
    dominance_boundary = []
    if result:
        for i in range(len(c_val)):
            values = [val[i] for val in [res[DIFF] for res in result]]
            min_val = min(values)
            dominance_boundary.append(result[values.index(min_val)][DIFF])
    return dominance_boundary

def compare(arr):
    # divide and conquer algorithm
    if len(arr) > 1:
        # finding the mid of the array
        mid = len(arr)//2
        # dividing array into left and right 
        left = arr[:mid]
        right = arr[mid:]
        compare(left)
        compare(right)
        # check domination 
        i = 0
        while i < len(left):
            if left[i][DOMINATED]:
                i += 1
                continue
            j = 0
            while j < len(right):
                if right[j][DOMINATED]:
                    j += 1
                    continue
                dom = check_domination(left[i][DIFF], right[j][DIFF])
                if dom == 1:
                    right[j][DOMINATED] = True
                elif dom == 2:
                    left[i][DOMINATED] = True
                j += 1
            i += 1
        # sorting 
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i][DOMINATED] <= right[j][DOMINATED]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        # checking if any element was left
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

def check_domination(val1, val2):
    # return value : 
    # 0 (saling mendominasi), 
    # 1 (val1 mendominasi), 
    # 2 (val2 mendominasi)
    result = [0 for i in range(len(val1))]
    for i in range(len(val1)):
        if val1[i] < val2[i]:
            result[i] = 1
        elif val1[i] > val2[i]:
            result[i] = 2
    if 1 in result:
        if 2 in result:
            return 0
        return 1
    return 2

def is_pivot(p_val, n_border, q_val):
    p_dominating = 0
    p_diff = calculate_diff(p_val, q_val)
    for pos in n_border:
        pos_diff = calculate_diff(pos, q_val)
        if check_domination(p_diff, pos_diff) == 1:
            p_dominating += 1
    return p_dominating == len(n_border)

def is_candidate(p_diff, dominance_boundary):
    dominated = 0
    if dominance_boundary:
        for boundary in dominance_boundary:
            if check_domination(boundary, p_diff) == 1:
                dominated += 1
        return dominated != len(dominance_boundary)
    return True
        