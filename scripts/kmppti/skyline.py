import numpy as np
from prettyprinter import pprint

from kmppti.constant import PRODUCT, CUSTOMER

ID = 0
VAL = 1
DOMINATED = 2

class Skyline:
    def __init__(self, grid):
        self.grid = grid
    
    def _search_space(self, obj_id, obj_val):
        # perlu dicek ulang kayaknya untuk ketepatan
        # HARUS DIBENAHI KARNA KURANG EFEKTIF 
        obj_pos = self.grid.get_pos(obj_id)
        queue = [obj_pos]
        result = []   # containing non-dominating partition                                           
        while queue:
            pos = queue.pop(0)
            result.append(pos)
            # immediate neighboring partition
            neighbor = self.grid.get_neighbor(pos, result)
            for n_pos in neighbor:
                n_cand = self.grid.get_data(PRODUCT, n_pos)
                n_is_dominated = False
                for res_pos in result:
                    res_cand = self.grid.get_data(PRODUCT, res_pos)
                    # get border which intersect with this space
                    n_border = self.grid.get_nearest_border(res_pos, n_pos)  
                    for p_id, p_val in res_cand.items():
                        # jika ada satu saja p yang mendominasi kedua n_border, 
                        # maka obj itu adalah pivot thd n_pos
                        if self._is_pivot(p_val, n_border, obj_val):
                            n_is_dominated = True
                            break
                    if n_is_dominated: 
                        break
                if not n_is_dominated:
                    queue.append(n_pos)
        return result 

    def _is_dominating(self, val1, val2, q_val):
        lte = 0
        lt = 0
        for i in range(len(val1)):
            diff1 = abs(q_val[i] - val1[i])
            diff2 = abs(q_val[i] - val2[i])
            if diff1 <= diff2:
                lte += 1
                if diff1 < diff2:
                    lt += 1
        return lte == len(val1) and lt > 0  
    
    def _is_pivot(self, p_val, n_border, q_val):
        p_dominating = 0
        for pos in n_border:
            if self._is_dominating(p_val, pos, q_val):
                p_dominating += 1
        return p_dominating == len(n_border)


class DynamicSkyline(Skyline):
    def __init__(self, grid, record):
        Skyline.__init__(self, grid)
        self.record = record

    def get(self, c_id, c_val):
        space = self._search_space(c_id, c_val)
        cand = self.grid.get_data(PRODUCT, space)
        result = []
        if cand: 
            # comparing
            result = [[key, val, []] for key, val in cand.items()]
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    if self._is_dominating(result[i][VAL], result[j][VAL], c_val):
                        result[j][DOMINATED].append(result[i][ID])
                    if self._is_dominating(result[j][VAL], result[i][VAL], c_val):
                        result[i][DOMINATED].append(result[j][ID])
        self.record.set_dsl(c_id, result)
    
    def get_update(self, c_id, c_val, p_id, p_val):
        result = self.record.get_dsl(c_id)
        if not result:
            result = [[p_id, p_val, []]]
        else:
            result.append([p_id, p_val, []])
            for i in range(len(result)):
                if self._is_dominating(result[i][VAL], p_val, c_val):
                    result[-1][DOMINATED].append(result[i][ID])
                if self._is_dominating(p_val, result[i][VAL], c_val):
                    result[i][DOMINATED].append(p_id)
        self.record.set_dsl(c_id, result)
    

class ReverseSkyline(Skyline):
    def __init__(self, grid):
        Skyline.__init__(self, grid)
    
    def get(self, p_id, p_val):
        orthant = self.__init_orthant(len(p_val))
        # dynamic skyline based on p query
        space = self._search_space(p_id, p_val)
        cand = self.grid.get_data(PRODUCT, space)
        if not cand:
            # gaada saingan 
            return self.grid.get_data(CUSTOMER)
        result = [[key, val, 0] for key, val in cand.items()]
        for i in range(len(result)):
            if result[i][DOMINATED]:
                continue
            for j in range(i + 1, len(result)):
                if result[j][DOMINATED]:
                    continue
                if self._is_dominating(result[i][VAL], result[j][VAL], p_val):
                    result[j][DOMINATED] = 1
                if self._is_dominating(result[j][VAL], result[i][VAL], p_val):
                    result[i][DOMINATED] = 1
        # midpoint skyline
        for res in result:
            if res[DOMINATED]: continue
            res_area = self.__get_orthant(res[VAL], p_val)
            midpoint = self.__get_midpoint(res[VAL], p_val)
            if not orthant[res_area]:
                orthant[res_area] = []
            orthant[res_area].append([res[ID], midpoint])
        # search space for cust
        space = self.__search_space_cust(p_id, p_val, orthant)
        return self.grid.get_data(CUSTOMER, space)

    def __init_orthant(self, dim_size):
        size = [2 for i in range(int(dim_size))]
        return np.empty(shape=size, dtype=object)

    def __get_orthant(self, p_val, p_val_query):
        return tuple([0 if p_val[i] <= p_val_query[i] else 1 for i in range(len(p_val))])

    def __get_midpoint(self, p_val1, p_val2):
        midpoint = []
        for i in range(len(p_val1)):
            midpoint.append((p_val1[i] + p_val2[i])/2)
        return midpoint
    
    def __get_orthant_border(self, border, p_val):
        orthant = None
        for pos in border:
            if not orthant:
                orthant = self.__get_orthant(pos, p_val)
                continue
            if orthant != self.__get_orthant(pos, p_val):
                return None
        return orthant
    
    def __search_space_cust(self, p_id, p_val, msl_result):
        p_pos = self.grid.get_pos(p_id)
        queue = [p_pos]
        result = []   # containing non-dominating partition                                           
        while queue:
            pos = queue.pop(0)
            result.append(pos)
            # immediate neighboring partition
            neighbor = self.grid.get_neighbor(pos, result)
            for n_pos in neighbor:
                n_cand = self.grid.get_data(PRODUCT, n_pos)
                n_is_dominated = False
                for res_pos in result:
                    n_border = self.grid.get_nearest_border(res_pos, n_pos)
                    n_orthant = self.__get_orthant_border(n_border, p_val)
                    if n_orthant and msl_result[n_orthant]:
                        for msl in msl_result[n_orthant]:
                            if self._is_pivot(msl[VAL], n_border, p_val):
                                n_is_dominated = True
                                break
                    if n_is_dominated: 
                        break
                if not n_is_dominated:
                    queue.append(n_pos)
        return result 

            