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


def get_proxies_pool():
    """获得代理IP池"""
    url = 'http://192.168.86.129:18100/?type=1&start=0&offset=10'
    data = requests.get(url).json()
    proxies_pool = data.get('proxies')
    return [{'http': '{ip}:{port}'.format(ip=ele.get('ip'), port=ele.get('port'))} for ele in proxies_pool]

# 代理IP池
##PROXIES_POOL = get_proxies_pool()  # 代理池
PROXIES_POOL = [{'https':'220.248.230.217:3128'},{'https':'119.18.234.60:80'},{'https':'218.90.174.167:3128'},{'https':'1.82.216.135:80'},{'https':'120.25.163.76:3128'}]


def get_random_proxies(proxies_pool):
    """e.g. proxies_pool = [{'http':'119.18.234.60:80'},{'https':'218.90.174.167:3128'},{'https':'1.82.216.135:80'},{'https':'120.25.163.76:3128'}]"""
    random_index = random.randint(0, len(proxies_pool) - 1)
    return proxies_pool[random_index]


def get_response_body(url, return_type='selector', timeout=20, try_times=1, delay=True, use_proxies=True, random_time_n = 1, headers=None):
    """返回响应的body.
    return_type='selector'/'json/html'
    """
    random_proxy = get_random_proxies(PROXIES_POOL)
##    print(random_proxy)

##    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    fail_times = 0

    if return_type == 'selector':  # 解析html，返回response Selector
        while True:
            if delay:  # 设置时间间隔
                sleep(random.random() * random_time_n)
            try:
                html = requests.get(url, headers=headers, timeout=timeout, proxies=random_proxy)
                print('selector: status_code -> {}\n'.format(html.status_code))
                resp = HtmlResponse(url, body=html.content)
                return HtmlXPathSelector(resp)

            except:
                fail_times += 1
                if fail_times > try_times:
                    return None
                pass

    elif return_type == 'json':  # 请求API, 返回json格式
        while True:
            if delay:  # 设置时间间隔
                sleep(random.random() * random_time_n)
            try:
                resp = requests.get(url, headers=headers, timeout=timeout, proxies=random_proxy)
                print('json: status_code -> {}\n'.format(resp.status_code))
                return resp.json()

            except:
                fail_times += 1
                if fail_times > try_times:
                    return None
                pass

    elif return_type == 'html':  # 返回html
        while True:
            if delay:  # 设置时间间隔
                sleep(random.random() * random_time_n)

            try:
                resp = requests.get(url, headers=headers, timeout=timeout, proxies=random_proxy)
                print('html: status_code -> {}\n'.format(resp.status_code))
##                encoding_type = resp.encoding
##                return resp.content.decode(encoding_type)  # response返回的是bytes，需要转换成string
                return resp.text

            except:
                fail_times += 1
                if fail_times > try_times:
                    return None
                pass
