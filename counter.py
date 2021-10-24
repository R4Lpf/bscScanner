
import csv
import scanner
import pandas as pd
from pprint import pprint


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

csv_file = csv.writer(open("shitcoins.csv", "w"))
csv_file.writerow(["Name", "Address","N-Transactions","LastTransactionIstance"]) # Write column headers as the first line

url= "https://bscscan.com/tokentxns"

ccoins = {}
count = {}
t = 100
for i in range(t):
    d = scanner.fillDictionary(ccoins)
    print(i,d)
    if d == 0 or d == None or type(d) == type(None):
        pass
    #print(i,d)   qui la funzione fillDictionary ritornava solo se rows(url) era un NoneType o no
    #print(d)
    else:
        if type(d) != type(None):
            for k in d:
# =============================================================================
#                 print(k)
#                 print(d[k])
# =============================================================================
                if k not in count:
                    count[k] = d[k]
                    count[k]["n-transactions"] = 1
                else:
                    if count[k]["transactionInstant"] != d[k]["transactionInstant"] or count[k]["transactionHash"] != d[k]["transactionHash"]:
                        count[k]["n-transactions"] += 1
                    else:
                        continue


#pprint(count)
columns = ("amount","coincode","n-transactions","transactionHash","transactionInstant")

# =============================================================================
# #used this to create the file for the first time
# df = pd.DataFrame(data=count).T
# df.to_csv('shitcoins.csv')
# print(df)
# =============================================================================
