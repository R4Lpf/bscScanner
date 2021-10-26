from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from pprint import pprint as pp



scam_url= "https://tokensniffer.com/tokens/scam"



# copied scanner function so i don't have a circular import.
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



def get_scam_addresses():
    scams = rows(scam_url)
    s = set()
    for row in scams:
        scam_address = row.find("a",{"class":"Home_address__2ERkX"}).text.strip()
        s.add(scam_address)
    return s

def isAScam(address):
    return address in get_scam_addresses()

# =============================================================================
# print(get_scam_addresses())
# print(isAScam("0xb3a6381070b1a15169dea646166ec0699fdaea79"))
# 
# =============================================================================
