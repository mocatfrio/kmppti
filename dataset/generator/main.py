import sys
import os
import csv 
import math 
import getopt
import random

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from prettyprinter import pprint

load_dotenv()

MAX_VALUE = 200
DISTANCE = 5

def main(argv):
    # get arguments 
    short_command = "hc:t:n:d:l:f:"
    long_command = ["help", "command=", "dataset_type=", "data_size=", "dim_size=", "label=", "file="]
    try:
        opts, args = getopt.getopt(argv, short_command, long_command)
    except getopt.GetoptError:
        print("main.py -c <command> -t <dataset_type> -n <data_size> -d <dim_size> -l <label_data> -f <filename>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("main.py -c <command> -t <dataset_type> -n <data_size> -d <dim_size> -l <label_data> -f <filename>")
            sys.exit()
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-t", "--dataset_type"):
            dataset_type = arg
        elif opt in ("-n", "--data_size"):
            data_size = int(arg)
        elif opt in ("-d", "--dim_size"):
            dim_size = int(arg)
        elif opt in ("-l", "--label"):
            label = arg
        elif opt in ("-f", "--file"):
            filename = os.getenv("DATASET_PATH") + arg
    # process based on command 
    if command == "generate":
        if is_real(dataset_type):
            data = preprocess_data(dim_size, data_size, label)
        else:
            data = generate_data(dim_size, data_size, dataset_type, label)
    elif command == "prepare":
        data = prepare_data(filename)
    elif command == "partition":
        data = partition_data(filename, data_size)
        dataset_type = filename.split("_")[0]
        dim_size = filename.split("_")[2]
        label = filename.split("_")[3]
        filename = "_".join([dataset_type, str(data_size), dim_size, label])
    if not "filename" in locals():
        filename = "_".join([dataset_type, str(data_size), str(dim_size), label])
        filename = os.getenv("DATASET_PATH") + filename + ".csv"
    # export data 
    export_data(filename, data)

def generate_data(dim_size, data_size, dataset_type, label):
    # generate data 
    columns_name = ["id", "label", "ts_in", "ts_out"] + ["attr_" + str(i+1) for i in range(dim_size)]
    data = [columns_name]
    for i in range(data_size):
        row = [i + 1, label + "-" + str(i + 1)]
        row += randomize_ts()
        row += randomize_data(dataset_type, dim_size)
        data.append(row)
    return data

def preprocess_data(dim_size, data_size, label):
    dataset_path = os.getenv("DATASET_PATH") + "generator/covtype.csv"
    df = pd.read_csv(dataset_path)
    # normalisasi min-max 
    for col in df.columns:
        normalized_value = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = round(normalized_value * 100).astype(int)
    # split data for product and customer
    if label == "product":
        # selecting rows that scope (as ts in) < aspect (as ts out)
        df = df[df["Slope"] < df["Aspect"]]
        df.insert(0, "Label", ["product-" + str(i+1) for i in range(len(df))], True)
        new_columns = ["Label", "Slope", "Aspect", "Elevation"] + [col for col in df.columns[4:]]
    else:
        df = df[df["Horizontal_Distance_To_Hydrology"] < df["Elevation"]]
        df.insert(0, "Label", ["customer-" + str(i+1) for i in range(len(df))], True)
        new_columns = ["Label", "Horizontal_Distance_To_Hydrology", "Elevation", "Aspect", "Slope"] + [col for col in df.columns[5:]]
    # swap columns
    df = df.reindex(columns = new_columns)
    # sort based on first column 
    df = df.sort_values(df.columns[1])
    # reset index 
    df = df.reset_index(drop=True)
    df.insert(0, "ID", [i + 1 for i in df.index], True)
    # get row based on required data and dim size 
    df = df.iloc[:data_size, :dim_size + 4]
    # convert df to list 
    result = [df.columns.tolist()]
    result += df.values.tolist()
    return result

def prepare_data(filename):
    data = []
    result = []
    data_temp = {}
    with open(filename, "r") as csv_file:
        first_row = True
        for row in csv_file:
            if first_row: 
                result.append([val.replace('\n', '') for val in row.split(',')])
                first_row = False
                continue
            col = row.split(',')[1:]
            # set name 
            data_id = len(data)
            data_temp[data_id] = {
                "label": col[0],
                "value": [val.replace('\n', '') for val in col[3:]]
            }
            data.append([int(val) for val in col[1:3]] + [data_id])
    # sorting ts in
    data = sort_data(data)
    # recombine 
    for i in range(len(data)):
        temp = [i + 1, data_temp[data[i][-1]]["label"]] + [data[i][0], data[i][1]] + data_temp[data[i][-1]]["value"]
        result.append(temp)
    return result

def partition_data(filename, data_size):
    result = []
    with open(filename, "r") as csv_file:
        i = 0
        for row in csv_file:
            if i > data_size:
                break
            result.append([val.replace('\n', '') for val in row.split(',')])
            i += 1
    return result

def randomize(arg=None):
    range_start = random.randint(0, MAX_VALUE) 
    range_end_start = 0
    if arg:
        range_start = arg
        range_end_start = round(MAX_VALUE/2) - round(math.sqrt(MAX_VALUE/2))
    range_end = range_start + random.randint(range_end_start, round(MAX_VALUE/2))
    rand = random.randint(range_start, range_end)
    return rand

def randomize_ts():
    ts = [randomize()]
    ts.append(randomize(ts[0]))
    return ts

def randomize_data(dataset_type, dim_size):
    if is_independent(dataset_type):
        data = randomize_independent(dim_size)
    if is_anticorrelated(dataset_type):
        data = randomize_anticorr(dim_size)
    return data
    
def randomize_independent(dim_size):
    data = []
    for i in range(dim_size):
        data.append(randomize())
    return data

def randomize_anticorr(dim_size):
    data = []
    val = randomize()
    selected_dim = random.randint(0, dim_size - 1)
    for i in range(dim_size):
        if i == selected_dim:
            data.append(val)
        else:
            other_val = MAX_VALUE - val + random.randint(-DISTANCE, DISTANCE)
            if other_val < 0:
                data.append(0)
            elif other_val > MAX_VALUE:
                data.append(MAX_VALUE)
            else:
                data.append(other_val)
    return data

def is_independent(dataset_type):
    return dataset_type.lower() == "ind"

def is_anticorrelated(dataset_type):
    return dataset_type.lower() == "ant"

def is_real(dataset_type):
    return dataset_type.lower() == "fc"

def export_data(filename, data):
    try:
        with open(filename, "w") as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(data)
        print("Exporting data", filename, "is success!")
    except Exception as e:
        print("Error due to", e)

def sort_data(data):
    arr = list(map(tuple, data)) 
    dt = np.dtype([("ts_in", np.int32), ("ts_out", np.int32), ("data_id", np.int32)])
    arr = np.array(arr, dtype=dt)
    return list(map(list, np.sort(arr, order=["ts_in"]).tolist()))

           
if __name__ == '__main__':
    main(sys.argv[1:])
    