# -*- coding: UTF-8 -*-


'''
数据名称：采购经理人指数(PMI)
数据描述：采购经理人指数是经济先行指标中一项非常重要的附属指标，它衡量制造业在生产、新订单、商品价格、存货、雇员、订单交货、新出口订单和进口等八个方面状况的指数。具有其高度的时效性。
数据来源：http://data.eastmoney.com/cjsj/pmi.html
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


def get_pmi(since, pfn):
    headers = {
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('cb', 'datatable3422373'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '21'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629358558537'),
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
                    '制造业': {
                        '指数': str2float(info[1]), 
                        '同比增长': str2float(info[2], '%'), 
                    },
                    '非制造业': {
                        '指数': str2float(info[3]), 
                        '同比增长': str2float(info[4], '%'), 
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('PMI', get_pmi)


if __name__ == '__main__':
    get_pmi(1514736000000, None) # 测试
    pass
    