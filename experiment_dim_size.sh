#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# dimension size experiments
# IND 
python3 main.py -p ind_100000_2_product.csv -c ind_100000_2_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_100000_5_product.csv -c ind_100000_5_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_100000_7_product.csv -c ind_100000_7_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT 
python3 main.py -p ant_100000_2_product.csv -c ant_100000_2_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_100000_3_product.csv -c ant_100000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_100000_5_product.csv -c ant_100000_5_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_100000_7_product.csv -c ant_100000_7_customer.csv -k 50 -g 3 -s 100 -e 200
# FC


