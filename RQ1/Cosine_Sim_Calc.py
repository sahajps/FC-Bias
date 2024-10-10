import pandas as pd
import json
import sys
import argparse
import datetime
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-n1", help = "First News Org")
parser.add_argument("-n2", help = "Second News Org")
parser.add_argument("-n3", help = "Third News Org")
parser.add_argument("-t", help = "Embedding Type (claim, who, what)")
parser.add_argument("-w", help = "Topical Window, default we should give 15")
str_format = '%B %d, %Y'

def all_data(n1,n2,n3,json_fin,window=15):
    # print("\n\n")
    print("-----"*6)
    a=pd.read_excel("Claim Norm Data/" + n1 + ".xlsx")
    a["date_obj"] = a["date"].map(lambda d:datetime.datetime.strptime(d, str_format))
    l1 = a.shape[0]
    b=pd.read_excel("Claim Norm Data/" + n2 + ".xlsx")
    b["date_obj"] =  b["date"].map(lambda d:datetime.datetime.strptime(d, str_format))
    c=pd.read_excel("Claim Norm Data/" + n3 + ".xlsx")
    c["date_obj"] = c["date"].map(lambda d:datetime.datetime.strptime(d, str_format))
    print(n1,n2,n3,a.shape,b.shape,c.shape)
    
    # sys.stdout.flush()
    with open("Intermediate Output Files/"+n1+"_"+n2+"_"+json_fin+"_PARALLEL.json", "r") as f:
        f1 = json.load(f)
    with open("Intermediate Output Files/"+n1+"_"+n3+"_"+json_fin+"_PARALLEL.json", "r") as f:
        f2 = json.load(f)
    print(n2,n3,len(f1),len(f2))
    # sys.stdout.flush()
    print("For N2")
    # sys.stdout.flush()
    match_set_ab = get_window_matches(a,b,window)
    print("For N3")
    # sys.stdout.flush()
    match_set_ac = get_window_matches(a,c,window)
    # sys.stdout.flush()
    del (a,b,c)
    print("For F1")
    f1 = list_2_dict(f1)
    print("For F2")
    f2 = list_2_dict(f2)
    # sys.stdout.flush()
    print("***"*20)
    fl1=get_row_wise(f1,match_set_ab, l1)
    print("Done1")
    print("--"*20)
    # sys.stdout.flush()
    fl2=get_row_wise(f2,match_set_ac, l1)
    print("Done2")
    print("--"*20)
    # sys.stdout.flush()
    print(len(fl1[0]),len(fl2[0]))
    data_dict={n2:fl1,n3:fl2}
    with open("Cosine Scores/"+n1+"_"+json_fin+"_all_cosine_NEW.json","w") as f:
        json.dump(data_dict,f,indent=True)
    
def get_window_matches(x,y,window):
    l1 = x.shape[0]
    l2 = y.shape[0]
    match_set = []
    for i in tqdm(range(l1)):
        # if i%100==0:
        #     print(i)
        #     sys.stdout.flush()
        datex = x.iloc[i]["date_obj"]
        for j in range(l2):
            datey = y.iloc[j]["date_obj"]
            diff = datey - datex
            if -window <= diff.days <= window:
                match_set.append((i,j))
    # print(len(match_set))
    match_set = frozenset(match_set)
    # print(len(match_set))
    return match_set

def list_2_dict(flist):
    final_dict={}
    for item in flist:
        i = item[0]
        j = item[1]
        if i in final_dict and j in final_dict[i]:
                continue
        elif i not in final_dict:
            final_dict[i]={}    
        final_dict[i][j]=item[4]
    return final_dict

def get_row_wise(fdict, match_set, l1):
    new_list= [[] for _ in range(l1)]
    count = 0
    for item in match_set:
        # print(count)
        # sys.stdout.flush()
        count+=1
        i = item[0]
        j = item[1]
        new_list[i].append(fdict[i][j])
    return new_list

if __name__=="__main__":
    args = parser.parse_args()
    print("Displaying N1 as: % s" % args.n1)
    print("Displaying N2 as: % s" % args.n2)
    print("Displaying N3 as: % s" % args.n3)
    print("Displaying TYPE as: % s" % args.t)
    print("Displaying WINDOW as: % s" % args.w)
    # sys.stdout.flush()
    n1 = args.n1
    n2 = args.n2
    n3 = args.n3
    json_fin = args.t
    window = int(args.w)
    all_data(n1,n2,n3,json_fin,window)
    print("All DONE :)")