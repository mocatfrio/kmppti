import numpy as np
import math, itertools
from prettyprinter import pprint

from kmppti.constant import PRODUCT, CUSTOMER

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
        return np.amax(self.value)
    
    def get_dim_size(self):
        return len(self.value[0])
    
    def get_p_size(self):
        return self.p_size
    
    def get_label(self):
        return self.name
    

class Grid:
    def __init__(self, grid_size, dim_size, max_val):
        self.grid = self.__init_grid(grid_size, dim_size)   # grid - numpy array
        self.range = self.__set_range(grid_size, max_val)   # range - int
        self.border = self.__set_border()                   # border - list of tuple
        self.pos = {}                                       # position - tuple

    """
    initialization
    """
    def __init_grid(self, grid_size, dim_size):
        size = [grid_size for i in range(int(dim_size))]
        return np.empty(shape=size, dtype=object)
    
    def __set_range(self, grid_size, max_val):
        if max_val % grid_size == 0:
            return int(max_val / grid_size)
        return int((max_val + (grid_size - (max_val % grid_size))) / grid_size)

    def __set_border(self):
        border = {}
        grid_pos = list(np.ndindex(*self.grid.shape))
        for pos in grid_pos:
            axis = []
            for i in pos:
                axis.append([i * self.range, i * self.range + self.range])
            border[pos] = list(itertools.product(*axis))
        return border
    
    def __get_pos(self, obj_id, obj_val):
        self.pos[obj_id] = tuple([0 if not val else (int((val/self.range) - 1) if val % self.range == 0 else math.floor(val/self.range)) for val in obj_val])
        return self.pos[obj_id]
    
    """
    Public function
    """
    def insert(self, obj_id, obj_type, obj_val):
        pos = self.__get_pos(obj_id, obj_val)
        if not self.grid[pos]:
            self.grid[pos] = [{}, {}]
        self.grid[pos][obj_type][obj_id] = obj_val
    
    def remove(self, obj_id, obj_type):
        pos = self.pos.pop(obj_id, None)
        if not pos: 
            return
        self.grid[pos][obj_type].pop(obj_id)
        if all(not d for d in self.grid[pos]):
            self.grid[pos] = None

    def get_empty_pos(self):
        return list(map(tuple, np.argwhere(self.grid == None)))
    
    def get_filled_pos(self):
        return list(map(tuple, np.argwhere(self.grid != None)))
    
    def get_pos(self, obj_id):
        return self.pos.get(obj_id, None)
    
    def get_val(self, obj_id, obj_type):
        obj_pos = self.get_pos(obj_id)
        return self.grid[obj_pos][obj_type][obj_id]

    def get_data(self, data_type, space=None):
        result = {}
        if not space:
            space = self.get_filled_pos()
        if isinstance(space, tuple):
            space = [space]
        space = list(set(space).intersection(set(self.get_filled_pos())))
        if not space: 
            return result
        cand = [self.grid[pos][data_type] for pos in space]
        result = {k: v for d in cand for k, v in d.items()}
        return result
    
    def get_neighbor(self, pos, excluded_space):
        axis = []
        for i in range(len(pos)):
            axis.append([])
            if pos[i] - 1 >= 0: 
                axis[i].append(pos[i] - 1)
            axis[i].append(pos[i])
            if pos[i] + 1 < len(self.grid):
                axis[i].append(pos[i] + 1)
        neighbor = list(set(itertools.product(*axis)) - set(excluded_space) - set(self.get_empty_pos()))
        return neighbor
    
    def get_nearest_border(self, pos, n_pos):
        return set(self.border[pos]).intersection(set(self.border[n_pos]))

    
class PandoraBox:
    def __init__(self, max_ts, p_size, record):
        self.pbox = [[0 for ts in range(max_ts)] for p in range(p_size)]
        self.record = record
    
    def get(self):
        return self.pbox

    def update(self, now_ts, c_id=None):
        if c_id: 
            c_keys = [c_id]
        else: 
            c_keys = self.record.get_cid() 
        for c_id in c_keys:
            dsl_result = self.record.get_pid_dsl(c_id)
            for p_id in dsl_result:
                score = 1/len(dsl_result)
                # now_ts - 1 because ts start from 1 (assumption)
                self.pbox[p_id][now_ts - 1] += score
    
    def print(self):
        for pb in self.pbox:
            print(pb)


class Record:
    def __init__(self):
        self.record = {}

    def set_dsl(self, c_id, dsl_result):
        self.record[c_id] = {res[ID_ARR]: [res[VAL_ARR], res[DOM_ARR]] for res in dsl_result}   
    
    def get_cid(self):
        return list(self.record.keys())
    
    def get_pid(self, c_id):
        return list(self.record[c_id].keys())
    
    def get_pid_dsl(self, c_id):
        try:
            return [key for key, val in self.record[c_id].items() if not val[DOMINATED]]
        except KeyError:
            return []
    
    def get_dsl(self, c_id):
        try:
            return [[key, val[VAL], val[DOMINATED]] for key, val in self.record[c_id].items()]
        except KeyError:
            return []
        
    def remove_cid(self, c_id):
        self.record.pop(c_id, None)
    
    def remove_pid(self, p_id):
        # update when product out
        for c_id in self.record:
            if p_id in self.record[c_id]:
                p_data = self.record[c_id].pop(p_id)
                if p_data[DOMINATED]: continue
                for other_p_id in self.record[c_id]:
                    if p_id in self.record[c_id][other_p_id][DOMINATED]:
                        self.record[c_id][other_p_id][DOMINATED].remove(p_id)
                
    def print(self):
        pprint(self.record)