##########################################################
#Import Statements
##########################################################
from os import path
import numpy as np
import pandas as pd
import aif360.datasets as aif
import json

from aif360.metrics import BinaryLabelDatasetMetric
from aif360.explainers import MetricJSONExplainer
from typing import Union
from aif360.explainers import MetricTextExplainer  
import sys
import aif360functions as f
from desbinarize_ranking import save_as_desbinarized
 
##########################################################
#Global Variables
##########################################################

path_directory_out = ''

#data_input_path='../0-Data/1_intermediate_generated_data/annotated_ranking_dataset_binarized.csv'
#data_input_path='../0-Data/results/with_mitigation_technique/new_rankings_binarized.csv'
data_output_path =' ' #Correct setting is in the following 


#ranking_list=['rank107733'] #modify this array in case of testing other column
#ranking_list=['newRank']
#ranking_list=['rank_manual', 'ranking_MNB', 'ranking_RF', 'ranking_SVC', 'ranking_DT', 'ranking_MLP']
#test='whole' #indicates that testing is performend on whole data, without test-train splitting


label_ranking=[] #is instantiated in main cicle below     
ranking_name='' #is instantiated in main cicle below
number_of_privilegeds_n=0 #the correct value is setten in main below

comments=""
protected_attribute_list=['country']

     
##########################################################
#Functions
##########################################################

def execute_bias_testing(tupla, ranking_name, label_ranking, data_output_path, mitigation_technique, data_input_path):
    privilegeds=tupla[0]
    priv=tupla[1] 
    unpriv=tupla[2]
    comments=''   

    (bLDataset, comments)=f.load_data_and_preprocessing(
    data_input_path, 
    ranking_name, 
    comments, 
    protected_attribute_list, 
    label_ranking)

    if (mitigation_technique == "Reweighing"):

        weights = f.mitigate_bias_reweighing(unpriv, priv, bLDataset)
        max_weight = np.max(weights)
        min_weight = np.min(weights)

        df_blDataset = bLDataset.convert_to_dataframe()[0]

        for idx, weight in enumerate(weights):
            if weight == max_weight:
                df_blDataset.loc[df_blDataset.index[idx], ranking_name] = 1
            elif weight == min_weight:
                df_blDataset.loc[df_blDataset.index[idx], ranking_name] = 0
    
        bLDataset = f.createBinaryLabelDataset(df_blDataset, protected_attribute_list, label_ranking)
        
        country_name = get_country_name_by_id(priv[0]['country'])
        save_as_desbinarized(df_blDataset, ranking_name, country_name)

    f.bias_testing(
    bLDataset, 
    data_input_path, 
    privilegeds, 
    unpriv, 
    priv, 
    mitigation_technique, 
    comments, 
    data_output_path, 
    ranking_name)


def country_bias_testing(ranking_list, mitigation_technique, data_input_path, path_directory_out):
    
    for i in range(1,2):
        number_of_privilegeds_n=i

        import itertools  
        dict_country_number = {
        'Australia':1,
        'Canada':2,
        'Hong Kong':3,
        'India':4,
        'Singapore':5,
        'South Africa':6,
        'United Kingdom':7,
        'United States':8}  

        countries=list(dict_country_number.keys())
        combinations_list=list(itertools.combinations(countries, number_of_privilegeds_n))

        experiment_list=[]
        for combination in combinations_list:
            label=''
            for index in range(len(combination)):
                label=label+', '+combination[index]

            privileged_list=[]
            for index in range(len(combination)):
                privileged_list.append({'country':dict_country_number[combination[index]]})
            
            unprivileged_list=[]
            for country in dict_country_number.keys():
                #if country is not privileged
                if country not in combination:
                    unprivileged_list.append({'country':dict_country_number[country]})
            
            #tupla=("de",
            #[{'Country':1}],
            #[{'Country':2},{'Country':3},{'Country':4},{'Country':5},{'Country':6},{'Country':7}, {'Country':8} ])
            tupla=(label, privileged_list, unprivileged_list)
            experiment_list.append(tupla)

        data_output_path = create_output_file(path_directory_out, number_of_privilegeds_n, 'whole')

        for experiment_tupla in experiment_list:
            for rn in ranking_list:
                ranking_name=rn 
                label_ranking=[ranking_name]         
                execute_bias_testing(experiment_tupla, ranking_name, label_ranking, data_output_path, mitigation_technique, data_input_path)  
                comments='' 
        

def create_output_file(path_directory_out, number_of_privilegeds_n, test):
    
    data_output_path = path_directory_out+'out_bias_country_x'+str(number_of_privilegeds_n)+'_'+test+'.csv'
    
    print("--------------------------------")
    print('Generating ' + data_output_path)

    import csv
    import os

    output_directory = os.path.dirname(data_output_path)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(data_output_path, 'w', newline = '') as csvfile:
            headers = ['dataset','privileged','ranking','Mitigation-technique','Disparate-impact','Bias-d','Statistical-parity','Bias-s','comments']
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvfile.close()    
    f.clean_data(data_output_path)

    return data_output_path

def get_country_name_by_id(country_id):
    
    dict_country_number = {
        1:'Australia',
        2:'Canada',
        3:'Hong Kong',
        4:'India',
        5:'Singapore',
        6:'South Africa',
        7:'United Kingdom',
        8:'United States' }
    
    return dict_country_number[country_id] 
 


  
              