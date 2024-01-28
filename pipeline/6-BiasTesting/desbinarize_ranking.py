import pandas as pd

data_output_path = "../0-Data/1_intermediate_generated_data/unbiased_rankings/rankings_0.csv"

def save_as_desbinarized(df_blDataset, ranking_name, country_name):
    
    new_column_name = ranking_name + country_name

    desbinarized_ranking_df = pd.DataFrame()
    desbinarized_ranking_df[new_column_name] = desbinarize_ranking(df_blDataset, ranking_name)
    desbinarized_ranking_df.reset_index(drop=True, inplace=True)
    
    try:
        desbinarized_rankings_df = pd.read_csv(data_output_path)

        if (new_column_name in desbinarized_rankings_df.columns):
            desbinarized_rankings_df[new_column_name] = desbinarized_ranking_df[new_column_name]
        else:
            desbinarized_rankings_df = pd.concat([desbinarized_rankings_df, desbinarized_ranking_df], axis=1)
        
        desbinarized_rankings_df.to_csv(data_output_path, index=False)
    
    except FileNotFoundError:
        desbinarized_ranking_df.to_csv(data_output_path, index=False)

def desbinarize_ranking(binary_rankings_df, ranking_name):

    binary_rankings_df = binary_rankings_df.filter(items=[ranking_name])
    binary_rankings_df.loc[(binary_rankings_df[ranking_name] == 1)] = 3

    return binary_rankings_df[ranking_name]
