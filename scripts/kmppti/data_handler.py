import numpy as np
import math, itertools
from prettyprinter import pprint

from kmppti.constant import PRODUCT, CUSTOMER

SCORE = 0
TS = 1

class Data:
    def __init__(self, c_file, p_file, time_start=None, time_end=None):
        self.timestamp = []
        self.name = []
        self.value = []
        self.p_size = 0
        self.__import(c_file, CUSTOMER, time_start, time_end)
        self.__import(p_file, PRODUCT, time_start, time_end)
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
                self.p_size += data_type        # count product data 
    
    def __set_name(self, name):
        data_id = len(self.name)
        self.name.append(name)
        return data_id
    
    def __set_value(self, value):
        self.value.append(tuple([int(val) for val in value]))

    def __set_timestamp(self, ts, data_id, data_type):
        for flag in range(len(ts)):
            self.timestamp.append([int(ts[flag]), data_id, data_type, flag])

    def __sort(self):
        arr = np.array(self.timestamp)
        self.timestamp = arr[arr[:, 0].argsort()].tolist()
    
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
        if not space:
            space = self.get_filled_pos()
        if isinstance(space, tuple):
            space = [space]
        space = list(set(space).intersection(set(self.get_filled_pos())))
        if not space:
            return None
        cand = [self.grid[pos][data_type] for pos in space]
        cand_flatten = {k: v for d in cand for k, v in d.items()}
        if not cand_flatten: 
            return None
        return cand_flatten
    
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
    def __init__(self, max_ts, p_size):
        self.pbox = [[0 for ts in range(max_ts)] for p in range(p_size)]
        self.record = {}

    """
    Public Functions
    """

    def insert(self, c_id, ts, dsl_result):
        # calculate score
        score = self.__calc_score(dsl_result)
        for p_id in dsl_result:
            self.__update_pbox(p_id, ts, score)
        self.__update_record(c_id, ts, dsl_result, score)
        print("INSERT")
        self.__print_pbox()
        pprint(self.record)
    
    def update(self, now_ts, c_id=None):
        if c_id:
            c_keys = [c_id]
        else:
            c_keys = list(self.record.keys())
        for c_id in c_keys:
            for p_id in self.record[c_id]:
                while self.record[c_id][p_id][TS] < now_ts:
                    print("now_ts: ", now_ts)
                    self.record[c_id][p_id][TS] += 1
                    self.__update_pbox(p_id, self.record[c_id][p_id][TS], self.record[c_id][p_id][SCORE])
        print("UPDATE")
        self.__print_pbox()
        pprint(self.record)

    def remove_record(self, c_id, ts):
        self.update(ts, c_id)
        self.record.pop(c_id, None)

    def __calc_score(self, dsl_result):
        if dsl_result:
            return 1/len(dsl_result)
        return 0

    def __update_record(self, c_id, ts, dsl_result, score):
        if c_id not in self.record:
            self.record[c_id] = {}
        self.record[c_id].update({p_id: [score, ts] for p_id in dsl_result})

    def __update_pbox(self, p_id, ts, score):
        p_id -= len(self.pbox)
        self.pbox[p_id][ts - 1] += score

    def __print_pbox(self):
        for pb in self.pbox:
            print(pb)

    