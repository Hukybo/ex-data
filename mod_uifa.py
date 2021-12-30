# -*- coding: UTF-8 -*-


'''
数据名称：城镇固定资产投资(Urban Investment in Fixed Assets)
数据描述：固定资产投资是建造和购置固定资产的经济活动，即固定资产再生产活动。固定资产再生产过程包括固定资产更新（局部和全部更新）、改建、扩建、新建等活动。新的企业财务会计制度规定：固定资产局部更新的大修理作为日常生产活动的一部分，发生的大修理费用直接在成本中列支。
数据来源：http://data.eastmoney.com/cjsj/gdzctz.html
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


def get_uifa(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(8, 0, -1):
        params = (
            ('cb', 'datatable9701762'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '12'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629363654283'),
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
                    '当月(亿元)': str2float(info[1]),
                    '当月同比增长': str2float(info[2], '%'),
                    '当月环比增长': str2float(info[3], '%'),
                    '自年初累计(亿元)': str2float(info[4]),
                }
                pfn(ts, dic)


def on_init():
    return ('UIFA', get_uifa)


if __name__ == '__main__':
    get_uifa(1514736000000, None) # 测试
    pass
