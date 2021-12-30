# -*- coding: UTF-8 -*-


'''
数据名称：消费者信心指数(Index of Consumer Sentiment，ICS)
数据描述：消费者信心指数是反映消费者信心强弱的指标，是综合反映并量化消费者对当前经济形势评价和对经济前景、收入水平、收入预期以及消费心理状态的主观感受，是预测经济走势和消费趋向的一个先行指标，是监测经济周期变化不可缺少的依据。
数据来源：http://data.eastmoney.com/cjsj/xfzxx.html
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
    if ratio == 100000:
        return int('%.0f' % (float(strs) / 100000))
    else:
        return float('%.2f' % float(strs))


def get_ics(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'Referer': 'https://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('cb', 'datatable5483088'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '4'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629267398507'),
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
                    '消费者信心指数': {
                        '指数值': str2float(info[1]), 
                        '同比增长': str2float(info[2], '%'), 
                        '环比增长': str2float(info[3], '%')
                    },
                    '消费者满意指数': {
                        '指数值': str2float(info[4]), 
                        '同比增长': str2float(info[5], '%'), 
                        '环比增长': str2float(info[6], '%')
                    },
                    '消费者预期指数': {
                        '指数值': str2float(info[7]), 
                        '同比增长': str2float(info[8], '%'), 
                        '环比增长': str2float(info[9], '%')
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('ICS', get_ics)


if __name__ == '__main__':
    get_ics(1514736000000, None) # 测试
    pass
    