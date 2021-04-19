#!/bin/bash

# dimension size experiments
# IND 
python3 main.py -m naive -p ind_2000_2_product.csv -c ind_2000_2_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_2000_5_product.csv -c ind_2000_5_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_2000_7_product.csv -c ind_2000_7_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT 
python3 main.py -m naive -p ant_2000_2_product.csv -c ant_2000_2_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_2000_5_product.csv -c ant_2000_5_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_2000_7_product.csv -c ant_2000_7_customer.csv -k 50 -g 3 -s 100 -e 200
# FC
python3 main.py -m naive -p fc_2000_2_product.csv -c fc_2000_2_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_2000_5_product.csv -c fc_2000_5_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_2000_7_product.csv -c fc_2000_7_customer.csv -k 50 -g 3 -s 100 -e 200

