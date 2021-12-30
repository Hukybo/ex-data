# -*- coding: UTF-8 -*-


'''
数据名称：全国税收收入
数据描述：税收是指国家为了向社会提供公共产品、满足社会共同需要、按照法律的规定，参与社会产品的分配、强制、无偿取得财政收入的一种规范形式。税收是一种非常重要的政策工具。
数据来源：http://data.eastmoney.com/cjsj/qgsssr.html
'''


import json
import time
import requests


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


def get_qgsssr(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(4, 0, -1):
        params = (
            ('cb', 'datatable4882634'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '3'),
            ('pageNo', '3'),
            ('pageNum', '3'),
            ('_', '1629361685313'),
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
                    '季度': date2quarter(info[0]),
                    '税收收入合计(亿元)': str2float(info[1]), 
                    '较上年同期': str2float(info[2], '%'), 
                    '季度环比': str2float(info[3], '%')
                }
                pfn(ts, dic)


def on_init():
    return ('QGSSSR', get_qgsssr)


if __name__ == '__main__':
    get_qgsssr(1514736000000, None) # 测试
    pass


