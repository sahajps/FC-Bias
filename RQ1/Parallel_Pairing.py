import numpy as np
import pandas as pd
import ast
# from scipy.spatial import distance
import json
import os
import datetime
# from concurrent.futures import ThreadPoolExecutor
from joblib import Parallel, delayed
import multiprocessing
# from tqdm.notebook import tqdm
import sys
import argparse
import torch
from torch import nn
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-n1", help = "First News Org")
parser.add_argument("-n2", help = "Second News Org")
parser.add_argument("-type", help = "Embedding Type (claim, who, what)")
str_format = '%B %d, %Y'
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
cosine_list = []

def all_data(n1,n2,json_fin):
    # print("\n\n")
    print("-----"*6)
    a=pd.read_excel("Intermediate Output Files/" + n1 + "_emb_all.xlsx")
    b=pd.read_excel("Intermediate Output Files/" + n2 + "_emb_all.xlsx")
    print(n1,n2,a.shape,b.shape, json_fin)
    print("***"*20)
    get_cosine_15_parallel(a,b,n1,n2,json_fin)
                
def process_item(i, embi, j, embj, ni, nj):
    cos = nn.CosineSimilarity(dim=0, eps=1e-6)
    #print(i,j)
    sys.stdout.flush()
    cs = cos(embi.to(device),embj.to(device))
    cs = cs.cpu().numpy().tolist()
    return (i, j, ni, nj, cs)

def get_cosine_15_parallel(a,b,n1,n2,json_fin):
    #print(n1, n2)
    la = len(a)
    lb = len(b)
    field = json_fin + "_emb"
    emb_n1_list = a[field]
    emb_n1_list = [torch.Tensor(ast.literal_eval(emb)) for emb in emb_n1_list]
    emb_n2_list = b[field]
    emb_n2_list = [torch.Tensor(ast.literal_eval(emb)) for emb in emb_n2_list]
    num_cores = multiprocessing.cpu_count()//4
    
    cosine_list = Parallel(n_jobs=num_cores, backend="threading")(delayed(process_item)(i, emb_n1_list[i], j, emb_n2_list[j], n1, n2) for i in tqdm(range(la)) for j in range(lb))
    with open(os.path.join("Intermediate Output Files", n1 + "_" + n2 + "_" + json_fin + "_PARALLEL.json"), "w") as f:
        json.dump(cosine_list, f, indent=True)
    
if __name__=="__main__":
    args = parser.parse_args()
    print("Displaying N1 as: % s" % args.n1)
    print("Displaying N2 as: % s" % args.n2)
    print("Displaying TYPE as: % s" % args.type)
    n1 = args.n1
    n2 = args.n2
    json_fin = args.type
    all_data(n1,n2,json_fin)

    print("DONE !!")