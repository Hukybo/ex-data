# -*- coding: UTF-8 -*-


'''
数据名称：工业增加值增长
数据描述：工业增加值增长是指工业企业在报告期内以货币形式表现的工业生产活动的最终成果，是指工业企业在一定时期内工业生产活动创造的价值，是国内生产总值的组成部分。公式： 工业增加值=固定资产折旧+劳动者报酬+生产税净值+营业盈余。
数据来源：http://data.eastmoney.com/cjsj/gyzjz.html
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


def mod_gyzjz(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(8, 0, -1):
        params = (
            ('cb', 'datatable5905568'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '0'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629257962972'),
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
                    '同比增长': str2float(info[1], '%'),
                    '累计增长': str2float(info[2], '%')
                }
                pfn(ts, dic)


def on_init():
    return ('GYZJZ', mod_gyzjz)


if __name__ == '__main__':
    mod_gyzjz(1514736000000, None) # 测试
    pass
    