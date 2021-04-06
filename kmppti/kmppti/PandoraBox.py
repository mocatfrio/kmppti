
class PandoraBox:
    def __init__(self, max_ts, p_size, rtree):
        self.pbox = [[0 for ts in range(max_ts)] for p in range(p_size)]
        self.rtree = rtree
    
    def get(self):
        return self.pbox

    def update(self, now_ts, c_id=None):
        if c_id: 
            c_keys = [c_id]
        else: 
            c_keys = self.rtree.get_customer() 
        for c_id in c_keys:
            dsl_result = self.rtree.get_dsl_result(c_id)
            if not dsl_result:
                continue
            for p_id in dsl_result:
                score = 1/len(dsl_result)
                # now_ts - 1 because ts start from 1 (assumption)
                self.pbox[p_id][now_ts - 1] += score
    
    def print(self):
        for pb in self.pbox:
            print(pb)