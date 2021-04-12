#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# python3 main.py -d precomputing -p ind_5_2_product.csv -c ind_5_2_customer.csv 
python3 main.py -d precomputing -p ind_5000_2_product.csv -c ind_5000_2_customer.csv 


