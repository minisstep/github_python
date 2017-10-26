# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 21:25:19 2017
糗事百科爬虫
@author: kemi
"""
headers ={
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, sdch, br",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":'xsrf=2|8d5da784|e4a2c94d220b797489ede5b63bf518bf|1496756915; _qqq_uuid_="2|1:0|10:1496756915|10:_qqq_uuid_|56:ODgwN2FhY2U4YzIwOTBiZjQ1ZmEzYjQ0YzM0MDlhOTJhOTc1NDVkNA==|074de4576483db106c25f8dd461be6a0d8fd0349c75c77df6e4dc1829dd9d9b2"; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1496328276,1496756912; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1496756912; _ga=GA1.2.458760632.1481815116; _gid=GA1.2.915668028.1496756912; _gat=1',
"Host":"www.qiushibaike.com",
"If-None-Match":'"abc119486309409a4bb9ef8c517da4389e1636fc"',
"Referer":"https://www.google.com/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

import requests 
import re
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
session = requests.Session()

##网页下载
def get_html(url,loop = 10):
    try:
        for i in range(loop):
            response = session.get(url,headers = headers)
            if response.status_code == 200:
                html = response.text
                break
            else:
                continue
                print('网页重新加载'+str(i))
                time.sleep(1)
    except:
         print('网页加载失败')
         html = None
    print(response.status_code)
    return html
    
if __name__ == "__main__":
    start_time = time.time() # 开始时间
    url ="https://www.qiushibaike.com/"
    html = get_html(url)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))
    
#网页解析 -----beautifulSoup
def get_content_bysoup(html):
    soup = BeautifulSoup(html,'lxml')
    collection = []
    try:
        items_content = soup.select('div.article.block.untagged.mb15')
        for item in items_content:
            record ={}
            record['content'] = item.select('div.content span')[0].text
            record['stats_vote'] = item.select('span.stats-vote')[0].text
            record['stats'] = re.findall('\d+',item.select('span.stats-vote')[0].text)[0]
            try:
                record['comments'] = item.select('span.stats-comments a i.number')[0].text
            except:
                record['comments'] = 0
            record['author']  = item.select('div.author.clearfix h2 ')[0].text
            collection.append(record)
    except:
        print('解析失败')
    return(collection)


 
#网页解析-----pyjquery
from pyquery import PyQuery as pq
def get_content_bypyquery(html): 
    doc = pq(html)
    collection = []
    items_content = doc.items("div.article.block.untagged.mb15")
    try:
        for item in items_content:
            record ={}
            record['content'] = item("div.content span").text()
            record['stats_vote'] = item('span.stats-vote').text()
            record['stats'] = re.findall('\d+',item('span.stats-vote').text())[0]
            try:
                record['comments'] = item('span.stats-comments a i.number').text()
            except:
                record['comments'] = 0    
            record['author']  = item('div.author.clearfix h2 ').text()
            collection.append(record)
    except:
        print('解析失败')
    return(collection)        

       
       
if __name__ == "__main__":
    start_time = time.time() # 开始时间
    url ="https://www.qiushibaike.com/"
    html = get_html(url)
    collection_soup = get_content_bysoup(html)
    collection_pq = get_content_bysoup(html)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time)) 



    