# -*- coding: UTF-8 -*-


'''
数据名称：贷款市场报价利率
数据描述：贷款市场报价利率是由具有代表性的报价行，根据本行对最优质客户的贷款利率，以公开市场操作利率（主要指中期借贷便利利率）加点形成的方式报价，由中国人民银行授权全国银行间同业拆借中心计算并公布的基础性的贷款参考利率，各金融机构应主要参考LPR进行贷款定价。
数据来源：http://data.eastmoney.com/cjsj/globalRateLPR.html
'''


import requests
import time
import re
from datetime import date
import datetime
import json


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt)) * 1000)


def str_to_num(s):
    if s == '-' or s == None:
        return 'NaN'
    else:
        return s


def get_lrp(since, pfn):
    for x in range(31, 0, -1):
        url = f'http://datacenter.eastmoney.com/api/data/get?type=RPTA_WEB_RATE&sty=ALL&token=894050c76af8597a853f5b408b759f5d&p={x}&ps=50&st=TRADE_DATE&sr=-1&var=ouOwuWss&rt=53001111'
        res = requests.get(url, timeout=300)
        if res.status_code != 200:
            continue
        res = res.text
        for i in json.loads(res.split('=')[1][:-1])['result']['data'][::-1]:
            ymd = re.match(r'(\d+)-(\d+)-(\d+) 00:00:00', i['TRADE_DATE'])
            y = int(ymd[1])
            m = int(ymd[2])
            d = int(ymd[3])
            ts = int(time.mktime(time.strptime(str(date(y, m, d) + datetime.timedelta(days=1)), '%Y-%m-%d'))*1000)
            if ts >= since:
                dic = {
                    '日期': i['TRADE_DATE'].split(' ')[0],
                    'LPR_1Y利率(%)': str_to_num(i['LPR1Y']),
                    'LPR_5Y利率(%)': str_to_num(i['LPR5Y']),
                    '短期贷款利率:6个月至1年(含)(%)': str_to_num(i['RATE_1']),
                    '中长期贷款利率:5年以上(%)': str_to_num(i['RATE_2'])
                }
                pfn(ts, dic)


def on_init():
    return ('LRP', get_lrp)


if __name__ == '__main__':
    get_lrp(0, None) # 测试
    pass
    