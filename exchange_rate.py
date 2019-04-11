#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import html5lib
from bs4 import BeautifulSoup
import re
import chardet
import json
import pandas as pd
import time


# In[2]:


class crawler():
    response = None
    session = None
    def __init__(self,headers = None, cookies = None, proxies = None):
        self.set_default_parameter()
        if headers != None:
            self.headers = self.headers_to_dict(headers)
        if cookies != None:
            cookies_dict = self.cookies_to_dict(cookies)
            self.cookies = cookies_dict
        if proxies != None:
            self.proxies = proxies
        self.update_parameter()
        
    def set_default_parameter(self):
        #default
        self.headers = {
            'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
            ,"referer":"https://www.pcstore.com.tw/"
            ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        }
        self.cookies = None
        self.proxies = None
        
    def update_parameter(self):
        parameter = {}
        if self.headers != None:
            parameter.update({'headers':self.headers})
        if self.cookies != None:
            parameter.update({'cookies':self.cookies})
        if self.proxies != None:
            parameter.update({'proxies':self.proxies})
        self.parameter = parameter
    
    def set_parameter(self,headers = None, cookies = None, proxies = None):
        """arg = 'None'，parameter clears"""
        if headers != None:
            self.headers = self.headers_to_dict(headers)
            if headers == "None":
                self.headers = None                
        if cookies != None:
            self.cookies = self.cookies_to_dict(cookies)
            if cookies == "None":
                self.cookies = None                
        if proxies != None:
            self.proxies = proxies
            if proxies == "None":
                self.proxies = None                
        self.update_parameter()
        
    @classmethod
    def cookies_to_dict(cls,cookie):
        """cookies(str) to cookies(dict)"""
        return dict([l.split("=", 1) for l in cookie.split("; ")])
    @classmethod
    def headers_to_dict(cls,header):
        """headers(str) to headers(dict)"""
        return dict(line.split(": ", 1) for line in header.split("\n"))
    
    def create_session(self):
        sess = requests.Session()
        self.session = sess
    
    def sess_get_url(self,url, **get_parameter):
        """get_parameter input: params,timeout..."""
        if self.session == None:
            self.create_session()
        sess = self.session
        parameter = self.parameter
        response = sess.get(url, **parameter, **get_parameter)
        self.response = response 
    
    def sess_post_url(self,url, **get_parameter):
        if self.session == None:
            self.create_session()
        sess = self.session
        parameter = self.parameter
        response = sess.post(url, **parameter, **get_parameter)
        self.response = response 
    
    def get_url(self, url, **get_parameter):
        """get_parameter input: params,timeout..."""
        parameter = self.parameter
        response = requests.get(url, **parameter, **get_parameter)
        self.response = response 
        
    def post_url(self,url, encoding=None, **get_parameter):
        parameter = self.parameter
        response = requests.post(url, **parameter, **get_parameter)
        self.response = response 
            
    def get_soup(self,encoding=None):
        response = self.response.text
        if encoding != None:
            response = self.response.content.decode(encoding,'ignore')
        soup = BeautifulSoup(response, "html5lib")
        return soup
    
    def save_res(self,path,encoding):
        res_write = self.response.content.decode(encoding,'ignore')
        with open(path,'w',encoding=encoding) as f:
            f.write(res_write)


# In[3]:


class Get_the_spoils():
    @classmethod
    def print_list(cls,in_list):
        for row in in_list:
            print(row)


# In[4]:


class control_spider():
    spider = None
    
    def __init__(self,session=True):
        self.create_spider()
        
    def create_spider(self,session=True):
        spider = crawler()
        if session == True:
            sess = spider.create_session()
        self.spider = spider
        return spider
    
    def get_classification(self):
        url = "https://www.bankchb.com/frontend/jsp/getG0100_history.jsp?mode=getOption"
        spider = self.spider   
        spider.sess_post_url(url)
        classification = json.loads(spider.response.text)
        return classification["data"]
    
    def get_search_parameter(self,):
        classification = self.get_classification()
        print(classification)
        input_eaiCode = input("輸入幣別，多選請用,隔開:"+"\n"+"(ex. CNY,USD):"+"\n")
        eaiCode_list = input_eaiCode.split(',')
        print("輸入查詢日期(不能超過3年) :")
        startDate = input("輸入開始日期"+"\n"+"(ex. 2016/05/01):"+"\n")
        endDate = input("輸入結束日期"+"\n"+"(ex. 2019/04/09):"+"\n")
        return eaiCode_list,startDate,endDate
    
    def search_rate(self):
        #url,headers
        url = "https://www.bankchb.com/frontend/jsp/getG0100_history.jsp"
        header = ( "Accept: application/json, text/javascript, */*; q=0.01"+"\n"
                "Accept-Encoding: gzip, deflate, br"+"\n"
                "Accept-Language: zh-TW,zh;q=0.9,en;q=0.8"+"\n"
                "Connection: keep-alive"+"\n"
                "Content-Length: 81"+"\n"
                "Content-Type: application/x-www-form-urlencoded; charset=UTF-8"+"\n"
                "Host: www.bankchb.com"+"\n"
                "Origin: https://www.bankchb.com"+"\n"
                "Referer: https://www.bankchb.com/frontend/G0100_history.jsp"+"\n"
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"+"\n"
                "X-Requested-With: XMLHttpRequest")
        #params
        default_params = ("interval: interval-one"
                                  "\n"
                                  "startDate: 2017/01/01"
                                  "\n"
                                  "endDate: 2019/04/09")
        params_dict = crawler.headers_to_dict(default_params)
        eaiCode_list,startDate,endDate = self.get_search_parameter()
        params_dict["startDate"] = startDate
        params_dict["endDate"] = endDate
        #get
        spider = self.spider
        for eaiCode in eaiCode_list:
            params_dict["eaiCode"] = eaiCode
            spider.set_parameter(headers=header)
            spider.sess_post_url(url,data=params_dict)
            data = json.loads(spider.response.text)['datas']
            pd_data = pd.DataFrame(data)
            col_list = pd_data.columns
            nwe_col = [col_list[2],col_list[1],col_list[0],col_list[4],col_list[3]]
            pd_data = pd_data.reindex(nwe_col,axis=1)
            pd_data.to_csv(str(eaiCode)+".csv")
            time.sleep(0.5)
        return spider


# In[5]:


if __name__ == "__main__":
    control = control_spider()
    spider = control.search_rate()


# In[ ]:




