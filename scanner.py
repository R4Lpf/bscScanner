"""
Initial JavaScript script used on the chrome extension: Custom JavaScript for Website 2.
The script made it so it hid all the coins with images so the "proper" coins so bscscan displayed only the rows with "coins"

  setTimeout(
     function() {
       const arra = []
       var cane = document.getElementsByTagName("tr")
       for(var i = 1; i < cane.length ; i++){
        var prova = cane[i].getElementsByTagName('img')[0].src
        var valore = cane[i].getElementsByTagName('a')[4].href
        if (prova != "https://bscscan.com/images/main/empty-token.png")
        {
          cane[i].style.display='none'
          console.log(valore)
        }
        if (arra.includes(valore))
        {
         cane[i].style.display='none'
        }
        arra.push(valore);
        }
     }, 1);
"""


from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen, FancyURLopener
from pprint import pprint as pp
import scam_coins
import asyncio
from dexguru_sdk import DexGuru

YOUR_API_KEY = 'EXeZ404OuO3dww0eRzESkPT77IORFvFiL33xRjwAXME'
BSC_CHAIN_ID = 56

sdk = DexGuru(api_key=YOUR_API_KEY)

url = "https://bscscan.com/tokentxns"
scam_url = "https://tokensniffer.com/tokens/scam"

try:
    SCAMS = scam_coins.get_scam_addresses()
except:
    SCAMS = []

with open("blacklist.txt", "r+") as file:
    blacklist = file.read().split("\n")

headers = {'User-Agent': 'Mozilla/5.0'}
req = Request(url, headers=headers)
page = urlopen(req)
soup = bs(page)

#print(soup.text)


coins = {} # every coinName : {Address:..., N-Transactions:..., LastTransactionIstance:...}



whitelist = "/images/main/empty-token.png"


print("---------------------------------------------")
print("")
print("_____________________________________________")

# =============================================================================
# #THIS TESTED WHICH WAS FASTER BETWEEN .find("table") and .table
# #NO SIGNIFICANT DIFFERENCE WAS FOUND BUT .find TENDS TO BE FASTER IN THIS CASE (3-7% faster)
# ipmort time
# w = [0,0]
# for i in range(10000):
#     t0 = time.time()
#     soup.find("table").find("tbody")
#     t1 = time.time()
#     soup.table.tbody
#     t2 = time.time()
#     print(i)
#     a = t1-t0
#     b = t2-t1
#     if a<b:
#         print("soup.find('table') WINS")
#         w[0] = w[0]+1
#     elif a>b:
#         print("soup.table WINS")
#         w[1] = w[1]+1
#     else:
#         print("TIE")
# print(w)   
# 
# =============================================================================

# =============================================================================
# rows = soup.find("table").find("tbody").find_all("tr")
# for row in rows:
#     info = row.find_all("td")
#     for i in range(len(info)):
#         print("---------------------------------------------")
#         print(i)
#         print(info[i])
#         print("_____________________________________________")
#     txnHash = info[1].text.strip()
#     amount = info[7].text.strip()
#     time = info[2].text.strip()
#     coincode = info[-1].text.strip()
#     address = info[-1].find("a")["href"].split("/")[-1]
#     img = info[-1].find("img")["src"]
#     if img == whitelist:
#         coins[address] = {}
#         coins[address]["coincode"] = coincode
#         coins[address]["transaction-instant"] = time
#         try:
#             coins[address]["n-transactions"]+=1
#         except:
#             coins[address]["n-transactions"]=1
# pp(coins)
# =============================================================================

# =============================================================================
# def coinCode(address):
#     url = "https://bscscan.com/token/{}".format(address)
#     hdr = {'User-Agent': 'Mozilla/5.0'}
#     req = Request(url,headers=hdr)
#     page = urlopen(req)
#     soup = bs(page)
#     coincode = soup.find("span",{"class":"text-secondary small"}).text.strip()
#     code = soup.find("div",{"class":"col-md-8 font-weight-medium"}).find("b").text.strip()
#     return coincode + "({})".format(code)
# =============================================================================


async def get_coin_data(address):
    try:
        #with time_limit(1):
        data = await asyncio.wait_for(sdk.get_token_finance(BSC_CHAIN_ID,address), timeout=1.0)
    except asyncio.TimeoutError:
        #print('timeout!')
        return -2,-2,-2
    except: #TimeoutException as e:
        #print("Timed out!")
        return -1,-1,-1 # WHEN IT FAILS TO GET THE PRICE DATA, IT MEANS THERE'S NOTHING ON DEXGURU ABOUT IT AND NEITHER IN POOCOIN.
    data_dict = {}
    for d in data:
        data_dict[d[0]] = d[1]

    return data_dict["price_usd"],data_dict["volume_24h_usd"],data_dict["liquidity_usd"],


def rows(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = bs(page)
    table = soup.find("table")
    if table != None:
        tbody = table.find("tbody")
        if tbody != None:
            r = tbody.find_all("tr")
            if r != None:
                return r

#scams = rows(scam_url)

async def markingCoins(row): #async 
    info = row.find_all("td")
    img = info[-1].find("img")["src"]
    address = info[-1].find("a")["href"].split("/")[-1]
    txnHash = info[1].text.strip()
    amount = info[7].text.strip()
    time = info[2].text.strip()
    coincode = info[-1].text.strip()
    if img == whitelist and address not in SCAMS and coincode != "()" and address not in blacklist: #and scam_coins.isAScam(address) == False  THIS WAS WITH ASYNC and price != -1
        #differentiated data in each row
        try:
            price,volume,pool = await asyncio.wait_for(get_coin_data(address), timeout=1.0)
            #print(price)
        except asyncio.TimeoutError:
            price,volume,pool = -2,-2,-2
        if price > -1 and volume>1 and pool>1 and volume < 500000 and pool < 10000 and price<1:
            return address, coincode, time, txnHash, amount, price, volume, pool 
    
# =============================================================================
# async def boh():
#     r = rows(url)
#     if r is None:
#         return 0
#     elif r is not None:
#         for row in r:
#             if await markingCoins(row) != None:
#                 address, coincode, time, txnHash, amount, price = await markingCoins(row)
#                 print("{0}: amount= {1}, price = {2}".format(address,amount,price))
# =============================================================================
    
async def fillDictionary(coins: dict()): #async
    r = rows(url)
    if r is None:
        return 0
    elif r is not None:
        for row in r:
            try:
                mark = await asyncio.wait_for(markingCoins(row), timeout=1.0)
                #print(mark)
            except asyncio.TimeoutError:
                mark = None
            if mark != None: #await 
                address = mark[0]
                coincode = mark[1]
                time = mark[2]
                txnHash = mark[3]
                amount = mark[4]
                price = mark[5]
                volume = mark[6]
                pool = mark[7]
                #address, coincode, time, txnHash, amount, price = await markingCoins(row) #await
    # =============================================================================
    #                 try:
    #                     g = await get_coin_data(address)
    #                 except:
    #                     g = 0
    # =============================================================================
                coins[address] = {}
                coins[address]["coincode"] = coincode
                coins[address]["transactionInstant"] = time
                coins[address]["transactionHash"] = txnHash
                coins[address]["amount"] = float(amount.replace(",",""))
                #coins[address]["amount_usd"] = float(amount.replace(",","")) * price
                coins[address]["price"] = price
                coins[address]["amount_usd"] = float(amount.replace(",","")) * price
                coins[address]["n-transactions"] = 1
                coins[address]["volume"] = volume
                coins[address]["pool_usd"] = pool
        return coins
    else: return 0


# =============================================================================
# try:
#     loop = asyncio.get_running_loop()
# except RuntimeError:  # 'RuntimeError: There is no current event loop...'
#     loop = None
# 
# if loop and loop.is_running():
#     print('Async event loop already running. Adding coroutine to the event loop.')
#     tsk = loop.create_task(fillDictionary({}))
#     # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
#     # Optionally, a callback function can be executed when the coroutine completes
#     tsk.add_done_callback(
#         lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
# else:
#     print('Starting new event loop')
#     asyncio.run(fillDictionary({}))
# 
# #print(fillDictionary(coins))
# 
# =============================================================================



# =============================================================================
# table = soup.table
# tbody = table.tbody
# tds = []
# for tr in tbody:
#     print("---------------------------------------------")
#     trr = tbody.tr
#     print(trr)
#     print("_____________________________________________")
#     print(type(trr))
# 
# =============================================================================
#print(tds)

# =============================================================================
# table = soup.find("tbody")
# 
# for i in table:
#     print("---------------------------------------------")
#     print(i)
#     i.name = "img"
#     print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
#     for td in i:
#         print("TDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTD")
#         token_address = td.find("a")
#         image = td.find("img")
#         print(token_address)
#         print(image)
#         print("TDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTDTD")
#     print("_____________________________________________")
# =============================================================================


#print(coins)


"""
for i,currency in enumerate(a):
    name = currency.find("a").attrs['href'].replace("/currencies/","").replace("/","").replace("-"," ").upper()
    price = currency.findAll("td")[-3].get_text(strip=True)
    marketcap = currency.findAll("td")[-1].get_text(strip=True)
    top_29[i+1] = {"Name":name,"Coin price: ":price,"Market Cap: ":marketcap}
    print("Place: ", i+1)
    print("Name: ",name)
    print("Coin price: ",price)
    print("Market Cap: ",marketcap)
    print("----------------")
"""

"""
FIRST IDEA CREATE ANOTHER WEBSITE WITH THE SCRAPPED COINS BUT I THINK IS USELESS USING FLASK FOR EASY CGI OPERATIONS

using flask library in Python you can achieve that. remember to store your HTML page to a folder named "templates" inside where you are running your python script.

so your folder would look like

templates (folder which would contain your HTML file)
your python script
this is a small example of your python script. This simply checks for plagiarism.

from flask import Flask
from flask import request
from flask import render_template
import stringComparison

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("my-form.html") # this should be the name of your html file

@app.route('/', methods=['POST'])
def my_form_post():
    text1 = request.form['text1']
    text2 = request.form['text2']
    plagiarismPercent = stringComparison.extremelySimplePlagiarismChecker(text1,text2)
    if plagiarismPercent > 50 :
        return "<h1>Plagiarism Detected !</h1>"
    else :
        return "<h1>No Plagiarism Detected !</h1>"

if __name__ == '__main__':
    app.run()
This a small template of HTML file that is used

<!DOCTYPE html>
<html lang="en">
<body>
    <h1>Enter the texts to be compared</h1>
    <form action="." method="POST">
        <input type="text" name="text1">
        <input type="text" name="text2">
        <input type="submit" name="my-form" value="Check !">
    </form>
</body>
</html>
"""