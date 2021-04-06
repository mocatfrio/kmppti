import csv, sys
import kmppti.data_handler as kd
import kmppti.Skyline as ks
from kmppti.Constant import PRODUCT, CUSTOMER, ENTER

TS = 0
ID = 1
TYPE = 2
ACT = 3
NAME = 4
VALUE = -1

def compute(c_file, p_file, time_start, time_end):
    data = kd.Data(c_file, p_file, time_start, time_end)
    return get_pbox(data), data.get_label()

def precompute(c_file, p_file, pbox_file):
    data = kd.Data(c_file, p_file)
    pbox_data = get_pbox(data)
    with open(pbox_file, 'w') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerows(pbox_data)
    csv_file.close()

def get_pbox(data):
    # get information from data 
    max_ts = data.get_max_ts()
    max_val = data.get_max_val()        # list, max value each dimension
    dim_size = data.get_dim_size()
    p_size = data.get_p_size()
    # initialization
    active_products = []
    r_tree = kd.RTree(max_val)
    record = kd.Record()
    dsl = ks.DynamicSkyline(active_products, r_tree, record)
    # rsl = ks.ReverseSkyline()
    pbox = kd.PandoraBox(max_ts, p_size, record)
    # start processing 
    now_ts = 0
    while now_ts <= max_ts:
        print("=============================================")
        print("TS", now_ts)
        objs = data.get(now_ts)
        for obj in objs:
            print(obj)
            if obj[ACT] is ENTER:
                # grid.insert(obj[ID], obj[TYPE], obj[VALUE])
                if obj[TYPE] is CUSTOMER:
                    dsl.compute(obj[ID], obj[VALUE])
                    # print("DSL Result of ", obj[ID], " : ", record.get_pid_dsl(obj[ID]))
                else:
                    active_products.append([obj[ID], obj[VALUE]])
                    # cust = grid.get_data(CUSTOMER)
                    # # cust = rsl.get(obj[ID], obj[VALUE])
                    # for c_id, c_val in cust.items():
                    #     dsl.update(c_id, c_val, obj[ID], obj[VALUE])
            # else:
            #     grid.remove(obj[ID], obj[TYPE])
            #     if obj[TYPE] is CUSTOMER:
            #         record.remove_cid(obj[ID])
            #     else:
            #         dsl.recompute(obj[ID], grid)
        #     record.print()
        # pbox.update(now_ts)
        # pbox.print()
        now_ts += 1
    # return pbox.get()

