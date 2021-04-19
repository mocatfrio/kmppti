#!/bin/bash

# data size experiments
# IND
python3 main.py -m online_kmppti -p ind_1000_3_product.csv -c ind_1000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_2000_3_product.csv -c ind_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_7000_3_product.csv -c ind_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_10000_3_product.csv -c ind_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT
python3 main.py -m online_kmppti -p ant_1000_3_product.csv -c ant_1000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_2000_3_product.csv -c ant_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_5000_3_product.csv -c ant_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_7000_3_product.csv -c ant_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_10000_3_product.csv -c ant_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# FC
python3 main.py -m online_kmppti -p fc_1000_3_product.csv -c fc_1000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_7000_3_product.csv -c fc_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_10000_3_product.csv -c fc_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
