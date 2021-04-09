import copy 
from prettyprinter import pprint


LEFT = 0
RIGHT = 1

class RTree:
    def __init__(self, dim_size, max_boundary):
        self.rtree = {}         # {node_id: [parent_id | boundary | [child_id, child_id, child_id]]} max 3 child
        self.root_id = self.set_global_root(max_boundary)
        self.dim_size = dim_size 
    
    """ Public Function """

    def insert(self, c_id, c_val, dsl_result):
        # generate boundary box 
        boundary_box = self.calculate_boundary(c_val, dsl_result)
        parent_id = self.choose_leaf(boundary_box)
        # get new node id 
        droplet_id = self.add_node(parent_id, boundary_box, c_id=c_id)
        # append child
        self.set_childs(parent_id, droplet_id)
        # adjust tree 
        self.adjust_tree(droplet_id)
        return droplet_id

    def delete(self, node_id):
        self.condense_tree(node_id)
    
    def search(self, p_id=None, p_val=None, node_id=None):
        if not p_id is None:
            candidate = []
            boundary = self.calculate_boundary(p_val)
            branch_id = self.search_branch(boundary)
        if not node_id is None:
            branch_id = self.get_parent(node_id)
        c_id = []
        return c_id

    def update(self, c_id, c_val, dsl_result, node_id):
        # generate boundary box 
        boundary_box = self.calculate_boundary(c_val, dsl_result)
        # set boundary at the existing node id
        self.set_boundary(node_id, boundary_box)
        # adjust tree 
        self.adjust_tree(node_id)

    """ Basic setter, getter, and definer """

    def set_parent(self, node_id, parent_id):
        if self.is_exist(node_id):
            self.rtree[node_id][0] = parent_id
    
    def set_boundary(self, node_id, boundary):
        if self.is_exist(node_id):
            self.rtree[node_id][1] = boundary
    
    def set_childs(self, node_id, child_id):
        if self.is_exist(node_id):
            if not self.rtree[node_id][-1]:
                self.rtree[node_id][-1] = []
            if isinstance(child_id, list):
                self.rtree[node_id][-1] = child_id
            else:
                self.rtree[node_id][-1].append(child_id)
    
    def set_cid(self, node_id, c_id):
        if self.is_exist(node_id):
            self.rtree[node_id][2] = c_id
            if len(self.rtree[node_id]) == 3:
                self.rtree[node_id].append(None)
            
    def set_global_root(self, max_boundary):
        root_id = self.add_node(boundary_box=max_boundary)
        return root_id

    def get_parent(self, node_id):
        if self.is_exist(node_id):
            return self.rtree[node_id][0]
    
    def get_boundary(self, node_id):
        if self.is_exist(node_id):
            return self.rtree[node_id][1]
    
    def get_childs(self, node_id):
        if self.is_exist(node_id):
            return self.rtree[node_id][-1]
    
    def get_cid(self, c_id, node_id):
        childs = self.get_childs(node_id)
        if childs:
            for child_id in childs:
                self.get_cid(c_id, child_id)
        else:
            c_id.append(self.rtree[node_id][2])

    def is_exist(self, node_id):
        return node_id in self.rtree
    
    def is_droplet(self, node_id):
        return not self.get_childs(node_id)
    
    def is_leaf(self, node_id):
        childs = self.get_childs(node_id)
        if childs:
            return self.is_droplet(childs[0])

    def is_root(self, node_id):
        return not self.get_parent(node_id)
    
    def is_branch(self, node_id):
        return not (self.is_leaf(node_id) or self.is_droplet(node_id) or self.is_root(node_id))

    def is_overlap(self, boundary_1, boundary_2):
        # overlap in all dimensions
        is_overlap = True
        for i in range(self.dim_size): 
            a_left, a_right = boundary_1[i]
            b_left, b_right = boundary_2[i]
            if a_left > b_right or a_right < b_left:
                is_overlap = False
                break
        return is_overlap
    
    def is_overchild(self, node_id):
        return len(self.get_childs(node_id)) > 3
        
    """ R-Tree operation """

    """ Tree """

    def adjust_tree(self, node_id):
        if self.is_root(node_id):
            return
        parent_id = self.get_parent(node_id) 
        if self.is_overchild(parent_id):
            self.split_tree(parent_id)
        else:
            childs = self.get_childs(parent_id)
            boundary = self.adjust_boundary(childs)
            self.set_boundary(parent_id, boundary)
        self.adjust_tree(parent_id)

    def condense_tree(self, node_id):
        if self.is_root(node_id):
            return
        parent_id = self.get_parent(node_id)
        if self.is_droplet(node_id):
            self.rtree.pop(node_id, None)
            self.delete_node(parent_id, node_id)
        childs = self.get_childs(parent_id)
        if childs:
            boundary = self.adjust_boundary(childs)  
            self.set_boundary(parent_id, boundary)
        self.condense_tree(parent_id)
    
    def split_tree(self, node_id):
        # origin childs 
        childs = self.get_childs(node_id)
        # separate childs of current node
        splitted_child = self.split_child(childs)
        # set childs and adjust boundary of current node
        boundary = self.adjust_boundary(splitted_child[0])
        self.set_childs(node_id, splitted_child[0])
        self.set_boundary(node_id, boundary)
        # adjust boundary and add new node 
        new_boundary = self.adjust_boundary(splitted_child[1])
        new_node_id = self.add_node(None, boundary, splitted_child[1])
        # adjust parent of splitted child 
        for child_id in splitted_child[1]:
            self.set_parent(child_id, new_node_id)
        # if global root 
        if self.is_root(node_id):
            # create new branch 
            branch_boundary = self.adjust_boundary([node_id, new_node_id])
            branch_id = self.add_node(self.root_id, branch_boundary, [node_id, new_node_id])
            self.set_childs(self.root_id, branch_id)
        else:
            branch_id = self.get_parent(node_id)
        # set parent of new node 
        self.set_parent(new_node_id, branch_id)
        # adjust child of parent of new node 
        self.set_childs(branch_id, new_node_id)

    """ Node """

    def add_node(self, parent_id=None, boundary_box=None, child_id=None, c_id=None):
        # generate new node id 
        if self.rtree:
            node_id = max(self.rtree.keys()) + 1
        else:
            node_id = 1
        self.rtree[node_id] = [parent_id, boundary_box, None]
        if child_id:
            self.set_childs(node_id, child_id)
        if c_id:
            self.set_cid(node_id, c_id)
        return node_id
    
    def delete_node(self, node_id, child):
        # delete from child 
        if self.is_exist(node_id):
            if self.get_childs(node_id):
                self.rtree[node_id][-1].remove(child)
    
    """ Split Child """

    def split_child(self, childs):
        # quadratic-cost algorithm
        # pick seed 
        seeds = self.pick_seed(childs)
        set_of_childs = [[seeds[0]], [seeds[1]]]
        # split child based on seeds
        for child_id in childs:
            if child_id in seeds:
                continue
            selected_seed = self.choose_expansion(self.get_boundary(child_id), seeds)
            set_of_childs[seeds.index(selected_seed)].append(child_id)
        return set_of_childs
    
    def pick_seed(self, childs):
        # get two child id that form the largest boundary
        candidate = []
        for i in range(self.dim_size):
            # collect all boundaries of childs in each dimension  
            left_boundaries = [self.get_boundary(child_id)[i][LEFT] for child_id in childs]
            right_boundaries = [self.get_boundary(child_id)[i][RIGHT] for child_id in childs]
            # get max and min 
            min_val = min(left_boundaries)
            max_val = max(right_boundaries)
            diff = max_val - min_val
            # get the child_id 
            child_id_min = self.get_indices(left_boundaries, min_val)
            child_id_max = self.get_indices(right_boundaries, max_val)
            i = 0
            while i == 0:
                if child_id_min[i] == child_id_max[i]:
                    if len(child_id_min) < len(child_id_max):
                        child_id = [childs[child_id_min[i]], childs[child_id_max[i+1]]]
                    if len(child_id_min) > len(child_id_max):
                        child_id = [childs[child_id_min[i+1]], childs[child_id_max[i]]]
                else:
                    child_id = [childs[child_id_min[i]], childs[child_id_max[i]]]
                i += 1
            candidate.append([child_id, diff])
        # get the largest difference between all dimension 
        diff = [c[1] for c in candidate]
        max_diff = max(diff)
        seeds = candidate[diff.index(max_diff)][0]  # [seed_id1, seed_id2]
        return seeds

    """ Boundary """
    
    def calculate_boundary(self, c_val, dsl_result=None):
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

    def adjust_boundary(self, childs):
        boundary = []
        for i in range(self.dim_size):
            # get max and min boundary
            min_val = min([self.get_boundary(child_id)[i][LEFT] for child_id in childs])
            max_val = max([self.get_boundary(child_id)[i][RIGHT] for child_id in childs])
            boundary.append([min_val, max_val])
        return boundary
    
    """ Choose Leaf """
    
    def choose_leaf(self, boundary_box, node_id=None):
        if not node_id:
            node_id = copy.deepcopy(self.root_id)
        if self.is_root(node_id) and self.is_droplet(node_id):
            # init new leaf 
            leaf_id = self.add_node(node_id, boundary_box, None)
            self.set_childs(node_id, leaf_id)
            return leaf_id
        # assume this is branch 
        child_id = self.choose_expansion(boundary_box, self.get_childs(node_id))
        # there is no overlap child
        if not child_id:
            # create new leaf 
            leaf_id = self.add_node(node_id, boundary_box, None)
            self.set_childs(node_id, leaf_id)
            return leaf_id
        if self.is_leaf(child_id):
            return child_id
        else:
            self.choose_leaf(boundary_box, child_id)
    
    def choose_expansion(self, boundary_box, childs, return_overlapped_childs=False):
        min_enlargement = None 
        expanded_child = None
        overlapped_childs = 0
        for child_id in childs:
            child_boundary = self.get_boundary(child_id)
            if self.is_overlap(boundary_box, child_boundary):
                # for each child, check if they are overlapped 
                enlargement = self.calculate_enlargement(child_boundary, boundary_box)
                if (not min_enlargement) or (enlargement < min_enlargement):
                    min_enlargement = enlargement
                    expanded_child = child_id
                overlapped_childs += 1
        if return_overlapped_childs:
            return overlapped_childs, expanded_child
        else:
            return expanded_child

    def calculate_enlargement(self, boundary_1, boundary_2):
        enlargement = 0
        for i in range(self.dim_size):
            # get overlap limit 
            min_val = min([boundary_1[i][LEFT], boundary_2[i][LEFT]])
            max_val = max([boundary_1[i][RIGHT], boundary_2[i][RIGHT]])
            if boundary_1[i][LEFT] < min_val:
                enlargement += abs(min_val - boundary_1[i][LEFT])
            if boundary_2[i][LEFT] < min_val:
                enlargement += abs(min_val - boundary_2[i][LEFT]) 
            if boundary_1[i][RIGHT] > max_val:
                enlargement += abs(boundary_1[i][RIGHT] - max_val) 
            if boundary_2[i][RIGHT] > max_val:
                enlargement += abs(boundary_2[i][RIGHT] - max_val) 
        return enlargement
    
    """ Choose Branch """

    def search_branch(self, boundary, node_id=None):
        if not node_id:
            node_id = copy.deepcopy(self.root_id)
        if self.is_root(node_id) and self.is_droplet(node_id):
            return None
        # assume this is branch 
        childs = self.get_childs(node_id)
        overlapped_childs, child_id = self.choose_expansion(boundary, childs, return_overlapped_childs=True)
        if overlapped_childs == len(childs):
            return node_id
        else:
            if child_id:
                self.search_branch(boundary, child_id)
            else:
                return node_id
    
    """ Others """

    def get_indices(self, mylist, value):
        return [i for i,x in enumerate(mylist) if x==value]

    