
import csv
import scanner
import numpy as np
import pandas as pd
from pprint import pprint
import time


"""
TO PUT DATA INTO CSV

from bs4 import BeautifulSoup
import csv 
import urllib.request as urllib2

url="http://www.conakat.com/states/ohio/cities/defiance/road_maps/"

page=urllib2.urlopen(url)

soup = BeautifulSoup(page.read())

f = csv.writer(open("Defiance Steets1.csv", "w"))
f.writerow(["Name", "ZipCodes"]) # Write column headers as the first line

links = soup.find_all('a')

for link in links:
    i = link.find_next_sibling('i')
    if getattr(i, 'name', None):
        a, i = link.string, i.string
        f.writerow([a, i])
"""

# =============================================================================
# csv_file = csv.writer(open("shitcoins.csv", "w"))
# csv_file.writerow(["Name", "Address","N-Transactions","LastTransactionIstance"]) # Write column headers as the first line
# =============================================================================

url= "https://bscscan.com/tokentxns"


count = {}
t = 1000
for i in range(t):
    time.sleep(1)
    mostbought_coins = []
    try:
        d = scanner.fillDictionary({})
    except:
        d = 0
    print(i,d)
    if d == 0 or d == None or type(d) == type(None):
        pass
    #print(i,d)   qui la funzione fillDictionary ritornava solo se rows(url) era un NoneType o no
    #print(d)
    else:
        if type(d) != type(None):
            try:
                dfUpdate = pd.read_csv("shitcoins.csv")
            except:
               dfUpdate = pd.DataFrame(data=d).T
               dfUpdate.to_csv("shitcoins.csv")  
               
            dfUpdate = pd.read_csv("shitcoins.csv")
            try:
                dfUpdate = dfUpdate.set_index("Unnamed: 0")
            except:
                continue
            for i in d:
               if i in dfUpdate.index:
                   print("{}: sono li dentro".format(i))
                   dfUpdate.loc[i, "transactionInstant"] = d[i]["transactionInstant"]
                   dfUpdate.loc[i, "transactionHash"] = d[i]["transactionHash"]
                   dfUpdate.loc[i, "amount"] = dfUpdate.loc[i, "amount"] + d[i]["amount"]
                   dfUpdate.loc[i, "n-transactions"] += 1
               else:
                   print("{}: non sono li dentro".format(i))
                   d[i]["n-transactions"] = 1
                   da_aggiungere = {i:d[i]}
                   dfDA = pd.DataFrame(data = da_aggiungere).T
                   dfUpdate = dfUpdate.append(dfDA)
                   
            dfUpdate.to_csv("shitcoins.csv")
# =============================================================================
#             for k in d:
# # =============================================================================
# #                 print(k)
# #                 print(d[k])
# # =============================================================================
#                 if k not in count:
#                     count[k] = d[k]
#                     count[k]["n-transactions"] = 1
#                 else:
#                     if count[k]["transactionInstant"] != d[k]["transactionInstant"] or count[k]["transactionHash"] != d[k]["transactionHash"]:
#                         count[k]["n-transactions"] += 1
#                     else:
#                         continue
# =============================================================================


#pprint(count)
columns = ("amount","coincode","n-transactions","transactionHash","transactionInstant")

# =============================================================================
# #used this to create the file for the first time
# df = pd.DataFrame(data=count).T
# df.to_csv('bruh2.csv')
# print(df)
# =============================================================================

# =============================================================================
# 
# try:
#     dfUpdate = pd.read_csv("shitcoins.csv")
# except:
#    dfUpdate = pd.DataFrame(data=count).T
#    dfUpdate.to_csv("shitcoins.csv")  
#    
# dfUpdate = pd.read_csv("shitcoins.csv")
# dfUpdate = dfUpdate.set_index("Unnamed: 0")
# for i in count:
#    if i in dfUpdate.index:
#        print("{}: sono li dentro".format(i))
#        dfUpdate.loc[dfUpdate["Unnamed: 0"] == i, "transactionInstant"] = count[i]["transactionInstant"]
#        dfUpdate.loc[dfUpdate["Unnamed: 0"] == i, "transactionHash"] = count[i]["transactionHash"]
#        dfUpdate.loc[dfUpdate["Unnamed: 0"] == i, "amount"] = count[i]["amount"]
#        dfUpdate.loc[dfUpdate["Unnamed: 0"] == i, "n-transactions"] += 1
#    else:
#        print("{}: non sono li dentro".format(i))
#        count[i]["n-transactions"] = 1
#        da_aggiungere = {i:count[i]}
#        dfDA = pd.DataFrame(data = da_aggiungere).T
#        dfUpdate = dfUpdate.append(dfDA)
#        
# dfUpdate.to_csv("shitcoins.csv")
# 
# =============================================================================

# =============================================================================
# 
# 
# present = {}
# 
# try:
#     dfUpdate = pd.read_csv("shitcoins.csv")
# except:
#     dfUpdate = pd.DataFrame(data=count).T
#     dfUpdate.to_csv("shitcoins.csv")
#     
# dfUpdate = pd.read_csv("shitcoins.csv")
# 
# for i,r in enumerate(dfUpdate["Unnamed: 0"]):
#     if r in count:
#         print("{}: sono li dentro".format(r))
#         dfUpdate.loc[i,["transactionInstant"]] = count[r]["transactionInstant"]
#         dfUpdate.loc[i,["transactionHash"]] = count[r]["transactionHash"]
#         dfUpdate.loc[i,["amount"]] = count[r]["amount"]
#         dfUpdate.loc[i,["n-transactions"]] = dfUpdate.loc[i,["n-transactions"]] + count[r]["n-transactions"]
#         present[r] = count[r]
#         
# rest = {k: count[k] for k in set(count)-set(present)}
# dfRest = pd.DataFrame(data = rest).T
# dfUpdate = dfUpdate.set_index("Unnamed: 0").append(dfRest)
# dfUpdate.to_csv("bruh2.csv")
# 
# =============================================================================
    

