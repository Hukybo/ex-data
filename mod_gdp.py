# -*- coding: UTF-8 -*-


import requests
import time
import json


'''
数据名称：国内生产总值(GDP)
数据描述：国内生产总值，Gross Domestic Product，简称GDP，是指在一定时期内（一个季度或一年），一个国家或地区的经济中所生产出的全部最终产品和劳务的价值，常被公认为衡量国家经济状况的最佳指标。
数据来源：http://data.eastmoney.com/cjsj/gdp.html
'''


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def date2quarter(date):
    if date[6] == '3':
        num = '1'
    if date[6] == '6':
        num = '2'
    if date[6] == '9':
        num = '3'
    if date[6] == '2':
        num = '4'
    return date[:4] + f'年第{num}季度'


def str2float(strs, ratio=None):
    if strs == '':
        return 'NaN'
    if ratio == '%':
        return float('%.4f' % (float(strs) / 100))
    else:
        return float('%.2f' % float(strs))


def get_gdp(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(4, 0, -1):
        params = (
            ('cb', 'datatable3833625'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '20'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629254213640'),
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
                    '季度': date2quarter(info[0]),
                    '国内生产总值': {
                        '绝对值(亿元)': str2float(info[1]), 
                        '同比增长': str2float(info[2], '%'), 
                    },
                    '第一产业': {
                        '绝对值(亿元)': str2float(info[3]), 
                        '同比增长': str2float(info[4], '%'), 
                    },
                    '第二产业': {
                        '绝对值(亿元)': str2float(info[5]), 
                        '同比增长': str2float(info[6], '%'), 
                    },
                    '第三产业': {
                        '绝对值(亿元)': str2float(info[7]), 
                        '同比增长': str2float(info[8], '%'), 
                    },
                }
                pfn(ts, dic)


def on_init():
    return ('GDP', get_gdp)


if __name__ == '__main__':
    get_gdp(1420041600000, None) # 测试
    pass
    