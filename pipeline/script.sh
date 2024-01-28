#!/bin/bash
#------------------------------------------------
# setup variables
#------------------------------------------------
experiment=$1
decimalPrecision=$2
chunkSize=10000

annotated_ranking_dataset="truthset_ranking.csv"
annotated_categorysentiment_dataset="truthset_features.csv"
data_to_rank="reviews_exportados_sin_emojis.csv"
        
#------------------------------------------------
# main
#------------------------------------------------

#In this pipeline we use these columns
#app_name
#user_id	
#user_name
#date
#****************country  
#version	
#****************score  
#url
#review_id
#****************revLen	
#****************sentimentScore
#time_diff
#****************category

#rank  (vamos a calcular)
#rank_manual  (ranking anotado)


case $experiment in
  1)
    echo "------------------------------------------------"
    echo "Experimento 1 - Ejecutar pipeline con funcion de pesos" 
    preprocesamiento=False
    useEntropy=False  
    lemmatization=False
    stemming=True
    extraccionFeatures=False
    rankingFunciondePesos=True
    evaluarNDCG=True
    evaluarBias=False
    mitigarBias=False
    ;;

  2)
    echo "------------------------------------------------"
    echo "Experimento 2 - Ejecutar pipeline reemplazando atributo RevLen por Entropy" 
    preprocesamiento=False
    useEntropy=True    
    lemmatization=False
    stemming=True
    extraccionFeatures=False
    rankingFunciondePesos=True
    evaluarNDCG=True
    evaluarBias=False
    mitigarBias=False
    ;;

  3)
    echo "------------------------------------------------"
    echo "Experimento 3 - Ejecutar pipeline con evaluacion de bias" 
    preprocesamiento=False
    useEntropy=True  
    lemmatization=False
    stemming=True
    extraccionFeatures=False
    rankingFunciondePesos=True
    evaluarNDCG=True
    evaluarBias=True
    mitigarBias=False
    ;;

  4)
    echo "------------------------------------------------"
    echo "Experimento 4 - Ejecutar pipeline con mitigacion de bias" 
    preprocesamiento=False
    useEntropy=True  
    lemmatization=False
    stemming=True
    extraccionFeatures=False
    rankingFunciondePesos=True
    evaluarNDCG=True
    evaluarBias=True
    mitigarBias=True
    ;;
esac
 
echo [PREPROCESSING]> "config.ini"
echo preprocesamiento=$preprocesamiento >> "config.ini"
echo lemmatization=$lemmatization >> "config.ini"
echo stemming=$stemming >> "config.ini"
echo extraccionFeatures=$extraccionFeatures >> "config.ini"
echo rankingFunciondePesos=$rankingFunciondePesos >> "config.ini"
echo evaluarNDCG=$evaluarNDCG >> "config.ini"
echo evaluarBias=$evaluarBias >> "config.ini"
echo mitigarBias=$mitigarBias >> "config.ini"
echo useEntropy=$useEntropy >> "config.ini"
echo decimalPrecision=$decimalPrecision >> "config.ini"
echo chunkSize=$chunkSize >> "config.ini"
#cat config.ini
#exit 1
cd 0-Data/

echo "------------------------------------------------" 
echo "Setting up data" 
echo "------------------------------------------------" 
cp 0_data_source/$annotated_ranking_dataset 1_intermediate_generated_data/annotated_ranking_dataset.csv
cp 0_data_source/$annotated_categorysentiment_dataset 1_intermediate_generated_data/annotated_categorysentiment_dataset.csv
cp 0_data_source/$data_to_rank 1_intermediate_generated_data/data.csv

echo "------------------------------------------------" 
echo "Setting up results folder" 
echo "------------------------------------------------" 
echo "deleting "+results${experiment}_${decimalPrecision}
rm -f -r results${experiment}_${decimalPrecision}
mkdir results${experiment}_${decimalPrecision}

echo "deleting "+results
rm -f -r results
mkdir results

cd results/
touch output.log
cd ../../
cp config.ini 0-Data/results/

execute_pipeline () {   
    echo "------------------------------------------------" 
    echo "1 - Preprocessing" 
    echo "------------------------------------------------" 
    cd 1-Preprocessing/
    pwd 
    python3.9 2_main_preprocessing.py
    
    echo "------------------------------------------------" 
    echo "2 - Feature Extracion" 
    echo "------------------------------------------------" 
    cd ../2-FeatureExtraction/
    pwd 
    python3.9 1_extractFeatures.py 

    echo "------------------------------------------------" 
    echo "4 - Ranking" 
    echo "------------------------------------------------" 
    cd ../4-Ranking/
    pwd
    rm -f -r ../0-Data/1_intermediate_generated_data/weight_combinations
    rm -f -r ../0-Data/1_intermediate_generated_data/rankings
    mkdir ../0-Data/1_intermediate_generated_data/weight_combinations
    mkdir ../0-Data/1_intermediate_generated_data/rankings
    python3.9 2_ranking_funcion_de_pesos.py
    cp -r ../0-Data/1_intermediate_generated_data/weight_combinations ../0-Data/results
    cp -r ../0-Data/1_intermediate_generated_data/rankings ../0-Data/results
    
    echo "------------------------------------------------" 
    echo "5-QualityTesting"
    echo "------------------------------------------------"
    cd ../5-QualityTesting/
    pwd
    rm -f -r ../0-Data/1_intermediate_generated_data/ndcgs
    mkdir ../0-Data/1_intermediate_generated_data/ndcgs
    python3.9 ndcg.py
    cp -r ../0-Data/1_intermediate_generated_data/ndcgs ../0-Data/results 

    echo "------------------------------------------------" 
    echo "6-BiasTesting"
    echo "------------------------------------------------"
    cd ../6-BiasTesting/
    pwd
    rm -f -r ../0-Data/1_intermediate_generated_data/unbiased_rankings
    rm -f -r ../0-Data/1_intermediate_generated_data/ndcg_unbiased_rankings
    mkdir ../0-Data/1_intermediate_generated_data/unbiased_rankings
    mkdir ../0-Data/1_intermediate_generated_data/ndcg_unbiased_rankings
    python3.9 biastesting.py # 2>/dev/null #para eliminar warnings molestos

    if [ "$mitigarBias" = "True" ] ; then
      echo "------------------------------------------------" 
      echo "6.2-QualityTesting"
      echo "------------------------------------------------"
      cd ../5-QualityTesting/
      pwd     
      python3.9 ndcg.py ../0-Data/1_intermediate_generated_data/unbiased_rankings ../0-Data/1_intermediate_generated_data/ndcg_unbiased_rankings
      cp -r ../0-Data/1_intermediate_generated_data/unbiased_rankings ../0-Data/results
      cp -r ../0-Data/1_intermediate_generated_data/ndcg_unbiased_rankings ../0-Data/results
    fi
        
    echo "------------------------------------------------" 
    echo "7-Statistics"
    echo "------------------------------------------------" 
    cd ../7-Statistics/
    pwd 
    Rscript statistics_and_plots.R
    
    mv Rplots.pdf ../0-Data/results/Rplots.pdf
    mv plot.png ../0-Data/results/plot.png
    mv statistics_output.txt ../0-Data/results/statistics_output.txt
    echo "End of experiment $experiment"
}


{ time execute_pipeline ; } 2>&1 | tee -a 0-Data/results/output.log

cat 0-Data/results/output.log | grep -v cudart | grep -v libcudart.so.11.0 | grep -v cudart_stub.cc:29 > 0-Data/results/output-nocudaerror.log



echo "------------------------------------------------" 
echo "Saving results"
echo "------------------------------------------------"    
pwd
cd 0-Data/
cp -r results results${experiment}_${decimalPrecision}
cp -r results${experiment}_${decimalPrecision} 3_experimentes_results 
rm -f -r results
rm -r results${experiment}_${decimalPrecision}

echo "------------------------------------------------" 
echo "Execution errors"
echo "------------------------------------------------"
cat 3_experimentes_results/results${experiment}_${decimalPrecision}/results/output-nocudaerror.log | grep error
cat 3_experimentes_results/results${experiment}_${decimalPrecision}/results/output-nocudaerror.log | grep warning
cat 3_experimentes_results/results${experiment}_${decimalPrecision}/results/output-nocudaerror.log | grep "not found"

