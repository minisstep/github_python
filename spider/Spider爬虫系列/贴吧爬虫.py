# -*- coding: utf-8 -*-
"""
Created on Wed May 10 22:26:21 2017
百度贴吧爬虫
王者荣耀爬虫
@author: kemi
"""

import requests 
import re
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import time, threading
session = requests.Session()

headers ={
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate, sdch",
"Accept-Language":"zh-CN,zh;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
#"Cookie":"TIEBA_USERTYPE=38124cb6c6fb306ccd167970; bdshare_firstime=1470839393334; __cfduid=de8377a1884e357ec45a64f43388e31e71489215624; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1490104212; BAIDUID=743B7DAE01232A134C7F965E88C69F8B:FG=1; BIDUPSID=743B7DAE01232A134C7F965E88C69F8B; PSTM=1493815557; FP_UID=d46b6ea345efa0b382e18c83b2bfaedf; BDUSS=EVpWXc5cy1ZWFlSbDVpV1h1aEVydFFJODg3cnJzVllHR2MtY1o1Uk4xS3ByenBaSUFBQUFBJCQAAAAAAAAAAAEAAAChi7ika2VtaXN0ZXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKkiE1mpIhNZd; STOKEN=ddf3f148290c24cd7bb2aa5c0c9f2b7655ac7143f6091dc3c802f0abf2beba9d; TIEBAUID=97d01c15f0a3c0487539ecc6; bottleBubble=1",
"Cookie":"TIEBA_USERTYPE=38124cb6c6fb306ccd167970; bdshare_firstime=1470839393334; __cfduid=de8377a1884e357ec45a64f43388e31e71489215624; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1490104212; FP_UID=d46b6ea345efa0b382e18c83b2bfaedf; TIEBAUID=97d01c15f0a3c0487539ecc6; re__f=%20www.google.com%2F; BAIDUID=50AC12B71C95337A165D1294D8F1B4AD:FG=1; BIDUPSID=50AC12B71C95337A165D1294D8F1B4AD; PSTM=1494941520; BDRCVFR[FuAjm1EhokC]=mk3SLVN4HKm; PSINO=1; H_PS_PSSID=1466_21116; _ga=GA1.2.1690506520.1494741663; _gid=GA1.2.655314876.1494941509; BDUSS=E10YVJlYlp1NHBWeTY3bVFYLS16OVU0UFpmMGhKVVFHcW51Q0ZrZ3Z4Nm5qRUpaSVFBQUFBJCQAAAAAAAAAAAEAAAChi7ika2VtaXN0ZXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKf~Glmn~xpZe; STOKEN=3027580569a5f5e018efdbd71ab08a8a979e9000c656b6308346131b51f47ccb; bottleBubble=1; 2763557793_FRSVideoUploadTip=1",
#"Cookie":"TIEBA_USERTYPE=38124cb6c6fb306ccd167970; bdshare_firstime=1470839393334; __cfduid=de8377a1884e357ec45a64f43388e31e71489215624; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1490104212; BAIDUID=743B7DAE01232A134C7F965E88C69F8B:FG=1; BIDUPSID=743B7DAE01232A134C7F965E88C69F8B; PSTM=1493815557; FP_UID=d46b6ea345efa0b382e18c83b2bfaedf; BDUSS=EVpWXc5cy1ZWFlSbDVpV1h1aEVydFFJODg3cnJzVllHR2MtY1o1Uk4xS3ByenBaSUFBQUFBJCQAAAAAAAAAAAEAAAChi7ika2VtaXN0ZXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKkiE1mpIhNZd; STOKEN=ddf3f148290c24cd7bb2aa5c0c9f2b7655ac7143f6091dc3c802f0abf2beba9d; TIEBAUID=97d01c15f0a3c0487539ecc6; bottleBubble=1",
"Host":"tieba.baidu.com",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}

def get_html(url):
    response = session.get(url,headers = headers)
    html = response.text
    if response.status_code == 200:
        soup = BeautifulSoup(html,'html.parser')
    else:
        #再加载一次
        time.sleep(1)
        response = session.get(url,headers = headers)
        html = response.text
        if response.status_code == 200:
            soup = BeautifulSoup(html,'html.parser')
        else:
            soup = None
            print('网页加载失败')
    return soup


def get_content(soup):
    items = soup.select('code#pagelet_html_frs-list/pagelet/thread_list')[0].string
    soup_items = BeautifulSoup(str(items),'lxml')
    collection = []
    
    for item in soup_items.select('li.j_thread_list.clearfix'):
        try:
            records = {}
            records['title'] = item.select('div.threadlist_lz.clearfix   div a.j_th_tit ')[0].get_text(strip=True)
            records['title_id'] = json.loads(item['data-field']).get('id',None)
            records['rep_num'] = item.select('div.col2_left.j_threadlist_li_left span.threadlist_rep_num.center_text')[0].get_text(strip=True)
            records['author'] = item.select('span.frs-author-name-wrap a.frs-author-name.j_user_card ')[0].get_text(strip=True)
            records['user_id'] = item.select('div > div > span.tb_icon_author ')[0]['data-field']
            records['create_time'] =item.select('div > div > span.pull-right.is_show_create_time ')[0].get_text(strip=True)
            records['replyer'] = item.select('div.threadlist_author.pull_right  span a.frs-author-name.j_user_card ')[0].get_text(strip=True)
            try:
                records['reply_date'] = item.select('div > div > span.threadlist_reply_date.pull_right.j_reply_data ')[0].get_text(strip=True)
            except:
                records['reply_date'] = None
            try:
                records['text'] = item.select('div.threadlist_detail.clearfix div  div.threadlist_abs.threadlist_abs_onlyline ')[0].get_text(strip=True)
            except:
                records['text'] = None
            collection.append(records)
        except:
            pass
    return collection
    
def insert_mongodb(posts):
    client = MongoClient('localhost', 27017)
    db = client.spider
    collection = db.tieba_xixiang
    try:
        result = collection.insert_many(posts)
    except:
        print('数据存入失败')
        result = None
    return(result)




    
def get_pageurl(soup):
    items = soup.select('code#pagelet_html_frs-list/pagelet/thread_list')[0].string
    soup_items = BeautifulSoup(str(items),'lxml')
    total_topic = soup_items.select('div.th_footer_l span:nth-of-type(1)')[0].get_text(strip=True)
    #total_note = soup_items.select('div.th_footer_l span:nth-of-type(2)')[0].get_text(strip=True)
    #total_number = soup_items.select('div.th_footer_l span:nth-of-type(3)')[0].get_text(strip=True)
    page_number = int(total_topic)/50
    #base_url = 'http://tieba.baidu.com/f?kw=%E8%A5%BF%E4%B9%A1&ie=utf-8&pn=50'
    url_list = []
    for i in range(int(page_number)):
        url = 'http://tieba.baidu.com/f?kw=%E8%A5%BF%E4%B9%A1&ie=utf-8&pn='
        page_url = url+str(i*50)
        url_list.append(page_url)
    return(url_list)


def get_pool(url):
    soup = get_html(url)
    posts = get_content(soup)
    insert_mongodb(posts)

if __name__ == '__main__':
    start_time = time.time()
    client = MongoClient('localhost', 27017)
    db = client.spider
    db.tieba_xixiang.remove()
    collection = db.tieba_xixiang
    url = 'http://tieba.baidu.com/f?ie=utf-8&kw=%E8%A5%BF%E4%B9%A1&red_tag=c2023221248'
    soup = get_html(url)
    url_list = get_pageurl(soup)
    pool_url = url_list[0:50]
    # 开8个 worker，没有参数时默认是 cpu 的核心数
    pool = ThreadPool(processes=8)
    # 在线程中执行 urllib2.urlopen(url) 并返回执行结果
    results2 = pool.map(get_pool, pool_url)
    pool.close()
    pool.join()
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))
    

if __name__ == "__main__":
    start_time = time.time() # 开始时间
    client = MongoClient('localhost', 27017)
    db = client.spider
    db.tieba_xixiang.remove()
    collection = db.tieba_xixiang
    url = 'http://tieba.baidu.com/f?ie=utf-8&kw=%E8%A5%BF%E4%B9%A1&red_tag=c2023221248'
    soup = get_html(url)
    url_list = get_pageurl(soup)
    posts = get_content(soup)
    insert_mongodb(posts)
    end_time = time.time() #结束时间
    print("程序耗时%f秒." % (end_time - start_time))


