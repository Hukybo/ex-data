# -*- coding: UTF-8 -*-


'''
数据名称：股票账户统计详细数据
数据描述：股票账户统计详细数据(新)
数据来源：http://data.eastmoney.com/cjsj/gpkhsj.html
'''


import requests
import time
import re
import json


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def get_gpzhsj(since, pfn):
    url_arr = [
        'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=GPKHData&token=894050c76af8597a853f5b408b759f5d&st=SDATE&sr=-1&p=2&ps=50&js=var%20zyNUXPsM={pages:(tp),data:(x)}&rt=52977745',
        'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=GPKHData&token=894050c76af8597a853f5b408b759f5d&st=SDATE&sr=-1&p=1&ps=50&js=var%20jaAUTdai={pages:(tp),data:(x)}&rt=52977808'
    ]
    for x in url_arr:
        res = requests.get(x, timeout=300)
        if res.status_code != 200:
            continue
        res = res.text
        for i in json.loads(res.split('data:')[1][:-1])[::-1]:
            m = re.match(r'(\d+)年(\d+)月', i['SDATE'])
            y = int(m[1])
            m = int(m[2]) + 1
            if m > 12:
                y += 1
                m -= 12
            ts = s2t('%d-%02d' % (y, m), "%Y-%m")
            if i['XZHB'] == '-':
                i['XZHB'] = 'NaN'
            if i['XZTB'] == '-':
                i['XZTB'] = 'NaN'
            if ts >= since:
                dic = {
                    '日期': i['SDATE'],
                    '新增投资者': {'数量(万户)': i['XZSL'], '同比增长': i['XZHB'], '环比增长': i['XZTB']},
                    '期末投资者(万户)': {'总量': i['QMSL'], 'A股账户': i['QMSL_A'], 'B股账户': i['QMSL_B']},
                    '沪深总市值(亿)': i['HSZSZ'], 
                    '沪深户均市值(万)': i['HJZSZ'],
                    '上证指数': {'收盘': i['SZZS'], '涨跌幅': i['SZZDF']}
                }
                pfn(ts, dic)


def on_init():
    return ('GPZHSJ', get_gpzhsj)


if __name__ == '__main__':
    get_gpzhsj(1514736000000, None) # 测试
    pass
    