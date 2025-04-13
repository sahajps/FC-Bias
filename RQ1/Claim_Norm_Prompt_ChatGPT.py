import os
import pandas as pd
import torch
from tqdm import tqdm
import time
from timeout_decorator import timeout
import openai
openai.api_key = "<KEY_HERE>"
import json
import sys

@timeout(15)
def chatGPT(prompt):
    res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                    {"role": "system", "content": prompt},
                    ],
                    temperature=0)

    return res

files=[
    "../Cleaned Data/checkyourfact.xlsx",
    "../Cleaned Data/politifact.xlsx",
    "../Cleaned Data/snopes.xlsx",
    "../Cleaned Data/opindia.xlsx",
    "../Cleaned Data/altnews.xlsx",
    "../Cleaned Data/boomlive.xlsx"
   ]
print(files)

for f in files:
    org_name = f.split("/")[-1]
    print(org_name)
    df = pd.read_excel(f)
    l = len(df)
    claim_norm = [[]]*l
    claim_not_json = []
    for i in tqdm(range(l)):
        row = df.iloc[i]
        prompt = "For the given news item, strictly return a list with the most important sentences highlighting the motivation behind spreading the fake news covered in the article. The selected sentences should be the ones that capture the central claim in the fake news. Quote verbatim: do not add any new sentences on your own. Strictly return a JSON decodable python list format. NEWS ARTICLE: " + row.text
        while(True):
            try:
                response = chatGPT(prompt)
                break
            except:
                print('sleep')
                sys.stdout.flush()
                time.sleep(50)
                print('here we go...')
                sys.stdout.flush()
                continue

        try:
            claim_norm[i] = json.loads(response["choices"][0]["message"]["content"].lower())
        except Exception as e:
                print(e)
                sys.stdout.flush()
                print("CURR ROW:: ", i)
                sys.stdout.flush()
                claim_not_json.append(i)
                claim_norm[i]="ERROR DECODING:: " + response["choices"][0]["message"]["content"].lower()

    
    df['claim_norm'] = claim_norm
    # adding date column as MM DD, YYYY eg. May 1, 2022
    df.insert(1, 'date', df['date_month'] + ' ' + df['date_day'].astype(str) + ', ' + df['date_year'].astype(str))
    df.drop(columns=['date_year', 'date_month', 'date_day'], inplace=True)
    df.to_excel('Claim Norm Data/'+org_name+".xlsx", index=False)
    print(claim_not_json)
    sys.stdout.flush()