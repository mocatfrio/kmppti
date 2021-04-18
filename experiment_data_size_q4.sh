#!/bin/bash

# data size experiments
# IND
python3 main.py -m online_kmppti -p ind_2000_3_product.csv -c ind_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_7000_3_product.csv -c ind_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_10000_3_product.csv -c ind_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ind_20000_3_product.csv -c ind_20000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT
python3 main.py -m online_kmppti -p ant_2000_3_product.csv -c ant_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_5000_3_product.csv -c ant_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_7000_3_product.csv -c ant_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_10000_3_product.csv -c ant_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p ant_20000_3_product.csv -c ant_20000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# FC
python3 main.py -m online_kmppti -p fc_2000_3_product.csv -c fc_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_7000_3_product.csv -c fc_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_10000_3_product.csv -c fc_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m online_kmppti -p fc_20000_3_product.csv -c fc_20000_3_customer.csv -k 50 -g 3 -s 100 -e 200

# IND
python3 main.py -m naive -p ind_2000_3_product.csv -c ind_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_5000_3_product.csv -c ind_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_7000_3_product.csv -c ind_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_10000_3_product.csv -c ind_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ind_20000_3_product.csv -c ind_20000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# ANT
python3 main.py -m naive -p ant_2000_3_product.csv -c ant_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_5000_3_product.csv -c ant_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_7000_3_product.csv -c ant_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_10000_3_product.csv -c ant_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p ant_20000_3_product.csv -c ant_20000_3_customer.csv -k 50 -g 3 -s 100 -e 200
# FC
python3 main.py -m naive -p fc_2000_3_product.csv -c fc_2000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_5000_3_product.csv -c fc_5000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_7000_3_product.csv -c fc_7000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_10000_3_product.csv -c fc_10000_3_customer.csv -k 50 -g 3 -s 100 -e 200
python3 main.py -m naive -p fc_20000_3_product.csv -c fc_20000_3_customer.csv -k 50 -g 3 -s 100 -e 200
