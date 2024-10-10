import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm
import json

def convS(s):
    """
    Ofcourse GPT-3.5 is a smart model and capable enough to return the results in said format (in-most of the cases).
    This function is trying to extract then entity-sentiment pair in a dict format.
    """
    s = s[1:-1]
    dic = {}

    positions=[match.end() for match in re.finditer(r'\b(?:positive|negative|neutral)\b,', s, flags=re.IGNORECASE)]
    for ss in [s[i:j] for i, j in zip([0] + positions, positions + [None])]:
        tmp = ss.split(':')
        try:
            dic[tmp[0]] = tmp[1].replace(",", "")
        except:
            continue
    
    return dic

def prepros(df, feature):
    """
    Some basic preprocessing & mapping of string sentiment data to dict format
    """
    df[feature] = df[feature].str.replace('[\n"\']', '', regex=True)
    df[feature] = df[feature].str.replace(r'{\s+', '{', regex=True)
    df[feature] = df[feature].str.replace(r'\s+}', '}', regex=True)
    df[feature] = df[feature].str.replace(r':\s+', ':', regex=True)
    df[feature] = df[feature].str.replace(r',\s+', ',', regex=True)
    
    df[feature] = df[feature].apply(convS)

    return df

def map_to_root(df, mapping, feature):
    """
    Returns a dict with poltical entities as keys and list of sentiments in values
    1. Entity names is used as per the annotated mapping (Top Entity folder)
    2. If entity isn't in top entity list then we are not including them into this dict.
       (B/C after top-100 frequency drops significantly)
    """
    top = list(mapping.index)
    vals = []
    for dic in df[feature]:
        tmp = {}
        for k in dic:
            #print(k)
            if k in top:
                tmp[mapping.loc[k].loc['map']] = dic[k]

        vals.append(tmp)

    df[feature] = vals
    return df

def datetoObj(df):
    """
    Converting the date string to datetime object
    """
    tmp = []
    for i in range(len(df)):
        row = df.iloc[i]
        #print(str(row.date_day)+" "+row.date_month+" "+str(row.date_year))
        tmp.append(datetime.strptime(str(row.date_day)+" "+row.date_month+" "+str(row.date_year), "%d %B %Y"))

    df['dateObj'] = tmp

    return df

def df_load(f):
    """
    Loads the entity-sentiment data and do needful processing
    """
    df = pd.read_excel('../RQ2/Entity Sentiment Data/'+f+'.xlsx')

    df = prepros(df, 'sentiments')

    mapping = pd.read_excel('../RQ2/Top Entity/'+f+'.xlsx')
    mapping = mapping[mapping.include==1]
    mapping.index = list(mapping.ent)

    df = map_to_root(df, mapping, 'sentiments')

    df.sentiments = df.sentiments.apply(lambda x: list(x))

    df = datetoObj(df)

    return df

def OverlapEnt(X, Y, Z):
    """
    For X's each articles, we are taking all articles of Y and Z
    X[i] = entities in article i of X org
    Y[i]/Z[i] = entities in all articles of Y/Z org which published in a 15-days window of the ith article of X org
    """
    id = []
    entX = []
    entY = []
    entZ = []
    
    for i in tqdm(range(len(X))):
        id.append(i)
        rowX = X.iloc[i]
        entX.append(rowX.sentiments)
        tmpY = []
        for j in range(len(Y)):
            rowY = Y.iloc[j]
            
            diff = rowY.dateObj - rowX.dateObj
            if -15 <= diff.days <= 15:
                tmpY += rowY.sentiments
        entY.append(list(set(tmpY)))

        tmpZ = []
        for k in range(len(Z)):
            rowZ = Z.iloc[k]
            
            diff = rowZ.dateObj - rowX.dateObj
            if -15 <= diff.days <= 15:
                tmpZ += rowZ.sentiments
        entZ.append(list(set(tmpZ)))

    json_data = {}
    json_data['id'] = id
    json_data['X'] = entX
    json_data['Y'] = entY
    json_data['Z'] = entZ

    return json_data

################################################

###### FOR USA ######
files = ['checkyourfact', 'politifact', 'snopes']
df1 = df_load(files[0])
df2 = df_load(files[1])
df3 = df_load(files[2])

for mode in files:
    print(mode)
    if(mode=='checkyourfact'):
        tmp_data = OverlapEnt(df1, df2, df3)
    elif(mode=='politifact'):
        tmp_data = OverlapEnt(df2, df1, df3)
    else:
        tmp_data = OverlapEnt(df3, df1, df2)

    with open('Entity Intersection/'+mode+'.json', 'w') as json_file:
        json.dump(tmp_data, json_file, indent=4)

###### FOR INDIA ######
files = ['altnews', 'boomlive', 'opindia']
df1 = df_load(files[0])
df2 = df_load(files[1])
df3 = df_load(files[2])

for mode in files:
    print(mode)
    if(mode=='altnews'):
        tmp_data = OverlapEnt(df1, df2, df3)
    elif(mode=='boomlive'):
        tmp_data = OverlapEnt(df2, df1, df3)
    else:
        tmp_data = OverlapEnt(df3, df1, df2)

    with open('Entity Intersection/'+mode+'.json', 'w') as json_file:
        json.dump(tmp_data, json_file, indent=4)
