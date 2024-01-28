#####################################################################
# Config
#####################################################################
from configparser import ConfigParser
#Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")
#Get the parameters
preprocessing_info = config_object["PREPROCESSING"]
chunk_size = int(format(preprocessing_info["chunkSize"]))

import math
import pandas as pd

#####################################################################
# Functions
#####################################################################


def is_solution(node, decimals, num_of_variables):
    return sum_node(node, decimals) == 1 and len(node) == num_of_variables


def is_feasible(node, decimals, num_of_variables):
    return sum_node(node, decimals) <= 1 and len(node) <= num_of_variables


def expand(node, decimals, num_of_variables, var_range):
    nodes = []

    for value in var_range:
        new_node = node + [value]

        if is_feasible(new_node, decimals, num_of_variables):
            nodes.append(new_node)

    return nodes


def num_of_decimals(number):
    return str(number)[::-1].find('.')


def sum_node(node, decimals):
    return round(math.fsum(node), decimals)


def get_var_range(granularity, start, end):
    range = []
    range_value = start

    while (range_value <= end):
        range.append(range_value)
        range_value = round(range_value + granularity, num_of_decimals(granularity))

    return range


def backtracking(node, granularity, num_of_variables, var_range):

    if is_solution(node, num_of_decimals(granularity), num_of_variables):        
        yield node

    else:
        for node_child in expand(node, num_of_decimals(granularity), num_of_variables, var_range):
            yield from backtracking(node_child, granularity, num_of_variables, var_range)


def generate_weight_combination(granularity, features):   
    var_range = get_var_range(granularity, 0.0, 1.0)
    weight_combinations_folder = '../0-Data/1_intermediate_generated_data/weight_combinations/'
    combinations_generator = iter(backtracking([], granularity, len(features), var_range))
    combination_chunk = [] #[combination id + weight combinations]
    combination_chunk_index = 0
    num_of_combination = 0

    canIterate = True
    while canIterate:
        try: 
            combination = next(combinations_generator)
            num_of_combination += 1
            combination_chunk.append([num_of_combination-1] + combination)        

            if len(combination_chunk) == chunk_size:
                save_combination_chunk(weight_combinations_folder, features, combination_chunk_index, combination_chunk)
                combination_chunk_index += 1               
                combination_chunk.clear()
        except:
            canIterate = False

            if len(combination_chunk) > 0:
                save_combination_chunk(weight_combinations_folder, features, combination_chunk_index, combination_chunk)
                combination_chunk_index += 1
                combination_chunk.clear()
         
    return num_of_combination, combination_chunk_index

def save_combination_chunk(weight_combinations_folder, features, combination_chunk_index, combination_chunk):
    weight_combinations_path = weight_combinations_folder + "weight_combinations_" + str(combination_chunk_index) + ".csv"
    columns = ['id'] + features
    combinations_df = pd.DataFrame(combination_chunk, columns=columns)
    combinations_df.to_csv(weight_combinations_path, index=False, encoding='utf-8-sig')
