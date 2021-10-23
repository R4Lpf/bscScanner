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


from datetime import datetime,date 
from bs4 import BeautifulSoup as bs
#import time
import csv 
from urllib.request import Request, urlopen

site= "https://bscscan.com/tokentxns"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = bs(page)
#print(soup.text)

csv_file = csv.writer(open("shitcoins.csv", "w"))
csv_file.writerow(["Name", "Address","N-Transactions","LastTransactionIstance"]) # Write column headers as the first line


shitcoins = soup.find("tbody")

for i in shitcoins:
    print("---------------------------------------------")
    print(i)
    print("_____________________________________________")

coins = {} # every coinName : {Address:..., N-Transactions:..., LastTransactionIstance:...}

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