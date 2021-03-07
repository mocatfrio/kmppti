import time
import numpy as np
import multiprocessing
import multiprocessing.managers

from streaming_kmppti.const import *

class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("streaming_server")

def main():
    manager = MyListManager(address=('/tmp/mypipe'), authkey=b"")
    manager.connect()
    shared_data = manager.streaming_server()

    print("shared queue = ", shared_data[QUEUE:])
    print("shared index = ", shared_data[COL])
    print("shared label = ", shared_data[LABEL])

    # start timer
    time_start = time.time()
    while True:
        try:
            print("minutes: ", str(shared_data[TIMER]))
        except IndexError:
            pass
        queue = [x for x in shared_data[QUEUE:]]
        if len(queue) > 1:
            indexes = get_index(queue, shared_data[TIMER], shared_data[COL])
            for i in range(len(indexes)-1, -1, -1):
                print ("remove ", str(shared_data[indexes[i][0] + QUEUE]))
                shared_data.pop(indexes[i][0] + QUEUE)
        time.sleep(TIME_SLEEP)

def get_index(data, current_time, index_of):
    """This is function to get index of data that has ts_out equal with the current time

    Args:
        data (list): queue of data
        current_time (int): global time
        index (dict): key-value pair that stores column name and index in list

    Returns:
        indexes (list): list of data's index that fulfill the requirements
    """
    numpy_arr = np.array(data, dtype=object)
    all_indexes = np.asarray(np.where(numpy_arr == current_time)).T.tolist()
    indexes = [i for i in all_indexes if i[1] == index_of["ts_out"]]
    return indexes
    
if __name__ == '__main__':
    main() 