# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import re, chardet
from lxml import etree

"""
整个爬虫负责对获得html进行解析，例如：解析获得url列表，通过正则表达式进行匹配获得数据
"""


class HtmlAnalysis:
    def __init__(self):

        '''
        设定xpath解析器的解析格式
        :return:
        '''

        self.parser = etree.HTMLParser(encoding='utf-8')

    def change_code(self, html):

        '''
        修改html的编码格式，全部转化为utf-8
        :param html:
        :return:
        '''

        if chardet.detect(html[0:1000])['encoding'] == 'GB2312':
            html = html.decode('gbk').encode('utf-8')
            return html
        else:
            return html

    def search(self, analysis, html):

        '''
        判断一个匹配方式的字符串是不是存在在html中
        :param analysis:解析字典
        :param html:html文档
        :return:
        '''

        html = self.change_code(html)
        return re.search(analysis, html)

    def xpath(self, analysis, html):

        '''
        xpath解析的方法对html进行解析。
        :param analysis:解析字典
        :param html:html文档
        :return:
        '''

        html = self.change_code(html)
        select = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        return select.xpath(analysis)

    def findAll(self, analysis, html, whether=True):

        '''
        使用正则表达式进行匹配。
        :param analysis:解析字典
        :param html:html文档
        :param whether:是否多行匹配
        :return:
        '''

        html = self.change_code(html)
        if whether:
            return re.findall(analysis, html, re.S)
        else:
            return re.findall(analysis, html)

    def getUrlList(self, urlRule, urllist):

        '''
        判断一个list中的url是不是可以匹配
        :param urlRule:匹配规则
        :param urllist:url列表
        :return:
        '''

        list = []
        for i in urllist:
            if re.match(urlRule, i):
                list.append(i)
        return list

    def modifyUrl(self, pattern, repl, string):

        '''
        使用正则表达式修改url
        :param pattern: 匹配式
        :param repl: 代替的url
        :param string: 原来的url
        :return:
        '''

        return re.sub(pattern, repl, string)

    def extract(self, element):

        '''
        将数据从element对象中提取出来
        :param element:
        :return:
        '''

        return element.xpath('string(.)')

    # def getInformation(self, information):
    #
    #
    #     '''
    #     从类似 '      qwe\n  qqwe\n qweqweq\n   '的字符串中将数据有效的提取出来
    #     :param information:
    #     :return:
    #     '''
    #
    #
    #     float = []
    #     behind = []
    #     informationList = []
    #     information = information.replace('\r\n','').replace('\n','').replace('\r','')
    #     for i in range(len(information) - 1):
    #         if (information[i + 1] != ' ' and information[i + 1] != '\n') and information[i] == ' ':
    #             float.append(i)
    #         if (information[i] != ' ' and information[i] != '\n') and information[i + 1] == ' ':
    #             behind.append(i + 1)
    #     length = min(len(float),len(behind))
    #     for i in range(length):
    #         informationList.append(information[float[i]:behind[i]].strip())
    #     return informationList


    def informationSplit(self, information, string):

        l = information.split(string)
        for i in xrange(len(l)):
            l[i] = l[i].strip()
        return l

    def getInformation(self, information):

        information = information.strip()
        if '\r\n' in information:
            l = self.informationSplit(information, '\r\n')
            return l
        elif '\r' in information:
            l = self.informationSplit(information, '\r')
            return l
        elif '\n' in information:
            l = self.informationSplit(information, '\n')
            return l
