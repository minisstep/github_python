# -*- coding: utf-8 -*-
"""
Created on Thu May 25 22:28:50 2017
知乎爬虫应用
@author: kemi
"""

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
import time

headers ={
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, sdch, br",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Host":"www.zhihu.com",
"Referer":"https://www.zhihu.com/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
} 




def get_cookie(account,password):
    path_chromedeiver = 'C:\\Program Files (x86)\\Google\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(path_chromedeiver)
    driver.get("https://www.zhihu.com/#signin")
    account ='minisstep@163.com'
    password ='kemi0618'
    ##网站已经记住密码了，不需要再登录了
    driver.find_element_by_css_selector('div.account.input-wrapper input').send_keys(account)
    driver.find_element_by_css_selector('div.verification.input-wrapper input').send_keys(password)
    driver.find_element_by_css_selector('div.button-wrapper.command button.sign-button.submit').click()
    time.sleep(5)
    try:
        driver.find_element_by_css_selector('#zh-top-nav-explore > a').text
        cookies = driver.get_cookies()
    except:
        cookies =None
        print('cookie加载失败')
    return cookies    


def get_html(url,cookies):
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get(url,headers=headers)   
    html = response.text
    if response.status_code == 200:
        soup = BeautifulSoup(html,'lxml')
    else:
        #再加载一次
        time.sleep(1)
        response = session.get(url,headers = headers)
        html = response.text
        if response.status_code == 200:
            soup = BeautifulSoup(html,'lxml')
        else:
            soup = None
            print('网页加载失败')
    return soup
#----------------------------------------------
if __name__ == '__main__':
    account ='minisstep@163.com'
    password ='kemi0618'
    cookies = get_cookie(account,password)
    url = 'https://www.zhihu.com/topic' 
    soup = get_html(url,cookies)
#----------------------------------------------
#----------------------------------------------
#----------------------------------------------
    
def get_content(soup):   
    collection = []
    items = soup.select('div h2 a') 
    try:
        for item in items:
            records = {}
            records['href'] = item['href']
            try:
                records['data_id'] = item['data-id']
            except:
                records['data_id'] = None
            records['title'] = item.get_text(strip=True)
            collection.append(records)
    except:
        print('内容解析失败')
    return collection
        
def insert_mongodb(posts):
    client = MongoClient('localhost', 27017)
    db = client.spider
    collection = db.zhihu
    try:
        result = collection.insert_many(posts)
    except:
        print('数据存入失败')
        result = None
    return(result)
    
if __name__ == '__main__':
    account ='minisstep@163.com'
    password ='kemi0618'
    cookies = get_cookie(account,password)
    url = 'https://www.zhihu.com/explore' 
    soup = get_html(url,cookies)       
    collection = get_content(soup)
    insert_mongodb(collection)
    
#-----------------------------------------------------------------
