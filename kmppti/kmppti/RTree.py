import copy 
from prettyprinter import pprint


class RTree:
    def __init__(self, grid, dim_size, max_boundary):
        self.rtree = {}
        self.root_id = 0
        self.__set(self.root_id, boundary=max_boundary)
        self.grid = grid
        self.dim_size = dim_size 

    """ Customer Insertion """

    def insert(self, c_id, c_val, dsl_result):
        # generate boundary box 
        boundary_box = self.calculate_boundary(c_val, dsl_result)
        print("Calculate boundary box: ", boundary_box)
        parent_id = self.choose_leaf(boundary_box)
        print("Choose leaf: ", parent_id)
        # get new node id 
        node_id = self.add_node(parent_id, boundary_box)
        print("New node id: ", node_id)
        # append child
        self.__set(parent_id, childs=node_id)
        print("Append child")
        pprint(self.rtree)
        # adjust tree 
        self.adjust_tree(node_id)
        print("Adjust R-tree")
        pprint(self.rtree)
    
    def calculate_boundary(self, c_val, dsl_result):
        boundary = []
        # per dimension 
        for i in range(self.dim_size):
            if dsl_result:
                values = [res[1][i] for res in dsl_result]
            else:
                values = []
            values.append(c_val[i])
            boundary.append([min(values), max(values)])
        return boundary
    
    def choose_leaf(self, boundary_box, node_id=None):
        if not node_id:
            print("not node_id")
            node_id = copy.deepcopy(self.root_id)
        if self.is_leaf(node_id):
            print("is leaf")
            return node_id
        if self.is_droplet(node_id):
            print("is droplet")
            # if there is no existing leaf 
            # create new leaf 
            leaf_id = self.add_node(node_id, boundary_box, None)
            self.__set(node_id, childs=leaf_id)
            return leaf_id
        min_enlargement = None
        selected_child = None
        childs = self.__get(node_id, childs=True)
        for child_id in childs:
            enlargement = self.calculate_enlargement(self.__get(child_id, boundary=True), boundary_box)
            if (not min_enlargement) or (enlargement < min_enlargement):
                min_enlargement = enlargement
                selected_child = child_id
        self.choose_leaf(boundary_box, selected_child)
    
    def add_node(self, parent_id, boundary_box, child_id=None):
        # generate new node id 
        node_id = max(self.rtree.keys()) + 1
        if child_id:
            child_id = [child_id]
        self.rtree[node_id] = [parent_id, boundary_box, child_id]
        return node_id
    
    def adjust_tree(self, node_id):
        if self.is_root(node_id):
            return
        parent_id = self.__get(node_id, parent=True)
        if self.has_excess_child(parent_id):
            self.split_node(parent_id)
        else:
            childs = self.__get(parent_id, childs=True)
            boundary = self.adjust_boundary(childs=childs)
            self.__set(parent_id, boundary=boundary)
        self.adjust_tree(parent_id)
    
    """ Customer Deletion """ 

    def delete(self, c_id):
        node_id = self.grid.get_node_id(c_id)
        print("Node id: ", node_id)
        self.condense_tree(node_id)
        print("Condense R-tree")
        pprint(self.rtree)
    
    def condense_tree(self, node_id):
        if self.is_leaf(node_id):
            deleted_node = self.rtree.pop(node_id, None)
            parent_id = deleted_node[0]
            self.delete_child(parent_id, node_id)
        else:
            parent_id = self.__get(node_id, parent=True)
        childs = self.__get(parent_id, childs=True)
        boundary = self.adjust_boundary(childs=childs)  
        self.__set(parent_id, boundary=boundary)
        if self.is_root(node_id):
            return
        self.condense_tree(parent_id)
    
    def delete_child(self, node_id, child):
        self.rtree[node_id][-1].remove(child)

    def __set(self, node_id, parent=None, boundary=None, products=None, childs=None):
        # {node_id: [parent_id | boundary | [child_id, child_id, child_id]]} max 3 child
        if node_id not in self.rtree:
            self.rtree[node_id] = [None, None, None]
        if parent:
            self.rtree[node_id][0] = parent_id
        if boundary:
            self.rtree[node_id][1] = boundary
        if childs:
            if not self.rtree[node_id][-1]:
                self.rtree[node_id][-1] = []
            if isinstance(childs, list):
                self.rtree[node_id][-1] = childs
            else:
                self.rtree[node_id][-1].append(childs)
    
    def __get(self, node_id, parent=False, boundary=False, products=False, childs=False):
        if node_id in self.rtree:
            if parent:
                return self.rtree[node_id][0]
            if boundary:
                return self.rtree[node_id][1]
            if childs:
                return self.rtree[node_id][-1]
            return self.rtree[node_id]
        return None
    
    def split_node(self, node_id):
        # separate childs of of current node
        childs = self.__get(node_id, childs=True)
        set_of_childs = self.split_child(childs)
        # set childs of current node
        self.__set(node_id, childs=set_of_childs[0])
        # adjust boundary of current node
        childs = self.__get(parent_id, childs=True)
        boundary = self.adjust_boundary(childs=childs)
        self.__set(node_id, boundary=boundary)            
        # adjust boundary of new node 
        new_boundary = self.adjust_boundary(childs=set_of_childs[1])
        # add new node 
        new_node_id = self.add_node(None, boundary, set_of_childs[1])
        # check root 
        if self.is_root(node_id):
            # create new root 
            root_boundary = self.adjust_boundary(boundary_1=boundary, boundary_2=new_boundary)
            root_id = self.add_node(None, root_boundary, [node_id, new_node_id])
            # set parent of current node
            self.__set(node_id, parent=root_id)
            # set new root id 
            self.root_id = root_id
        else:
            root_id = self.__get(node_id, parent=True)
        # set parent of new node 
        self.__set(new_node_id, parent=root_id)

    def split_child(self, childs):
        # quadratic-cost algorithm
        # get two child id that form the largest boundary
        seeds = self.pick_seed(childs)
        set_of_childs = [[seeds[0]], [seeds[1]]]
        for child_id in childs:
            if child_id in seeds:
                continue
            min_enlargement = None
            selected_seed = None
            for seed_id in seeds:
                enlargement = self.calculate_enlargement(self.__get(seed_id, boundary=True), self.__get(new_id, boundary=True))
                if (not min_enlargement) or (enlargement < min_enlargement):
                    min_enlargement = enlargement
                    selected_seed = seed_id
            set_of_childs[seeds.index(selected_seed)].append(child_id)
        return set_of_childs

    def pick_seed(self, childs):
        candidate = []
        for i in range(self.dim_size):
            # collect all boundaries of childs in each dimension  
            boundaries = [self.__get(child_id, boundary=True)[i] for child_id in childs]
            # get max and min 
            min_val = min(boundaries)
            max_val = max(boundaries)
            diff = max_val[1] - min_val[0]
            # get the child_id 
            child_id = [childs[boundaries.index(min_val)], childs[boundaries.index(max_val)]]
            candidate.append([child_id, diff])
        max_diff = max([c[1] for c in candidate])
        seeds = candidate[candidate.index(max_diff)][0]  # [seed_id1, seed_id2]
        return seeds
    
    def adjust_boundary(self, childs=None, boundary_1=None, boundary_2=None):
        boundary = []
        for i in range(self.dim_size):
            # collect all boundaries of childs in each dimension  
            if childs:
                boundaries = [self.__get(child_id, boundary=True)[i] for child_id in childs]
            if boundary_1 and boundary_2:
                boundaries = [boundary_1[i], boundary_2[i]]
            # get max and min boundary
            min_val = min(boundaries)
            max_val = max(boundaries)
            boundary.append([min_val[0], max_val[1]])
        return boundary

    def calculate_enlargement(self, current_boundary, new_boundary):
        enlargement = 0
        for i in range(self.dim_size):
            diff = [current_boundary[i][j] - new_boundary[i][j] for j in range(2)]
            if diff[0] < 0:
                enlargement += abs(diff[0])
            if diff[1] > 0:
                enlargement += abs(diff[1])
        return enlargement
    
    def is_droplet(self, node_id):
        childs = self.__get(node_id, childs=True) 
        return not childs
    
    def is_leaf(self, node_id):
        childs = self.__get(node_id, childs=True) 
        if childs:
            return self.is_leaf(childs[0])

    def is_root(self, node_id):
        parent = self.__get(node_id, parent=True) 
        return not parent
    
    def has_excess_child(self, node_id):
        childs = self.__get(node_id, childs=True) 
        return len(childs) > 3

    