
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

url = 'https://www.msn.com/en-us/sports/golf/leaderboard/sp-id-70401000401967075'
page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
html = soup.find("div", attrs={"id": "standings"})
table= pd.read_html(html.prettify())
df = table[0]
#df.drop(columns=['Unnamed: 0'], inplace=True)
#df.dropna(how='all',inplace=True)
#df['PLAYER']=df['PLAYER'].str.strip("*")
df.to_csv('leaderboard2.csv')