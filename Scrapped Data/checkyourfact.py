import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd

article_urls = []

url=['https://checkyourfact.com/'] + ['https://checkyourfact.com/page/'+str(i)+'/' for i in range(2,346)]

for i in tqdm(url):
  response = requests.get(i)

  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find('atom').find('articles').find_all('a')

  for x in headlines:
    article_urls+=['https://checkyourfact.com'+x.get('href')]

df = pd.DataFrame()
df['links'] = article_urls

date = []
title = []
text = []

for l in tqdm(df.links):
  response = requests.get(l)
  soup = BeautifulSoup(response.text, 'html.parser').find('article')

  try:
    title.append(soup.find('h1').text)
  except:
    title.append(None)
  
  try:
    date.append(soup.find('time').text)
  except:
    date.append(None)

  try:
    tmp = ''

    txt = soup.find_all('p')

    for t in txt:
      tmp += t.text + " "

    text.append(tmp)
  except:
    text.append(None)

df['date'] = date
df['title'] = title
df['text'] = text

df.to_excel('data/checkyourfact.xlsx', index=False)