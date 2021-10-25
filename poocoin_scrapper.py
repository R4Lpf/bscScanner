# =============================================================================
# 
# from bs4 import BeautifulSoup as bs
# from urllib.request import Request, urlopen
# from pprint import pprint as pp
# import requests
# 
# 
# url= "https://poocoin.app/tokens/0xcbd7142e42666132abe1f4c57996b2d5e8b0c9e2"
# 
# 
# hdr = {'User-Agent': 'Mozilla/5.0'}
# req = Request(url,headers=hdr)
# page = urlopen(req)
# soup = bs(page)
# 
# root = soup.find("div",{"id":"root"})
# print(root)
# 
# =============================================================================

from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pyvirtualdisplay import Display
#import telegram_send
#from api.constants import *

coin_address = '0xcbd7142e42666132abe1f4c57996b2d5e8b0c9e2'


def scraping(url):
# =============================================================================
#     display = Display(visible=0, size=(1200, 1200))
#     display.start()
# =============================================================================
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-plugins-discovery")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.delete_all_cookies()
    driver.get(url)

    time.sleep(5)  # 5 seconds
    html = driver.page_source
# =============================================================================
#     display.stop()
# =============================================================================

    return BeautifulSoup(html, 'lxml')

# Get Html
page = scraping("https://poocoin.app/tokens/" + coin_address)
print(page)
# Extract price as str
prices = page.find_all("span", class_="text-success")
# the element position always changes
price = prices[7].getText()
print(price)
# =============================================================================
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import time
# from pyvirtualdisplay import Display
# 
# 
# url = "https://poocoin.app/tokens/0xcbd7142e42666132abe1f4c57996b2d5e8b0c9e2"
# coin_address = '0xcbd7142e42666132abe1f4c57996b2d5e8b0c9e2'
# 
# 
# def scraping(url):
#     display = Display(visible=0, size=(1200, 1200))
#     display.start()
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--disable-extensions')
#     chrome_options.add_argument('--profile-directory=Default')
#     chrome_options.add_argument("--incognito")
#     chrome_options.add_argument("--disable-plugins-discovery")
#     chrome_driver_dir = "/chrome_driver/chromedriver.exe"
#     driver = webdriver.Chrome(executable_path=chrome_driver_dir, options=chrome_options)
#     driver.delete_all_cookies()
#     driver.get(url)
# 
#     time.sleep(5)  # 5 seconds
#     html = driver.page_source
#     display.stop()
# 
#     return BeautifulSoup(html, 'lxml')
# 
# # Get Html
# page = scraping("https://poocoin.app/tokens/" + coin_address)
# 
# # Extract price as str
# prices = page.find_all("span", class_="text-success")
# # the element position always changes
# price = prices[7].getText()
# print(price)
#     
# =============================================================================



# =============================================================================
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from time import sleep
# 
# s=Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=s)
# driver.maximize_window()
# driver.get('https://www.google.com')
# driver.find_element(By.NAME, 'q').send_keys('Yasser Khalil')
# 
# # create object for chrome options
# chrome_options = Options()
# base_url = "https://poocoin.app/tokens/0xcbd7142e42666132abe1f4c57996b2d5e8b0c9e2"
# 
# chrome_options.add_argument('disable-notifications')
# chrome_options.add_argument('--disable-infobars')
# chrome_options.add_argument('start-maximized')
# chrome_options.add_argument("--headless")
# # To disable the message, "Chrome is being controlled by automated test software"
# chrome_options.add_argument("disable-infobars")
# # Pass the argument 1 to allow and 2 to block
# chrome_options.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 2
#     })
# # invoke the webdriver
# browser = webdriver.Chrome(executable_path = 'chrome_driver/chromedriver.exe',
#                           options = chrome_options)
# browser.get(base_url)
# 
# html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
# browser.close()
# soup = BeautifulSoup(html, "html.parser")
# 
# =============================================================================

