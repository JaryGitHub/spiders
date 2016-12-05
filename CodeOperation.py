# ! /usr/bin/env python
# -*- coding: utf-8 -*-
from control.Controls import ControlThread
from util import Util
import sys
d = {'Id':'X/html/body//div[@class="title"]/p[@class="gray9"]/span[@class="mr10"]','Date':'R\d{4}\W\d{2}\W\d{2}\s{2}','UnitPrice':'R\d+元/㎡','ApartmentLayout':'R\d室\d厅\d厨\d卫','Total':'X/html/body/div//dl/dt[@class="gray6 zongjia1"]/span[@class="red20b"]','Area':'X/html/body/div//dl/dd/span[@class="black "]','ResidentialQuarters':'X/html/body//dl/dt/a[@id="agantesfxq_B02_08"]','Age':'X/html/body//dl/dd','Floor':'X/html/body//dl/dd','Decoration':'X/html/body//dl/dd','Address':'R<dt><span class="gray6">楼盘名称：</span>(.*?)  &nbsp;&nbsp;','url':'X//a//@href'}
q = ControlThread()
# q.add_parameter({'^.*(fang)\.com\/(?<!chushou)$':{'url':'X//a//@href'},'\S+fang\S+(chushou)\S+\d+\S+':d,'\S+fang\S+house\S+i\d\d\S+':{'url':'X//a//@href'}},keyword='add',analysiss='http://esf.nb.fang.com/',maximum=10,maxumunqueue=100,limit=['\S+nb.fang\S+chushou\S+','^.*(nb.fang)\.com\/(?<!chushou)$','\S+nb.fang\S+house\S+i\d\d\S+'],operation_file=['json','D:\\fuck.txt','a'],whether=True)
# q.add_parameter({'^.*(fang)\.com\/(?<!chushou)$':{'url':'X//a//@href'},'\S+fang\S+(chushou)\S+\d+\S+':d,'\S+fang\S+house\S+i\d\d\S+':{'url':'X//a//@href'}},keyword='add',analysiss='http://esf.nb.fang.com/',maximum=10,maxumunqueue=100,limit=['\S+nb.fang\S+chushou\S+','^.*(nb.fang)\.com\/(?<!chushou)$','\S+nb.fang\S+house\S+i\d\d\S+'],operation_file=['mongodb','mongodb://localhost:27017/','first','firstCollection'],whether=True)
q.write_start_url(['http://esf.nb.fang.com/house/i32/'])
q.add_analysis({'^.*(fang)\.com\/(?<!chushou)$':{'url':'X//a//@href'},'\S+fang\S+(chushou)\S+\d+\S+':{'Id':'X/html/body//div[@class="title"]/p[@class="gray9"]/span[@class="mr10"]','Date':'R\d{4}\W\d{2}\W\d{2}\s{2}','UnitPrice':'R\d+元/㎡','ApartmentLayout':'R\d室\d厅\d厨\d卫','Total':'X/html/body/div//dl/dt[@class="gray6 zongjia1"]/span[@class="red20b"]','Area':'X/html/body/div//dl/dd/span[@class="black "]','ResidentialQuarters':'X/html/body//dl/dt/a[@id="agantesfxq_B02_08"]','Age':'X/html/body//dl/dd','Floor':'X/html/body//dl/dd','Decoration':'X/html/body//dl/dd','Address':'R<dt><span class="gray6">楼盘名称：</span>(.*?)  &nbsp;&nbsp;','url':'X//a//@href'},'\S+fang\S+house\S+i\d\d\S+':{'url':'X//a//@href'}})
q.add_modift_url(keyword='add', analysiss='http://esf.nb.fang.com/')
q.add_maximum_operating_frequency(sys.maxint)
q.add_maxumunqueue(50000)
q.add_limit_queue(['\S+nb.fang\S+chushou\S+','^.*(nb.fang)\.com\/(?<!chushou)$','\S+nb.fang\S+house\S+i\d\d\S+'])
q.add_operation_file(['json', u'/home/van/文档/房价数据新/fuck14.txt', 'a'])
q.add_sleeptime(3)
# q.add_proxy(Util.make_proxy_ip_list(proxylist=l))
q.start()

