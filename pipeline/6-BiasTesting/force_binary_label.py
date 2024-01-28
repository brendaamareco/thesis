##########################################################
#Import Statements
##########################################################
import pandas as pd

##########################################################
#Global Variables
##########################################################

##########################################################
#Main
##########################################################

def force_binary_label_for_bias_testing(label, favorable_label, data_input_path, data_output_path):

	df = pd.read_csv(data_input_path, skipinitialspace=True, usecols=[label, 'country'])
	df_out=binarize(label,favorable_label, df)
	df_out.to_csv(data_output_path, index=False, encoding='utf-8-sig')		
		
def binarize(label, favorable_label, df):
	print('label before forcing binary label')
	
	info=df[label].value_counts()
	print(info)
	print(len(df.index))
	
	df.loc[df[label] < favorable_label, label] = 0
	df.loc[df[label] >= favorable_label, label] = 1
		
	print('label after forcing binary label')
	info=df[label].value_counts()
	print(info)
	print(len(df.index))
	
	return df
	
	
