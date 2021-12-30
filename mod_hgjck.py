# -*- coding: UTF-8 -*-


'''
数据名称：海关进出口增减情况一览表
数据描述：海关进出口增减指实际进出我国国境的货物总金额。进出口总额用以观察一个国家在对外贸易方面的总规模。我国规定出口货物按离岸价格统计，进口货物按到岸价格统计。
数据来源：http://data.eastmoney.com/cjsj/hgjck.html
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
    if ratio == 100000:
        return float('%.2f' % (float(strs) / 100000))
    else:
        return float('%.2f' % float(strs))


def get_hgjck(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('cb', 'datatable5099829'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '1'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629261712061'),
        )
        response = requests.get('http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx', headers=headers, params=params, verify=False, timeout=300)
        if response.status_code != 200:
            continue
        text = response.text
        if 'data:' not in text or ',pages' not in text:
            continue
        for i in json.loads(text[text.index('data:') + 5 : text.index(',pages')])[::-1]:
            info = i.split(',')
            ts = s2t(info[0], "%Y-%m-%d")
            if ts >= since:
                dic = {
                    '日期': info[0],
                    '当月出口额': {
                        '金额(亿美元)': str2float(info[1], 100000), 
                        '同比增长': str2float(info[2], '%'), 
                        '环比增长': str2float(info[3], '%')
                    },
                    '当月进口额': {
                        '金额(亿美元)': str2float(info[4], 100000), 
                        '同比增长': str2float(info[5], '%'), 
                        '环比增长': str2float(info[6], '%')
                    },
                    '累计出口额': {
                        '金额(亿美元)': str2float(info[7], 100000), 
                        '同比增长': str2float(info[8], '%'), 
                    },
                    '累计进口额': {
                        '金额(亿美元)': str2float(info[9], 100000), 
                        '同比增长': str2float(info[10], '%'), 
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('HGJCK', get_hgjck)


if __name__ == '__main__':
    get_hgjck(1514736000000, None) # 测试
    pass
    