# -*- coding: UTF-8 -*-


'''
数据名称：存款准备金率
数据描述：存款准备金是指金融机构为保证客户提取存款和资金清算需要而准备的，是缴存在中央银行的存款，中央银行要求的存款准备金占其存款总额的比例就是存款准备金率。
数据来源：http://data.eastmoney.com/cjsj/ckzbj.html
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


def get_ckzbj(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(3, 0, -1):
        params = (
            ('cb', 'datatable3285662'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '23'),
            ('pageNo', '3'),
            ('pageNum', '3'),
            ('_', '1629197945828'),
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
                    '公布时间': info[0],
                    '生效时间': info[1],
                    '大型金融机构': {
                        '调整前': str2float(info[2], '%'), 
                        '调整后': str2float(info[3], '%'), 
                        '调整幅度': str2float(info[4], '%')
                    },
                    '中小金融机构': {
                        '调整前': str2float(info[5], '%'), 
                        '调整后': str2float(info[6], '%'), 
                        '调整幅度': str2float(info[7], '%')
                    }
                }
                pfn(ts, dic)


def on_init():
    return ('CKZBJ', get_ckzbj)


if __name__ == '__main__':
    get_ckzbj(1420041600000, None) # 测试
    pass
