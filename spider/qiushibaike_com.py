# -*- coding: utf-8 -*-
"""
Created on Sun May  7 15:35:35 2017
糗事百科热门 下载
@author: kemi
"""

import requests 
import re
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
session = requests.Session()

headers = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, sdch, br",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Cookie":"_xsrf=2|c1b13e58|26b36330fe840be167395ad8376785ed|1494142469; _qqq_uuid_=2|1:0|10:1494142469|10:_qqq_uuid_|56:YmVlN2ZiOGMzNDBhNDk2Nzc0NDZiMGVjNWEyMWNmYjYxN2M5ZDgzMQ==|f957c76e32c0a68abca5f0af51f7f80adab0c80253f6da8c1dcbf9838bf9472e; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1494142467; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1494142503; _ga=GA1.2.458760632.1481815116; _gid=GA1.2.736547038.1494142503",
"Host":"www.qiushibaike.com",
"If-None-Match":"e12ccac4431536d5bd7ca9d80c0286ffcb79c936",
"Referer":"https://www.qiushibaike.com/",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}



def get_html_loop(url,loop = 10):
    try:
        for i in range(loop):
            response = session.get(url,headers = headers)
            html = response.text
            if response.status_code == 200:
                soup = BeautifulSoup(html,'lxml')
                break
            else:
                continue
                print('网页重新加载'+str(i))
                time.sleep(1)
    except:
         print('网页加载失败')
         soup = None
    print(response.status_code)
    return soup

def get_content(soup):
    collection = []
    try:
        items_content = soup.select('div.article.block.untagged.mb15')
        for item in items_content:
            content = item.select('div.content span')[0].text
            stats_vote = item.select('span.stats-vote')[0].text
            stats = re.findall('\d+',stats_vote)[0]
            try:
                comments = item.select('span.stats-comments a i.number')[0].text
            except:
                comments = 0
            author  = item.select('div.author.clearfix h2 ')[0].text
            record  = {"content":content,"stats":stats,"comments":comments,
            "author":author,'datetime':str(datetime.now())}
            collection.append(record)
    except:
        print('解析失败')
    return(collection)
    
def insert_mongodb(posts):
    client = MongoClient('67.216.204.220', 27017)
    db = client.spider
    douban = db.qiushibaike_com
    try:
        result = douban.insert_many(posts)
    except:
        print('数据存入失败')
        result = None
    return(result)



if __name__ == "__main__":
    start_time = time.time() # 开始时间
    url = 'https://www.qiushibaike.com/'
    try:
        soup = get_html_loop(url,loop = 10)
        page_numbers = soup.select('span.page-numbers')[-1].get_text(strip= True)
        for page_number in range(1,int(page_numbers)+1):
            url_base = 'https://www.qiushibaike.com/8hr/page/'
            url = url_base+str(page_number)
            print(url)
            soup = get_html_loop(url)
            records = get_content(soup)
            insert_mongodb(records)
    except:
        print('程序出错')
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))

