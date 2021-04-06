

    
class ReverseSkyline(Skyline):
    def __init__(self, grid):
        Skyline.__init__(self, grid)
    
    def get(self, p_id, p_val):
        orthant = self.__init_orthant(len(p_val))
        # dynamic skyline based on p query
        cand = self.grid.get_data(PRODUCT, space )
        if cand:
            result = [[key, val, False] for key, val in cand.items()]
            self.compare(result, p_val)
            result = [res for res in result if not res[DOMINATED]]
            # midpoint skyline
            for res in result:
                res_area = self.get_orthant(res[VAL], p_val)
                midpoint = [(res[VAL][i] + p_val[i])/2 for i in range(len(res[VAL]))]
                if not orthant[res_area]:
                    orthant[res_area] = []
                orthant[res_area].append([res[ID], midpoint])
            # search space for cust
            
            space = self.__search_space(p_id, p_val, orthant)
            return self.grid.get_data(CUSTOMER, space)
        return self.grid.get_data(CUSTOMER)

    def __init_orthant(self, dim_size):
        size = [2 for i in range(int(dim_size))]
        return np.empty(shape=size, dtype=object)

    def get_orthant(self, p_val, p_val_query):
        return tuple([0 if p_val[i] <= p_val_query[i] else 1 for i in range(len(p_val))])
    
    def __search_space(self, p_id, p_val, msl_result):
        p_pos = self.grid.get_pos(p_id)
        queue = [p_pos]
        result = []   # containing non-dominating partition                                           
        while queue:
            pos = queue.pop(0)
            result.append(pos)
            # immediate neighboring partition
            neighbor = self.grid.get_neighbor(pos, result)
            for n_pos in neighbor:
                n_is_dominated = False
                for res_pos in result:
                    n_border = self.grid.get_nearest_border(res_pos, n_pos)
                    n_orthant = self.__get_orthant_border(n_border, p_val)
                    if n_orthant and msl_result[n_orthant]:
                        for msl in msl_result[n_orthant]:
                            if self.is_pivot(msl[VAL], n_border, p_val):
                                n_is_dominated = True
                                break
                    if n_is_dominated: 
                        break
                if not n_is_dominated:
                    queue.append(n_pos)
        return result 

    def __get_orthant_border(self, border, p_val):
        orthant = None
        for pos in border:
            if not orthant:
                orthant = self.get_orthant(pos, p_val)
                continue
            if orthant != self.get_orthant(pos, p_val):
                return None
        return orthant
            

    # def search_space(self, obj_id, obj_val):
    #     # perlu dicek ulang kayaknya untuk ketepatan
    #     obj_pos = self.grid.get_pos(obj_id)
    #     queue = [obj_pos]
    #     result = []   # containing non-dominating partition                                           
    #     while queue:
    #         pos = queue.pop(0)
    #         result.append(pos)
    #         # immediate neighboring partition
    #         neighbor = self.grid.get_neighbor(pos, result)
    #         for n_pos in neighbor:
    #             n_is_dominated = False
    #             for res_pos in result:
    #                 res_cand = self.grid.get_data(PRODUCT, res_pos)
    #                 # get border which intersect with this space
    #                 n_border = self.grid.get_nearest_border(res_pos, n_pos)  
    #                 for p_id, p_val in res_cand.items():
    #                     # jika ada satu saja p yang mendominasi kedua n_border, 
    #                     # maka obj itu adalah pivot thd n_pos
    #                     if self.is_pivot(p_val, n_border, obj_val):
    #                         n_is_dominated = True
    #                         break
    #                 if n_is_dominated: 
    #                     break
    #             if not n_is_dominated:
    #                 queue.append(n_pos)
    #     return result 
    
    # def is_pivot(self, p_val, n_border, q_val):
    #     p_dominating = 0
    #     for pos in n_border:
    #         if self.check_domination(p_val, pos, q_val) == 1:
    #             p_dominating += 1
    #     return p_dominating == len(n_border)



class DynamicSkyline(Skyline):
    def __init__(self, rtree):
        Skyline.__init__(self, rtree)
    
    def compute(self, c_id, c_val):
        # using r-tree 
        result = [res + [False] for res in copy.deepcopy(self.products)]
        self.compare(result, c_val)
        result = [res for res in result if not res[DOMINATED]]
        bounding_box = self.get_bounding_box(result, c_val)
        print(c_id, " - ", c_val)
        pprint(result)
        print("bounding box ", bounding_box)
        # insert bounding box to r-tree 
        # self.rtree.insert(c_id, c_val, bounding_box, result)
        # insert record of dsl result
        self.record.set_dsl(c_id, result)
    
    def get_bounding_box(self, dsl_result, c_val):
        bb = []
        # per dimension 
        for i in range(len(dsl_result[0][VAL])):
            values = [res[VAL][i] for res in dsl_result]
            values.append(c_val[i])
            bb.append([min(values), max(values)])
        return bb

    def compare(self, arr, c_val):
        # divide and conquer algorithm
        if len(arr) > 1:
            # finding the mid of the array
            mid = len(arr)//2
            # dividing array into left and right 
            left = arr[:mid]
            right = arr[mid:]
            self.compare(left, c_val)
            self.compare(right, c_val)
            # check domination 
            i = 0
            while i < len(left):
                if left[i][DOMINATED]:
                    i += 1
                    continue
                j = 0
                while j < len(right):
                    if right[j][DOMINATED]:
                        j += 1
                        continue
                    dom = self.check_domination(left[i][VAL], right[j][VAL], c_val)
                    if dom == 1:
                        right[j][DOMINATED] = True
                    elif dom == 2:
                        left[i][DOMINATED] = True
                    j += 1
                i += 1
            # sorting 
            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i][DOMINATED] <= right[j][DOMINATED]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1
            # checking if any element was left
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1

    # def compute(self, c_id, c_val):
    #     space = self.search_space(c_id, c_val)
    #     cand = self.grid.get_data(PRODUCT, space)
    #     result = []
    #     if cand: 
    #         result = [[key, val, False] for key, val in cand.items()]
    #         self.compare(result, c_val)
    #     self.record.set_dsl(c_id, result)
    
    # def update(self, c_id, c_val, p_id, p_val):
    #     # cara 1 - dicompare pake divide n conquer
    #     # result = self.record.get_dsl(c_id)
    #     # result.append([p_id, p_val, False])
    #     # self.compare(result, c_val)
    #     # cara 2 - dicompare 1 1 
    #     result = self.record.get_dsl(c_id)
    #     new_cand = [p_id, p_val, False]
    #     for i in range(len(result)):
    #         dom = self.check_domination(new_cand[VAL], result[i][VAL], c_val)
    #         if dom == 1:
    #             result[i][DOMINATED] = True
    #         elif dom == 2:
    #             new_cand[DOMINATED] = True
    #             break
    #     result.append(new_cand)
    #     self.record.set_dsl(c_id, result)
    
    # def recompute(self, p_id, grid):
    #     for c_id in self.record.get_cid():
    #         self.record.remove_pid(c_id, p_id)
    #         result = self.record.get_dsl(c_id, True)
    #         self.compare(result, grid.get_val(c_id, CUSTOMER))
    #         self.record.set_dsl(c_id, result)
    

