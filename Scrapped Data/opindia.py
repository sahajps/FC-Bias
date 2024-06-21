import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd

article_urls = []

url=['https://www.opindia.com/category/fact-check/'] + ['https://www.opindia.com/category/fact-check/page/'+str(i) for i in range(2,155)]

for i in tqdm(url):
  response = requests.get(i)

  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find('div', id='tdi_119').find_all('a', class_='td-image-wrap')

  for x in headlines:
    article_urls+=[x.get('href')]

df = pd.DataFrame()
df['links'] = article_urls

date = []
title = []
text = []

for l in tqdm(df.links):
  response = requests.get(l)
  soup = BeautifulSoup(response.text, 'html.parser')

  title.append(soup.find('h1', class_='tdb-title-text').text)
  date.append(soup.find('time', class_='entry-date updated td-module-date').text)

  txt = soup.find_all('p' , dir=lambda x: True if x!='ltr' else False)

  tmp = ''
  for t in txt[:-8]:
    tmp += t.text + " "

  text.append(tmp)

df['date'] = date
df['title'] = title
df['text'] = text

df.to_excel('data/opindia.xlsx', index=False)