import copy
import numpy as np
from prettyprinter import pprint

from kmppti.constant import PRODUCT, CUSTOMER

VAL = 0
DOMINATED = 1
ID_ARR = 0
VAL_ARR = 1
DOM_ARR = 2

class Queue:
    def __init__(self, p_file, c_file, time_start=None, time_end=None):
        self.id_product = 0
        self.id_customer = 300000 # adjust it based on the the largest amount of data
        self.queue = []
        self.info = {}
        self.import_data(p_file, PRODUCT, time_start, time_end)
        self.product_size = len(self.info)
        self.import_data(c_file, CUSTOMER, time_start, time_end)
        self.sort_data()
        
    def pop(self, now_ts):
        result = []
        while True: 
            if not self.queue: 
                break
            if self.queue[0][0] != now_ts: 
                break
            data = self.queue.pop(0)
            data += [self.info[data[1]]["label"], self.info[data[1]]["value"]]
            result.append(data)
        return result

    def get_max_ts(self):
        return np.asarray(self.queue).max(axis=0, keepdims=True)[0][0]

    def get_max_val(self):
        list_of_value = [val["value"] for key, val in self.info.items()]
        return max(list(np.amax(list_of_value, axis=0)))

    def get_dim_size(self):
        return len(self.info[0]["value"])
    
    def get_data_size(self):
        return len(self.info)
    
    def get_product_size(self):
        return self.product_size
    
    def get_max_boundary(self):
        list_of_value = [val["value"] for key, val in self.info.items()]
        max_val = list(np.amax(list_of_value, axis=0))
        min_val = list(np.amin(list_of_value, axis=0))
        boundary = []
        for i in range(self.get_dim_size()):
            boundary.append([min_val[i], max_val[i]])
        return boundary

    def import_data(self, file_path, data_type, time_start, time_end):
        with open(file_path, "r") as csv_file:
            first_row = True
            for row in csv_file:
                if first_row: 
                    first_row = False
                    continue
                col = row.split(',')[1:]
                if time_start and time_end:
                    if int(col[1]) > time_end: 
                        continue
                    else: 
                        if int(col[2]) > time_end: 
                            col[2] = time_end
                    if int(col[2]) < time_start: 
                        continue
                    else: 
                        if int(col[1]) < time_start: 
                            col[1] = time_start
                data_id = self.set_info(data_type, col[0], col[3:])
                self.set_queue(col[1:3], data_id, data_type)
    
    def set_info(self, data_type, label, value):
        if data_type is PRODUCT:
            data_id = copy.deepcopy(self.id_product)
            self.id_product += 1
        else:
            data_id = copy.deepcopy(self.id_customer)
            self.id_customer += 1
        self.info[data_id] = {
            "label": label,
            "value": tuple([int(val) for val in value])
        }
        return data_id

    def set_queue(self, ts, data_id, data_type):
        for flag in range(len(ts)):
            self.queue.append([int(ts[flag]), data_id, data_type, flag])

    def sort_data(self):
        arr = list(map(tuple, self.queue)) 
        dt = np.dtype([("ts", np.int32), ("id", np.int32), ("data_type", np.int32), ("act_type", np.int32)])
        arr = np.array(arr, dtype=dt)
        self.queue = list(map(list, np.sort(arr, order=["ts", "act_type"]).tolist()))

    
    