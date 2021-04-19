#!/bin/bash

# ratio data experiments
# IND 
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_15000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_10000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_15000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT 
python3 main.py -m naive -p ant_5000_3_product.csv -c ant_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_5000_3_product.csv -c ant_15000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_10000_3_product.csv -c ant_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_15000_3_product.csv -c ant_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# FC
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_15000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_10000_3_product.csv -c fc_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_15000_3_product.csv -c fc_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200


