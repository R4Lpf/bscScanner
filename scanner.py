"""
Initial JavaScript script used on the chrome extension: Custom JavaScript for Website 2.
The script made it so it hid all the coins with images so the "proper" coins so bscscan displayed only the rows with "shitcoins"

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
from urllib.request import Request, urlopen
from pprint import pprint as pp


url= "https://bscscan.com/tokentxns"


hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(url,headers=hdr)
page = urlopen(req)
soup = bs(page)

#print(soup.text)


coins = {} # every coinName : {Address:..., N-Transactions:..., LastTransactionIstance:...}



whitelist = "/images/main/empty-token.png"


print("---------------------------------------------")
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
            

def markingCoins(row):
    info = row.find_all("td")
    #differentiated data in each row
    txnHash = info[1].text.strip()
    amount = info[7].text.strip()
    time = info[2].text.strip()
    coincode = info[-1].text.strip()
    address = info[-1].find("a")["href"].split("/")[-1]
    img = info[-1].find("img")["src"]
    if img == whitelist:
       return address, coincode, time, txnHash, amount
    
def fillDictionary(coins: dict()):
    r = rows(url)
    if r is None:
        return 0
    elif r is not None:
        for row in rows(url):
            if markingCoins(row) != None:
                address, coincode, time, txnHash, amount = markingCoins(row)
                coins[address] = {}
                coins[address]["coincode"] = coincode
                coins[address]["transactionInstant"] = time
                coins[address]["transactionHash"] = txnHash
                coins[address]["amount"] = amount
        return coins
    else: return 0


#print(fillDictionary(coins))




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


#print(shitcoins)


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