import sys
import os
import csv 
import math 
import getopt
import random
from dotenv import load_dotenv

load_dotenv()

MAX_VALUE = 200
DISTANCE = 5


def main(argv):
    short_command = "ht:n:d:l:"
    long_command = ["help", "dataset_type=", "data_size=", "dim_size=", "label="]
    try:
        opts, args = getopt.getopt(argv, short_command, long_command)
    except getopt.GetoptError:
        print("main.py -t <dataset_type> -n <data_size> -d <dim_size> -l <label_data>")
        sys.exit(2)
    print(opts)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("main.py -t <dataset_type> -n <data_size> -d <dim_size> -l <label_data>")
            sys.exit()
        elif opt in ("-t", "--dataset_type"):
            dataset_type = arg
        elif opt in ("-n", "--data_size"):
            data_size = int(arg)
        elif opt in ("-d", "--dim_size"):
            dim_size = int(arg)
        elif opt in ("-l", "--label"):
            label = arg
    # generate data 
    data = [["id", "label", "ts_in", "ts_out"]]
    for i in range(data_size):
        row = [i + 1, label + "-" + str(i + 1)]
        row += randomize_ts()
        row += randomize_data(dataset_type, dim_size)
        data.append(row)
    filename = "_".join([dataset_type, str(data_size), str(dim_size), label])
    csvfile = os.getenv("DATASET_PATH") + filename + ".csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(data)
    print(csvfile)

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
    selected_dim = random.uniform(0, dim_size - 1)
    for i in range(dim_size):
        if i == selected_dim:
            data.append(val)
        else:
            other_val = MAX_VALUE - val + random.uniform(-DISTANCE, DISTANCE)
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

           
if __name__ == '__main__':
    main(sys.argv[1:])
    