# -*- coding: UTF-8 -*-


import requests
import json
from lxml import etree
import time
import datetime
import random
from io import BytesIO
from zipfile import ZipFile


'''
数据名称：交易所会员成交量及持仓明细(Daily traded positions)
数据描述：当期货合约持仓量达到规定条件时，交易所将公布该月份合约前20名期货公司会员的成交量、买持仓量和卖持仓量，以及该合约所属期货品种期货公司会员、非期货公司会员的总成交量、总买持仓量和总卖持仓量。
数据来源：上期所、大商所、郑商所、上海能源等官网
'''


def to_timestamp(date_str):
    # 日期转时间戳(非整点)
    dates = date_str.split(' ')[0] + " 18:00:00"
    time_array = time.strptime(dates, "%Y-%m-%d %H:%M:%S")
    return int(round(time.mktime(time_array) * 1000))


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def t2s(t=None, fmt="%Y-%m-%d %H:%M:%S"):
    # 时间戳转日期
    if t is None:
        t = time.time()
    else:
        t /= 1000
    return time.strftime(fmt, time.localtime(t))


def to_timestamp_zero(date_str):
    # 日期转时间戳(整点)
    dates = date_str.split(' ')[0] + " 00:00:00"
    time_array = time.strptime(dates, "%Y-%m-%d %H:%M:%S")
    return int(round(time.mktime(time_array) * 1000))


def date_arr(since):
    # 输入时间戳
    # 输出时间戳到当前时间的二维数组：[['20200501', '2020-05-01', 5, 1588327200000, 1588348800000],]
    date_split = list(map(int, t2s(since).split(' ')[0].split('-')))
    # 返回日期数组
    begin = datetime.date(date_split[0], date_split[1], date_split[2])
    end = datetime.date.today()
    arr = []
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        arr.append([str(day).replace('-', ''), str(day),
                    day.weekday() + 1, to_timestamp(str(day)), to_timestamp_zero(str(day)) + 86400000])
    return arr


def keep_chinese(content):
    # 字符串只保留中文
    new_str = ''
    for i in content:
        if i >= u'\u4e00' and i <= u'\u9fa5':
            new_str = new_str + i
    return new_str


def str_to_int(con):
    # 字符串转换为整型或浮点型
    if isinstance(con, int) or isinstance(con, float):
        return con
    if '.' in con:
        return float(con.replace(',', ''))
    if ',' in con:
        return int(con.replace(',', ''))
    elif con == '-':
        return 'NaN'
    elif 'E' in con:
        sp = con.split('E')
        return float(sp[0]) * int('1' + '0' * int(sp[1]))
    try:
        return int(con)
    except:
        return 'NaN'


def is_have_data(dic):
    num = 0
    for i in dic:
        if dic[i] == {}:
            num = num + 1
        if num >= len(dic) - 1:
            return False
    return True


def shfe_dtp(dates):
    # 获取上期所会员成交及持仓明细
    # 数据来源：上期所
    # 数据地址：http://www.shfe.com.cn/statements/dataview.html?paramid=kx
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'If-Modified-Since': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'http://www.shfe.com.cn/statements/dataview.html?paramid=pm',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    url = f'http://www.shfe.com.cn/data/dailydata/kx/pm{dates}.dat'
    res = requests.get(url, headers=headers, timeout=300)
    if res.status_code != 200:
        return {}
    res = res.text
    data = {}
    if res[0] == '{':
        for x in json.loads(res)['o_cursor']:
            out_arr = ['', '期货公司', '非期货公司']
            if x['PARTICIPANTABBR1'].replace(' ', '') in out_arr:
                continue
            code_id = x['INSTRUMENTID'].replace(' ', '')
            fc1 = x['PARTICIPANTABBR1'].replace(' ', '')
            fc2 = x['PARTICIPANTABBR2'].replace(' ', '')
            fc3 = x['PARTICIPANTABBR3'].replace(' ', '')
            if code_id not in data:
                data[code_id] = {}
            if fc1 not in data[code_id]:
                data[code_id][fc1] = {}
            if fc2 not in data[code_id]:
                data[code_id][fc2] = {}
            if fc3 not in data[code_id]:
                data[code_id][fc3] = {}
            data[code_id][fc1]['成交量'] = str_to_int(x['CJ1'])
            data[code_id][fc1]['成交量增减'] = str_to_int(x['CJ1_CHG'])
            data[code_id][fc2]['持买单量'] = str_to_int(x['CJ2'])
            data[code_id][fc2]['持买单量增减'] = str_to_int(x['CJ2_CHG'])
            data[code_id][fc3]['持卖单量'] = str_to_int(x['CJ3'])
            data[code_id][fc3]['持卖单量增减'] = str_to_int(x['CJ3_CHG'])
    return data


def dce_dtp(dates):
    # 获取大商所会员成交及持仓明细
    # 数据来源：大商所
    # 数据地址：http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rcjccpm/index.html
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://www.dce.com.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    dates = dates.split('-')
    month = int(dates[1]) - 1
    url = f'http://www.dce.com.cn/publicweb/quotesdata/exportMemberDealPosiQuotesBatchData.html?year={dates[0]}&month={month}&day={dates[2]}'
    res = requests.get(url, headers=headers, timeout=300)
    if res.status_code != 200:
        return {}
    res = res.content
    data = {}
    try:
        zipfile = ZipFile(BytesIO(bytes(res)), "r")
    except:
        return {}
    for x in zipfile.namelist():
        code_id = x.split('_')[1]
        data[code_id] = {}
        for line in zipfile.open(x).readlines():
            try:
                line = line.decode('utf-8')
            except:
                line = line.decode('gbk')
            if '\t' in line:
                arr = line.split('\t')
            elif ' ' in line:
                arr = line.split(' ')
            new_arr = []
            for y in arr:
                y = y.replace('\n', '').replace('\r', '')
                if y != '':
                    new_arr.append(y)
            if '总成交量' in new_arr or '总持买单量' in new_arr or '总持卖单量' in new_arr or '大连商品交易所' in new_arr:
                continue
            if '成交量' in new_arr:
                type1 = '成交量'
                type2 = '成交量增减'
            elif '持买单量' in new_arr:
                type1 = '持买单量'
                type2 = '持买单量增减'
            elif '持卖单量' in new_arr:
                type1 = '持卖单量'
                type2 = '持卖单量增减'
            if len(new_arr) == 4:
                if new_arr[1] not in data[code_id]:
                    data[code_id][new_arr[1]] = {}
                if '成交量' in new_arr or '持买单量' in new_arr or '持卖单量' in new_arr or '总计' in new_arr:
                    continue
                data[code_id][new_arr[1]][type1] = int(
                    new_arr[2].replace(',', ''))
                data[code_id][new_arr[1]][type2] = int(
                    new_arr[3].replace(',', ''))
        if '会员简称' in data[code_id]:
            data[code_id].pop('会员简称')
    return data


def czce_dtp(dates):
    # 获取郑商所会员成交及持仓明细
    # 数据来源：郑商所
    # 数据地址：http://www.czce.com.cn/cn/jysj/ccpm/H770304index_1.htm
    url1 = f'http://www.czce.com.cn/cn/DFSStaticFiles/Future/{dates[:4]}/{dates}/FutureDataHolding.htm'
    url2 = f'http://www.czce.com.cn/cn/exchange/{dates[:4]}/datatradeholding/{dates}.htm'
    res = requests.get(url1, timeout=300)
    if res.status_code == 404:
        res = requests.get(url2, timeout=300)
        if res.status_code != 200:
            return {}
    res_elements = etree.HTML(res.content.decode('UTF-8'))
    data = {}
    code_id = None
    for x in res_elements.xpath("//tr"):
        arr = []
        for y in x.xpath("./td/b/text()"):
            arr.append(y)
        for z in x.xpath("./td/text()"):
            arr.append(z)
        if '合约' in arr[0]:
            code_id = arr[0].split('\xa0')[0].split('：')[1]
            code_id = "".join(code_id.split())
        if '会员简称 ' in arr or '合计' in arr or ' 会员简称' in arr or '会员简称' in arr:
            continue
        if code_id == '-':
            continue
        if code_id and len(arr) == 10:
            if code_id not in data:
                data[code_id] = {}
            if arr[1] not in data[code_id]:
                data[code_id][arr[1]] = {}
            if arr[4] not in data[code_id]:
                data[code_id][arr[4]] = {}
            if arr[7] not in data[code_id]:
                data[code_id][arr[7]] = {}
            data[code_id][arr[1]]['成交量'] = str_to_int(arr[2])
            data[code_id][arr[1]]['成交量增减'] = str_to_int(arr[3])
            data[code_id][arr[4]]['持买仓量'] = str_to_int(arr[5])
            data[code_id][arr[4]]['持买仓量增减'] = str_to_int(arr[6])
            data[code_id][arr[7]]['持卖仓量'] = str_to_int(arr[8])
            data[code_id][arr[7]]['持卖仓量增减'] = str_to_int(arr[9])
    for datas in data:
        if '-' in data[datas]:
            data[datas].pop('-')
    return data


def cffex_dtp(dates):
    # 获取中金所会员成交及持仓明细
    # 数据来源：中金所
    # 数据地址：http://www.cffex.com.cn/ccpm/
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/plain, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.cffex.com.cn/ccpm/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    arr = ['IF', 'IC', 'IH', 'TS', 'TF', 'T']
    data = {}
    for code in arr:
        url = f'http://www.cffex.com.cn/sj/ccpm/{dates[:6]}/{dates[-2:]}/{code}.xml'
        res = requests.get(url, headers=headers, timeout=300)
        if res.status_code != 200:
            return {}
        try:
            res_elements = etree.XML(bytes(bytearray(res.text, encoding='utf-8')))
        except:
            res_elements = etree.HTML(res.content)
        for x in res_elements.xpath("//data"):
            arr = []
            for y in x.xpath("./*/text()"):
                arr.append(y.replace(' ', ''))
            if arr[0] not in data:
                data[arr[0]] = {}
            if arr[4] not in data[arr[0]]:
                data[arr[0]][arr[4]] = {}
            if arr[2] == '0':
                data[arr[0]][arr[4]]['成交量'] = int(arr[5])
                data[arr[0]][arr[4]]['成交量增减'] = int(arr[6])
            elif arr[2] == '1':
                data[arr[0]][arr[4]]['持买单量'] = int(arr[5])
                data[arr[0]][arr[4]]['持买单量增减'] = int(arr[6])
            elif arr[2] == '2':
                data[arr[0]][arr[4]]['持卖单量'] = int(arr[5])
                data[arr[0]][arr[4]]['持卖单量增减'] = int(arr[6])
    return data


def ine_dtp(dates):
    # 获取上海能源会员成交及持仓明细
    # 数据来源：上海国际能源交易中心
    # 数据地址：http://www.ine.cn/statements/daily/?paramid=kx
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.ine.cn/statements/daily/?paramid=kx',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    url = f'http://www.ine.cn/data/dailydata/kx/pm{dates}.dat'
    res = requests.get(url, headers=headers, timeout=300)
    if res.status_code != 200:
        return {}
    res = res.text
    data = {}
    if res[0] == '{':
        for x in json.loads(res)['o_cursor']:
            # out_arr = ['', '期货公司', '非期货公司']
            # if x['PARTICIPANTABBR1'].replace(' ', '') in out_arr:
            #     continue
            code_id = x['INSTRUMENTID']
            fc1 = x['PARTICIPANTABBR1'].split('$')[0]
            fc2 = x['PARTICIPANTABBR2'].split('$')[0]
            fc3 = x['PARTICIPANTABBR3'].split('$')[0]
            if code_id not in data:
                data[code_id] = {}
            if fc1 not in data[code_id]:
                data[code_id][fc1] = {}
            if fc2 not in data[code_id]:
                data[code_id][fc2] = {}
            if fc3 not in data[code_id]:
                data[code_id][fc3] = {}
            data[code_id][fc1]['成交量'] = x['CJ1']
            data[code_id][fc1]['成交量增减'] = x['CJ1_CHG']
            data[code_id][fc2]['持买单量'] = x['CJ2']
            data[code_id][fc2]['持买单量增减'] = x['CJ2_CHG']
            data[code_id][fc3]['持卖单量'] = x['CJ3']
            data[code_id][fc3]['持卖单量增减'] = x['CJ3_CHG']
            if '' in data[code_id]:
                data[code_id].pop('')
    return data


def get_dtp(since, pfn):
    if since == 0:
        since = 1009814400000
    for i in date_arr(since):
        time.sleep(random.uniform(0, 5))  # 因网站限制访问频率，测试用
        try:
            # 有时候上期所与上海国际能源会出现重复的数据
            data = dict({'日期': i[1]}, **shfe_dtp(i[0]), **dce_dtp(i[1]),
                        **czce_dtp(i[0]), **cffex_dtp(i[0]), **ine_dtp(i[0]))
        except:
            data = dict({'日期': i[1]}, **shfe_dtp(i[0]), **dce_dtp(i[1]),
                        **czce_dtp(i[0]), **cffex_dtp(i[0]))
        if i[4] >= since:
            if len(data) > 1 and is_have_data(data):
                pfn(i[4], data)


def on_init():
    return ('DTP', get_dtp)


if __name__ == '__main__':
    get_dtp(0, None) # 测试
    pass
    