# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import ClearData, json, pymongo


def save_data_json(Dict, file_position='', way=''):
    '''
    将数据通过json的方式保存在txt中。
    :param Dict:以字典形式存放的数据
    :param file_position:如果不存在那么就是默认保存在file文件夹下面，否则是保存在其他路径下.
    :param way:以json格式进行保存
    :return:
    '''

    Dict = ClearData.clear_dict_space(Dict)
    if way == '':
        way = 'a'
    f = open(file_position, way)
    Dict = json.dumps(Dict)
    f.write(Dict)
    f.write('\n')
    f.close()


def save_data_mongodb(Dict, mongodbUrl, databaseName, collectionName):
    '''
    :param Dict:以字典形式存放的数据
    :param mongodbUrl:mongodb的地址
    :param databaseName:数据库的名字
    :param collectionName:集合的名字
    :return:
    '''

    Dict = ClearData.clear_dict_space(Dict)
    client = pymongo.MongoClient(mongodbUrl)
    db = client[databaseName]
    posts = db[collectionName]
    posts.insert(Dict)
    client.close()
