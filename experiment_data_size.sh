#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# data size experiments
# IND
python3 main.py -p ind_50000_3_product.csv -c ind_50000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_75000_3_product.csv -c ind_75000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_200000_3_product.csv -c ind_200000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ind_300000_3_product.csv -c ind_300000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT
python3 main.py -p ant_50000_3_product.csv -c ant_50000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_75000_3_product.csv -c ant_75000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_100000_3_product.csv -c ant_100000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_200000_3_product.csv -c ant_200000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -p ant_300000_3_product.csv -c ant_300000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# FC


