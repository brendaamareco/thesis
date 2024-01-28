##########################################################
#Global Variables
##########################################################
#top 3 labels=["rank107733", "rank110490", "rank113173", "rank_manual"] #column to binarize. rank107733
#label="rank107733"
#label="newRank"

#variables to force binary label
# data_binary_input_path='../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv'
# data_binary_output_path='../0-Data/1_intermediate_generated_data/annotated_ranking_dataset_binarized.csv'
# data_binary_input_path='../0-Data/results/with_mitigation_technique/new_rankings.csv'
# data_binary_output_path='../0-Data/results/with_mitigation_technique/new_rankings_binarized.csv'

data_input_path = '../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv'
data_binary_path = '../0-Data/1_intermediate_generated_data/annotated_ranking_dataset_binarized.csv'
#label = 'rank107733'
#label = 'rank_manual'
data_copy_path='original_ranking_dataset.csv'
favorable_label = 2

#####################################################################
# Config
#####################################################################
from configparser import ConfigParser
import sys
#Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")
#Get the parameters
preprocessing_info = config_object["PREPROCESSING"]
evaluarBias=format(preprocessing_info["evaluarBias"])
mitigarBias=format(preprocessing_info["mitigarBias"])

##########################################################
#Functions
##########################################################

def save_rankings_copy(data_binary_input_path, cols, data_copy_path):
    df = pd.read_csv(data_binary_input_path, skipinitialspace=True, usecols=cols)
    df.to_csv(data_copy_path, index=False, encoding='utf-8-sig')

##########################################################
#Main
##########################################################

if (evaluarBias == "True"):
    import sys
    import force_binary_label as fbl 
    import biastesting_AIF360_country as countrybt  
    from matplotlib import pyplot as plt
    import pandas as pd
    import json 

    with open('../0-Data/1_intermediate_generated_data/best_ranking.json', 'r') as openfile:
        best_ranking_dict = json.load(openfile)

    #best_ranking_id = int(best_ranking_dict["RankingFuncionPesos"])
    #label = "rank" + str(best_ranking_id)
    label = best_ranking_dict["RankingFuncionPesos"]

    save_rankings_copy(data_input_path, [label, 'country'], data_copy_path)

    print("-----------------------------------")
    print("force_binary_label_for_bias_testing")
    print("-----------------------------------")

    fbl.force_binary_label_for_bias_testing(label, favorable_label, data_input_path, data_binary_path)

    print("-----------------------------------")
    print("country_bias_testing")
    print("-----------------------------------")

    if (mitigarBias == "True"):
        mitigationTechnique = "Reweighing"
    else:
        mitigationTechnique = "None"

    countrybt.country_bias_testing([label], mitigationTechnique, data_binary_path, '../0-Data/results/')

else:
    print("no biasTesting carried out")
