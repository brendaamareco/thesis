#####################################################################
# Add a new column to your data set
#####################################################################
import pandas as pd 

#####################################################################
# We are going to calculate the entropy of a text
#####################################################################
import math
from collections import Counter

def entropy(text, unit='shannon'):
    base = {
        'shannon' : 2.,
        'natural' : math.exp(1),
        'hartley' : 10.
    }

    if len(text) <= 1:
        return 0

    counts = Counter()

    for d in text:
        counts[d] += 1

    probs = [float(c) / len(text) for c in counts.values()]
    probs = [p for p in probs if p > 0.]

    ent = 0

    for p in probs:
        if p > 0.:
            ent -= p * math.log(p, base[unit])

    return ent

####################################################################

def save_entropy():
    data = pd.read_csv("../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv")
    data['entropy'] = data.apply(lambda x: entropy(str(x['review'])), axis=1)
    df= pd.DataFrame(data)
    df.to_csv('../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv', index=False, encoding='utf-8-sig')