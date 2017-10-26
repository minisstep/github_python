# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 21:40:06 2017
爬去豆瓣视频
@author: kemi
"""
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
chromedriver ='C:\\chromedriver_win32\\chromedriver.exe'

os.environ["webdriver.chrome.driver"] = chromedriver
#path ='C:\\chromedriver_win32'
browser = webdriver.Chrome(chromedriver)
url = 'https://movie.douban.com/tag/%E7%88%B1%E6%83%85'

browser.get(url)

title_tags  = browser.find_element_by_css_selector('div#wrapper div#content h1 ' ).text

#爬去单个页面信息
gather = browser.find_elements_by_css_selector('#content > div > div.article > div:nth-child(3) > table')

df =  pd.DataFrame([],columns= ['title','content','star','coupon'])
for item in gather:
    title =item.find_element_by_css_selector('tbody >tr > td>div>a').text
    content = item.find_element_by_css_selector('tbody >tr > td>div.pl2>p.pl').text
    star = item.find_element_by_css_selector('tbody >tr > td>div.pl2>div.star.clearfix>span.rating_nums').text
    coupon = item.find_element_by_css_selector('tbody >tr > td>div.pl2>div.star.clearfix>span.pl').text
    
    temp = pd.DataFrame({'title':[title],'content':[content],'star':[star],'coupon':[coupon]})

    df = pd.concat([temp,df])

#爬去所有页面信息
url = 'https://movie.douban.com/tag/%E7%88%B1%E6%83%85'
browser.get(url)
df =  pd.DataFrame([],columns= ['title','content','star','coupon'])
n=0
try:
    for i in range(391):
        browser.find_element_by_css_selector('#content > div > div.article > div.paginator > span.next').click()
        gather = browser.find_elements_by_css_selector('#content > div > div.article > div:nth-child(3) > table')
        for item in gather:
            title =item.find_element_by_css_selector('tbody >tr > td>div>a').text
            content = item.find_element_by_css_selector('tbody >tr > td>div.pl2>p.pl').text
            star = item.find_element_by_css_selector('tbody >tr > td>div.pl2>div.star.clearfix>span.rating_nums').text
            coupon = item.find_element_by_css_selector('tbody >tr > td>div.pl2>div.star.clearfix>span.pl').text
            temp = pd.DataFrame({'title':[title],'content':[content],'star':[star],'coupon':[coupon]})
            df = pd.concat([temp,df])
        n=n+1
        print('第'+str(n)+'页')
        time.sleep(1)
except:
    print('错误')
    

df.count()    
    
    


browser.find_element_by_css_selector('#content > div > div.article > div.paginator > span.thispage').text



browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[3]/span[3]').text

browser.find_element_by_css_selector('#content > div > div.article > div.paginator > span.next').text



















title = browser.find_element_by_css_selector('#content > div > div.article > div:nth-child(3) > table:nth-child(2) > tbody > tr > td:nth-child(2) > div > a ').text

content  = browser.find_element_by_css_selector('#content > div > div.article > div:nth-child(3) > table:nth-child(2) > tbody > tr > td:nth-child(2) > div > p').text

star  = browser.find_element_by_css_selector('#content > div > div.article > div:nth-child(3) > table:nth-child(2) > tbody > tr > td:nth-child(2) > div > div > span.rating_nums').text

coupon = browser.find_element_by_css_selector('#content > div > div.article > div:nth-child(3) > table:nth-child(2) > tbody > tr > td:nth-child(2) > div > div > span.pl').text


gather  = browser.find_elements_by_css_selector('#content > div > div.article>div>table')

gather = browser.find_elements_by_css_selector('#content > div > div.article > div:nth-child(3) > table')

df =  pd.DataFrame([],columns= ['title','content','star','coupon'])
for item in gather:
    title =item.find_element_by_css_selector('tbody >tr > td>div>a').text
    content = item.find_element_by_css_selector('tbody >tr > td>div.pl2>p.pl').text
    star = item.find_element_by_css_selector('tbody >tr > td>div.pl2>div.star.clearfix>span.rating_nums').text
    coupon = item.find_element_by_css_selector('tbody >tr > td>div.pl2>div.star.clearfix>span.pl').text
    
    temp = pd.DataFrame({'title':[title],'content':[content],'star':[star],'coupon':[coupon]})

    df = pd.concat([temp,df])
    

