#####################################################################
# Global Variables
#####################################################################

rankings_folder = \
    '../0-Data/1_intermediate_generated_data/rankings'
annotated_ranking_path = \
    '../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv'
ndcgs_result_folder = \
        '../0-Data/1_intermediate_generated_data/ndcgs'

#####################################################################
# Config
#####################################################################
from configparser import ConfigParser
import sys
import json
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

#Read args
if len(sys.argv) == 3:
    rankings_folder = sys.argv[1]
    ndcgs_result_folder = sys.argv[2]

#####################################################################
# Functions
#####################################################################

#dataframe with one column rank
def calculate_ndcg(data):
    column_name = data['column_name']

    #col_rank_predicted_list = data[column_name].tolist()
    predicted_rel = np.asarray([data['rankings']])
    
    ndcg = ndcg_score(true_rel, predicted_rel)
    #ranking_id = int(re.search(r'\d+', str(column_name)).group())
    ranking_id = column_name
    
    return { 'ndcgColumn': [ranking_id, ndcg], 'rankColumnName': column_name, 'rankColumnValues': np.squeeze(predicted_rel) }

     

def get_best_ranking(data):
    return data.loc[data['ndcg'].idxmax()].to_dict()



def save_ranking(ranking):
    json_object = json.dumps(ranking, indent=4)
    
    with open("../0-Data/1_intermediate_generated_data/best_ranking.json", "w") as outfile:
        outfile.write(json_object) 

#####################################################################
# Main
#####################################################################
if evaluarNDCG=="True":
    print("perform evaluarNDCG")
    import os
    from sklearn.metrics import dcg_score
    from sklearn.metrics import ndcg_score
    import numpy as np
    import pandas as pd
    import re
    from multiprocessing import Pool

    #open
    print("--------------------------------------------------")
    print("Load dataset ")
    annotated_ranking_df = pd.read_csv(annotated_ranking_path)

    # Corpus
    # True relevance score
    col_rank_anotated_list = annotated_ranking_df['rank_manual'].tolist()
    true_rel = np.asarray([col_rank_anotated_list])


    #----------------------------------------------------------------------
    print("--------------------------------------------------")
    print("Perfect ranking ----------------------------------")

    predicted_rel = true_rel

    res1 = dcg_score(true_rel, predicted_rel)
    res2 = ndcg_score(true_rel, predicted_rel)
    print("dcg_score: " + str(res1) )
    print("ndcg_score: " + str(res2) )



    #----------------------------------------------------------------------
    print("--------------------------------------------------")
    print("Alertme normalizado ranking -------------------------------------")

    # relevance list processed as array
    col_rank_predicted_list = annotated_ranking_df['alertme_rank_normalized'].tolist()
    predicted_rel = np.asarray([col_rank_predicted_list])

    res1 = dcg_score(true_rel, predicted_rel)
    res2 = ndcg_score(true_rel, predicted_rel)
    print("dcg_score: " + str(res1) )
    print("ndcg_score: " + str(res2) )

    #----------------------------------------------------------------------
    print("--------------------------------------------------")
    print("Ranking con Funcion de pesos")

    # relevance list processed as array
    #rankings_df = pd.read_csv(rankings_folder)
    ranking_chunks_length = len(os.listdir(rankings_folder))
    max_ndcg = {'RankingFuncionPesos': -1 , 'ndcg': -1, 'column' : pd.DataFrame()}
    pool = Pool()

    for i in range(0, ranking_chunks_length):
        rankings_file = "/rankings_" + str(i) + ".csv"
        rankings_df_path = rankings_folder + rankings_file
        rankings_df = pd.read_csv(rankings_df_path)

        #result = pool.map(calculate_ndcg, [{ 'column_name': str(c), 'rankings': rankings_df[c].tolist()} for c in rankings_df.columns])
        results_async = pool.map_async(calculate_ndcg, [{ 'column_name': str(c), 'rankings': rankings_df[c].tolist()} for c in rankings_df.columns])
        results = []

        for result in results_async.get():
            results.append(result['ndcgColumn'])
            ndcg = result['ndcgColumn'][1]
            if ndcg > max_ndcg['ndcg']:    
                max_ndcg['RankingFuncionPesos'] = result['ndcgColumn'][0]
                max_ndcg["ndcg"] = ndcg
                max_ndcg['column'] = pd.DataFrame( { result['rankColumnName'] : result['rankColumnValues'] })

        results_async.wait()
        result_df = pd.DataFrame(results, columns=['RankingFuncionPesos', 'ndcg'])
        result_df.to_csv(ndcgs_result_folder + "/ndcg_" + str(i) + ".csv", index=False)
    
    pool.close()
    pool.join()

    print("Best ranking based on ndcg_score: ")
    
    save_ranking({'RankingFuncionPesos': max_ndcg['RankingFuncionPesos'], 'ndcg': max_ndcg["ndcg"]})
    print('RankingID: ' + str(max_ndcg['RankingFuncionPesos']) + ", ndcg: " + str(max_ndcg["ndcg"]) )
    print("--------------------------------------------------")  

    annotated_ranking_df = pd.concat([annotated_ranking_df, max_ndcg['column']], axis=1)
    annotated_ranking_df.to_csv(annotated_ranking_path)

else:
    print("no evaluarNDCG carried out")



            





