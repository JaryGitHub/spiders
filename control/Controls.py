# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import gc
import logging
import os
import psutil
import re
import sys
import threading
import time

from data import SaveData
from download import DownLoad
from htmlanalysis.HtmlAnalysis import HtmlAnalysis
from norepeatqueue.NoRepeatQueue import NoRepeatQueue
from util import Util

reload(sys)
sys.setdefaultencoding('utf-8')
"""
整个爬虫的核心 引擎部分
类的构造函数中传入(某个网页的匹配以及相应网页xpath相应的采集方法或者是正则表达式形式的方法)字典形式
在找到url后 是否要对url进行裁剪或者添加，并且加入到一个url队列中（可以设定进行队列的url形式以此控制url的数量加大效率）
另一个方面则是对数据部分的获得，将数据传给data部分进行清洗和储存
"""


class ControlThread(threading.Thread):
    def __init__(self):

        '''
        初始化各个参数
        '''

        threading.Thread.__init__(self)
        self.analysis = None
        self.thread_run = True
        self.keyword = None
        self.analysiss = None
        self.maximum = 1000
        self.limit = None
        self.operation_file = None
        self.whether = True
        self.sleeptime = 0
        self.maxumunqueue = 100
        self.urlList = []
        self.proxy_ip_list = []

    def add_analysis(self, analysis):

        '''
        初始化从什么类型的网页上采用怎么样的提取规则
        :param analysis: 一个字典包含了url的匹配规则和html抽取规则
        :return:
        '''

        self.analysis = analysis

    def add_modift_url(self, keyword=None, analysiss=None):

        '''
        初始化是否需要对残缺的url添加前缀
        :param keyword: add or replace
        :param analysiss: 一个前缀字符串
        :return:
        '''

        self.keyword = keyword
        self.analysiss = analysiss

    def add_maximum_operating_frequency(self, maxnumber):

        '''
        设置最大运行次数，超过则爬虫停止运行
        :param maxnumber:
        :return:
        '''

        self.maximum = maxnumber

    def add_limit_queue(self, limit):

        '''
        设置进入队列的url的限制（列表传入），通过正则表达式来限制
        :param limit:
        :return:
        '''

        self.limit = limit

    def add_operation_file(self, operation_file):

        '''
        设置数据保存的形式,设置了以json格式保存在txt中和nosql数据库中两种形式
        :param operation_file:以列表显示传入,例如['json','D:\\fuck.txt','a'],['mongodb','mongodb://localhost:27017/','first','firstCollection']
        :return:
        '''

        self.operation_file = operation_file

    def add_whether_re_multiple_line_matching(self, whether):

        '''
        设置是否需要正则表达式多行匹配
        :param whether: True or False
        :return:
        '''

        self.whether = whether

    def add_sleeptime(self, sleeptime):

        '''
        添加线程休息时间,如果不采用代理必须设置时间否则被封IP的概率很大
        :param sleeptime:时间以秒为参数
        :return:
        '''

        self.sleeptime = sleeptime

    def add_maxumunqueue(self, maxumunqueue):

        '''
        设置队列的最大容量
        :param maxumunqueue:最大容量的多少
        :return:
        '''

        self.maxumunqueue = maxumunqueue

    def add_proxy(self, proxy_ip_list):

        '''
        设置代理ip，传入一个列表
        :param proxy_ip_list: 代理ip列表
        :return:
        '''

        self.proxy_ip_list = proxy_ip_list

    def modiftUrl(self, craw, keyword=None, repart=None, list=None):

        '''
        对于直接从网页上获得的url可能会有缺陷，缺少了一部分等。因为对于这些url需要处理添加部分或者替代
        :param craw:crawlSpider的实例
        :param keyword:有两个选择add或者是replace。
        :param repart:需要添加的url或者是需要修改的url列表。如果是列表那个第一个是匹配的方式，第二个是代替的Url
        :param list:需要修改的List列表
        :return:一个处理完成的url列表
        '''

        if keyword == 'add':
            for i in xrange(len(list)):
                if 'http' not in list[i]:
                    list[i] = repart + list[i]
            return list
        elif keyword == 'replace':
            for i in xrange(len(list)):
                list[i] = craw.modifyUrl(repart[0], repart[1], list[i])
            return list
        else:
            return list

    def judge_url(self, url, limit):

        '''
        在对于限制进入队列的url需要判断是不是满足相应的条件。
        :param url:需要判断的Url
        :param limit:限制的条件，可能为列表或者是字符串
        :return:True or False
        '''

        if isinstance(limit, str):
            return re.match(limit, url)
        elif isinstance(limit, list):
            for i in limit:
                if re.match(i, url):
                    return True
        return False

    def queue_add_url(self, urlList, queue, limit=None, limitnumber=None):

        '''
        将url加入到队列中，并且根本相应的限制条件进行筛选。
        :param urlList:一个存有url的list
        :param queue:队列的实例
        :param limit:url限制条件
        :param limitnumber:队列大小的限制
        :return:返回一个已经添加好数据的队列
        '''

        if urlList:
            for i in urlList:
                if limitnumber and limitnumber == queue.qsize():
                    break
                elif i and limit:
                    if self.judge_url(i, limit):
                        queue.put(i)
                elif i:
                    queue.put(i)
        return queue

    def getHtmlUrl(self, craw, html, analysisDict, keyword=None, analysis=None):

        '''
        从html文档上面获取url
        :param craw:crawlSpider的实例
        :param html:html文档
        :param analysisDict:一开始已经传入的字典解析，从中获得url键的解析方式
        :param keyword:add或者是replace
        :param analysis:需要修改url的部分可以是列表或者是字符串
        :return:从网页获得url列表
        '''

        if analysisDict:
            if analysisDict['url'][0] == 'R':
                list = craw.findAll(analysisDict['url'][1:len(analysisDict['url'])], html)
                list = self.modiftUrl(craw, keyword, analysis, list)
                return list
            elif analysisDict['url'][0] == 'X':
                list = craw.xpath(analysisDict['url'][1:len(analysisDict['url'])], html)
                list = self.modiftUrl(craw, keyword, analysis, list)
                return list
        return None

    def find_analysis(self, url, analysisDict):

        '''
        字典解析的结构是相应的Url对应相应的解析方法，因为首先要匹配url，然后再去寻找这个url的解析方法
        :param url:一个url
        :param analysisDict:字典解析
        :return:返回解析字典的方法
        '''

        for i in analysisDict.keys():
            if re.match(i, url):
                return self.analysis[i]
        return None

    def write_start_url(self, url):

        '''
        设置初始的url队列
        :param url:url列表
        :return:
        '''

        self.urlList.extend(url)

    def getItem(self, craw, analysisDict, html, whether=True):

        '''
        解析html文档中的所需内容。
        :param craw:crawlSpider的实例
        :param analysisDict:相应url的解析方法
        :param html:html文档
        :param whether:在正则表达式的时候是不是需要多行匹配
        :return:
        '''

        item = {}
        for i in analysisDict.keys():
            if i != 'url' and analysisDict[i][0] == 'R':
                item[i] = craw.findAll(analysisDict[i][1:len(analysisDict[i])], html, whether=whether)
            elif i != 'url' and analysisDict[i][0] == 'X':
                item[i] = craw.xpath(analysisDict[i][1:len(analysisDict[i])], html)
        return item

    def run(self):

        '''
        主要的爬虫运行逻辑
        :return:
        '''

        ans = 0
        q = NoRepeatQueue()  # 初始化队列
        c = HtmlAnalysis()  # 初始化解析类
        p = psutil.Process(os.getpid())
        while self.thread_run:  # 判断线程是否还在运行
            if self.thread_run == False:
                break
            if self.urlList:  # 控制队列的大小
                for i in self.urlList:
                    if q.qsize() <= self.maxumunqueue:
                        q.put(i)
                        self.urlList.remove(i)
                    else:
                        break
            if q.qsize() == 0:
                break
            while q.empty() == False:
                url = q.get()
                logging.debug('Now this url is running' + '  ' + url)
                logging.debug('Now' + '   ' + str(q.qsize()) + '  ' + 'in the queue')
                logging.debug('Now the spiders in run' + '   ' + str(ans) + '  ' + 'times')
                logging.debug('Now the queue is ' + '   ' + str(
                    Util.calculation_mebibyte(sys.getsizeof(q.queue.map))) + '  ' + 'MB')
                logging.debug('Now the urllist is ' + '   ' + str(
                    Util.calculation_mebibyte(sys.getsizeof(self.urlList))) + '  ' + 'MB')
                logging.debug('Now the queue is ' + '   ' + str(p.memory_percent()) + '%')
                ans += 1
                if ans == self.maximum or self.thread_run == False:  # 如果线程不能运行则返回退出
                    self.thread_run = False
                    break
                elif p.memory_percent() >= 30:  # 当进程内存使用量超过系统内存30%时,自动开始释放内存
                    break
                else:
                    try:
                        if self.proxy_ip_list:  # 通过代理获得html页面
                            html = DownLoad.getHtmlByGAndF(url, proxyiplist=self.proxy_ip_list)
                        else:
                            html = DownLoad.getHtmlByR(url)
                        time.sleep(self.sleeptime)
                        analysisDict = self.find_analysis(url, self.analysis)  # 获得解析的字典
                        if analysisDict and html:
                            listUrl = self.getHtmlUrl(c, html, analysisDict, keyword=self.keyword,
                                                      analysis=self.analysiss)  # 从html中提取到url
                            q = self.queue_add_url(listUrl, q, self.limit, self.maxumunqueue)
                            listKey = analysisDict.keys()
                            listKey.remove('url')
                            if self.operation_file[0] == 'json' and len(listKey) != 0:  # 控制数据保存的地点
                                SaveData.save_data_json(self.getItem(c, analysisDict, html, self.whether),
                                                        file_position=self.operation_file[1],
                                                        way=self.operation_file[2])
                            elif self.operation_file[0] == 'mongodb' and len(listKey) != 0:
                                SaveData.save_data_mongodb(self.getItem(c, analysisDict, html, self.whether),
                                                           self.operation_file[1], self.operation_file[2],
                                                           self.operation_file[3])
                    except Exception:
                        logging.error('a error has happened')
                        continue
            while q.empty() == False:  # 定期控制释放内存
                if Util.calculation_mebibyte(sys.getsizeof(self.urlList)) <= 10:  # 当urllist的中转部分大小超过10mb时就不存入url
                    self.urlList.append(q.get())
                else:
                    break
            gc.collect()

    def stop(self):
        self.thread_run = False
        exit(0)
