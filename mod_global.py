# -*- coding: UTF-8 -*-


'''
数据名称：全球经济数据
数据描述：全球经济数据汇总，全球主要国家和地区的宏观经济数据。
数据来源：http://cn.stockq.org/economy/
备注：该数据没有历史数据，只有当前数据
'''


import requests
from lxml import etree
import time


def get_global(since, pfn):
    ts = int(time.time() * 1000)
    dic = {
        'date': time.strftime('%Y-%m-%d',time.localtime(time.time()))
    }
    name_dic = {
        '台湾': '中国台湾',
        '沙地阿拉伯': '沙特阿拉伯',
        '奈及利亚': '尼日利亚',
        '阿联大公国': '阿联酋',
        '孟加拉': '孟加拉国'
    }
    response = requests.get('http://cn.stockq.org/economy/', timeout=300)
    if response.status_code != 200:
        return {}
    res_elements = etree.HTML(response.content)
    for td in res_elements.xpath("//tr[@valign='top']"):
        arr = []
        for tr in td.xpath("./td/text()"):
            if tr in name_dic:
                tr = name_dic[tr]
            elif ',' in tr:
                if '.' in tr:
                    tr = float(tr.replace(',', ''))
                else:
                    tr = int(tr.replace(',', ''))
            elif '%' in tr:
                tr = int(float(tr.replace('%', '')) * 100) / 10000
            elif '.' in tr:
                tr = float(tr)
            elif not (tr >= u'\u4e00' and tr<=u'\u9fa5'):
                tr = int(tr)
            arr.append(tr)
        dic[arr[0]] = {
            'GDP(十亿美元)': arr[1],
            'GDP同比': arr[2],
            'GDP环比': arr[3],
            '利率': arr[4],
            '通胀率': arr[5],
            '失业率': arr[6],
            '政府预算': arr[7],
            '负债/GDP': arr[8],
            '经常账户余额/GDP': arr[9],
            '人口(百万人)': arr[10],
            '人均GDP(美元)': round(arr[1] * 1000 / arr[10])
        }
    pfn(ts, dic)


def on_init():
    return ('GLAL', get_global)


# 测试
if __name__ == '__main__':
    get_global(1483200000000, None)
    pass
    