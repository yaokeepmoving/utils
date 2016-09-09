# -*- coding: utf-8 -*-
# Python version: Python 3.4.3
# QQ群: 258681031

"""定义爬取的字段信息"""


##class ChinaEntrepreneursForumItem(Item):
##    title = Field()  # 文章标题
##    text = Field()  # 文章正文
##    date_time = Field()  # 日期时间
##    author = Field()  # 作者
##    hits = Field()  # 点击量
##
##    page_url = Field()  # 文章地址
##    category = Field()  # 所属分类
##    source = Field()  # 来源
##    source_homepage = Field()  # 来源主页
##
##    download_time = Field()  # 下载日期


class Field:
    """定义字段类"""

    def __init__(self, field_name, field_value=''):
        self._field_name = field_name
        self._field_value = field_value

    def _get_field_name(self):
        return self._field_name

    def _get_field_value(self):
        return self._field_value

    def _set_field_value(self, new_field_value):
        self._field_value = new_field_value

##field = Field('title', '')


class UserDefinedSpiderItem:
    """用户自定义的爬虫item类"""

    def __init__(self, spider_name='MySpiderItem', *args):
        self._spider_name = spider_name
        self._field_set = set()
        self.add_new_fields(args)


    def add_new_fields(self, args):
        """添加新的属性"""
        for attr in args:
            setattr(self, attr, Field(attr))
            self._field_set.add(attr)

    def get_field_set(self):
        """获取所有的field名字的列表"""
        return self._field_set

    def __str__(self):
        return 'spider_name: {0}, field information: {1}\n'.format(self._spider_name, str(self.get_field_set()))

if __name__ == '__main__':

    fields = 'title', 'text', 'date_time', 'url'
    spider_items = UserDefinedSpiderItem('ChinaEntrepreneursForumItem', *fields)