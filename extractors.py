# -*- coding: utf-8 -*-
# Python version: Python 3.4.3
# QQ群: 258681031


# 小结
def collect_urls(url, xpath):
    """由原始url开始，收集response页面的url.
    收集下一级的urls.
    e.g.
    http://business.sohu.com/s2012/6285/s356264585/
    ->
    http://business.sohu.com/20121104/n356615868.shtml
    """
    resp = get_response_body(url, return_type='selector')
    save_response_body(url, coll_response_body, resp, response_type='selector')
    subcategoty_urls = resp.select(xpath).extract()

    return subcategoty_urls


class TextExtractor:
    """正文提取器"""

    def __init__(self, url):
        pass


class UrlExtractor:
    """url提取器"""
    pass

