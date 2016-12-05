# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import math, os

def calculation_mebibyte(byte):


    '''
    将byte转化为mb
    :param byte:
    :return:
    '''


    return byte / math.pow(1024,2)


def get_position():


    '''
    获得当前脚本的位置
    :return:返回脚本的位置
    '''


    strfilepath = os.path.realpath(__file__)
    string = "%s\\" % (os.path.dirname(strfilepath),)
    return string

def make_proxy_ip_list(protocol='http',proxylist=None):


    '''
    将普通的代理ip转化成{'http':url}的格式
    :param protocol:
    :param proxylist:
    :return:
    '''



    l = []
    for i in proxylist:
        d = {}
        d[protocol] = i
        l.append(d)
    return l

def judge_list_none(List):


    '''
    判断这个List是不是为空
    :param List:
    :return: True or False
    '''


    length = len(List)
    ans = 0
    for i in List:
        if i == None:
            ans += 1
    if ans == length:
        return True
    else:
        return False

def get_list_one(List):


    '''
    获得列表中第一个不为none的值
    :param List:
    :return:
    '''


    for i in List:
        if i != None:
            return i


