# -*- coding: utf-8 -*-
# Python version: Python 3.4.3
# xml 转 json
# xml2json.py
# Version 1.0
# **************
# [版权声明]该脚本改编自https://zhuanlan.zhihu.com/p/21349442,版权归原作者所有
# **************


"""xml转成json"""

from xml.parsers.expat import ParserCreate
import json
import codecs


class Xml2Json:
    LIST_TAGS = ['COMMANDS']

    def __init__(self, data=None):
        """data: xml格式的字符串"""
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self._result = None
        if data:
            self.feed(data)
            self.close()

    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse('', 1)
        del self._parser

    def start(self, tag, attrs):
        assert attrs == {}
        assert self._data.strip() == ''
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1:  # leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if not isinstance(el, list):
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else:  # force into a lsit
                data = [{k: v} for k, v in last_tag[1:]]

        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self._result = {tag: data}

        self._data = ''

    def data(self, data):
        self._data = data

    def get_json(self):
        """获得json对象"""
        return self._result

    def dump2json(self, file_name='output.json', encoding='UTF-8'):
        """将转换后的json对象保存到文件中"""
        with codecs.open(file_name, 'w', encoding=encoding) as fid:
            json.dump(self._result, fid, ensure_ascii=False, indent=2)  # 导出中文,需要设置ensure_ascii=False, indent参数指定缩进，漂亮打印pretty print
            fid.close()
        print('>>> json object dump to file: {}\n'.format(file_name))


##if __name__ == '__main__':
##    xml = codecs.open('result2.xml', 'r', encoding='UTF-8').read()
##    json_obj = Xml2Json(xml)
##    res = json_obj.get_json()
##    print(res)
##
##    json_obj.dump2json('result2.json')


