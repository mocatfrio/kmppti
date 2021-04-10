import sys
import os
import getopt
import time
from dotenv import load_dotenv
from prettyprinter import pprint

from kmppti.Method import kmppti
from kmppti.Logger import Logger

load_dotenv()

def main(argv):
    short_command = "hp:c:k:g:s:e:"
    long_command = ["help", "product=", "customer=", "k=", "grid=", "time_start=", "time_end="]
    try:
        opts, args = getopt.getopt(argv, short_command, long_command)
    except getopt.GetoptError:
        print("main.py -p <product_file> -c <customer_file> -k <k_size> -g <grid_size> -s <time_start> -e <time_end>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("main.py -p <product_file> -c <customer_file> -k <k_size> -g <grid_size> -s <time_start> -e <time_end>")
            sys.exit()
        elif opt in ("-p", "--product"):
            p_file = os.getenv("DATASET_PATH") + arg
        elif opt in ("-c", "--customer"):
            c_file = os.getenv("DATASET_PATH") + arg
        elif opt in ("-k", "--k"):
            k = int(arg)
        elif opt in ("-g", "--grid"):
            grid = int(arg)
        elif opt in ("-s", "--time_start"):
            time_start = int(arg)
        elif opt in ("-e", "--time_end"):
            time_end = int(arg)
    # run method 
    log = Logger(os.getenv("LOG_PATH"), p_file, [k, grid, time_start, time_end])
    log.start()
    result = kmppti(p_file, c_file, k, grid, time_start, time_end)
    pprint(result)
    log.end()
    log.write()
    
if __name__ == '__main__':
    main(sys.argv[1:])
    
    