# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests, StringIO, gzip, urllib2, grequests, chardet, urllib, cookielib
from util import Util

"""
这个模块是专门为了下载相应url的html文档
getHtmlByR通过requests的模块进行下载
getHtmlByU通过urllib2的模块进行下载速度较requests快
获得的文档是字节码没有进行任何转码
"""
time = 10
req_header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
              'Accept': 'text/plain, */*; q=0.01',
              'Connection': 'keep-alive',
              }


def getHtmlByR(url, data=None, proxyip=None):
    """
    通过requests的方式进行html文档下载
    :param url:
    :return:html文档
    """

    try:
        if data:
            if proxyip:
                html = requests.post(url, timeout=time, proxies=proxyip, data=data, headers=req_header).content
                return html
            else:
                html = requests.post(url, timeout=time, data=data, headers=req_header).content
                return html
        else:
            if proxyip:
                html = requests.get(url, timeout=time, proxies=proxyip, headers=req_header).content
                return html
            else:
                html = requests.get(url, timeout=time, headers=req_header).content
                return html
    except Exception:
        raise Exception("can't get the html")


def getHtmlByU(url, data=None, proxyIp=None):
    req = urllib2.Request(url, headers=req_header)
    if proxyIp:
        proxy = urllib2.ProxyHandler({'http': proxyIp})
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()), proxy)
    else:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    if data:
        data = urllib.urlencode(data)
        response = opener.open(req, data, timeout=time)
    else:
        response = opener.open(req, timeout=time)
    return response.read()


def getHtmlByGAndF(url, data, proxyiplist=None):
    '''
    在使用代理的情况下必须异步快速测试每一个代理ip,来获取html页面
    :param url: 使用的url
    :param proxyiplist: 代理ip列表
    :return:
    '''

    if proxyiplist:
        rs = (grequests.post(url, proxies={'http': proxyurl}, timeout=time, data=data, cookies=cookielib.CookieJar(), headers=req_header)
              for proxyurl in proxyiplist)
        responselist = grequests.map(rs)
        return responselist
