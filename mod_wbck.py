# -*- coding: UTF-8 -*-


'''
数据名称：本外币存款
数据描述：人民币是本位币，其他国家货币的都是外币。以上币种在国内金融机构的存款统称本外币存款。
数据来源：http://data.eastmoney.com/cjsj/wbck.html
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


def get_wbck(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(8, 0, -1):
        params = (
            ('cb', 'datatable6455657'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '18'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629365502936'),
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
                    '累计(亿元)': str2float(info[4]),
                }
                pfn(ts, dic)


def on_init():
    return ('WBCK', get_wbck)


if __name__ == '__main__':
    get_wbck(1514736000000, None) # 测试
    pass

