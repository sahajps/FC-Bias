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
    claim_norm = [[]]*l # this worked well! but it's not a good practice :(
    claim_not_json = []
    for i in tqdm(range(l)):
        row = df.iloc[i]
        prompt = 'From the following fact-checking news article, quote full and complete sentences from within the post answering the what and why of the 5W based only on the misinformed part and related to the fake news. It is possible that each W can have multiple sentences. Return the result in the format {"what":[], "why":[]}. Quote verbatim: do not add any new sentences on your own, do not paraphrase. Do not focus on how the factchecking is done. Strictly return a JSON decodable Python list format. NEWS ARTICLE: ' + row.text

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
    df.to_excel('Claim Norm Data/'+org_name+"_5W.xlsx", index=False)
    print(claim_not_json)
    sys.stdout.flush()