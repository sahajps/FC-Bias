import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd

article_urls = []

url=['https://www.snopes.com/fact-check/'] + ['https://www.snopes.com/fact-check/?pagenum='+str(i) for i in range(2,530)]

for i in tqdm(url):
  response = requests.get(i)

  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find_all('a', class_="outer_article_link_wrapper")

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

  try:
    title.append(soup.find('h1').text)
  except:
    title.append(None)
  
  try:
    date.append(soup.find('h3', class_="publish_date").text)
  except:
    date.append(None)

  try:
    try:
      tmp = soup.find('section', id="fact_check_rating_container").get_text()
      for sec in soup.find_all('section', id="fact_check_rating_container"):
        sec.decompose()
    except:
      tmp = ''

    txt = soup.find('article', id="article-content").find_all(['p', 'h2'])

    for t in txt:
      if(t.text=='Sources'):
        break
      tmp += t.text + " "

    text.append(tmp)
  except:
    text.append(None)


df['date'] = date
df['title'] = title
df['text'] = text

df.to_excel('data/snopes.xlsx', index=False)