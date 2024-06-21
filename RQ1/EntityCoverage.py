import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm
import json

def convS(s):
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
    df[feature] = df[feature].str.replace('[\n"\']', '', regex=True)
    df[feature] = df[feature].str.replace(r'{\s+', '{', regex=True)
    df[feature] = df[feature].str.replace(r'\s+}', '}', regex=True)
    df[feature] = df[feature].str.replace(r':\s+', ':', regex=True)
    df[feature] = df[feature].str.replace(r',\s+', ',', regex=True)
    #df.fear = df.fear.str.replace('none', 'neutral', regex=True)
    df[feature] = df[feature].apply(convS)

    return df

def map_to_root(df, mapping, feature):
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
    tmp = []
    for i in range(len(df)):
        row = df.iloc[i]
        #print(str(row.date_day)+" "+row.date_month+" "+str(row.date_year))
        tmp.append(datetime.strptime(str(row.date_day)+" "+row.date_month+" "+str(row.date_year), "%d %B %Y"))

    df['dateObj'] = tmp

    return df

def df_load(f):
    df = pd.read_excel('../RQ2/Topic Sentiment Data/'+f+'.xlsx')

    df = prepros(df, 'sentiments')

    mapping = pd.read_excel('../RQ2/Top Topics/'+f+'.xlsx')
    mapping = mapping[mapping.include==1]
    mapping.index = list(mapping.ent)

    df = map_to_root(df, mapping, 'sentiments')

    df.sentiments = df.sentiments.apply(lambda x: list(x))

    df = datetoObj(df)

    return df

def OverlapEnt(X, Y, Z):
    id = []
    entX = []
    entY = []
    entZ = []
    #err = 0
    for i in tqdm(range(len(X))):
        id.append(i)
        rowX = X.iloc[i]
        entX.append(rowX.sentiments)
        tmpY = []
        for j in range(len(Y)):
            rowY = Y.iloc[j]
            
            diff = rowY.dateObj - rowX.dateObj
            #print(diff.days)
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

    #print(err)
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

    with open('EntityIntersection/'+mode+'.json', 'w') as json_file:
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

    with open('EntityIntersection/'+mode+'.json', 'w') as json_file:
        json.dump(tmp_data, json_file, indent=4)
