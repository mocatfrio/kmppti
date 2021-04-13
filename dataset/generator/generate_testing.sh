#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# GENERATE DATA
# IND 
python3 main.py -c generate -t ind -n 5000 -d 3 -l product
python3 main.py -c generate -t ind -n 5000 -d 3 -l customer

# PREPARE DATA 
# IND 
python3 main.py -c prepare -f ind_5000_3_product.csv
python3 main.py -c prepare -f ind_5000_3_customer.csv

# PARTITION DATA
# IND 
python3 main.py -c partition -f ind_5000_3_product.csv -n 1000
python3 main.py -c partition -f ind_5000_3_customer.csv -n 1000
python3 main.py -c partition -f ind_5000_3_product.csv -n 2000
python3 main.py -c partition -f ind_5000_3_customer.csv -n 2000