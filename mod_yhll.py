# -*- coding: UTF-8 -*-


'''
数据名称：银行利率调整
数据描述：表示一定时期内利息量与本金的比率，通常用百分比表示，按年计算则称为年利率。其计算公式是：利息率= 利息量 ÷ 本金÷时间×100%
数据来源：http://data.eastmoney.com/cjsj/yhll.html
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


def get_yhll(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(2, 0, -1):
        params = (
            ('cb', 'datatable7114872'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '13'),
            ('pageNo', '2'),
            ('pageNum', '2'),
            ('_', '1629366538971'),
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
                    '存款基准利率': {
                        '调整前': str2float(info[1], '%'), 
                        '调整后': str2float(info[2], '%'), 
                        '调整幅度': str2float(info[3], '%')
                    },
                    '贷款基准利率': {
                        '调整前': str2float(info[4], '%'), 
                        '调整后': str2float(info[5], '%'), 
                        '调整幅度': str2float(info[6], '%')
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('YHLL', get_yhll)


if __name__ == '__main__':
    get_yhll(1325347200000, None) # 测试
    pass
