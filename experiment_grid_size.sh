#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# grid size experiments
# IND 
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 20 -g 3 -s 100 -e 200
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 50 -g 5 -s 100 -e 200
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 100 -g 7 -s 100 -e 200
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 200 -g 9 -s 100 -e 200
# ANT 
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 20 -g 3 -s 100 -e 200
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 50 -g 5 -s 100 -e 200
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 100 -g 7 -s 100 -e 200
python3 kmppti/main.py -p ind_100000_3_product.csv -c ind_100000_3_customer.csv -k 200 -g 9 -s 100 -e 200
# FC


