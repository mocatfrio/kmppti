# standard library
import sys
import os
import getopt
import csv
import json

# 3rd party packages 
import numpy as np
from dotenv import load_dotenv
from prettyprinter import pprint

# local source
from kmppti.queue import Queue
from kmppti.logger import Logger
from kmppti.core import process

load_dotenv()

def main(argv):
    short_command = "hd:p:c:k:g:s:e:"
    long_command = ["help", "command=", "product=", "customer=", "k=", "grid=", "time_start=", "time_end="]
    try:
        opts, args = getopt.getopt(argv, short_command, long_command)
    except getopt.GetoptError:
        print("main.py -d precomputing -p <product_file> -c <customer_file>")
        print("main.py -d kmppti -p <product_file> -c <customer_file> -k <k_size> -g <grid_size> -s <time_start> -e <time_end>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("main.py -d precomputing -p <product_file> -c <customer_file>")
            print("main.py -d kmppti -p <product_file> -c <customer_file> -k <k_size> -g <grid_size> -s <time_start> -e <time_end>")
            sys.exit()
        elif opt in ("-d", "--command"):
            command = arg
        elif opt in ("-p", "--product"):
            p_file = os.getenv("DATASET_PATH") + arg
        elif opt in ("-c", "--customer"):
            c_file = os.getenv("DATASET_PATH") + arg
        elif opt in ("-k", "--k"):
            k = int(arg)
        elif opt in ("-g", "--grid"):
            grid_size = int(arg)
        elif opt in ("-s", "--time_start"):
            time_start = int(arg)
        elif opt in ("-e", "--time_end"):
            time_end = int(arg)
    if is_precomputing(command):
        grid_size = 3
        k = time_start = time_end = "-"
    # init logger 
    log = Logger(os.getenv("LOG_PATH"), p_file, [command, k, grid_size, time_start, time_end])
    log.start()
    # run method 
    if is_precomputing(command):
        precomputing(p_file, c_file, grid_size)
    else:
        result = kmppti(p_file, c_file, k, grid_size, time_start, time_end)
        pprint(result)
    # logger end 
    log.end()
    log.write()

def precomputing(p_file, c_file, grid_size):
    print("Precompute", p_file, c_file, grid_size)
    # import product and customer files as queue 
    queue = Queue(p_file, c_file)
    # import history data for precomputation efficiency - stored based on dim_size
    history_file = get_history_file(p_file)
    if os.path.exists(history_file):
        history_data = import_history(history_file)
    else:
        history_data = {}
    # precomputing
    pbox_data, history_data = process(queue, grid_size, history_data)
    print("Successfully precomputed data!")
    # export pbox data 
    pbox_file = get_pbox_file(p_file, c_file)
    export_pbox(pbox_file, pbox_data)
    print("Save Pandora box in ", pbox_file)
    # export history data 
    if not os.path.exists(history_file):
        export_history(history_file, history_data)
        print("Save History data in ", history_file)

def kmppti(p_file, c_file, k, grid_size, time_start, time_end):
    # import pbox data 
    pbox_file = get_pbox_file(p_file, c_file)
    pbox_data = np.genfromtxt(pbox_file, delimiter=',')
    # get pbox data based on the query time interval
    pbox_data = pbox_data[0 : len(pbox_data), time_start - 1 : time_end - 1]
    # get k products with the largest total market contribution
    result = sort(np.sum(pbox_data, axis = 1), k)
    # get product's name 
    label = get_products(p_file)
    # reshape result 
    json = [
        {
            "label": label[result[i][0]], 
            "market_contribution": result[i][1]
        } for i in range(len(result))
    ]
    return json 

""" Helper Functions """

def sort(pbox_data, k):
    # restructure data
    score = [tuple([i, pbox_data[i]]) for i in range(len(pbox_data))]
    dtype = [("p_id", int), ("score", float)]
    market_contribution = np.array(score, dtype=dtype)
    # reverse sorting
    market_contribution[::-1].sort(order="score")
    return market_contribution[:k].tolist()

def get_filename(p_file, c_file):
    connector = "_"
    filename = connector.join([c_file.split("/")[-1].split(".")[0], p_file.split("/")[-1].split(".")[0]])
    return filename

def get_pbox_file(p_file, c_file):
    path = os.getenv("PBOX_PATH")
    # handle if pbox directory is not exist 
    if not os.path.exists(path):
        os.mkdir(path)
    ext = ".csv"
    pbox_file = path + get_filename(p_file, c_file) + ext
    return pbox_file

def get_history_file(p_file):
    path = os.getenv("JSON_PATH")
    dim_size = p_file.split("_")[2]
    # handle if directory is not exist 
    if not os.path.exists(path):
        os.mkdir(path)
    ext = ".json"
    history_file = path + get_filename(p_file, c_file) + ext
    return history_file

def get_products(p_file):
    with open(p_file) as csv_file:
        products = []
        first_row = True
        for row in csv_file:
            if first_row: 
                first_row = False
                continue
            products.append(row.split(',')[1])
    return products

def import_history(history_file):
    with open(history_file) as json_file:
        history_data = json.load(json_file)
    return history_data

def export_history(history_file, history_data):
    with open(history_file, 'w') as json_file:
        json.dump(history_data, json_file)

def export_pbox(pbox_file, pbox_data):
    with open(pbox_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(pbox_data)
    csv_file.close()

def is_precomputing(command):
    return command == "precomputing"

if __name__ == '__main__':
    main(sys.argv[1:])
    
    