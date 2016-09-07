# -*- coding: utf-8 -*-
# Python version: Python 3.4.3

import codecs
import requests
from time import sleep
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
import random
import re
import time
import json


def compare_doc_keys(old_doc, new_doc):
    """比较两个doc的keys，返回新的keys,前提两者具有相同的_id,"""
    old_keys = set(old_doc.keys())
    new_keys = set(new_doc.keys())

    return new_keys.difference(old_keys)


def insert_one_doc(coll, doc):
    """插入一条记录"""
    _id = doc.get('_id')
    if not coll.find_one({'_id': _id}):
        coll.insert(doc)
        print('> [new doc!] coll: {}, _id: {}\n'.format(coll.full_name, _id))
    else:
        old_doc = coll.find_one({'_id': _id})
        have_new_keys = compare_doc_keys(old_doc, doc)
        if have_new_keys:  # 有新的字段
            new_doc = {k: doc.get(k) for k in have_new_keys}
            coll.update({'_id': _id}, {'$set': new_doc})
            print('> [new fields!] coll: {}, _id: {}, new fields: {}\n'.format(coll.full_name, _id, have_new_keys))
        else:
            print('> [have existed!] coll: {}, _id: {}\n'.format(coll.full_name, _id))


def save_response_body(url, coll_response_body, response_body, response_type=''):
    """保存请求结果，避免多次请求"""
    if not coll_response_body.find_one({'_id': url}):
        if response_type == 'selector':  #
            response_body = response_body.response.text
        coll_response_body.insert({'_id': url, 'url': url, 'response_body': response_body, 'response_type': response_type})
        print('> [new!] save_response_body(url, response_body, response_type='') -> {}\n'.format(url))


def combine_collection(coll_master, coll_slave):
    """将coll_slave的doc合并到coll_master中"""
    for doc in coll_slave.find({}):
        _id = doc.get('_id')
        if not coll_master.find_one({'_id': _id}):
            coll_master.insert(doc)
            print('> from {} to {}\n -> {}'.format(coll_slave, coll_master, _id))


def txt2list(file_path, has_header=False, delimiter='\t', filler='---'):
    """读取文本文件内容到list中"""

    content = []
    fr = codecs.open(file_path, 'r', encoding='utf-8')
    first_line = fr.readline().rstrip('\n').split(delimiter)
    print('first line: {}\n'.format(delimiter.join(first_line)))
    num_fields = len(first_line)
    if not has_header:  # 没有头部
        content.append(first_line)

    for line in fr:
        line = line.rstrip('\n').split(delimiter)
        content.append(line)

    fr.close()
    print("> [successful!] <txt2list(file_path, has_header=False, delimiter='\t', filler='---')> load {} into list.\n".format(file_path))
    return content

##res = txt2list(u'姐妹淘心话.txt', has_header=True)


def get_task_list_from_redis(redis_client, key, chunk_size=100):
    """从redis产生任务片段"""
    while True:
        task_chunk =[]
        for i in range(chunk_size):
            job = client_redis.rpop(key)
            if job:
                dic = json.loads(job.decode('utf-8'))
                _id = dic.get('_id')
                task_chunk.append(_id)
            else:
                print('Done!')
                break
        yield task_chunk


def put_task_into_redis(redis_client, key, task_list):
    """将任务队列push到redis中"""
    for dic in task_list:
        doc = {'_id': dic.get('_id')}
        redis_client.rpush(key, json.dumps(doc))
    print('[Done!] task list pushed into redis key: {}\n'.format(key))


def put_task_into_mongo(mongo_client, coll_name, task_list):
    """将任务队列push到mongo中"""
    pass


def compare_doc_id(coll_1, coll_2):
    """在coll_1中，但不在coll_2中"""
    keys_1 = set(coll_1.distinct('_id'))
    keys_2 = set(coll_2.distinct('_id'))

    return keys_1.difference(keys_2)


def update_new_fields(coll, new_doc):
    """向原有document添加新的key:value"""

    _id = new_doc.get('_id')
    old_doc = coll.find_one({'_id': _id})
    new_keys = get_new_keys(new_doc, old_doc)
    if new_keys:
        update_doc = {k: new_doc.get(k) for k in new_keys if k}  # 需要更新的key:value对
##        print(update_doc)
        coll.update({'_id': _id}, {'$set': update_doc})
        print('>>> [New fields!] collection_name: < {coll_name} > || new_fields: < {new_fields} > || _id: < {doc_id} >\n'.format(coll_name=coll.full_name, new_fields=new_keys, doc_id=_id))
    else:
        print('>>> [No new fields!] collection_name: < {coll_name} > || new_fields: < {new_fields} > || _id: < {doc_id} >\n'.format(coll_name=coll.full_name, new_fields=new_keys, doc_id=_id))


def get_new_keys(new_doc, old_doc):
    """获得新的keys"""
    new_keys = list(new_doc.keys())
    old_keys = list(old_doc.keys())
    return set(new_keys) - set(old_keys)