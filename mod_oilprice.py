# -*- coding: UTF-8 -*-


'''
数据名称：汽柴油历史调价信息
数据描述：汽柴油历史调价信息
数据来源：http://data.eastmoney.com/cjsj/oil_default.html
'''


import requests
import time
import re
from datetime import date
import datetime
import json


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def get_oilprice(since, pfn):
    for x in range(23, 0, -1):
        url1 = f'http://datacenter.eastmoney.com/api/data/get?type=RPTA_WEB_YJ_BD&sty=ALL&source=WEB&p={x}&ps=50&st=dim_date&sr=-1&var=gVoEFQTB&rt=52983846'
        url2 = f'http://datacenter-web.eastmoney.com/api/data/get?callback=datatable255108&type=RPTA_WEB_YJ_BD&sty=ALL&st=dim_date&sr=-1&token=894050c76af8597a853f5b408b759f5d&p={x}&ps=10&source=WEB&pageNo=21&pageNum=21&_=1631698599049'
        res = requests.get(url1, timeout=300)
        if len(res.text) < 100 or res.status_code != 200:
            res = requests.get(url2, timeout=300)
            if len(res.text) < 100 or res.status_code != 200:
                continue
            res = res.text
            data = json.loads(res[res.index('(') + 1 : res.index(')')])['result']['data'][::-1]
        else:
            res = res.text
            if '=' not in res and res[-1] != ';':
                continue
            data = json.loads(res.split('=')[1][:-1])['result']['data'][::-1]
        for i in data:
            ymd = re.match(r'(\d+)/(\d+)/(\d+)', i['dim_date'])
            y = int(ymd[1])
            m = int(ymd[2])
            d = int(ymd[3])
            ts = int(time.mktime(time.strptime(str(date(y, m, d) + datetime.timedelta(days=1)), '%Y-%m-%d'))*1000)
            if ts >= since:
                dic = {
                    '日期': i['dim_date'].replace('/', '-'),
                    '汽油(元/吨)': int(i['value']),
                    '柴油(元/吨)': int(i['cy_jg'])
                }
                pfn(ts, dic)


def on_init():
    return ('OILPRICE', get_oilprice)


if __name__ == '__main__':
    get_oilprice(1514736000000, None) # 测试
    pass
    