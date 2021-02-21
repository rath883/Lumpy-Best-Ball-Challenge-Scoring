import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

par = 70
tournament_id='401219802'
AIRTABLE_API_KEY = 'keybBQGNdYeJkRwcs'
base_key = 'appmCQ7CzGefKPdmu'
url = 'https://www.espn.com/golf/leaderboard/_/tournamentId/'+str(tournament_id)

# 'https://www.espn.com/golf/leaderboard?tournamentId='+str(tournament_id)

# https://www.cbssports.com/golf/leaderboard/pga-tour/26441720/mayakoba-golf-classic-presented-by-unifin/

page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
html = soup.find("table", attrs={"class": "Table Table--align-right"})
table= pd.read_html(html.prettify())
# html.prettify()
print(table)