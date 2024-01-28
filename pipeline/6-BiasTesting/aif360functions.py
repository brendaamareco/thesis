import pandas as pd
import aif360.datasets as aif
import json
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.metrics import DatasetMetric
from aif360.explainers import MetricJSONExplainer
# For explaining class
from typing import Union
from aif360.explainers import MetricTextExplainer
from aif360.algorithms.preprocessing import Reweighing  
from aif360.algorithms.preprocessing import DisparateImpactRemover

#import warnings
#warnings.filterwarnings('ignore')
#import os
#import tensorflow as tf
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

COUNTRIES = {1: 'Australia', 2: 'Canada', 3: 'Hong Kong', 4: 'India', 5: 'Singapore', 6: 'South Africa', 7: 'United Kingdom', 8: 'United States'}
  
##########################################################
def clean_data(path):
    df = pd.read_csv(path)
    df.drop(df.index, inplace=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')

##########################################################
def getNumberFromJSON(param):
	param = json.loads(param)
	for key, value in param.items():
		if(key=="message"):
			#print(key, value)
			words = value.split()
			number = words[-1]
			return number
			
			
##########################################################
def load_data_and_preprocessing(
data_input_path, 
ranking_name, 
comments, 
protected_attribute_list,
label_ranking):

	#Step 1 Load dataset and Preprocessing        
	df = pd.read_csv(data_input_path, skipinitialspace=True, usecols=['country', ranking_name])

	#only use some columns, drop unwanted columns
	encoded_df = df.filter(['country', ranking_name], axis=1)

	# Encode Country 
	encoded_df.loc[encoded_df.country == 'Australia', 'country'] = 1
	encoded_df.loc[encoded_df.country == 'Canada', 'country'] = 2
	encoded_df.loc[encoded_df.country == 'Hong Kong', 'country'] = 3
	encoded_df.loc[encoded_df.country == 'India', 'country'] = 4
	encoded_df.loc[encoded_df.country == 'Singapore', 'country'] = 5
	encoded_df.loc[encoded_df.country == 'South Africa', 'country'] = 6
	encoded_df.loc[encoded_df.country == 'United Kingdom', 'country'] = 7
	encoded_df.loc[encoded_df.country == 'United States', 'country'] = 8

	binaryLabelDataset = createBinaryLabelDataset(encoded_df, protected_attribute_list, label_ranking)
	resTupla=(binaryLabelDataset, comments)
	
	return resTupla


def createBinaryLabelDataset(encoded_df, protected_attribute_list, label_ranking):
	return aif.BinaryLabelDataset(
	df=encoded_df,
	protected_attribute_names=protected_attribute_list,
	label_names= label_ranking,
	favorable_label=1,
	unfavorable_label=0)

def mitigate_bias_reweighing(unpriv, priv, binaryLabelDataset):

	reweighing = Reweighing(unpriv, priv)
	reweighing.fit(binaryLabelDataset)
	mitigated_dataset = reweighing.transform(binaryLabelDataset)
	weights = mitigated_dataset.convert_to_dataframe()[1]['instance_weights']
	#print("mitigated_dataset",mitigated_dataset.convert_to_dataframe()[1])
	return weights

##########################################################
def bias_testing(LabelDataset_param, dataset, privilegeds, unpriv, priv, mitigation_technique, comments, data_output_path, ranking_name):

	#Step 2 Testing Bias
	#print("--------------------------------")
	#print("privileged = "+privilegeds)

	metric_df = BinaryLabelDatasetMetric(LabelDataset_param, unprivileged_groups=unpriv, privileged_groups=priv)

	#create json_explainer 
	json_explainer = MetricJSONExplainer(metric_df)

	#print("disparate_impact_function ---------------------------")   
	#Disparate Impact
	#DI ≥ 0.8 are legal.     
	#DI = 1.0 full fairness"     
	json_str= json_explainer.disparate_impact()
	value=getNumberFromJSON(json_str)
	#print("disparate_impact")
	#print(value)
	disparate_impact=float(value)        
	bias_d='-'
	if(disparate_impact < 0.8):
		#print("bias detected")        
		bias_d=True

	#print("statistical_parity_difference ---------------------------")
	#Statistical parity difference
	#Legal between -0.09 y 0.09"
	json_str= json_explainer.statistical_parity_difference()
	value=getNumberFromJSON(json_str)
	#print("statistical_parity_difference")
	#print(value)
	statistical_parity=float(value)        
	bias_s='-'
	#if(statistical_parity < -0.09 or statistical_parity > 0.09):
	if(statistical_parity < -0.09):
		#print("bias detected")
		bias_s=True

	#print("Saving bias testing --------------------")
	dfout = pd.read_csv(data_output_path)
	dfout.loc[len(dfout.index)] = [dataset, privilegeds, ranking_name, mitigation_technique, disparate_impact, bias_d, statistical_parity, bias_s, comments] 
	
	dfout.to_csv(data_output_path, index=False, encoding='utf-8-sig')

def mitigate_bias_diRemover(binaryLabelDataset):
	di = DisparateImpactRemover(repair_level = 1.0)
	dataset_transf_train = di.fit_transform(binaryLabelDataset)
	transformed = dataset_transf_train.convert_to_dataframe()[0]
	
	return transformed


