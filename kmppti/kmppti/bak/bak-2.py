import numpy as np
import math, itertools, copy
from prettyprinter import pprint

from kmppti.Constant import PRODUCT, CUSTOMER

VAL = 0
DOMINATED = 1
ID_ARR = 0
VAL_ARR = 1
DOM_ARR = 2

class Data:
    def __init__(self, c_file, p_file, time_start=None, time_end=None):
        self.timestamp = []
        self.name = {}
        self.value = []
        self.__import(p_file, PRODUCT, time_start, time_end)
        self.p_size = len(self.name)
        self.__import(c_file, CUSTOMER, time_start, time_end)
        self.__sort()

    """
    initialization
    """
    def __import(self, file_path, data_type, time_start, time_end):
        with open(file_path, "r") as csv_file:
            first_row = True
            for row in csv_file:
                if first_row: first_row = False; continue
                col = row.split(',')[1:]
                if time_start and time_end:
                    if int(col[1]) > time_end: continue
                    else: 
                        if int(col[2]) > time_end: col[2] = time_end
                    if int(col[2]) < time_start: continue
                    else: 
                        if int(col[1]) < time_start: col[1] = time_start
                data_id = self.__set_name(col[0])
                self.__set_value(col[3:])
                self.__set_timestamp(col[1:3], data_id, data_type)
    
    def __set_name(self, name):
        data_id = len(self.name)
        self.name[data_id] = name
        return data_id
    
    def __set_value(self, value):
        self.value.append(tuple([int(val) for val in value]))

    def __set_timestamp(self, ts, data_id, data_type):
        for flag in range(len(ts)):
            self.timestamp.append([int(ts[flag]), data_id, data_type, flag])

    def __sort(self):
        arr = list(map(tuple, self.timestamp)) 
        dt = np.dtype([("ts", np.int32), ("id", np.int32), ("data_type", np.int32), ("act_type", np.int32)])
        arr = np.array(arr, dtype=dt)
        self.timestamp = list(map(list, np.sort(arr, order=["ts", "act_type"]).tolist()))

    def print(self):
        pprint(self.timestamp)
        # pprint(self.name)
        # pprint(self.value)
    
    """
    Public function
    """
    def get(self, now_ts):
        result = []
        while True: 
            if not self.timestamp: 
                break
            if self.timestamp[0][0] != now_ts: 
                break
            data = self.timestamp.pop(0)
            data += [self.name[data[1]], self.value[data[1]]]
            result.append(data)
        return result

    def get_max_ts(self):
        return np.asarray(self.timestamp).max(axis=0, keepdims=True)[0][0]

    def get_max_val(self):
        return list(np.amax(self.value, axis=0))
    
    def get_dim_size(self):
        return len(self.value[0])
    
    def get_p_size(self):
        return self.p_size
    
    def get_label(self):
        return self.name




class Record:
    def __init__(self):
        self.record = {}

    def set_dsl(self, c_id, dsl_result):
        if c_id not in self.record:
            self.record[c_id] = {}
        self.record[c_id].update({res[ID_ARR]: [res[VAL_ARR], res[DOM_ARR]] for res in dsl_result})
    
    def get_cid(self):
        return list(self.record.keys())
    
    def get_pid(self, c_id):
        return list(self.record[c_id].keys())
    
    def get_pid_dsl(self, c_id):
        try:
            return [key for key, val in self.record[c_id].items() if not val[DOMINATED]]
        except KeyError:
            return []
    
    def get_dsl(self, c_id, get_all=False):
        try:
            if get_all:
                return [[key, val[VAL], False] for key, val in self.record[c_id].items()]
            return [[key, val[VAL], val[DOMINATED]] for key, val in self.record[c_id].items() if not val[DOMINATED]]
        except KeyError:
            return []
    
    def remove_cid(self, c_id):
        self.record.pop(c_id, None)
    
    def remove_pid(self, c_id, p_id):
        self.record[c_id].pop(p_id, None)

    # def remove_pid(self, p_id):
    #     # update when product out
    #     for c_id in self.record:
    #         if p_id in self.record[c_id]:
    #             p_data = self.record[c_id].pop(p_id)
    #             if p_data[DOMINATED]: continue
    #             for other_p_id in self.record[c_id]:
    #                 if p_id in self.record[c_id][other_p_id][DOMINATED]:
    #                     self.record[c_id][other_p_id][DOMINATED].remove(p_id)
                
    def print(self):
        pprint(self.record)