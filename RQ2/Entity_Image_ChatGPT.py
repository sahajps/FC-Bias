import pandas as pd
import torch
import torch.nn as nn
from datasets import load_dataset
from tqdm import tqdm
import time
from timeout_decorator import timeout
import openai
openai.api_key = "Your OpenAI key"

@timeout(15)
def chatGPT(prompt):
    res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                    {"role": "system", "content": prompt},
                    ],
                    temperature=0)

    return res

###########################################################
files = ['../Cleaned Data/checkyourfact.xlsx',
 '../Cleaned Data/politifact.xlsx',
 '../Cleaned Data/snopes.xlsx',
 '../Cleaned Data/opindia.xlsx',
 '../Cleaned Data/boomlive.xlsx',
 '../Cleaned Data/altnews.xlsx']

# This code runs all files for the given prompt but we highly suggest to use the below code to run it one by one because sometimes ChatGPT api stops working due the over-requast (although we have handled that error)

# files = [files["ENTER A FILE INDEX say: 0,1,2,..."]]
# print(files)

for f in files:
    df = pd.read_excel(f)
    
    senti = []
    for i in tqdm(range(df.shape[0])):
        row = df.iloc[i]
        prompt = "List (in python dictionary type eg. {a: tag_a, b: tag_b}) the names of political figures and parties, categorizing each entity as positive if it helps improve their image, negative if it has the opposite effect, and neutral if it presents balanced views: " + row.text 

        # handling non-resposive api request error !
        while(True):
            try:
                response = chatGPT(prompt)
                break
            except:
                print('sleep')
                time.sleep(50)
                print('here we go...')
                continue
            
        senti += [response["choices"][0]["message"]["content"].lower()]
    
    df['sentiments'] = senti
    df.to_excel('Entity Sentiment Data/'+f[16:], index=False)