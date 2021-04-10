#!/bin/bash
# MY_DIR='../dataset/independent/'

# if [ -d "$MY_DIR" ]; then
#   rm -rf ${MY_DIR}*
# fi

python3 kmppti/main.py -p ind_5_2_product.csv -c ind_5_2_customer.csv -k 5 -g 3 -s 1 -e 15
# python3 kmppti/main.py -p ind_5000_2_product.csv -c ind_5000_2_customer.csv -k 5 -g 3 -s 1 -e 200


