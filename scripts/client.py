import time
import multiprocessing
import multiprocessing.managers
import numpy as np
from pprint import pprint

from streaming_kmppti.const import *

# import logging
# logger = multiprocessing.log_to_stderr()
# logger.setLevel(logging.INFO)

class MyListManager(multiprocessing.managers.BaseManager):
    pass

MyListManager.register("streaming_server")

def main():
    manager = MyListManager(address=('/tmp/mypipe'), authkey=b"")
    manager.connect()
    data = manager.streaming_server()

    print("Queue: ", data[QUEUE:])
    print("Column: ", data[COL])
    print("Label: ", data[LABEL])
    print("Result: ", data[RESULT])

    total_dim = len([k for k in data[COL].keys() if "dim" in k])
    while True:
        print("=============================")
        print("Queue: ", data[QUEUE:])
        index_unprocessed = get_index(data[QUEUE:], data[COL])
        # process data
        if index_unprocessed is None:
            pass
        else:
            current_data = data[index_unprocessed]
            # get product and customer active
            products = get_all_products(data[QUEUE:], data[COL])
            customers = get_all_customers(data[QUEUE:], data[COL])
            print("----------------")
            print("Product active: ", products)
            print("Customer active: ", customers)

            # enter
            if is_product(current_data[data[COL]["label_type"]]):
                rsl_result = compute_rsl(
                    current_data[data[COL]["dim_0"]:data[COL]["dim_" + str(total_dim - 1)] + 1],
                    current_data[data[COL]["label_id"]],
                    products,
                    customers,
                    data[COL]
                )
            else:
                if len(products) > 0:
                    data[RESULT] = initialize_dsl(
                        current_data[data[COL]["dim_0"]:data[COL]["dim_" + str(total_dim - 1)] + 1],
                        products,
                        data[COL],
                        data[LABEL],
                        data[RESULT]
                    )
            current_data[data[COL]["is_processed"]] = 1
            data.insert(index_unprocessed, current_data)
            data.pop(index_unprocessed + 1)
        if bool(result):
            print("----------------")
            print("Most Promising Product: ")
            for key in result:
                print(key, "->", result[key])
            print("============")
        time.sleep(1)

def get_all_products(data, col):
    return [d for d in data if is_product(d[col["label_type"]])]

def get_all_customers(data, col):
    return [d for d in data if not is_product(d[col["label_type"]])]

def get_index(data, col):
    for i in range(len(data)):
        return i + QUEUE if not is_processed(data[i][col["is_processed"]]) else None

def is_product(label_type):
    return label_type == 0

def is_processed(status):
    return status == 1

# Dynamic skyline functions
def initialize_dsl(customer_val, products, col, label, result):
    """This function called when customer get in, to find dynamic skyline of customer (products that are not dominated by other products)

    Args:
        customer_val (list): list of customer value in each dim, [dim_0, dim_1, dst]
        products (list): list of products active
        col (dict): key-value that store colname and index in list

    Returns:
        dsl_result (list): list of products that are not dominated by other products
    """
    # prepare data
    dsl = [
        [products[i][col["label_id"]],
        calc_diff(
            customer_val,
            products[i][col["dim_0"]:col["dim_" + str(len(customer_val) - 1)] + 1]
        ),
        0]
        for i in range(len(products))
    ]
    np_dsl = np.array(dsl, dtype=object)
    # sort based on value
    sorted_dsl = np_dsl[np_dsl[:,1].argsort()].tolist()
    print("----------------")
    print("Sorted DSL:")
    pprint(sorted_dsl)
    # compare domination
    dominated_index = []
    for i in range(len(sorted_dsl)):
        if sorted_dsl[i][2] == 1:
            continue
        for j in range(i+1, len(sorted_dsl)):
            if sorted_dsl[j][2] == 1:
                continue
            if is_dominating(sorted_dsl[i][1], sorted_dsl[j][1]):
                sorted_dsl[j][2] = 1
                dominated_index.append(j)
            elif is_dominating(sorted_dsl[j][1], sorted_dsl[i][1]):
                sorted_dsl[i][2] = 1
                dominated_index.append(i)
    # delete dominated index
    for i in dominated_index:
        sorted_dsl.pop(i)
    # add to result
    for product in sorted_dsl:
        if label[product[0]] in result:
            result[label[product[0]]] += calc_probability(sorted_dsl)
        else:
            result[label[product[0]]] = calc_probability(sorted_dsl)
    return result

def calc_diff(cust_val, prod_val):
    """calculating the difference between product value and customer value

    Args:
        cust_val (list): list of customer value
        prod_val (list): list of product value
    """
    return [abs(cust_val[i] - prod_val[i]) for i in range(len(cust_val))]

def is_dominating(prod_subj, prod_obj):
    dominating = 0
    dominated = 0
    for i in range(len(prod_subj)):
      if prod_subj[i] < prod_obj[i]:
        dominating += 1
      elif prod_subj[i] > prod_obj[i]:
        dominated += 1
      else:
        continue
    return dominated == 0 and dominating >= 1

def calc_probability(dsl_result):
    try:
      return 1.0/len(dsl_result)
    except:
      return 0

# Reverse skyline functions
def compute_rsl(product_val, product_id, products, customers, col):
    orthant = define_orthant(len(product_val))
    # find midpoint skyline
    for prod in products:
        if prod[col["label_id"]] == product_id:
            continue
        midpoint = calc_midpoint(product_val, prod[col["dim_0"]:col["dim_" + str(len(product_val) - 1)] + 1])
        area = get_orthant_area(prod[col["dim_0"]:col["dim_" + str(len(product_val) - 1)] + 1])
        if not orthant[area]:
            orthant[area] = [prod[col["label_id"]], midpoint]
        else:
            for i in orthant[area]:
                if 

    pass

def define_orthant(total_dim):
    orthant = {}
    for i in range(2**total_dim): 
      id = format(i, '#0{}b'.format(total_dim + 2))[2:]
      orthant[id] = {}
    return orthant

def get_orthant_area(product_val):
    res = []
    for i in range(self.dim):
      if product_val[i] <= self.my_value[i]:
        res.append('0')
      else:
        res.append('1')
    res = ''.join(res)
    return res

def calc_midpoint(prod_val, cust_val):
    return [(prod_val[i] + cust_val[i])/2 for i in range(len(prod_val))]
    

if __name__ == '__main__':
    main()