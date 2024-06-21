import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import time
from timeout_decorator import timeout

article_urls = []

url=['https://www.altnews.in/?s=+']  + ['https://www.altnews.in/page/'+str(i)+'/?s=+/' for i in range(2,470)]

for i in tqdm(url):
  response = requests.get(i)

  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find_all('a', rel='bookmark')

  for x in headlines:
    article_urls+=[x.get('href')]

df = pd.DataFrame()
df['links'] = article_urls

date = []
title = []
text = []

######################################################
@timeout(10)
def GetPage(l):
  return requests.get(l)

for l in tqdm(df.links):
  while(True):
    try:
      response = GetPage(l)
      break
    except:
      time.sleep(30)
  
  soup = BeautifulSoup(response.text, 'html.parser')

  for div in soup.find_all('div', class_='fb-video'):
    div.decompose()

  for blockquote in soup.find_all('blockquote', class_="twitter-tweet"):
    blockquote.decompose()

  title.append(soup.find('h1').text)
  try:
    date.append(soup.find('header', class_="entry-header e-h").find('time').text)
  except:
    date.append(None)

  txt = soup.find_all('p')# , dir=lambda x: True if x!='ltr' else False)

  tmp = ''
  tp = False
  for t in txt:
    if(t.text=="This slideshow requires JavaScript."):
      continue
    if(t.text=='Donate Now'):
      break
    tmp += t.text + " "

  text.append(tmp)

df['date'] = date
df['title'] = title
df['text'] = text

df.to_excel('data/altnews.xlsx', index=False)