#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

# GENERATE DATA
# IND 
python3 main.py -c generate -t ind -n 300000 -d 3 -l product
python3 main.py -c generate -t ind -n 300000 -d 3 -l customer
python3 main.py -c generate -t ind -n 100000 -d 2 -l product
python3 main.py -c generate -t ind -n 100000 -d 2 -l customer
python3 main.py -c generate -t ind -n 100000 -d 5 -l product
python3 main.py -c generate -t ind -n 100000 -d 5 -l customer
python3 main.py -c generate -t ind -n 100000 -d 7 -l product
python3 main.py -c generate -t ind -n 100000 -d 7 -l customer

# ANT 
python3 main.py -c generate -t ant -n 300000 -d 3 -l product
python3 main.py -c generate -t ant -n 300000 -d 3 -l customer
python3 main.py -c generate -t ant -n 100000 -d 2 -l product
python3 main.py -c generate -t ant -n 100000 -d 2 -l customer
python3 main.py -c generate -t ant -n 100000 -d 5 -l product
python3 main.py -c generate -t ant -n 100000 -d 5 -l customer
python3 main.py -c generate -t ant -n 100000 -d 7 -l product
python3 main.py -c generate -t ant -n 100000 -d 7 -l customer

# FC (generate + prepare)
python3 main.py -c generate -t fc -n 300000 -d 3 -l product
python3 main.py -c generate -t fc -n 300000 -d 3 -l customer
python3 main.py -c generate -t fc -n 100000 -d 2 -l product
python3 main.py -c generate -t fc -n 100000 -d 2 -l customer
python3 main.py -c generate -t fc -n 100000 -d 5 -l product
python3 main.py -c generate -t fc -n 100000 -d 5 -l customer
python3 main.py -c generate -t fc -n 100000 -d 7 -l product
python3 main.py -c generate -t fc -n 100000 -d 7 -l customer

# PREPARE DATA 

# IND 
python3 main.py -c prepare -f ind_300000_3_product.csv
python3 main.py -c prepare -f ind_300000_3_customer.csv
python3 main.py -c prepare -f ind_100000_2_product.csv
python3 main.py -c prepare -f ind_100000_2_customer.csv
python3 main.py -c prepare -f ind_100000_5_product.csv
python3 main.py -c prepare -f ind_100000_5_customer.csv
python3 main.py -c prepare -f ind_100000_7_product.csv
python3 main.py -c prepare -f ind_100000_7_customer.csv

# ANT 
python3 main.py -c prepare -f ant_300000_3_product.csv
python3 main.py -c prepare -f ant_300000_3_customer.csv
python3 main.py -c prepare -f ant_100000_2_product.csv
python3 main.py -c prepare -f ant_100000_2_customer.csv
python3 main.py -c prepare -f ant_100000_5_product.csv
python3 main.py -c prepare -f ant_100000_5_customer.csv
python3 main.py -c prepare -f ant_100000_7_product.csv
python3 main.py -c prepare -f ant_100000_7_customer.csv

# PARTITION DATA

# IND 
python3 main.py -c partition -f ind_300000_3_product.csv -n 200000
python3 main.py -c partition -f ind_300000_3_customer.csv -n 200000
python3 main.py -c partition -f ind_300000_3_product.csv -n 100000
python3 main.py -c partition -f ind_300000_3_customer.csv -n 100000
python3 main.py -c partition -f ind_300000_3_product.csv -n 75000
python3 main.py -c partition -f ind_300000_3_customer.csv -n 75000
python3 main.py -c partition -f ind_300000_3_product.csv -n 50000
python3 main.py -c partition -f ind_300000_3_customer.csv -n 50000
python3 main.py -c partition -f ind_300000_3_customer.csv -n 33000

# ANT 
python3 main.py -c partition -f ant_300000_3_product.csv -n 200000
python3 main.py -c partition -f ant_300000_3_customer.csv -n 200000
python3 main.py -c partition -f ant_300000_3_product.csv -n 100000
python3 main.py -c partition -f ant_300000_3_customer.csv -n 100000
python3 main.py -c partition -f ant_300000_3_product.csv -n 75000
python3 main.py -c partition -f ant_300000_3_customer.csv -n 75000
python3 main.py -c partition -f ant_300000_3_product.csv -n 50000
python3 main.py -c partition -f ant_300000_3_customer.csv -n 50000
python3 main.py -c partition -f ant_300000_3_customer.csv -n 33000

# FC 
python3 main.py -c partition -f fc_300000_3_product.csv -n 200000
python3 main.py -c partition -f fc_300000_3_customer.csv -n 200000
python3 main.py -c partition -f fc_300000_3_product.csv -n 100000
python3 main.py -c partition -f fc_300000_3_customer.csv -n 100000
python3 main.py -c partition -f fc_300000_3_product.csv -n 75000
python3 main.py -c partition -f fc_300000_3_customer.csv -n 75000
python3 main.py -c partition -f fc_300000_3_product.csv -n 50000
python3 main.py -c partition -f fc_300000_3_customer.csv -n 50000
python3 main.py -c partition -f fc_300000_3_customer.csv -n 33000