# -*- coding: UTF-8 -*-


'''
数据名称：居民消费价格指数(CPI)
数据描述：居民消费价格指数是反映与居民生活有关的产品及劳务价格统计出来的物价变动指标，以百分比变化为表达形式。它是衡量通货膨胀的主要指标之一。一般定义超过3％为通货膨胀，超过5％就是比较严重的通货膨胀。
数据来源：http://data.eastmoney.com/cjsj/cpi.html
'''


import json
import time
import requests


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def str2float(strs, ratio=None):
    if strs == '':
        return 'NaN'
    if ratio == '%':
        return float('%.4f' % (float(strs) / 100))
    else:
        return float('%.2f' % float(strs))


def get_cpi(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('cb', 'datatable8439057'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '19'),
            ('pageNo', '3'),
            ('pageNum', '3'),
            ('_', '1629200901961'),
        )
        response = requests.get('http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx', headers=headers, params=params, verify=False, timeout=300)
        if response.status_code != 200:
            continue
        text = response.text
        if 'data' not in text or ',pages' not in text:
            continue
        for i in json.loads(text[text.index('data:') + 5 : text.index(',pages')])[::-1]:
            info = i.split(',')
            ts = s2t(info[0], "%Y-%m-%d")
            if ts >= since:
                dic = {
                    '月份': info[0],
                    '全国': {
                        '当月': str2float(info[1]), 
                        '同比增长': str2float(info[2], '%'), 
                        '环比增长': str2float(info[3], '%'),
                        '累计': str2float(info[4])
                    },
                    '城市': {
                        '当月': str2float(info[5]), 
                        '同比增长': str2float(info[6], '%'), 
                        '环比增长': str2float(info[7], '%'),
                        '累计': str2float(info[8])
                    },
                    '农村': {
                        '当月': str2float(info[9]), 
                        '同比增长': str2float(info[10], '%'), 
                        '环比增长': str2float(info[11], '%'),
                        '累计': str2float(info[12])
                    },
                }
                pfn(ts, dic)


def on_init():
    return ('CPI', get_cpi)


if __name__ == '__main__':
    get_cpi(1420041600000, None) # 测试
    pass
