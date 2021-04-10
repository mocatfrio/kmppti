import math
import itertools
import numpy as np
from prettyprinter import pprint

from kmppti.Skyline import is_pivot
from kmppti.Constant import PRODUCT, CUSTOMER

class Grid:
    def __init__(self, grid_size, dim_size, max_val):
        # initialize grid as numpy array
        self.grid = np.empty(shape=[grid_size for i in range(int(dim_size))], dtype=object)   
        # calculate range 
        if max_val % grid_size == 0:
            self.range = int(max_val / grid_size)
        else:
            self.range = int((max_val + (grid_size - (max_val % grid_size))) / grid_size)
        # set boundary 
        self.boundary = {}
        grid_pos = list(np.ndindex(*self.grid.shape))
        for pos in grid_pos:
            axis = [[i * self.range, i * self.range + self.range] for i in pos]
            self.boundary[pos] = list(itertools.product(*axis))
        # init empty pos 
        self.pos = {}                                           # position - tuple

    def insert(self, obj_id, obj_type, obj_val):
        pos = self.get_pos(obj_id, obj_val)
        if not self.grid[pos]:
            self.grid[pos] = [{}, {}]
        if self.is_product(obj_type):
            self.grid[pos][obj_type][obj_id] = {
                "value": obj_val,
                "rsl_result": None
            }
        if self.is_customer(obj_type):
            self.grid[pos][obj_type][obj_id] = {
                "value": obj_val,
                "dsl_result": None,
                "dominance_boundary": None,
                "node_id": None
            }
    
    def remove(self, obj_id, obj_type):
        pos = self.pos.pop(obj_id, None)
        if pos: 
            obj_data = self.grid[pos][obj_type].pop(obj_id)
            if all(not d for d in self.grid[pos]):
                self.grid[pos] = None
        return obj_data
    
    def update_customer(self, obj_id, dsl_result=None, dominance_boundary=None, node_id=None):
        pos = self.get_pos(obj_id)
        if self.is_exist(pos, CUSTOMER, obj_id):
            self.grid[pos][CUSTOMER][obj_id]["dsl_result"] = dsl_result
            self.grid[pos][CUSTOMER][obj_id]["dominance_boundary"] = dominance_boundary
            self.grid[pos][CUSTOMER][obj_id]["node_id"] = node_id
    
    def update_product(self, obj_id, rsl_result=None):
        pos = self.get_pos(obj_id)
        if self.is_exist(pos, PRODUCT, obj_id):
            if rsl_result:
                self.grid[pos][PRODUCT][obj_id]["rsl_result"] = rsl_result
    
    # Getter 
    def get_empty_pos(self):
        return list(map(tuple, np.argwhere(self.grid == None)))
    
    def get_filled_pos(self):
        return list(map(tuple, np.argwhere(self.grid != None)))
    
    def get_pos(self, obj_id, obj_val=None):
        if obj_val:
            self.pos[obj_id] = tuple([0 if not val else (int((val/self.range) - 1) if val % self.range == 0 else math.floor(val/self.range)) for val in obj_val])
        return self.pos.get(obj_id, None)
    
    def get_value(self, obj_id, obj_type):
        pos = self.get_pos(obj_id)
        if self.is_exist(pos, obj_type, obj_id):
            return self.grid[pos][obj_type][obj_id]["value"]
    
    def get_dsl_result(self, c_id):
        pos = self.get_pos(c_id)
        if self.is_exist(pos, CUSTOMER, c_id):
            return self.grid[pos][CUSTOMER][c_id]["dsl_result"]
    
    def get_rsl_result(self, p_id):
        pos = self.get_pos(p_id)
        if self.is_exist(pos, PRODUCT, p_id):
            return self.grid[pos][PRODUCT][p_id]["rsl_result"]

    def get_node_id(self, c_id):
        pos = self.get_pos(c_id)
        if self.is_exist(pos, CUSTOMER, c_id):
            return self.grid[pos][CUSTOMER][c_id]["node_id"]

    def get_data(self, obj_type, space=None, obj_id=None):
        result = {}
        if not space and not obj_id:
            space = self.get_filled_pos()
        if space:
            if isinstance(space, tuple):
                space = [space]
            space = list(set(space).intersection(set(self.get_filled_pos())))  # just take position that are filled
            cand = [self.grid[pos][obj_type] for pos in space]
            result = {k: v for d in cand for k, v in d.items()}
        if obj_id: 
            if not isinstance(obj_id, list):
                obj_id = [obj_id]
            for o_id in obj_id:
                pos = self.get_pos(o_id)
                result[o_id] = self.grid[pos][obj_type][o_id]
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
        return set(self.boundary[pos]).intersection(set(self.boundary[n_pos]))
    
    def search_space(self, obj_id, obj_val):
        obj_pos = self.get_pos(obj_id)
        queue = [obj_pos]
        result = []                         # containing non-dominating partition                                           
        while queue:
            pos = queue.pop(0)
            result.append(pos)
            # immediate neighboring partition
            neighbor = self.get_neighbor(pos, result)
            for n_pos in neighbor:
                n_is_dominated = False
                for res_pos in result:
                    res_cand = self.get_data(PRODUCT, res_pos)
                    # get border which intersect with this space
                    n_border = self.get_nearest_border(res_pos, n_pos)  
                    for p_id, p_val in res_cand.items():
                        # jika ada satu saja p yang mendominasi kedua n_border, 
                        # maka obj itu adalah pivot thd n_pos
                        if is_pivot(p_val["value"], n_border, obj_val):
                            n_is_dominated = True
                            break
                    if n_is_dominated: 
                        break
                if not n_is_dominated:
                    queue.append(n_pos)
        return result 
    
    def is_product(self, obj_type):
        return obj_type == PRODUCT 
    
    def is_customer(self, obj_type):
        return obj_type == CUSTOMER
    
    def is_exist(self, pos, obj_type, obj_id):
        try:
            return obj_id in self.grid[pos][obj_type]
        except:
            return False

    def remove_rsl_result(self, p_id, c_id):
        pos = self.get_pos(p_id)
        if pos:
            if self.get_rsl_result(p_id):
                if c_id in self.grid[pos][PRODUCT][p_id]["rsl_result"]:
                    self.grid[pos][PRODUCT][p_id]["rsl_result"].remove(c_id)
