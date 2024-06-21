import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import time
from timeout_decorator import timeout

article_urls = []

url=['https://www.boomlive.in/fact-check'] + ['https://www.boomlive.in/fact-check/'+str(i)+'/?s=+/' for i in range(2,287)]

for i in tqdm(url):
  response = requests.get(i)

  soup = BeautifulSoup(response.text, 'html.parser')
  headlines = soup.find_all('a', class_='heading_link')

  for x in headlines:
    article_urls+=['https://www.boomlive.in' + x.get('href')]

df = pd.DataFrame()
df['links'] = article_urls
print(df.links)
date = []
title = []
text = []
xx=0

@timeout(10)
def GetPage(l):
  return requests.get(l)
    
for l in tqdm(df.links):
  try:
    response = GetPage(l)
  except:
    time.sleep(30)
    print("App None")
    date.append(None)
    title.append(None)
    text.append(None)
    continue
      
  soup = BeautifulSoup(response.text, 'html.parser')#.find('div', id="post-content-wrapper")

  try:
    title.append(soup.find('header', class_='entry-header entry-header1').find('h1').text)
    
    date.append(soup.find('span', class_='convert-to-localtime').text)
    
    txt = soup.find_all('p')
    
    tmp = soup.find('header', class_='entry-header entry-header1').find('h2').text + " "
    for t in txt:
        if(t.text.startswith('Click here to view the post')):
            continue
        if(t.text.startswith('Also Read')):
            continue
        tmp += t.text + " "
    
    text.append(tmp)
  except:
      title.append(None)
      date.append(None)
      text.append(None)
  
df['date'] = date
df['title'] = title
df['text'] = text

df.to_excel('data/boomlive.xlsx', index=False)