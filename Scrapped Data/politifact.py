import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import time

article_urls = []

url=['https://www.politifact.com/factchecks/list/'] + ['https://www.politifact.com/factchecks/list/?page='+str(i) for i in range(2, 340)]

for i in tqdm(url):
  response = requests.get(i)

  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find_all('div', class_="m-statement__quote")
 
  for x in headlines:
    article_urls+=['https://www.politifact.com' + x.find('a').get('href')]

df = pd.DataFrame()
df['links'] = article_urls

date = []
title = []
text = []

for l in tqdm(df.links):
  flag =False
  try:
    response = requests.get(l)
  except:
    time.sleep(30)
    try:
      response = requests.get(l)
    except:
      time.sleep(30)
      try:
        response = requests.get(l)
      except:
        time.sleep(30)
        try:
          response = requests.get(l)
        except:
          flag=True

  if(flag):
    title.append(None)
    date.append(None)
    title.append(None)
    continue

  soup = BeautifulSoup(response.text, 'html.parser')

  try:
    title.append(soup.find('div', class_='m-statement__meta').find('a').text + soup.find('div', class_='m-statement__meta').find('div').text + soup.find('div', class_='m-statement__quote').text)
  except:
    title.append(None)

  try:
    date.append(l[38:49])
  except:
    date.append(None)

  try:
    txt = soup.find('article', class_="m-textblock")

    for em in txt.find_all('em'):
      em.decompose()

    txt = txt.find_all('p')

    tmp = ''
    for t in txt:
      tmp += t.text + " "

    text.append(tmp)
  except:
    text.append(None)

df['date'] = date
df['title'] = title
df['text'] = text

df.to_excel('data/politifact.xlsx', index=False)