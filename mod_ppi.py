# -*- coding: UTF-8 -*-


'''
数据名称：工业品出厂价格指数(PPI)
数据描述：工业品出厂价格指数是衡量工业企业产品出厂价格变动趋势和变动程度的指数，是反映全部工业产品出厂价格总水平的变动趋势和程度的相对数，也是制定有关经济政策和国民经济核算的重要依据。
数据来源：http://data.eastmoney.com/cjsj/ppi.html
'''


import requests
import time
import json


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def str2float(strs, ratio=None):
    if strs == '':
        return 'NaN'
    if ratio == '%':
        return float('%.4f' % (float(strs) / 100))
    else:
        return float('%.2f' % float(strs))


def get_ppi(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(10, 0, -1):
        params = (
            ('cb', 'datatable4304217'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '22'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629359245625'),
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
                    '当月': str2float(info[1]),
                    '当月同比增长': str2float(info[2], '%'),
                    '累计': str2float(info[3]),
                }
                pfn(ts, dic)


def on_init():
    return ('PPI', get_ppi)


if __name__ == '__main__':
    get_ppi(946656000000, None) # 测试
    pass
  