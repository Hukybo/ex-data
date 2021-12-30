# -*- coding: UTF-8 -*-


'''
数据名称：交易结算资金(银证转账)
数据描述：银证转账是指将股民在银行开立的个人结算存款账户与证券公司的资金账户建立对应关系，通过银行的电话银行、网上银行、网点自助设备和证券公司的电话、网上交易系统及证券公司营业部的自助设备将资金在银行和证券公司之间划转。
数据来源：http://data.eastmoney.com/cjsj/bankTransfer.html
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


def get_btsf(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://data.eastmoney.com/cjsj/banktransfer.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(9, 0, -1):
        params = (
            ('p', str(i)),
            ('ps', '20'),
            ('pageNo', '2'),
            ('pageNum', '2'),
        )
        response = requests.get('http://data.eastmoney.com/dataapi/cjsj/getbanktransferdata', headers=headers, params=params, verify=False, timeout=300)
        if response.status_code != 200:
            continue
        text = response.text
        data = json.loads(text)
        if 'data' not in data:
            continue
        for i in data['data'][::-1]:
            ts = s2t(i['EndDate'], "%Y-%m-%d")
            if ts >= since:
                dic = {
                    '开始时间': i['StartDate'],
                    '截至时间': i['EndDate'],
                    '交易结算资金期末余额(亿)': int(i['SettleFunds']),
                    '交易结算资金日均余额(亿)': int(i['AvgSettleFunds']),
                    '银证转账增加额(亿)': int(i['SettleFundsAdd']),
                    '银证转账减少额(亿)': int(i['SettleFundsLow']),
                    '银证转账变动净额(亿)': int(i['SettleFundsNet']),
                    '上证指数收盘': str2float(i['SHIndex']),
                    '上证指数涨跌幅': str2float(i['SHIndexChangeRatio'], '%'),
                }
                pfn(ts, dic)


def on_init():
    return ('BTSF', get_btsf)


if __name__ == '__main__':
    get_btsf(1441382400000, None)
    pass
    