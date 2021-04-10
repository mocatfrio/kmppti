import copy 
import sys
from collections import Counter
from prettyprinter import pprint


LEFT = 0
RIGHT = 1

class RTree:
    """
    There are four main components of RTree:
    - Root      : Main nodes
    - Branch    : Nodes between root and leaf (max 3 childs)
    - Leaf      : Nodes for sticking droplets (max 3)
    - Droplet   : Nodes for storing each c boundary

    """
    def __init__(self, dim_size, max_boundary):
        self.rtree = {}         # {node_id: [parent_id | boundary | [child_id, child_id, child_id]]} max 3 child
        self.root_id = self.set_global_root(max_boundary)
        self.dim_size = dim_size 
    
    """ Public Function """

    def insert(self, c_id, c_val, dsl_result):
        # calculate boundary box based on c value and dsl result
        boundary_box = self.calculate_boundary(c_val, dsl_result)
        # get leaf id for sticking droplet
        leaf_id = self.choose_leaf(boundary_box)
        # create new droplet
        droplet_id = self.add_node(leaf_id, boundary_box, c_id=c_id)
        # append droplet to leaf
        self.set_childs(leaf_id, droplet_id)
        # adjust tree 
        self.adjust_tree(droplet_id)
        # return the droplet id 
        return droplet_id

    def delete(self, node_id):
        # delete droplet
        self.condense_tree(node_id)
    
    def search(self, p_id=None, p_val=None, node_id=None):
        # search starting branch 
        if not p_id is None:
            candidate = []
            boundary = self.calculate_boundary(p_val)
            branch_id = self.choose_branch(boundary)
        if not node_id is None:
            branch_id = self.get_parent(node_id)
        # get all droplets start from the selected branch
        c_id = []
        if branch_id:
            self.get_cid(c_id, branch_id)
        return c_id

    def update(self, c_id, c_val, dsl_result, node_id):
        # calculate boundary box 
        boundary_box = self.calculate_boundary(c_val, dsl_result)
        # set boundary at the existing node id
        self.set_boundary(node_id, boundary_box)
        # adjust tree 
        self.adjust_tree(node_id)

    """ Basic setter, getter, and definer """
    
    def set_global_root(self, max_boundary):
        root_id = self.add_node(boundary_box=max_boundary)
        return root_id

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
            if self.is_overchild(node_id):
                # split and automatically adjust the boundary 
                self.split_tree(node_id, is_root=True)
                return
            else:
                return
        elif not self.is_droplet(node_id):
            if self.is_overchild(node_id):
                # split and automatically adjust the boundary 
                self.split_tree(node_id)
            else:
                # adjust the boundary 
                childs = self.get_childs(node_id)
                boundary = self.adjust_boundary(childs)
                self.set_boundary(node_id, boundary)
        parent_id = self.get_parent(node_id) 
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
    
    def split_tree(self, node_id, is_root=False):
        # origin childs 
        childs = self.get_childs(node_id)
        # separate childs of current node
        splitted_child = self.split_child(childs)
        # adjust first node 
        new_boundary_1 = self.adjust_boundary(splitted_child[0])
        if is_root:
            new_node_id_1 = self.add_node(node_id, new_boundary_1, splitted_child[0])
            # adjust parent of splitted child 1
            for child_id in splitted_child[0]:
                self.set_parent(child_id, new_node_id_1)
        else:
            # if it's not root, adjust the existing node 
            new_node_id_1 = node_id
            self.set_childs(new_node_id_1, splitted_child[0])
            self.set_boundary(new_node_id_1, new_boundary_1)
        # adjust second node 
        if is_root:
            parent_id = node_id
        else:
            parent_id = self.get_parent(node_id)
        new_boundary_2 = self.adjust_boundary(splitted_child[1])
        new_node_id_2 = self.add_node(parent_id, new_boundary_2, splitted_child[1])
        # adjust parent of splitted child on second node
        for child_id in splitted_child[1]:
            self.set_parent(child_id, new_node_id_2)
        # adjust child of root to the new nodes
        if is_root:
            self.set_childs(parent_id, [new_node_id_1, new_node_id_2])
        else:
            self.set_childs(parent_id, new_node_id_2)

    """ Node """

    def add_node(self, parent_id=None, boundary_box=None, child_id=None, c_id=None):
        # generate new node id 
        if self.rtree:
            node_id = max(self.rtree.keys()) + 1
        else:
            node_id = 1
        # add new node
        self.rtree[node_id] = [parent_id, boundary_box, None]
        if child_id:
            self.set_childs(node_id, child_id)
        if c_id:
            self.set_cid(node_id, c_id)
        return node_id

    def add_leaf(self, parent_id, boundary_box):
        # init new leaf 
        leaf_id = self.add_node(parent_id, boundary_box, None)
        self.set_childs(parent_id, leaf_id)
        return leaf_id
    
    def delete_node(self, node_id, child):
        # delete from child 
        if self.is_exist(node_id):
            if self.get_childs(node_id):
                self.rtree[node_id][-1].remove(child)
    
    """ Split Child """

    def split_child(self, childs):
        # using quadratic-cost algorithm
        # pick two seeds
        seeds = self.pick_seed(childs)
        set_of_childs = [[seeds[0]], [seeds[1]]]
        # split other childs based on the given seeds
        for child_id in childs:
            if child_id in seeds:
                continue
            selected_seed = self.choose_expansion(self.get_boundary(child_id), seeds)
            set_of_childs[seeds.index(selected_seed)].append(child_id)
        return set_of_childs
    
    def pick_seed(self, childs):
        # get two childs that form the largest boundary
        candidate = []
        for i in range(self.dim_size):
            # collect all boundaries of childs in each dimension  
            childs_left_temp = copy.deepcopy(childs)
            childs_right_temp = copy.deepcopy(childs)
            left_boundaries = [self.get_boundary(child_id)[i][LEFT] for child_id in childs_left_temp]
            right_boundaries = [self.get_boundary(child_id)[i][RIGHT] for child_id in childs_right_temp]
            min_val = None
            max_val = None
            child_min = None
            child_max = None
            selecting = True
            while selecting:
                # get max and min value
                min_temp = min(left_boundaries)
                max_temp = max(right_boundaries)
                # get the child_id 
                min_idx_temp = left_boundaries.index(min_temp)
                max_idx_temp = right_boundaries.index(max_temp)
                # if the childs index are same 
                if child_min:
                    if abs(min_val - min_temp) < abs(max_val - max_temp):
                        min_val = left_boundaries.pop(min_idx_temp)
                        child_min = childs_left_temp.pop(min_idx_temp)
                    else:
                        max_val = right_boundaries.pop(max_idx_temp)
                        child_max = childs_right_temp.pop(max_idx_temp)
                else:
                    min_val = left_boundaries.pop(min_idx_temp)
                    child_min = childs_left_temp.pop(min_idx_temp)
                    max_val = right_boundaries.pop(max_idx_temp)
                    child_max = childs_right_temp.pop(max_idx_temp)
                if child_min != child_max:
                    selecting = False
            diff = max_val - min_val
            candidate.append([[child_min, child_max], diff])
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
        # start from global root 
        if not node_id:
            node_id = copy.deepcopy(self.root_id)
        # if there is only root node 
        if self.is_root(node_id) and self.is_droplet(node_id):
            return self.add_leaf(node_id, boundary_box)
        # choose expansion 
        child_id = self.choose_expansion(boundary_box, self.get_childs(node_id))
        # there is no overlapping child
        if not child_id:
            return self.add_leaf(node_id, boundary_box)
        # if expanded child is leaf 
        if self.is_leaf(child_id):
            return child_id
        return self.choose_leaf(boundary_box, child_id)
    
    def choose_expansion(self, boundary_box, childs, return_overlapped_childs=False):
        # get the minimum expansion between origin boundary and new boundary
        enlargements = []
        total_childs = []
        is_overlapped = []
        overlapping_childs = 0
        for child_id in childs:
            child_boundary = self.get_boundary(child_id)
            # for each child, calculate enlargement, number of childs, and is_overlapped 
            enlargement = self.calculate_enlargement(boundary_box, child_boundary)
            enlargements.append(enlargement)
            childs_num = self.get_childs(child_id)
            if childs_num:
                childs_num = len(childs_num)
            total_childs.append(childs_num)
            is_overlapped.append(self.is_overlap(boundary_box, child_boundary))
        total_overlapping_childs = is_overlapped.count(True)
        # first-priority - overlapped 
        if any(is_overlapped):
            idx = self.get_indices(is_overlapped, True)
            enlargements = [enlargements[i] for i in idx]
            total_childs = [total_childs[i] for i in idx]
            is_overlapped = [is_overlapped[i] for i in idx]
            childs = [childs[i] for i in idx]
        # second-priority - enlargement 
        min_enlargement = min(enlargements)
        idx = self.get_indices(enlargements, min_enlargement)
        # third-priority - total childs 
        total_childs = [total_childs[i] for i in idx]
        childs = [childs[i] for i in idx]
        enlargements = [enlargements[i] for i in idx]
        if len(idx) > 1 and not all(tot == None for tot in total_childs):
            min_total_childs = min([tot for tot in total_childs if tot])
            expanded_child = childs[total_childs.index(min_total_childs)]
        else:
            expanded_child = childs[enlargements.index(min_enlargement)]
        if return_overlapped_childs:
            return total_overlapping_childs, expanded_child
        else:
            return expanded_child

    def calculate_enlargement(self, origin_boundary, new_boundary):
        enlargement = 0
        for i in range(self.dim_size):
            if origin_boundary[i][LEFT] > new_boundary[i][LEFT]:
                enlargement += origin_boundary[i][RIGHT] - new_boundary[i][RIGHT]
            if new_boundary[i][RIGHT] > origin_boundary[i][RIGHT]:
                enlargement += new_boundary[i][RIGHT] - origin_boundary[i][RIGHT]
        return enlargement
    
    """ Choose Branch """

    def choose_branch(self, boundary, node_id=None):
        # start from global root 
        if not node_id:
            node_id = copy.deepcopy(self.root_id)
        # if there is only root node 
        if self.is_root(node_id) and self.is_droplet(node_id):
            return None
        # assume this is leaf/branch 
        childs = self.get_childs(node_id)
        # check if all childs of this node overlap with the given boundary 
        overlapped_childs, child_id = self.choose_expansion(boundary, childs, return_overlapped_childs=True)
        # there is no overlapping child
        if not child_id:
            return None
        # if overlapping child same with the number of childs, return the branch
        if overlapped_childs == len(childs):
            return node_id
        else:
            # if it is leaf, return the leaf
            if self.is_leaf(child_id):
                return node_id
            # if it is branch, recursive
            else:
                self.choose_branch(boundary, child_id)
    
    """ Others """

    def get_indices(self, mylist, value):
        return [i for i,x in enumerate(mylist) if x==value]
