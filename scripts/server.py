import multiprocessing
import multiprocessing.managers
import sys, csv
from pprint import pprint
import numpy as np
import time
import operator

from streaming_kmppti.const import *

# import logging
# logger = multiprocessing.log_to_stderr()
# logger.setLevel(logging.INFO)

class MyListManager(multiprocessing.managers.BaseManager):
    pass

# global variables
data = [
    0, #timer
    {}, #label
    {}, #index
    {}, #result
]

def get_shared_data():
    return data

def main():
    # register server
    MyListManager.register("streaming_server", get_shared_data, exposed=['__getitem__', '__setitem__', '__str__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'])

    # start server
    manager = MyListManager(address=('/tmp/mypipe'), authkey=b"")
    manager.start()
    shared_data = manager.streaming_server()
    
    # get arguments
    dataset_type = sys.argv[1]
    total_row = sys.argv[2]
    total_dim = sys.argv[3]

    # get all data customer and product in csv + preparing data
    data, label, index = get_data(dataset_type, total_row, total_dim)

    shared_data[LABEL] = label
    shared_data[COL] = index

    print("shared queue = ", shared_data[QUEUE:])
    print("shared index = ", shared_data[COL])
    print("shared label = ", shared_data[LABEL])

    input("Start the client and controller first!")
    
    # start timer
    time_start = time.time()
    while True:
        print("minutes: " + str(shared_data[TIMER]))
        try:
            for i in range(len(data)):
                if shared_data[TIMER] == data[0][0]:
                    shared_data.append(data[0])
                    print("send " + str(data[0]))
                    data.pop(0)
                else:
                    break
            time.sleep(TIME_SLEEP)
            shared_data[TIMER] += 1
        except IndexError:
            pass
    
    # shutdown server
    print("Streaming done!")
    input("Press any key (NOT Ctrl-C!) to kill server (but kill client first)".center(50, "-"))
    manager.shutdown()

def get_data(dataset_type, total_row, total_dim):
    """This is function to import data from excel

    Args:
        dataset_type (char): define types of dataset, there are 3 types: ind, ant, fc
        total_row (int): numbers of row
        total_dim (int): numbers of dimension

    Returns:
        imported_data (list): imported data from excel that already prepared
        label (dict): key-value pair that stores label id and label name
        index (dict): key-value pair that stores column name and index in list

    """
    imported_data = []
    for data_name in ["customer", "product"]:
        filename = "_".join([data_name, dataset_type, total_row, total_dim]) + '.csv'
        filepath = "dataset/" + dataset_type + "/" + filename
        with open(filepath, 'r') as csv_file:
            data = list(csv.reader(csv_file, delimiter=','))
            index = {v:k for k,v in enumerate(data[0])}
            imported_data += data[1:]
    imported_data, label, index = prepare_data(imported_data, index)
    return imported_data, label, index

def prepare_data(data, index):
    """This is function for preparing data before it sent to client

    Args:
        data (list): data collected from excel
        index (dict): key-value that store information about column name and index

    Returns:
        prepared_data (list): data processed using numpy
        label (dict): key-value pair that stores label id and label name
        index (dict): an updated version of key-value pair that stores index
    """
    np_data = np.array(data)
    # delete id column
    np_data = np.delete(np_data, index["id"], 1)
    index = delete_index(index, "id")
    # separate label and generate id
    label = np_data[:,[index["label"]]].flatten().tolist()
    additional_col = [[i+1, 0 if is_product(label[i]) else 1, 0] for i in range(len(label))]
    label = {additional_col[i][0]:label[i] for i in range(len(label))}
    # save value as int
    np_value = np.delete(np_data, index["label"], 1).astype(int) 
    index = delete_index(index, "label")
    # as a replacement, save label id
    np_value = np.append(np_value, additional_col, axis=1)
    # update index
    index["label_id"] = generate_new_index(index)
    index["label_type"] = generate_new_index(index)
    index["is_processed"] = generate_new_index(index)
    # sort array by ts in
    np_value = np_value[np.argsort(np_value[:,index["ts_in"]])]
    prepared_data = np_value.tolist()
    return prepared_data, label, index

def generate_new_index(index):
    return max(index.items(), key=operator.itemgetter(1))[1] + 1

def delete_index(index, key):
    deleted_index = index[key]
    index.pop(key, None)
    return {k:v-1 for k,v in index.items() if v > deleted_index}

def is_product(string):
    return "product" in string

if __name__ == '__main__':
  main()
