#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io  
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import  PyQuery as pq
import pymongo
import time


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome()

MAX_PAGE=5

MONGO_URL = 'localhost'
MONGO_DB ='jandan'
MONGO_COLLECTION = 'duanzi0419'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_page (page):
    url = 'http://jandan.net/duan/page-'+str(page)+'#comments'
    try:
        browser.get(url)
        #print(browser.page_source)
        time.sleep(2)
        get_texts()
        print('正在获取源代码')
    except TimeoutException:
        get_page (page)
    
def get_texts ():
#获取段子内容，id,ooxx数
    html = browser.page_source
    doc = pq(html)
    items = doc('li').items()
    for item in items :
        text ={
        'id':item.find('href').text(),
        'duanzi': item.find('p').text(),
        'oo': item.find('tucao-like-container').text(),
        'xx': item.find('tucao-unlike-container').text()
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
#需要遍历的页面
    for i  in range(1,MAX_PAGE+1):
        get_page(i)
    browser.close()

if __name__ == '__main__' :
    main()


    
        
        
    
    

