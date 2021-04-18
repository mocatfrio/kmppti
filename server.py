import os
import sys
import time
import getopt

import multiprocessing
import multiprocessing.managers
from dotenv import load_dotenv
from pprint import pprint

from streaming_kmppti.queue import Queue
from streaming_kmppti.constant import *

load_dotenv()

class MyListManager(multiprocessing.managers.BaseManager):
    pass

# global variables
data = [
    0,          # timer
    None,       # grid size,
    None,       # k
    None,       # max boundary 
    # queue (list of list)
]

def get_shared_data():
    return data

def main(argv):
    # register server
    MyListManager.register("streaming_server", get_shared_data, exposed=['__getitem__', '__setitem__', '__str__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'])

    # start server
    manager = MyListManager(address=('/tmp/mypipe'), authkey=b"")
    manager.start()
    shared_data = manager.streaming_server()
    
    # get arguments
    short_command = "hp:c:k:g:"
    long_command = ["help", "product=", "customer=", "k=", "grid="]
    try:
        opts, args = getopt.getopt(argv, short_command, long_command)
    except getopt.GetoptError:
        print("python3 server.py -p <product_file> -c <customer_file> -k <k_size> -g <grid_size>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("python3 server.py -p <product_file> -c <customer_file> -k <k_size> -g <grid_size>")
            sys.exit()
        elif opt in ("-p", "--product"):
            p_file = os.getenv("DATASET_PATH") + arg
        elif opt in ("-c", "--customer"):
            c_file = os.getenv("DATASET_PATH") + arg
        elif opt in ("-k", "--k"):
            k = int(arg)
        elif opt in ("-g", "--grid"):
            grid_size = int(arg)
    if not "grid_size" in locals():
        grid_size = 3
    if not "k" in locals():
        k = 3
    # import product and customer files as queue 
    queue = Queue(p_file, c_file)
    
    # set the grid size and k 
    shared_data[GRID_SIZE] = grid_size
    shared_data[K_SIZE] = k
    shared_data[MAX_BOUNDARY] = queue.get_max_boundary()
    
    input("Start the client first!")

    # start timer
    time_start = time.time()
    while True:
        print("Minutes: " + str(shared_data[TIMER]))
        try:
            objs = queue.pop(shared_data[TIMER])
            for obj in objs:
                shared_data.append(obj)
                print("Send " + str(obj))
            time.sleep(TIME_SLEEP)
            shared_data[TIMER] += 1
        except IndexError:
            pass
    
    # shutdown server
    print("Streaming done!")
    input("Press any key (NOT Ctrl-C!) to kill server (but kill client first)".center(50, "-"))
    manager.shutdown()

if __name__ == '__main__':
    main(sys.argv[1:])
