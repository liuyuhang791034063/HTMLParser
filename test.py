#!/usr/bin/python3
# _*_ coding: utf-8 _*_
# @Time     : 2018/1/30 17:11
__author__ = 'White'

from html.parser import HTMLParser
from urllib import request
import re

class MyHTMLParser(HTMLParser):
    flag = 0
    new = []
    get_data = 0

    def handle_starttag(self, tag, attrs):
        #判断该标签是否存在
        if tag == 'ul':
            for attr in attrs:
                if re.match("list-recent-events menu",attr[1]):
                    self.flag = 1
        #处理a元素
        if tag == 'a' and self.flag == 1:
            self.get_data = 'tittle'
        #处理time元素
        if tag == 'time' and self.flag == 1:
            self.get_data = 'time'
        #处理span元素
        if tag == 'span' and self.flag == 1:
            self.get_data = 'addr'

    #当处理尾标签时则初始flag
    def handle_endtag(self, tag):
        if self.flag == 1 and tag == 'ul':
            self.flag = 0

    #对data的处理
    def handle_data(self, data):
        if self.get_data and self.flag == 1:
            #如果找到了题目，则新建一个dict来保存
            if self.get_data == 'tittle':
                self.new.append({self.get_data : data})
            #如果找到了时间或者地点，则取出new这个list最后一个dict，然后添加键值
            else:
                self.new[len(self.new)-1][self.get_data] = data
            self.get_data = None

parser = MyHTMLParser()

with request.urlopen('https://www.python.org/events/python-events/') as f:
    data = f.read().decode('utf-8')

parser.feed(data)
for item in MyHTMLParser.new:
    print('-------------------------')
    for k,v in item.items():
        print("%s : %s" % (k,v))
