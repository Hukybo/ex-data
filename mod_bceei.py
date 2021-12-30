# -*- coding: utf-8 -*-


'''
数据名称：企业景气及企业家信心指数(Business Climate & Entrepreneur Expectation Index)
数据描述：企业家信心指数也称"宏观经济景气指数"，是根据企业家对企业外部市场经济环境与宏观政策的认识、看法、判断与预期而编制的指数，用以综合反映企业家对宏观经济环境的感受与信心。
数据来源：http://data.eastmoney.com/cjsj/qyjqzs.html
'''


import requests
import time
import json


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


def get_bceei(since, pfn):
    headers = {
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(4, 0, -1):
        params = (
            ('cb', 'datatable8145907'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '8'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629178520760'),
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
                    '企业景气指数': {
                        '指数': str2float(info[1]), 
                        '同比': str2float(info[2], '%'), 
                        '环比': str2float(info[3], '%')
                    },
                    '企业家信心指数': {
                        '指数': str2float(info[4]), 
                        '同比': str2float(info[5], '%'), 
                        '环比': str2float(info[6], '%')
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('BCEEI', get_bceei)


if __name__ == '__main__':
    get_bceei(1441382400000, None) # 测试
    pass
