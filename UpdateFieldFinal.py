import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import json
from airtable import Airtable
import simplejson as json
import ast
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


# def tick():
# adjust round
currentRound = 'R1'
# Current Tournament ID for Open Championship
tournament_id='401056547'
# check par
par = 71
table_name = 'OPEN_FIELD'
entries_table = 'OPEN_ENTRIES'

AIRTABLE_API_KEY = 'keybBQGNdYeJkRwcs'
base_key = 'appmCQ7CzGefKPdmu'
url = 'http://www.espn.com/golf/leaderboard?tournamentId='+str(tournament_id)
# url = 'http://www.espn.com/golf/leaderboard'



pd.options.mode.chained_assignment = None

page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
html = soup.find("table", attrs={"class": "Table2__table__wrapper"})
table= pd.read_html(html.prettify())
df = table[2]
df['PLAYER'] = df['PLAYER'].str.replace("'","")
df = df.set_index("PLAYER")
df.to_csv('espnfield.csv')


airtable = Airtable(base_key, table_name, AIRTABLE_API_KEY)
field = airtable.get_all()
field = pd.DataFrame.from_dict(field)


field_data= [0]*len(field)
for (i, entry) in enumerate(field_data):
        entry = field.loc[i]['fields']
        field_data[i] = entry

field_data = pd.DataFrame.from_dict(field_data)
field_data = field_data.join(df, on='PLAYER')
field_data = field_data.set_index('Index')

field_data.to_csv('entryscores.csv')
field_data = field_data[field_data['status'] == 'available']
field_data[currentRound].replace(to_replace='--',value=0, inplace=True)
field_data[currentRound] = field_data[currentRound].astype('int64')

highScore = int(field_data[currentRound].max())
print(highScore)

field_data[currentRound].replace(to_replace=0,value=highScore, inplace=True)




airtableEntries = Airtable(base_key, entries_table, AIRTABLE_API_KEY)
entries = airtableEntries.get_all()
entries = pd.DataFrame.from_dict(entries)

entries_new= [0]*len(entries)

for (i, entry) in enumerate(entries_new):
    entry = entries.loc[i]['fields']
    entries_new[i] = entry

entries_newDF = pd.DataFrame.from_dict(entries_new)
entries_newDF = entries_newDF.join(entries['id'])
scoreDF = [0]*len(entries_newDF)



for (i, team) in enumerate(scoreDF):  
    team = entries_newDF.loc[i]['entry']
    team=ast.literal_eval(team)
    teamPlayerNames = [0]*len(team)
    for(j, player) in enumerate(teamPlayerNames):
        player = team[j]
        player = int(player)+1
        player = int(field_data.loc[player][currentRound])
        teamPlayerNames[j] = player
    scoreDF[i]=teamPlayerNames
entries_newDF[currentRound]=scoreDF

roundtotalDF = [0]*len(entries_newDF)
tournamentTotalDF = [0]*len(entries_newDF)
teamScoresDF = [0]*len(entries_newDF)

# print(entries_newDF)
for i in range(len(entries_newDF)):
    players = entries_newDF.loc[i]['players']
    players = ast.literal_eval(players)
    playerScores = entries_newDF.loc[i][currentRound]
    # print(players)
    # print(playerScores)
    entryscores = pd.DataFrame({'players': players, 'scores': playerScores})
    entryscores.sort_values(by='scores', inplace=True)

    # print(entryscores)
    scoringEntries = entryscores.nsmallest(4, 'scores')
    # print(scoringEntries)
    countedScores= scoringEntries['scores'].sum()
    teamScores = entryscores.to_json(orient='index')

    # print(countedScores)
    roundtotalDF[i] = countedScores-(par * 4)
    teamScoresDF[i] = teamScores

entries_newDF[currentRound+'Total']=roundtotalDF
entries_newDF[currentRound]= teamScoresDF

entries_newDF.to_csv('entries.csv')

# for i in range(len(entries_newDF)):
#     R1Total = entries_newDF.loc[i]['R1Total']
#     R2Total = entries_newDF.loc[i]['R2Total']
#     R3Total = entries_newDF.loc[i]['R3Total']
#     R4Total = entries_newDF.loc[i]['R4Total']
#     tournamentTotalDF[i] = int(R1Total)+int(R2Total)+int(R3Total)+int(R4Total)

# entries_newDF['TournamentTotal']=tournamentTotalDF

# # entries_newDF[currentRound]=entries_newDF[currentRound].astype('str')
# entries_newDF[currentRound+'Total']=entries_newDF[currentRound+'Total'].astype('str')
# entries_newDF['TournamentTotal']=entries_newDF['TournamentTotal'].astype('str')

# entries_newDF.to_csv('entries.csv')
# for i in range(len(entries_newDF)):
#     entry_id= entries_newDF.loc[i]['id']
#     fields = {
#         currentRound: entries_newDF.loc[i][currentRound],
#         currentRound+'Total': entries_newDF.loc[i][currentRound+'Total'],
#         'TournamentTotal': entries_newDF.loc[i]['TournamentTotal']
#     }
#     airtableEntries.update(entry_id,fields)
    
# print('Tick! The time is: %s' % datetime.now())
    
# if __name__ == '__main__':
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(tick, 'interval',  minutes=10)
#     scheduler.start()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

#     try:
#         # This is here to simulate application activity (which keeps the main thread alive).
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         # Not strictly necessary if daemonic mode is enabled but should be done if possible
#         scheduler.shutdown()
