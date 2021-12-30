# -*- coding: UTF-8 -*-


'''
数据名称：外汇和黄金储备(Foreign exchange & gold reserves)
数据描述：外汇又称为外汇存底，是指一国政府所持有的国际储备资产中的外汇部分，即一国政府保有的以外币表示的债权。是一个国家货币当局持有并可以随时兑换外国货币的资产。黄金储备：指一国货币当局持有的，用以平衡国际收支，维持或影响汇率水平，作为金融资产持有的黄金。
数据来源：http://data.eastmoney.com/cjsj/hjwh.html
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


def get_fegr(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('cb', 'datatable7964158'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '16'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629252644311'),
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
                    '国家外汇储备(亿美元)': str2float(info[1]),
                    '外汇同比': str2float(info[2], '%'),
                    '外汇环比': str2float(info[3], '%'),
                    '黄金储备(万盎司)': str2float(info[4]),
                    '黄金同比': str2float(info[5], '%'),
                    '黄金环比': str2float(info[6], '%'),
                }
                pfn(ts, dic)


def on_init():
    return ('FEGR', get_fegr)


if __name__ == '__main__':
    get_fegr(1420041600000, None) # 测试
    pass
    