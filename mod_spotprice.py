# -*- coding: UTF-8 -*-


'''
数据名称：现货价格
数据描述：现货价格是指商品在现货交易中的成交价格。现货交易是一经成交立即交换的买卖行为，一般是买主即时付款，但也可以采取分期付款和延期交付的方式。由于付款方式的不同，同一现货在同一时期往往可能出现不同的价格。
数据来源：http://www.100ppi.com/sf2
'''


import requests
import time
import re
import random
import datetime
from lxml import etree
import random


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


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


def str_to_int_or_float(str_arr):
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


def str_to_num(s):
    if isinstance(s, int) or isinstance(s, float):
        return s
    if ',' in s and '.' in s:
        return float(s.replace(',', ''))
    if '.' in s:
        return float(s)
    if ',' in s:
        return int(s.replace(',', ''))
    if s == '-':
        return 'NaN'
    if '%' in s:
        return round(float(s.split('%')[0]) / 100, 4)
    if s.isdigit():
        return int(s)
    return 'NaN'


def arr_to_num(arr):
    new_arr = []
    for i in range(0, len(arr), 8):
        new_arr.append(str_to_num("".join(arr[i].split())))
    return new_arr
    

def get_spotprice(since, pfn):
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
            values = arr_to_num(
                y.xpath("//tr[@align='center']/td/text()"))
            break
        if len(keys) == len(values):
            dictionary = dict(zip(keys, values))
        else:
            continue
        if len(dictionary) > 0:
            dictionary['日期'] = x
        myd = re.match(r'(\d+)-(\d+)-(\d+)', x)
        y = int(myd[1])
        m = int(myd[2])
        d = int(myd[3])
        ts = int(time.mktime(time.strptime(
            str(datetime.date(y, m, d) + datetime.timedelta(days=1)), '%Y-%m-%d'))*1000)
        if ts >= since:
            if dictionary:
                pfn(ts, dictionary)


def on_init():
    return ('SPOTPRICE', get_spotprice)


if __name__ == '__main__':
    get_spotprice(0, None) # 测试
    pass
