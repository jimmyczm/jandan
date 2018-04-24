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
import pymongo
import re
import time


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser,10)

MAX_PAGE=100  #抓取的页面数

MONGO_URL = 'localhost'
MONGO_DB ='jandan'
MONGO_COLLECTION = 'duanzi0423'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page (page):
    url = 'http://jandan.net/duan/page-'+str(page)+'#comments'
    try:
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.commentlist ')))
        time.sleep(20)
        get_texts()
        print('正在获取页面')
    except TimeoutException:
        get_page (page)
    
def get_texts ():
#获取段子内容，id,ooxx数
    html = browser.page_source
    doc = bs(html,'lxml')
    items = doc(id = re.compile('comment-.*'))
    for item in items :
        if item('bad_content'):
            continue
        text ={
            'text':repr(item.p.string).replace('\\r\\n','').replace(' ','').replace('\'',''),
            'oo':int(item.find(class_ = 'tucao-like-container').span.get_text(strip=True)),
            'xx':int(item.find(class_ = 'tucao-unlike-container').span.get_text(strip=True))

        }
        print('正在保存',text)
        save(text)
                                
def save (result):
#保存到mongo
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('储存成功')
    except Exception:
        print('储存失败')
        
       
def main ():
#遍历页面
    for i  in range(1,MAX_PAGE+1):
        get_page(i)
    browser.close()

if __name__ == '__main__' :
    main()


    
        
        
    
    

