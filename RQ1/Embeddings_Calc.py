from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
from collections import Counter
import ast
from scipy.spatial import distance
import os
import datetime
from tqdm import tqdm

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

media_name = [
    'politifact', 
    'snopes', 
    'checkyourfact', 
    'altnews', 
    'boomlive', 
    'opindia']
str_format = '%B %d, %Y'

for media in media_name:
    data1 = pd.read_excel("Claim Norm Data/" + media + ".xlsx")
    l = len(data1)
    print("\n\n","---"*10,media, l)
    data2 = pd.read_excel("Claim Norm Data/" + media + "_5W.xlsx")
    data1["what_why"] = data2["claim_norm"]    
    embedding_list_claim = []
    embedding_list_what = []
    embedding_list_why = []
    for i in tqdm(range(l)):
        if i%1000==0:
            print(i)
        row = data1.iloc[i]
        x = row["claim_norm"]
        y1 = row["what_why"]
        y2 = row["what_why"]
        
        try:
            x = ast.literal_eval(x)
            assert len(x)!=0 and type(x)==list
            embedding = model.encode(x)
            embedding = np.mean(embedding,axis=0)
            embedding = embedding.tolist()
            embedding_list_claim.append(embedding)
        except Exception as e:
            embedding_list_claim.append([0.000001]*768)    
        
        try:
            y1 = ast.literal_eval(y1)
            what = y1.get("what",[])
            assert len(what)!=0 and type(what)==list
            embedding = model.encode(what)
            embedding = np.mean(embedding,axis=0)
            embedding = embedding.tolist()
            embedding_list_what.append(embedding)
        except Exception as e:
            embedding_list_what.append([0.000001]*768)
              
        try:
            y2 = ast.literal_eval(y2)
            why = y2.get("why",[])
            assert len(why)!=0 and type(why)==list
            embedding = model.encode(why)
            embedding = np.mean(embedding,axis=0)
            embedding = embedding.tolist()
            embedding_list_why.append(embedding)
        except Exception as e:
            embedding_list_why.append([0.000001]*768)
            
    data1["claim_emb"] = embedding_list_claim
    data1["what_emb"] = embedding_list_what
    data1["why_emb"] = embedding_list_why
    data1.to_excel("Intermediate Output Files/" + media + "_emb_all.xlsx",index=False)
