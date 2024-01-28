#####################################################################
# Global Variables
#####################################################################

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
useEntropy=format(preprocessing_info["useEntropy"])
decimalPrecision=format(preprocessing_info["decimalPrecision"])
   
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


def ranking(review_id, category, sentiment, score, revLen, maxLen, country, entropy, weights, maxEntropy):
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
    
    #-------------------------------------
    #-------- feature : SENTIMENT --------
    #f3(review)= 1/(sentiment+3) (low sentiment score implies more developer attention)
    #We add 3 to sentiment in order to avoid division by zero, 
    #sentiment can be -2 -1 0 1 2        
    f_SENTIMENT = 1/(sentiment+3)
    if f_SENTIMENT > 0: 
        rank = rank + f_SENTIMENT * weights['SENTIMENT']
    
    #-------------------------------------
    #-------- feature : SCORE --------
    f_SCORE =  1/score if score > 0 else 0
    if f_SCORE > 0:
        rank = rank + f_SCORE * weights['SCORE']


    if (useEntropy == "True"):
        #-------------------------------------
        #-------- feature : ENTROPY --------
        f_ENTROPY = entropy/maxEntropy
        rank = rank + f_ENTROPY * weights['ENTROPY'] 
    else:
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
    from weight_generator import generate_weight_combination
    from multiprocessing import Pool

    data = pd.read_csv(data_input_output_path)
    decimalPrecision = float(decimalPrecision)

    if useEntropy == "True":
        features = ['CATEGORY', 'SENTIMENT', 'SCORE', 'ENTROPY']
    else:
        features = ['CATEGORY', 'SENTIMENT', 'SCORE', 'REVLEN']

    print("Using features: ", features)
    print("Using decimal precision:", decimalPrecision)

    number_of_combinations, combinations_chunk_length = generate_weight_combination(decimalPrecision, features)
    print("Number of combinations found: ", number_of_combinations)

    def generate_column(weight_combination):
        len_max = data['revLen'].max()
        max_entropy = data['entropy'].max()
        new_column = data.apply(lambda x: ranking(x['review_id'], x['category'], x['sentimentScore'], x['score'],  x['revLen'], len_max, x['country'], x['entropy'], weight_combination, max_entropy), axis=1)
        new_column.name = 'rank'+str(weight_combination['id'])

        return new_column
    

    pool = Pool()
    weight_combinations_folder = '../0-Data/1_intermediate_generated_data/weight_combinations/'
    ranks_folder = '../0-Data/1_intermediate_generated_data/rankings/'

    for i in range(0, combinations_chunk_length):
        weight_combinations_file = "weight_combinations_" + str(i) + ".csv"
        weight_combinations_df_path = weight_combinations_folder + weight_combinations_file

        weight_combinations_df = pd.read_csv(weight_combinations_df_path)
        result = pool.map(generate_column, weight_combinations_df.reset_index().to_dict(orient='records'))
        result_df = pd.concat(result, axis=1)

        result_df.to_csv(ranks_folder + "rankings_" + str(i) + ".csv", index=False)

    pool.close()
    pool.join()

else:
    print("no rankingFunciondePesos carried out")
    
