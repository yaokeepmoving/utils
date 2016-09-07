# -*- coding: utf-8 -*-
# Python version: Python 3.4.3

import requests
from time import sleep
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
import random
import re
import time
import json



def get_url_hxs(url,is_json=False):
    """使用代理IP请求"""
    proxies = [{'https':'220.248.230.217:3128'},{'https':'119.18.234.60:80'},{'https':'218.90.174.167:3128'},{'https':'1.82.216.135:80'},{'https':'120.25.163.76:3128'}]
    ran_index = random.randint(0,5)
    hxs = None
    try_count = 10
    while try_count > 0:
        if is_json:
            try:
                user_agent = ['"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"']
                headers={'User-Agent':user_agent}
                json_content = requests.get(url,headers=headers,timeout=50,proxies = proxies[ran_index]).json()
                break
            except Exception as e:
                json_content = []
        else:
            try:
                user_agent = ['"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"']
                headers={'User-Agent':user_agent}
                body = requests.get(url,headers=headers,timeout=50,proxies = proxies[ran_index]).content
                response = HtmlResponse(url=url, body=body)
                hxs = HtmlXPathSelector(response)
                break
            except Exception as e:
                hxs = None
        try_count -= 1
    return json_content if is_json else hxs


def get_response_body(url, return_type='selector', timeout=10, try_times=2, delay=True):
    """返回响应的body.
    return_type='selector'/'json/html'
    """
    proxies = [{'https':'220.248.230.217:3128'},{'https':'119.18.234.60:80'},{'https':'218.90.174.167:3128'},{'https':'1.82.216.135:80'},{'https':'120.25.163.76:3128'}]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    ran_index = random.randint(0, len(proxies) - 1)

    fail_times = 0

    if return_type == 'selector':  # 解析html，返回response Selector
        while True:
            if delay:  # 设置时间间隔
                sleep(random.random() * 10)
            try:
                html = requests.get(url, headers=headers, timeout=timeout, proxies=proxies[ran_index]).content
                resp = HtmlResponse(url, body=html)
                return HtmlXPathSelector(resp)

            except:
                fail_times += 1
                if fail_times > try_times:
                    return None
                pass

    elif return_type == 'json':  # 请求API, 返回json格式
        while True:
            if delay:  # 设置时间间隔
                sleep(random.random() * 10)
            try:
                resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxies[ran_index]).json()
                return resp

            except:
                fail_times += 1
                if fail_times > try_times:
                    return None
                pass

    elif return_type == 'html':  # 返回html
        while True:
            if delay:  # 设置时间间隔
                sleep(random.random() * 10)

            try:
                resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxies[ran_index]).content
                return resp.decode('utf-8')  # response返回的是bytes，需要转换成string

            except:
                fail_times += 1
                if fail_times > try_times:
                    return None
                pass


def get_url_json(url,try_times = 2):
    """请求API，返回json格式的数据"""
    data = None
    while try_times:
        try:
            sleep(random.random() * 10)
            data = requests.get(url, headers=headers).json()
            break
        except:
            try_times -= 1
            print ('> [request error!] [get_url_json(url,try_times = 5)] get <{}>\n'.format(url))
    return data

##res = get_url_json('http://api.m.mtime.cn/Person/Movie.api?personId=893017&pageIndex=1&orderId=2')