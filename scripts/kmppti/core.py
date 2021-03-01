import kmppti.data_handler as kd
import kmppti.skyline as ks
from kmppti.constant import PRODUCT, CUSTOMER

TS = 0
ID = 1
TYPE = 2
ACT = 3
NAME = 4
VALUE = -1

def compute(c_file, p_file, grid_size, time_start, time_end):
    data = kd.Data(c_file, p_file, time_start, time_end)
    main(data, grid_size)

def precompute(c_file, p_file, grid_size):
    pass

def main(data, grid_size):
    max_ts = data.get_max_ts()
    max_val = data.get_max_val()
    dim_size = data.get_dim_size()
    p_size = data.get_p_size()

    grid = kd.Grid(grid_size, dim_size, max_val)
    dsl = ks.DynamicSkyline(grid)
    pbox = kd.PandoraBox(max_ts, p_size)
    now_ts = 0
    while now_ts <= max_ts:
        objs = data.get(now_ts)
        now_ts += 1
        if len(objs) == 0: continue
        for obj in objs:
            print(obj)
            if is_enter(obj[ACT]):
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                if is_customer(obj[TYPE]):
                    dsl_result = dsl.get(obj[ID], obj[TYPE], obj[VALUE])
                    if dsl_result:
                        pbox.insert(obj[ID], obj[TS], dsl_result)
                else:
                    # get rsl but pending
                    cust = grid.get_data(CUSTOMER)
                    for c_id, c_val in cust.items():
                        dsl_result = dsl.get_update(c_id, c_val, obj[ID], obj[VALUE])
                        if dsl_result:
                            pbox.insert(c_id, obj[TS], dsl_result)
            else:
                grid.remove(obj[ID], obj[TYPE])
                if is_customer(obj[TYPE]):
                    dsl.remove_record(obj[ID])
                    pbox.remove_record(obj[ID], obj[TS])
                else:
                    # when product out 
                    pass
        pbox.update(now_ts - 1)
        print("")

def is_enter(act):
    return act == 0

def is_customer(data_type):
    return data_type == 0
