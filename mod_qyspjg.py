# -*- coding: UTF-8 -*-


'''
数据名称：企业商品价格指数
数据描述：CGPI的前身是国内批发物价指数(Wholesale Price Index，简称WPI)，指数编制始于1994年1月。是反映国内企业之间物质商品集中交易价格变动的统计指标，是比较全面的测度通货膨胀水平和反映经济波动的综合价格指数。CGPI调查是经国家统计局批准、由中国人民银行建立并组织实施的一项调查统计制度。
数据来源：http://data.eastmoney.com/cjsj/qyspjg.html
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


def get_qyspjg(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(10, 0, -1):
        params = (
            ('cb', 'datatable8938281'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '9'),
            ('pageNo', '3'),
            ('pageNum', '3'),
            ('_', '1629362503804'),
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
                    '总指数': {
                        '指数值': str2float(info[1]), 
                        '同比增长': str2float(info[2], '%'), 
                        '环比增长': str2float(info[3], '%')
                    },
                    '农产品': {
                        '指数值': str2float(info[4]), 
                        '同比增长': str2float(info[5], '%'), 
                        '环比增长': str2float(info[6], '%')
                    },
                    '矿产品': {
                        '指数值': str2float(info[7]), 
                        '同比增长': str2float(info[8], '%'), 
                        '环比增长': str2float(info[9], '%')
                    },
                    '煤油电': {
                        '指数值': str2float(info[10]), 
                        '同比增长': str2float(info[11], '%'), 
                        '环比增长': str2float(info[12], '%')
                    },
                }
                pfn(ts, dic)


def on_init():
    return ('QYSPJG', get_qyspjg)


if __name__ == '__main__':
    get_qyspjg(1514736000000, None) # 测试
    pass
