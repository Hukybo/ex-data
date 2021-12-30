# -*- coding: UTF-8 -*-


'''
数据名称：货币供应量
数据描述：货币供应量亦称货币存量、货币供应，指某一时点流通中的现金量和存款量之和。货币供应量是各国中央银行编制和公布的主要经济统计指标之一。它由包括中央银行在内的金融机构供应的存款货币和现金货币两部分构成。世界各国中央银行货币估计口径不完全一致，但划分的基本依据是一致的，即流动性大小。
数据来源：http://data.eastmoney.com/cjsj/hbgyl.html
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


def get_hbgyl(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('cb', 'datatable6585761'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '11'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629260458626'),
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
                    '货币和准货币(M2)': {
                        '数量(亿元)': str2float(info[1]), 
                        '同比增长': str2float(info[2], '%'), 
                        '环比增长': str2float(info[3], '%')
                    },
                    '货币(M1)': {
                        '数量(亿元)': str2float(info[4]), 
                        '同比增长': str2float(info[5], '%'), 
                        '环比增长': str2float(info[6], '%')
                    },
                    '流通中的现金(M0)': {
                        '数量(亿元)': str2float(info[7]), 
                        '同比增长': str2float(info[8], '%'), 
                        '环比增长': str2float(info[9], '%')
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('HBGYL', get_hbgyl)


if __name__ == '__main__':
    get_hbgyl(1514736000000, None) # 测试
    pass
    