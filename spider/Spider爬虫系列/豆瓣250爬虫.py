# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests 
import re
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
session = requests.Session()
headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, sdch, br",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Host":"movie.douban.com",
"Referer":"https://www.google.com/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}


def get_html(url):
    response = session.get(url,headers=headers)
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    
    return soup


def get_items(soup):
    collection = []
    items = soup.select('ol.grid_view > li')
    try:
        for item in items:
            title = item.select('span.title')[0].text
            actor = item.select('div.bd p.')[0].get_text(strip=True)
            year = re.findall(r'[0-9]{4}',actor)[0]
            star = item.select('div.star span.rating_num')[0].get_text(strip=True)
            coupon = item.select('div.star span')[3].get_text(strip=True)
            people = re.findall(r'\d*',coupon)[0]
            try:
                quote = item.select('p.quote span.inq')[0].get_text(strip=True)
            except:
                quote = None
            movie ={'title':title,'actor':actor,'yaer':year,'star':star,
                   'people':people,'quote':quote}
            #print(movie)
            collection.append(movie)
    except:
        print('解析失败')
    
    return(collection)

def insert_mongodb(posts):
    client = MongoClient('localhost', 27017)
    db = client.spider
    douban = db.douban
    result = douban.insert_many(posts)
    return(result)
    

if __name__ == "__main__":
    # 删除mongo数据及
    #db.douban.remove()
    start_time = time.time() # 开始时间
    url = 'https://movie.douban.com/top250'
    page_number = 10   
    for number in range(page_number):
        url = 'https://movie.douban.com/top250'
        payload = {'start':number*25}
        response = session.get(url, params=payload)
        url = response.url
        soup = get_html(url)
        items = get_items(soup)
        insert_mongodb(items)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))
