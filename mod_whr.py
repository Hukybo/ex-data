# -*- coding: UTF-8 -*-


import requests
import json
from lxml import etree
import time
import datetime
import random


'''
数据名称：期货标准仓单(warehouse_receipt)
数据描述：期货标准仓单是由期货交易所指定交割仓库按照交易所规定的程序签发的符合合约规定质量的实物提货凭证。由于期货标准仓单可以作为一种流通工具，因此它可以用作借款的质押品或用于期货合约的交割。
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
    date_split = list(map(int, t2s(since).split(' ')[0].split('-')))
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


def shfe_warehouse_receipt(dates):
    # 获取仓单
    # 数据来源：上期所
    # 数据地址：
    # http://www.shfe.com.cn/statements/dataview.html?paramid=dailystock
    # 返回多维字典，以品种为key，其value分别为：仓单数量
    request_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.shfe.com.cn',
        'If-Modified-Since': '0',
        'Referer': 'http://www.shfe.com.cn/statements/dataview.html?paramid=dailystock',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    }

    url_new = f'http://www.shfe.com.cn/data/dailydata/{dates}dailystock.dat'
    url_old = f'http://www.shfe.com.cn/data/dailydata/{dates}dailystock.html'
    
    def old_data():
        res = requests.get(url_old, headers=request_headers, timeout=300)
        if res.status_code != 200:
            return {}
        res_elements = etree.HTML(res.content.decode('UTF-8'))
        all_arr = []
        for tr in res_elements.xpath("//tr"):
            arr = []
            for td in tr.xpath("./td/text()"):
                arr.append(td)
            all_arr.append(arr)
        data = {}
        key_name = None
        for td in all_arr:
            if len(td) >= 2:
                if (td[0] == '总' or td[0] == '合') and td[1] == '计':
                    continue
                for i in td:
                    if '单位：' in i:
                        key_name = td[0]
                        data[key_name] = 0
                    if i.isdigit() and key_name:
                        data[key_name] = data[key_name] + int(i)
                        break
        return data
    res = requests.get(url_new, headers=request_headers, timeout=300)
    if res.status_code != 200:
        return old_data()
    res = res.text
    data = {}
    new_data = {}
    if res[0] == '{':
        a = json.loads(res)['o_cursor']
        for i in json.loads(res)['o_cursor']:
            if i['WRTWGHTS'] != '0' and '合计' not in i['WHABBRNAME'] and '总计' not in i['WHABBRNAME']:
                if '厂库' in i['VARNAME']:
                    i['VARNAME'] = i['VARNAME'].replace('仓库', '')
                elif '仓库' in i['VARNAME']:
                    i['VARNAME'] = i['VARNAME'].replace('厂库', '')
                elif '中质含硫' in i['VARNAME']:
                    i['VARNAME'] = i['VARNAME'].replace('中质含硫', '')
                if i['VARNAME'] not in data:
                    data[i['VARNAME']] = int(i['WRTWGHTS'])
                else:
                    data[i['VARNAME']] = data[i['VARNAME']] + int(i['WRTWGHTS'])
        for y in data:
            new_data[y.split('$')[0]] = data[y]
    return new_data


def dce_warehouse_receipt(dates):
    # 获取仓单
    # 数据来源：大商所
    # 数据地址：
    # http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/cdrb/index.html
    # 返回多维字典，以品种为key，其value分别为：仓单数量
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://www.dce.com.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    data = {
        'wbillWeeklyQuotes.variety': 'all',
    }
    dates = dates.split('-')
    data['year'] = dates[0]
    data['month'] = int(dates[1]) - 1
    data['day'] = dates[2]
    res = requests.post('http://www.dce.com.cn/publicweb/quotesdata/wbillWeeklyQuotes.html', headers=headers, data=data, verify=False, timeout=300)
    if res.status_code != 200:
        return {}
    res_elements = etree.HTML(res.content.decode('UTF-8'))
    data = {}
    for x in res_elements.xpath("//table[@cellpadding='0']/tr"):
        arr = []
        for y in x.xpath("./td/text()"):
            s = y.strip()
            if s:
                arr.append(s.replace(',', ''))
        if len(arr) == 0 or len(arr) == 4 or '小计' in arr[0] or '总计' in arr[0]:
            continue
        if arr[0] not in data:
            data[arr[0]] = {}
            data[arr[0]] = int(arr[3])
        else:
            data[arr[0]] = data[arr[0]] + int(arr[3])
    return data

def czce_warehouse_receipt(dates):
    # 获取仓单
    # 数据来源：郑商所
    # 数据地址：http://www.czce.com.cn/cn/jysj/cdrb/H770310index_1.htm
    # 返回多维字典，以品种为key，其value分别为：仓单数量
    url_old = f'http://www.czce.com.cn/cn/exchange/{dates[:4]}/datawhsheet/{dates}.htm'
    url_new = f'http://www.czce.com.cn/cn/DFSStaticFiles/Future/{dates[:4]}/{dates}/FutureDataWhsheet.htm'
    res = requests.get(url_new, timeout=300)
    if res.status_code != 200:
        res = requests.get(url_old, timeout=300)
        if res.status_code != 200:
            return {}
    res_elements = etree.HTML(res.content.decode('UTF-8'))
    keys = []
    values = []
    for x in res_elements.xpath("//table/tr"):
        for y in x.xpath("./td[1]/b/text()"):  # 品种
            if y[0] == '品':
                key_content = keep_chinese("".join(y.split()).split('：')[1][:-2])
                if key_content == '':
                    key_content = 'PTA'
                keys.append(key_content)
        value_arr = []
        for z in x.xpath("./td/text()"):  # 内容
            value_arr.append(z.replace(' ', ''))
        values.append(value_arr)
    data = {}
    subscript = None
    for k in keys:
        data[k] = 0
        for v in range(len(values)):
            new_v = []
            for x in values[v]:
                new_v.append(x.strip())
                if '数量' in x:
                    break
            if '仓单数量' in values[v]:
                subscript_old = values[v].index('仓单数量')
            elif '仓单数量(完税)' in values[v]:
                subscript_old = values[v].index('仓单数量(完税)')
            elif '确认书数量' in values[v]:
                subscript_old = values[v].index('确认书数量')
            if '总计' in new_v:
                if k == '甲醇' and len(values) - v >= 2 and values[v + 1][0] == values[v + 2][0] and values[v + 1][0].isdigit():
                    data[k] = int(values[v + 1][0])
                elif '\xa0' in values[v]:
                    if values[v][subscript_old].isdigit():
                        data[k] = int(values[v][subscript_old])
                else:
                    subscript = new_v.index('总计')
                    if new_v[subscript + 1].isdigit():
                        data[k] = int(new_v[subscript + 1])
                del values[ : v + 1]
                break
    return data


def ine_warehouse_receipt(dates):
    # 数据来源：上海国际能源交易中心
    # 数据地址：http://www.ine.cn/statements/daily/?paramid=kx
    # 返回多维字典，以品种为key，其value分别为：仓单数量
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.ine.cn/statements/daily/?paramid=kx',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    url = f'http://www.ine.cn/data/dailydata/{dates}dailystock.dat'
    res = requests.get(url, headers=headers, timeout=300)
    if res.status_code != 200:
        return {}
    res = res.text
    data = {}
    if res[0] == '{':
        for i in json.loads(res)['o_cursor']:
            if i['WRTWGHTS'] != 0 and '合计' not in i['WHABBRNAME'] and '总计' not in i['WHABBRNAME']:
                if '原油' in i['VARNAME']:
                    i['VARNAME'] = i['VARNAME'].replace('中质含硫', '')
                var_name = i['VARNAME'].split('$')[0]
                if var_name not in data:
                    data[var_name] = {}
                    data[var_name] = int(i['WRTWGHTS'])
                else:
                    data[var_name] = data[var_name] + int(i['WRTWGHTS'])
    return data


def get_whr(since, pfn):
    if since == 0:
        since = 1223222400000
    for i in date_arr(since):
        time.sleep(random.uniform(0, 5))  # 因网站限制访问频率，测试用
        data = dict({'日期': i[1]}, 
                    **shfe_warehouse_receipt(i[0]), 
                    **dce_warehouse_receipt(i[1]), 
                    **czce_warehouse_receipt(i[0]),
                    # **ine_warehouse_receipt(i[0])
                )
        if i[4] >= since:
            if len(data) > 1:
                pfn(i[4], data)


def on_init():
    return ('WHR', get_whr)


if __name__ == '__main__':
    get_whr(1287994309000, None) # 测试
    pass
    