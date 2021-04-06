import copy
import operator
import numpy as np
from prettyprinter import pprint

from kmppti.Constant import PRODUCT, CUSTOMER

ID = 0
VAL = 1
DOMINATED = 2

def dynamic_skyline(c_id, c_val, products):
    result = []
    if products: 
        # calculate diff from the first 
        result = [[key, [abs(c_val[i] - val["value"][i]) for i in range(len(c_val))], False] for key, val in products.items()]
        pprint(result)
        compare(result, c_val)
    # get data that is not dominated 
    result = [[res[ID], res[VAL]] for res in result if not res[DOMINATED]]
    # calculate dominance boundary 
    dominance_boundary = []
    if result:
        for i in range(len(c_val)):
            values = [res[VAL] for res in result]
            values = [val[i] for val in values]
            min_val = min(values)
            dominance_boundary.append(result[values.index(min_val)][VAL])
    # get actual data value
    result = [[res[ID], products[res[ID]]["value"]] for res in result]
    return result, dominance_boundary

def compare(arr, c_val):
    # divide and conquer algorithm
    if len(arr) > 1:
        # finding the mid of the array
        mid = len(arr)//2
        # dividing array into left and right 
        left = arr[:mid]
        right = arr[mid:]
        compare(left, c_val)
        compare(right, c_val)
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
                dom = check_domination(left[i][VAL], right[j][VAL], c_val)
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

def check_domination(val1, val2, q_val):
    # return value : 
    # 0 (saling mendominasi), 
    # 1 (val1 mendominasi), 
    # 2 (val2 mendominasi)
    result = [0 for i in range(len(val1))]
    for i in range(len(diff1)):
        if diff1[i] < diff2[i]:
            result[i] = 1
        elif diff1[i] > diff2[i]:
            result[i] = 2
    if 1 in result:
        if 2 in result:
            return 0
        return 1
    return 2

def is_pivot(p_val, n_border, q_val):
    p_dominating = 0
    for pos in n_border:
        if check_domination(p_val, pos, q_val) == 1:
            p_dominating += 1
    return p_dominating == len(n_border)
