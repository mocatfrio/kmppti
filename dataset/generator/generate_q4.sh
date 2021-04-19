#!/bin/bash



# 1000 
# python3 main.py -c generate -t ind -n 1000 -d 3 -l product
# python3 main.py -c generate -t ind -n 1000 -d 3 -l customer
# python3 main.py -c generate -t ant -n 1000 -d 3 -l product
# python3 main.py -c generate -t ant -n 1000 -d 3 -l customer
# python3 main.py -c generate -t fc -n 1000 -d 3 -l product
# python3 main.py -c generate -t fc -n 1000 -d 3 -l customer

# python3 main.py -c prepare -f ind_1000_3_product.csv
# python3 main.py -c prepare -f ind_1000_3_customer.csv
# python3 main.py -c prepare -f ant_1000_3_product.csv
# python3 main.py -c prepare -f ant_1000_3_customer.csv
# python3 main.py -c prepare -f fc_1000_3_product.csv
# python3 main.py -c prepare -f fc_1000_3_customer.csv

# Dimension 
python3 main.py -c generate -t ind -n 2000 -d 2 -l product
python3 main.py -c generate -t ind -n 2000 -d 2 -l customer
python3 main.py -c generate -t ind -n 2000 -d 5 -l product
python3 main.py -c generate -t ind -n 2000 -d 5 -l customer
python3 main.py -c generate -t ind -n 2000 -d 7 -l product
python3 main.py -c generate -t ind -n 2000 -d 7 -l customer

python3 main.py -c generate -t ant -n 2000 -d 2 -l product
python3 main.py -c generate -t ant -n 2000 -d 2 -l customer
python3 main.py -c generate -t ant -n 2000 -d 5 -l product
python3 main.py -c generate -t ant -n 2000 -d 5 -l customer
python3 main.py -c generate -t ant -n 2000 -d 7 -l product
python3 main.py -c generate -t ant -n 2000 -d 7 -l customer

python3 main.py -c generate -t fc -n 2000 -d 2 -l product
python3 main.py -c generate -t fc -n 2000 -d 2 -l customer
python3 main.py -c generate -t fc -n 2000 -d 5 -l product
python3 main.py -c generate -t fc -n 2000 -d 5 -l customer
python3 main.py -c generate -t fc -n 2000 -d 7 -l product
python3 main.py -c generate -t fc -n 2000 -d 7 -l customer

python3 main.py -c prepare -f ind_2000_2_product.csv
python3 main.py -c prepare -f ind_2000_2_customer.csv
python3 main.py -c prepare -f ind_2000_5_product.csv
python3 main.py -c prepare -f ind_2000_5_customer.csv
python3 main.py -c prepare -f ind_2000_7_product.csv
python3 main.py -c prepare -f ind_2000_7_customer.csv

python3 main.py -c prepare -f ant_2000_2_product.csv
python3 main.py -c prepare -f ant_2000_2_customer.csv
python3 main.py -c prepare -f ant_2000_5_product.csv
python3 main.py -c prepare -f ant_2000_5_customer.csv
python3 main.py -c prepare -f ant_2000_7_product.csv
python3 main.py -c prepare -f ant_2000_7_customer.csv

python3 main.py -c prepare -f fc_2000_2_product.csv
python3 main.py -c prepare -f fc_2000_2_customer.csv
python3 main.py -c prepare -f fc_2000_5_product.csv
python3 main.py -c prepare -f fc_2000_5_customer.csv
python3 main.py -c prepare -f fc_2000_7_product.csv
python3 main.py -c prepare -f fc_2000_7_customer.csv

# IND 
#python3 main.py -c generate -t ind -n 2000 -d 3 -l product
#python3 main.py -c generate -t ind -n 2000 -d 3 -l customer
#python3 main.py -c generate -t ind -n 5000 -d 3 -l product
#python3 main.py -c generate -t ind -n 5000 -d 3 -l customer
#python3 main.py -c generate -t ind -n 7000 -d 3 -l product
#python3 main.py -c generate -t ind -n 7000 -d 3 -l customer
#python3 main.py -c generate -t ind -n 10000 -d 3 -l product
#python3 main.py -c generate -t ind -n 10000 -d 3 -l customer

#python3 main.py -c prepare -f ind_2000_3_product.csv
#python3 main.py -c prepare -f ind_2000_3_customer.csv
#python3 main.py -c prepare -f ind_5000_3_product.csv
#python3 main.py -c prepare -f ind_5000_3_customer.csv
#python3 main.py -c prepare -f ind_7000_3_product.csv
#python3 main.py -c prepare -f ind_7000_3_customer.csv
#python3 main.py -c prepare -f ind_10000_3_product.csv
#python3 main.py -c prepare -f ind_10000_3_customer.csv

# ANT 
#python3 main.py -c generate -t ant -n 2000 -d 3 -l product
#python3 main.py -c generate -t ant -n 2000 -d 3 -l customer
#python3 main.py -c generate -t ant -n 5000 -d 3 -l product
#python3 main.py -c generate -t ant -n 5000 -d 3 -l customer
#python3 main.py -c generate -t ant -n 7000 -d 3 -l product
#python3 main.py -c generate -t ant -n 7000 -d 3 -l customer
#python3 main.py -c generate -t ant -n 10000 -d 3 -l product
#python3 main.py -c generate -t ant -n 10000 -d 3 -l customer

#python3 main.py -c prepare -f ant_2000_3_product.csv
#python3 main.py -c prepare -f ant_2000_3_customer.csv
#python3 main.py -c prepare -f ant_5000_3_product.csv
#python3 main.py -c prepare -f ant_5000_3_customer.csv
#python3 main.py -c prepare -f ant_7000_3_product.csv
#python3 main.py -c prepare -f ant_7000_3_customer.csv
#python3 main.py -c prepare -f ant_10000_3_product.csv
#python3 main.py -c prepare -f ant_10000_3_customer.csv

# FC 
#python3 main.py -c generate -t fc -n 2000 -d 3 -l product
#python3 main.py -c generate -t fc -n 2000 -d 3 -l customer
#python3 main.py -c generate -t fc -n 5000 -d 3 -l product
#python3 main.py -c generate -t fc -n 5000 -d 3 -l customer
#python3 main.py -c generate -t fc -n 7000 -d 3 -l product
#python3 main.py -c generate -t fc -n 7000 -d 3 -l customer
#python3 main.py -c generate -t fc -n 10000 -d 3 -l product
#python3 main.py -c generate -t fc -n 10000 -d 3 -l customer

#python3 main.py -c prepare -f fc_2000_3_product.csv
#python3 main.py -c prepare -f fc_2000_3_customer.csv
#python3 main.py -c prepare -f fc_5000_3_product.csv
#python3 main.py -c prepare -f fc_5000_3_customer.csv
#python3 main.py -c prepare -f fc_7000_3_product.csv
#python3 main.py -c prepare -f fc_7000_3_customer.csv
#python3 main.py -c prepare -f fc_10000_3_product.csv
#python3 main.py -c prepare -f fc_10000_3_customer.csv
