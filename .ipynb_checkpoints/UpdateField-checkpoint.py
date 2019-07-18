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

def tick():
    tournament_id='401056527'
    AIRTABLE_API_KEY = 'keybBQGNdYeJkRwcs'
    base_key = 'appmCQ7CzGefKPdmu'
    url = 'http://www.espn.com/golf/leaderboard?tournamentId='+str(tournament_id)

    pd.options.mode.chained_assignment = None

    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    html = soup.find("table", attrs={"class": "Table2__table-scroller Table2__right-aligned Table2__table"})
    table= pd.read_html(html.prettify())
    df = table[0]
    df = df.set_index("PLAYER")

    table_name = 'Masters_Field'
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
    field_data['TODAY'].replace(to_replace='E',value=0, inplace=True)
    field_data['TODAY'].replace(to_replace='-',value=0, inplace=True)
    field_data['TODAY'].astype('int64')
    highScore = int(field_data['R3'].max())-72

    for i in range(len(field_data)):
        if field_data.loc[i+1]['THRU'] == 'CUT':
            print(field_data.loc[i+1]['THRU'])
            field_data.at[i+1,'TODAY'] = highScore
    field_data.to_csv('scores.csv')

    entries_table = 'masters2019Entries'
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
            player = int(field_data.loc[player]['TODAY'])+72
            teamPlayerNames[j] = player
        scoreDF[i]=teamPlayerNames
    entries_newDF['R3']=scoreDF

    roundtotalDF = [0]*len(entries_newDF)
    tournamentTotalDF = [0]*len(entries_newDF)

    for i in range(len(entries_newDF)):
        playerScores = entries_newDF.loc[i]['R3']
        playerScores.sort()
        countedScores = playerScores[:4]
        roundtotalDF[i] = sum(countedScores)-288
        R1Total = entries_newDF.loc[i]['R1Total']
        R2Total = entries_newDF.loc[i]['R2Total']
        tournamentTotalDF[i] = int(R1Total)+int(R2Total)+roundtotalDF[i]
    entries_newDF['R3Total']=roundtotalDF
    entries_newDF['TournamentTotal']=tournamentTotalDF

    print(entries_newDF)

    entries_newDF['R3']=entries_newDF['R3'].astype('str')
    entries_newDF['R3Total']=entries_newDF['R3Total'].astype('str')
    entries_newDF['TournamentTotal']=entries_newDF['TournamentTotal'].astype('str')

    entries_newDF.to_csv('entries2.csv')

    for i in range(len(entries_newDF)):
        entry_id= entries_newDF.loc[i]['id']
        fields = {
            'R3': entries_newDF.loc[i]['R3'],
            'R3Total': entries_newDF.loc[i]['R3Total'],
            'TournamentTotal': entries_newDF.loc[i]['TournamentTotal']
        }
        airtableEntries.update(entry_id,fields)
        print(i)
        print('Tick! The time is: %s' % datetime.now())
    
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval',  minutes=5)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
