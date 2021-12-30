# -*- coding: UTF-8 -*-


'''
数据名称：外商直接投资数据(FDI)
数据描述：外商直接投资指外国企业和经济组织或个人(包括华侨、港澳台胞以及我国在境外注册的企业)按我国有关政策、法规，用现汇、实物、技术等在我国境内开办外商独资企业、与我国境内的企业或经济组织共同举办中外合资经营企业、合作经营企业或合作开发资源的投资(包括外商投资收益的再投资)，以及经政府有关部门批准的项目投资总额内企业从境外借入的资金。
数据来源：http://data.eastmoney.com/cjsj/fdi.html
'''


import json
import time
import requests


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def str2float(strs, ratio=None):
    if strs == '':
        return 'NaN'
    if ratio == '%':
        return float('%.4f' % (float(strs) / 100))
    if ratio == 100000:
        return float('%.2f' % (int(strs) / 100000))
    else:
        return float('%.2f' % float(strs))


def get_fdi(since, pfn):
    headers = {
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://data.eastmoney.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    for i in range(8, 0, -1):
        params = (
            ('cb', 'datatable8917283'),
            ('type', 'GJZB'),
            ('sty', 'ZGZB'),
            ('js', '({data:[(x)],pages:(pc)})'),
            ('p', str(i)),
            ('ps', '20'),
            ('mkt', '15'),
            ('pageNo', '3'),
            ('pageNum', '3'),
            ('_', '1629251373120'),
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
                    '月份': info[0],
                    '当月(亿美元)': str2float(info[1], 100000),
                    '当月同比增长': str2float(info[2], '%'),
                    '环比增长': str2float(info[3], '%'),
                    '累计(亿美元)': str2float(info[4], 100000),
                    '累计同比增长': str2float(info[5], '%'),
                }
                pfn(ts, dic)


def on_init():
    return ('FDI', get_fdi)


if __name__ == '__main__':
    get_fdi(946656000000, None) # 测试
    pass
    