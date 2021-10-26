
import csv
import scanner
import numpy as np
import pandas as pd
from pprint import pprint
import time
import scam_coins
import time
import asyncio
from dexguru_sdk import DexGuru

YOUR_API_KEY = 'EXeZ404OuO3dww0eRzESkPT77IORFvFiL33xRjwAXME'
BSC_CHAIN_ID = 56

sdk = DexGuru(api_key=YOUR_API_KEY)
#address = "0xcbd7142e42666132abe1f4c57996b2d5e8b0c9e2"
 


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
t0 = time.time()
url= "https://bscscan.com/tokentxns"
SCAMS = scam_coins.get_scam_addresses()

async def get_coin_data(address):
    data = await sdk.get_token_finance(BSC_CHAIN_ID,address)
    data_dict = {}
    for d in data:
        data_dict[d[0]] = d[1]
        
    return data_dict

async def main():
    count = {}
    t = 100
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
                    #g = await get_coin_data(i)
                    #print(g)
                    if i in SCAMS:
                        print("{}: SCAMMINO".format(i))
                        continue
                    if i in dfUpdate.index:
                        print("{}: sono li dentro".format(i))
                        dfUpdate.loc[i, "transactionInstant"] = d[i]["transactionInstant"]
                        dfUpdate.loc[i, "transactionHash"] = d[i]["transactionHash"]
                        dfUpdate.loc[i, "amount"] = dfUpdate.loc[i, "amount"] + d[i]["amount"]#*g["price_usd"]
                        dfUpdate.loc[i, "n-transactions"] += 1
                    else:
                        print("{}: non sono li dentro".format(i))
                        d[i]["n-transactions"] = 1
                        #d[i]["amount"] = d[i]["amount"]*g["price_usd"]
                        da_aggiungere = {i:d[i]}
                        dfDA = pd.DataFrame(data = da_aggiungere).T
                        dfUpdate = dfUpdate.append(dfDA)
                       
                dfUpdate.to_csv("shitcoins.csv")

try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # 'RuntimeError: There is no current event loop...'
    loop = None

if loop and loop.is_running():
    print('Async event loop already running. Adding coroutine to the event loop.')
    tsk = loop.create_task(main())
    # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
    # Optionally, a callback function can be executed when the coroutine completes
    tsk.add_done_callback(
        lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
else:
    print('Starting new event loop')
    asyncio.run(main())

#pprint(count)
columns = ("amount","coincode","n-transactions","transactionHash","transactionInstant")
t1 = time.time()
print(t1-t0)
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
    

