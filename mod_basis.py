# -*- coding: UTF-8 -*-


'''
数据名称：基差
数据描述：基差是某一特定商品于某一特定的时间和地点的现货价格与期货价格之差。它的计算方法是现货价格减去期货价格。若现货价格低于期货价格，基差为负值；现货价格高于期货价格，基差为正值。
数据来源：http://www.100ppi.com/sf2
'''


import requests
import time
import re
import random
from datetime import date
import datetime
from lxml import etree
import random


def t2s(t=None, fmt="%Y-%m-%d %H:%M:%S"):
    # 时间戳转日期
    if t is None:
        t = time.time()
    else:
        t /= 1000
    return time.strftime(fmt, time.localtime(t))


def since_to_datearr(since):
    # 输入时间戳
    # 输出时间戳到当前时间的日期数组：['2020-01-01',]
    since = t2s(since).split(' ')[0]
    date_split = list(map(int, since.split('-')))
    # 返回日期数组
    begin = datetime.date(date_split[0], date_split[1], date_split[2])
    end = datetime.date.today()
    arr = []
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        arr.append(str(day))
    return arr


def arr_reserve_chinese(arr):
    # 将列表中的元素只保留中文
    new_arr = []
    for i in arr:
        if i == 'PTA':
            new_arr.append(i)
        else:
            pattern = re.compile(r'[^\u4e00-\u9fa5]')
            chinese = re.sub(pattern, '', i)
            new_arr.append(chinese)
    return new_arr


def str_to_num(str_arr):
    # 将列表是字符串的元素转换为数字
    # 如果有小数点就转换为float
    # 如果无小数点就转换为int
    new_arr = []
    for i in str_arr:
        if '.' in i:
            new_arr.append(float(i))
        else:
            new_arr.append(int(i))
    return new_arr


def get_basis(since, pfn):
    request_headers = {
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Referer': 'http://www.100ppi.com/sf2/'
    }
    if since == 0:
        since = 1294156800000
    for x in since_to_datearr(since):
        time.sleep(random.uniform(0, 5))
        url = f"http://www.100ppi.com/sf2/day-{x}.html"
        res = requests.get(url, headers=request_headers, timeout=300)
        if res.status_code != 200:
            continue
        res_elements = etree.HTML(res.content.decode('UTF-8'))
        keys = []
        values = []
        for y in res_elements.xpath("//tr[@align='center']"):
            keys = arr_reserve_chinese(
                y.xpath("//tr[@align='center']//a/text()"))
            values = str_to_num(
                y.xpath("//tr[@align='center']//td[1]/font/text()"))
            break
        dictionary = dict(zip(keys, values))
        if len(dictionary) > 0:
            dictionary['日期'] = x
        myd = re.match(r'(\d+)-(\d+)-(\d+)', x)
        y = int(myd[1])
        m = int(myd[2])
        d = int(myd[3])
        ts = int(time.mktime(time.strptime(
            str(date(y, m, d) + datetime.timedelta(days=1)), '%Y-%m-%d'))*1000)
        if ts >= since:
            if dictionary:
                pfn(ts, dictionary)


def on_init():
    return ('BASIS', get_basis)


if __name__ == '__main__':
    get_basis(1630771200000, None) # 测试
    pass
    