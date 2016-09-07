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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains


def get_current_time(time_format='%Y-%m-%d %H:%M:%S'):
    """获得系统当前时间"""
    return time.strftime(time_format, time.localtime())

def get_13_timestamp():
    """13位unix时间戳"""
    return int(time.time() * 1000)


def init_browser(url='https://www.baidu.com'):
    """初始化浏览器"""

    opts = webdriver.ChromeOptions()
    opts.binary_location = r"D:\Program Files\Chrome\chrome.exe"
    driver = webdriver.Chrome(chrome_options = opts)
    wait = ui.WebDriverWait(driver,10)

    driver.get(url)
    sleep(random.random() * 30)

    return driver


def test_func(func, *args, **kwargs):
    """测试函数"""
    func_call = func(*args, **kwargs)


def list2dic(mat, field_tup):
    """
    e.g.:
    mat: [['zy', 90], ['xh', 100]]
    field_tup: ('name', 'score')
    return: [{'name': 'zy', 'score': 90}, {'name': 'xh', 'score': 100}]
    返回列表或生成器
    """
    for rec in mat:
        yield dict(zip(field_tup, rec))

##mat = [['zy', 90], ['xh', 100]]
##field_tup = ('name', 'score')
##res = list2dic(mat, field_tup)
##print(list(res))


def has_chinease(st):
    """判断字符串里是否含有中文"""
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    has_zh = zhPattern.findall(st)
    if has_zh:
        return True
    return False


##combine_collection(coll_peopleIds, coll_directors)


def split_list(max_index, start_index=0, chunk_size=500):
    """切分列表"""
    for i in range(start_index, max_index, chunk_size):
        j = i + chunk_size
        if j < max_index:
            yield range(i, i+chunk_size)
        else:
            yield range(i, max_index+1)

##res = split_list(100, 7, 7)
##for ele in res:
##    print(list(ele))
