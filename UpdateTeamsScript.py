
import pandas as pd
import csv
import json
from airtable import Airtable
import simplejson as json
import ast


AIRTABLE_API_KEY = 'keybBQGNdYeJkRwcs'
base_key = 'appmCQ7CzGefKPdmu'
table_name = 'OPEN_ENTRIES'
airtable = Airtable(base_key, table_name, AIRTABLE_API_KEY)
entries = json.dumps(airtable.get_all())
entriesDF = pd.read_json(entries)

entriesDF.sort_values(by='createdTime')


entries_new= [0]*len(entriesDF)
for (i, entry) in enumerate(entries_new):
        entry = entriesDF.loc[i]['fields']
        entries_new[i] = entry

entries_newDF = pd.DataFrame.from_dict(entries_new)
entries_newDF = entries_newDF.join(entriesDF['id'])
entries_newDF


AIRTABLE_API_KEY = 'keybBQGNdYeJkRwcs'
base_key = 'appmCQ7CzGefKPdmu'
table_name = 'OPEN_FIELD'
airtable = Airtable(base_key, table_name, AIRTABLE_API_KEY)
field = json.dumps(airtable.get_all())
field = pd.read_json(field)
fieldDF= [0]*len(field)
for (i, player) in enumerate(fieldDF):
        player = field.loc[i]['fields']
        fieldDF[i] = player

fieldDF = pd.DataFrame.from_dict(fieldDF)
fieldDF = fieldDF.set_index('Index')
fieldDF


playersDF = [0]*len(entries_newDF)

for (i, team) in enumerate(playersDF):  
    team = entries_newDF.loc[i]['entry']
    team=ast.literal_eval(team)
    teamPlayerNames = [0]*len(team)
    for(j, player) in enumerate(teamPlayerNames):
        player = team[j]
        player = int(player)+1
        
        try:
            player = fieldDF.loc[player]['PLAYER']
        except:
            player = Null
        teamPlayerNames[j] = player
    playersDF[i]=teamPlayerNames 

entries_newDF['players']=playersDF
entries_newDF['players']=entries_newDF['players'].astype('str')

entries_newDF
#entries_newDF = entries_newDF.set_index('id')

for i in range(len(entries_newDF)):
    entry_id= entries_newDF.loc[i]['id']
    players = {'players': entries_newDF.loc[i]['players']}
    airtable.update(entry_id,players)
    print(i)




