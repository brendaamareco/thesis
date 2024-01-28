#####################################################################
# Global Variables
#####################################################################
weights = {'CATEGORY': 0.60, 'SENTIMENT': 0.25, 'SCORE': 0.10, 'REVLEN': 0.05}  


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

   
if preprocesamiento=="False" and extraccionFeatures=="False":
    print("working with annotated ranking dataset")
    data_input_output_path = \
    '../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv'
else:
    data_input_output_path = \
    '../0-Data/1_intermediate_generated_data/data_preprocessed.csv'
    
    
#####################################################################
# Functions
#####################################################################
def print_basic_statistics(data_frame):
    r, c = data_frame.shape
    print("rows "+str(r)+" columns "+str(c))        
    #print('ranking')
    #info=data_frame['rank'].value_counts()
    #print(info)
    info=data_frame['rank'].describe()
    print(info)    


def ranking(review_id, category, sentiment, score, revLen, maxLen, country):
    rank=0
    #-------------------------------------
    #-------- feature : CATEGORY --------
    f_CATEGORY = 0
    if category == 'isBugReport' :
        f_CATEGORY = 1
    elif category == 'isFeatureShortcoming/isFeatureRequest':
    	f_CATEGORY = 0.5
    else:
        f_CATEGORY = 0
    
    if f_CATEGORY > 0: 
        rank = rank + f_CATEGORY * weights['CATEGORY']
    
    #-------- feature : RETWEETS --------
    # number of retweets = how many people does the comment reach?
    # we dont have this information in our dataset of app reviews

    
    #-------- feature : LIKES --------
    # we dont have this information in our dataset of app reviews


    #-------------------------------------
    #-------- feature : SENTIMENT --------
    #f3(review)= 1/(sentiment+3) (low sentiment score implies more developer attention)
    #We add 3 to sentiment in order to avoid division by zero, 
    #sentiment can be -2 -1 0 1 2        
    f_SENTIMENT = 1/(sentiment+3)
    if f_SENTIMENT > 0: 
        rank = rank + f_SENTIMENT * weights['SENTIMENT']
    
    #-------- feature : SOCIAL_RANK --------
    #followers of the user, its a measure of popularity and thus of importance
    # we dont have this information in our dataset of app reviews
    
    
    #-------- feature : DUPLICATES --------
    # f6(review)= number of duplicates of review, lexical similarity, how many users are discussing the same issue 
    # we dont calculater duplicates in this implementation

    #-------------------------------------
    #-------- feature : SCORE --------
    f_SCORE =  1/score if score > 0 else 0
    if f_SCORE > 0:
        rank = rank + f_SCORE * weights['SCORE']

    #-------------------------------------
    #-------- feature : REVLEN --------
    f_REVLEN = revLen/maxLen
    if f_REVLEN > 0:
        rank = rank + f_REVLEN * weights['REVLEN']  
   
    #-------------------------------------
    ranking =  rank*3  
    return ranking 
    
#####################################################################
# Main
#####################################################################
if rankingFunciondePesos=="True":
    print("perform rankingFunciondePesos")
    import pandas as pd
    import matplotlib.pyplot as plt
    import math
    from collections import Counter
    import numpy as np


    data = pd.read_csv(data_input_output_path)
    len_max = data['revLen'].max()

    data['rank'] = data.apply(lambda x: ranking(x['review_id'], x['category'], x['sentimentScore'], x['score'],  x['revLen'], len_max, x['country']), axis=1)


    #print statistics and save our new dataset to a file
    print_basic_statistics(data)
    data.to_csv(data_input_output_path, index=False, encoding='utf-8-sig')

else:
    print("no rankingFunciondePesos carried out")










