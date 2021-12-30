# -*- coding: UTF-8 -*-


'''
数据名称：全国股票交易统计表
数据描述：股票账户统计详细数据(旧)
数据来源：http://data.eastmoney.com/cjsj/gpjytj.html
'''


import requests
import time
import json


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def str2int(strs):
    if strs == '':
        return 'NaN'
    return int('%.0f' % float(strs))


def get_gpjytj(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    params = (
        ('cb', 'jQuery112300404071026934687_1629255155914'),
        ('type', 'GJZB'),
        ('sty', 'ZGZB'),
        ('js', '([(x)])'),
        ('p', '1'),
        ('ps', '200'),
        ('mkt', '2'),
        ('_', '1629255155915'),
    )
    response = requests.get('http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx', headers=headers, params=params, verify=False, timeout=300)
    if response.status_code != 200:
        return {}
    text = response.text
    if '(' not in text and ')' not in text:
        return {}
    for i in json.loads(text[text.index('(') + 1 : text.index(')')])[::-1]:
        arr = i.split(',')
        ts = s2t(arr[0], "%Y-%m-%d")
        if ts >= since:
            dic = {
                '日期': arr[0],
                '发行总股本': {'上海': str2int(arr[1]), '深圳': str2int(arr[2])},
                '市价总值': {'上海': str2int(arr[3]), '深圳': str2int(arr[4])},
                '成交金额': {'上海': str2int(arr[5]), '深圳': str2int(arr[6])},
                '成交量': {'上海': str2int(arr[7]), '深圳': str2int(arr[8])},
                'A股最高综合股价指数': {'上海': str2int(arr[9]), '深圳': str2int(arr[10])},
                'A股最低综合股价指数': {'上海': str2int(arr[11]), '深圳': str2int(arr[12])}
            }
            pfn(ts, dic)


def on_init():
    return ('GPJYTJ', get_gpjytj)


if __name__ == '__main__':
    get_gpjytj(1420041600000, None) # 测试
    pass
    