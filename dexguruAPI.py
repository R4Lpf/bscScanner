# =============================================================================
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
#   
# 
# GURU_KEY = ""
# 
# #url of the page we want to scrape
# url = "https://www.naukri.com/top-jobs-by-designations# desigtop600"
#   
# # initiating the webdriver. Parameter includes the path of the webdriver.
# driver = webdriver.Chrome('./chromedriver') 
# driver.get(url) 
#   
# # this is just to ensure that the page is loaded
# time.sleep(5) 
#   
# html = driver.page_source
#   
# # this renders the JS code and stores all
# # of the information in static HTML code.
#   
# # Now, we could simply apply bs4 to html variable
# soup = BeautifulSoup(html, "html.parser")
# all_divs = soup.find('div', {'id' : 'nameSearch'})
# job_profiles = all_divs.find_all('a')
#   
# # printing top ten job profiles
# count = 0
# for job_profile in job_profiles :
#     print(job_profile.text)
#     count = count + 1
#     if(count == 10) :
#         break
#   
# driver.close() # closing the webdriver
# 
# =============================================================================


"""
async get_token_finance(self, chain_id: int, token_address: str) -> dexguru_sdk.models.token_models.TokenFinanceModel
async get_tokens_finance(self, chain_id: int, token_addresses: List[str] = None, verified: bool = None, sort_by: str = None, limit: dexguru_sdk.sdk.dg_sdk.ConstrainedIntValue = 10, offset: dexguru_sdk.sdk.dg_sdk.ConstrainedIntValue = 0) -> dexguru_sdk.models.token_models.TokensFinanceListModel
"""

import asyncio
from dexguru_sdk import DexGuru
import pandas as pd
import time

# =============================================================================
# import signal
# from contextlib import contextmanager
# 
# class TimeoutException(Exception): pass
# 
# @contextmanager
# def time_limit(seconds):
#     def signal_handler(signum, frame):
#         raise TimeoutException("Timed out!")
#     signal.signal(signal.SIGALRM, signal_handler)
#     signal.alarm(seconds)
#     try:
#         yield
#     finally:
#         signal.alarm(0)
# =============================================================================

# =============================================================================
# try:
#     with time_limit(10):
#         long_function_call()
# except TimeoutException as e:
#     print("Timed out!")
# =============================================================================


t0 = time.time()

YOUR_API_KEY = ''
BSC_CHAIN_ID = 56

sdk = DexGuru(api_key=YOUR_API_KEY)
#address = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
addr = ["0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c","0x00e1656e45f18ec6747f5a8496fd39b50b38396d","0x04298a8062daaa53d4f8a2f7df0e02e97e17b492","0x93300d53cc51dc7fc15f3bf56c9fe541228d2dd0","0x0b7cfd1379e4a914be026461215010c577dbc64f"]
add = []
l = {}

dfUpdate = pd.read_csv("shitcoins.csv")
try:
    dfUpdate = dfUpdate.set_index("Unnamed: 0")
except:
    pass

# =============================================================================
# for i in dfUpdate.index:
#     add.append(i)
#     l[i] = {}
# =============================================================================

async def get_coin_data(address):
    try:
        #with time_limit(1):
        data = await asyncio.wait_for(sdk.get_token_finance(BSC_CHAIN_ID,address), timeout=1.0)
    except asyncio.TimeoutError:
        #print('timeout!')
        return 0, "timedout!!!"
    except: #TimeoutException as e:
        #print("Timed out!")
        return 0 # WHEN IT FAILS TO GET THE PRICE DATA, IT MEANS THERE'S NOTHING ON DEXGURU ABOUT IT AND NEITHER IN POOCOIN.
    data_dict = {}
    for d in data:
        data_dict[d[0]] = d[1]

    return data_dict


async def main(address_list,price_dict):
    print("Ha funzionato")
    
    for i in address_list:
        price_dict[i] = {}
        d = await get_coin_data(i)
        print("{0} price: {1}".format(i,d))
        price_dict[i]["price"] = d["price_usd"]
    t1 = time.time()
    return l, t1-t0
# =============================================================================
# print(main())
# print(tokenData(address))
# =============================================================================

try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # 'RuntimeError: There is no current event loop...'
    loop = None

if loop and loop.is_running():
    print('Async event loop already running. Adding coroutine to the event loop.')
    tsk = loop.create_task(main(addr,l))
    # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
    # Optionally, a callback function can be executed when the coroutine completes
    tsk.add_done_callback(
        lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
else:
    print('Starting new event loop')
    asyncio.run(main(addr,l))

# =============================================================================
# if __name__ == '__main__':
#     asyncio.run(main())
# 
# =============================================================================
# =============================================================================
# from bs4 import BeautifulSoup as bs
# from urllib.request import Request, urlopen
# from pprint import pprint as pp
# import scam_coins
# import time
# from ghost import Ghost
# 
# 
# address = "0x5dd1e31e1a0e2e077ac98d2a4b781f418ca50387"
# url = "https://dex.guru/token/{}-bsc".format(address)
# url2 = "https://dex.guru/token/0x5dd1e31e1a0e2e077ac98d2a4b781f418ca50387-bsc"
# g = Ghost()
# with g.start() as session:
#     session.open(url2)
#     print(session)
# =============================================================================
# =============================================================================
# 
# hdr = {'User-Agent': 'Mozilla/5.0'}
# req = Request(url,headers=hdr)
# #time.sleep(10)
# page = urlopen(req)
# time.sleep(10)
# soup = bs(page)
# div = soup.find_all("div")
# print(soup)
# print(div)
# =============================================================================



