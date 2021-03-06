import os, sys
import numpy as np
from dotenv import load_dotenv
from prettyprinter import pprint

from kmppti.core import precompute, compute
import kmppti.logger as log

load_dotenv()
# LOGGER = log.Logger(os.getenv("LOG_PATH"))

def main():
    approach = {
        1: srondti_approach,
        2: srofdti_approach,
        3: prondti_approach,
        4: profdti_approach
    }
    approach_type = int(sys.argv[1])
    c_file = os.getenv("DATASET_PATH") + sys.argv[2]
    p_file = os.getenv("DATASET_PATH") + sys.argv[3]
    grid_size = int(sys.argv[4])
    k = int(sys.argv[5])
    time_start = int(sys.argv[6])
    time_end = int(sys.argv[7])
    # select approach
    result, label = approach[approach_type](c_file, p_file, grid_size, k, time_start, time_end)
    # convert to json
    json_result = {label[result[i][0]]: result[i][1] for i in range(len(result))}
    pprint(json_result)

def srondti_approach(c_file, p_file, grid_size, k, time_start, time_end):
    # get data in interval time query
    pbox_data, label = compute(c_file, p_file, grid_size, time_start, time_end)
    pbox_data = np.sum(pbox_data, axis = 1)
    return sort(pbox_data, k), label

def srofdti_approach(c_file, p_file, grid_size, k, time_start, time_end):
    filename = "_".join([
        c_file.split("/")[-1].split(".")[0],
        p_file.split("/")[-1].split(".")[0],
        str(grid_size)]) + ".csv"
    pbox_file = os.getenv("PBOX_PATH") + filename
    # precompute first
    if not exist(pbox_file):
        precompute(c_file, p_file, grid_size, pbox_file)
    # import pbox data 
    pbox_data = np.genfromtxt(pbox_file, delimiter=',')
    pbox_data = pbox_data[0 : len(pbox_data), time_start - 1 : time_end - 1]  # menyamakan dengan srondti_approach
    # sum up product score 
    pbox_data = np.sum(pbox_data, axis = 1)
    # get products 
    label = get_products(p_file)
    return sort(pbox_data, k), label

def prondti_approach(c_file, p_file, grid_size, k, time_start, time_end):
    # paralel 
    pass

def profdti_approach(c_file, p_file, grid_size, k, time_start, time_end):
    # paralel 
    pass

def exist(filename):
    if os.path.exists(filename):
        return True
    return False

def sort(pbox_data, k):
    # restructure
    score = [tuple([i, pbox_data[i]]) for i in range(len(pbox_data))]
    dtype = [("p_id", int), ("score", float)]
    market_contribution = np.array(score, dtype=dtype)
    # reverse sorting
    market_contribution[::-1].sort(order="score")
    return market_contribution[:k].tolist()

def get_products(p_file):
    with open(p_file) as csv_file:
        products = []
        first_row = True
        for row in csv_file:
            if first_row: first_row = False; continue
            products.append(row.split(',')[1])
    return products

if __name__ == '__main__':
    main()
