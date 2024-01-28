#####################################################################
# Global Variables
#####################################################################

data_input_path = \
    '../0-Data/1_intermediate_generated_data/data_preprocessed.csv'

data_output_path = \
    '../0-Data/1_intermediate_generated_data/data_preprocessed.csv'


from configparser import ConfigParser
#Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")
#Get the parameters
preprocessing_info = config_object["PREPROCESSING"]
preprocesamiento=format(preprocessing_info["preprocesamiento"])
lemmatization=format(preprocessing_info["lemmatization"])
stemming=format(preprocessing_info["stemming"])
extraccionFeatures=format(preprocessing_info["extraccionFeatures"])
rankingFunciondePesos=format(preprocessing_info["rankingFunciondePesos"])
evaluarNDCG=format(preprocessing_info["evaluarNDCG"])


#####################################################################
# Main
#####################################################################
if extraccionFeatures=="True":
    print("perform full feature extraction")
    print('Loading libraries')
    import pandas as pd 
    import csv
    import sys
    import math
    from collections import Counter
    from pandas import DataFrame
    import numpy
    import numpy as np
    import pandas as pd
    from nltk.util import Index
    import nltk
    import string
    import re
   
else:
    from add_entropy import save_entropy
    
    save_entropy()
    print("no feature extration carried out")


