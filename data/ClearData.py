# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import lxml


def clear_dict_space(Dict):


    '''
    对于字典中的数据进行清除空格
    :param Dict:字典
    :return:清除空格的字典
    '''


    for i in Dict.keys():
        if isinstance(Dict[i],list):
            if Dict[i]:
                Dict[i] = clear_list_space(Dict[i])
        elif isinstance(Dict[i],lxml.etree._Element):
            Dict[i] = Dict[i].xpath('string(.)').strip()
        elif isinstance(Dict[i],str):
            Dict[i] = Dict[i].strip()
    return Dict

def clear_list_space(List):


    '''
    对列表中的数据进行去重空格
    :param List: 列表
    :return: 清除空格的列表
    '''


    List = analysis_element(List)
    for i in List:
        if i == '':
            List.remove('')
    return List

def analysis_element(List):


    '''
    对列表中的数据进行去重空格
    :param List: 列表
    :return: 清除空格的列表
    '''


    for i in range(len(List)):
        if isinstance(List[i],lxml.etree._Element):
            List[i] = List[i].xpath('string(.)').strip()
    return List


