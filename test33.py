#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io  
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
from pyquery import  PyQuery as pq
import pymongo
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser,3)


page = 90
url = 'http://jandan.net/duan/page-'+str(page)+'#comments'

MONGO_URL = 'localhost'
MONGO_DB ='jandan'
MONGO_COLLECTION = 'duanzi0419'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


browser.get(url)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.commentlist ')))
html = browser.page_source
doc = pq(html)
#print(doc)
#doc =bs(html,'lxml')
items = doc('#comments .commentlist').items()
#print(items)

for item in items :
    text={
    'id':item.find( '.righttext').text()

    
    }
    print(text)
                          

