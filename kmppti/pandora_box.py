from prettyprinter import pprint

ID = 0
VAL = 1

class PandoraBox:
    def __init__(self, max_ts, p_size):
        self.pbox = [[0 for ts in range(max_ts)] for p in range(p_size)]
    
    def get(self):
        return self.pbox

    def update(self, now_ts, c_data):
        for key, val in c_data.items():
            if not val["dsl_result"]:
                continue
            for p_data in val["dsl_result"]:
                score = 1/len(val["dsl_result"])
                # now_ts - 1 because ts start from 1 (assumption)
                self.pbox[p_data[ID]][now_ts - 1] += score
    
    def print(self):
        for pb in self.pbox:
            print(pb)