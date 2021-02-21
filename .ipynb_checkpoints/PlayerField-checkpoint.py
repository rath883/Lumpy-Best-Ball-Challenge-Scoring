
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv

url = 'https://www.golfchannel.com/tours/pga-tour/2018/greenbrier-classic/'
page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
html = soup.find("table", attrs={"id": "fullLeaderboard"})
table= pd.read_html(html.prettify())
df = table[0]
df.drop(columns=['Unnamed: 0'], inplace=True)
df.dropna(how='all',inplace=True)
df['PLAYER']=df['PLAYER'].str.strip("*")
df.to_csv('leaderboard.csv')