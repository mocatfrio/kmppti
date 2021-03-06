import csv

import kmppti.data_handler as kd
import kmppti.skyline as ks
from kmppti.constant import PRODUCT, CUSTOMER, ENTER

TS = 0
ID = 1
TYPE = 2
ACT = 3
NAME = 4
VALUE = -1

def compute(c_file, p_file, grid_size, time_start, time_end):
    data = kd.Data(c_file, p_file, time_start, time_end)
    return get_pbox(data, grid_size), data.get_label()

def precompute(c_file, p_file, grid_size, pbox_file):
    data = kd.Data(c_file, p_file)
    pbox_data = get_pbox(data, grid_size)
    with open(pbox_file, 'w') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerows(pbox_data)
    csv_file.close()

def get_pbox(data, grid_size):
    # get information from data 
    max_ts = data.get_max_ts()
    max_val = data.get_max_val()
    dim_size = data.get_dim_size()
    p_size = data.get_p_size()
    # initialization
    grid = kd.Grid(grid_size, dim_size, max_val)
    record = kd.Record()
    dsl = ks.DynamicSkyline(grid, record)
    pbox = kd.PandoraBox(max_ts, p_size, record)
    # start processing 
    now_ts = 0
    while now_ts <= max_ts:
        # print("=============================================")
        # print("TS", now_ts)
        objs = data.get(now_ts)
        for obj in objs:
            # print(obj)
            if obj[ACT] is ENTER:
                grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                if obj[TYPE] is CUSTOMER:
                    dsl.get(obj[ID], obj[TYPE], obj[VALUE])
                else:
                    # get rsl but pending
                    cust = grid.get_data(CUSTOMER)
                    for c_id, c_val in cust.items():
                        dsl.get_update(c_id, c_val, obj[ID], obj[VALUE])
            else:
                grid.remove(obj[ID], obj[TYPE])
                if obj[TYPE] is CUSTOMER:
                    record.remove_cid(obj[ID])
                else:
                    record.remove_pid(obj[ID])
        # record.print()
        pbox.update(now_ts)
        # pbox.print()
        now_ts += 1
    return pbox.get()

