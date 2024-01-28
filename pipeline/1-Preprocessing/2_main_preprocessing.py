#####################################################################
# Global Variables
#####################################################################

data_input_path = \
    '../0-Data/1_intermediate_generated_data/data.csv'

data_output_path = \
    '../0-Data/1_intermediate_generated_data/data_preprocessed.csv'


#####################################################################
# Config
#####################################################################
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
# Functions
#####################################################################


#####################################################################
# Main
#####################################################################
if preprocesamiento=="True":
    print("perform full preprocessing")
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
    from sklearn.feature_extraction.text import TfidfVectorizer
    import nltk
    nltk.download('stopwords')
    nltk.download('omw-1.4')

    from nltk.stem.snowball import SnowballStemmer
    from nltk.corpus import stopwords
    from nltk.stem.porter import *
    from nltk.tokenize.treebank import TreebankWordDetokenizer

else:
    import pandas as pd

    data_with_review = pd.read_csv('../0-Data/1_intermediate_generated_data/data.csv')
    ranking_dataset = pd.read_csv('../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv')
    
    merged_dataset = pd.merge(ranking_dataset, data_with_review[['review','review_id']],
                    on='review_id', 
                    how='inner')
    
    merged_dataset.to_csv('../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv',index = False)

    print("no full preprocessing carried out")
    
    

    





