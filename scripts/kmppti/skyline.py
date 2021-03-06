from prettyprinter import pprint

from kmppti.constant import PRODUCT

ID = 0
VAL = 1
DOMINATED = 2

class DynamicSkyline:
    def __init__(self, grid, record):
        self.grid = grid
        self.record = record

    def get(self, c_id, c_type, c_val):
        space = self.__search_space(c_id, c_type)
        cand = self.grid.get_data(PRODUCT, space)
        result = []
        if cand: 
            # comparing
            result = [[key, val, []] for key, val in cand.items()]
            for i in range(len(result)):
                for j in range(i + 1, len(result)):
                    if self.__is_dominating(result[i][VAL], result[j][VAL], c_val):
                        result[j][DOMINATED].append(result[i][ID])
                    if self.__is_dominating(result[j][VAL], result[i][VAL], c_val):
                        result[i][DOMINATED].append(result[j][ID])
        self.record.set_dsl(c_id, result)
    
    def get_update(self, c_id, c_val, p_id, p_val):
        result = self.record.get_dsl(c_id)
        if not result:
            result = [[p_id, p_val, []]]
        else:
            result.append([p_id, p_val, []])
            for i in range(len(result)):
                if self.__is_dominating(result[i][VAL], p_val, c_val):
                    result[-1][DOMINATED].append(result[i][ID])
                if self.__is_dominating(p_val, result[i][VAL], c_val):
                    result[i][DOMINATED].append(p_id)
        self.record.set_dsl(c_id, result)

    def __search_space(self, c_id, c_type):
        c_pos = self.grid.get_pos(c_id)
        c_val = self.grid.get_val(c_id, c_type)
        result = [c_pos]    # containing non-dominating partition
        queue = [c_pos]
        while queue:
            pos = queue.pop(0)
            neighbor = self.grid.get_neighbor(pos, result)
            cand = self.grid.get_data(PRODUCT, pos)
            if not cand:
                # memperluas space secara otomatis
                result += neighbor
                queue += neighbor
                continue
            for n_pos in neighbor:
                n_cand = self.grid.get_data(PRODUCT, n_pos)
                if not n_cand: 
                    continue
                # get border which intersect with this space
                n_border = self.grid.get_nearest_border(pos, n_pos)
                n_dominating = True
                for p_id, p_val in cand.items():
                    # jika ada satu saja p yang mendominasi kedua n_border, 
                    # maka obj itu adalah pivot thd n_pos
                    if self.__is_pivot(p_val, n_border, c_val):
                        n_dominating = False
                        break
                if n_dominating:
                    result.append(n_pos)
                    queue.append(n_pos)
        return result 
    
    def __is_pivot(self, p_val, n_border, c_val):
        p_dominating = 0
        for pos in n_border:
            if self.__is_dominating(p_val, pos, c_val):
                p_dominating += 1
        return p_dominating == len(n_border)
    
    def __is_dominating(self, val1, val2, q_val):
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

    