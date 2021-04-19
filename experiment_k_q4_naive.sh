#!/bin/bash

# k size experiments
# IND 
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 20 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 100 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 200 -g 3 -s 100 -e 200
# ANT 
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 20 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 100 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 200 -g 3 -s 100 -e 200
# FC
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 20 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 100 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 200 -g 3 -s 100 -e 200

