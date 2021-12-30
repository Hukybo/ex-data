# -*- coding: UTF-8 -*-


'''
数据名称：财政收入
数据描述：财政收入是指政府为履行其职能、实施公共政策和提供公共物品与服务需要而筹集的一切资金的总和。它是衡量一国政府财力的重要指标，政府在社会经济活动中提供公共物品和服务的范围和数量，在很大程度上决定于财政收入的充裕状况。
数据来源：http://data.eastmoney.com/cjsj/czsr.html
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


def get_czsr(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(8, 0, -1):
        params = (
            ('cb', 'datatable8239063'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '14'),
            ('pageNo', '3'),
            ('pageNum', '3'),
            ('_', '1629203587696'),
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
                    '当月(亿元)': str2float(info[1]),
                    '当月同比增长': str2float(info[2], '%'),
                    '环比增长': str2float(info[3], '%'),
                    '累计(亿元)': info[4],
                    '累计同比增长': str2float(info[5], '%'),
                }
                pfn(ts, dic)


def on_init():
    return ('CZSR', get_czsr)


if __name__ == '__main__':
    get_czsr(1420041600000, None) # 测试
    pass
