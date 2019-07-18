import pandas as pd

urls = ("120", "152", "02447", "02675")
dfs = [0]*len(urls)

for (i, url) in enumerate(urls):
    url = r"https://www.pgatour.com/stats/stat."+urls[i]+".html"
    tables = pd.read_html(url)
    table = (tables[1])
    ##print(type(table))
    dfs[i] = table
    dfs[i].drop(dfs[i].columns[[0, 1]], axis=1, inplace=True)
    dfs[i]=dfs[i].set_index("PLAYER NAME")
    dfs[i].to_csv(urls[i]+".csv")
    #print(dfs[i])
 
table = pd.concat(dfs, axis=1, ignore_index=False, sort=False)
#print(table)
table.to_csv("stats.csv")
