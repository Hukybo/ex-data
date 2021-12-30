'''
数据名称：商品指数
数据描述：中证商品期货综合性指数系列包括1条综合指数、4条主要类别综合指数（农产品、金属、化工材料、能源）和4条细分类别综合指数（粮食、油脂、工业金属、纺织），以多维度反映国内商品期货市场表现。
数据来源：http://www.csindex.com.cn/zh-CN/indices/index?class_13=13
'''


import requests
import json
import time


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def get_index_code_list():
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.csindex.com.cn/zh-CN/indices/index?class_13=13',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    params = (
        ('page', '1'),
        ('page_size', '50'),
        ('by', 'asc'),
        ('order', '\u53D1\u5E03\u65F6\u95F4'),
        ('data_type', 'json'),
        ('class_13', '13'),
    )
    response = requests.get('http://www.csindex.com.cn/zh-CN/indices/index', headers=headers, params=params, verify=False)
    if response.status_code == 200:
        decoded_data=response.text.encode().decode('utf-8-sig') 
        arr = []
        for i in json.loads(decoded_data)['list']:
            if i['class_classify'] == '其他':
                arr.append([i['index_code'], i['indx_sname']])
    else:
        arr = [['H11069', '油脂CFCI'], ['H11068', '纺织CFCI'], ['H11067', '工金CFCI'], ['H11066', '粮食CFCI'], ['H11065', '能源CFCI'], 
               ['H11064', '化工CFCI'], ['H11063', '金属CFCI'], ['H11062', '农产CFCI'], ['H11061', '商品CFCI'], ['H30009', '商品CFI'], 
               ['H30008', '商品LCFI'], ['H30072', '贵金CFI'], ['H30071', '能化CFI'], ['H30070', '工金CFI'], ['H30069', '农产CFI'], 
               ['H30078', '期指反两'], ['H30077', '期指反向'], ['H30076', '期指两倍'], ['H30075', '300期指'], ['H30228', '商品OCFI'], 
               ['H30227', '工业CFI'], ['H30226', '化工CFI'], ['H30225', '有色CFI'], ['H30224', '粮油CFI'], ['H30530', '农产中期'], 
               ['H30529', '农产短期'], ['H30528', '商品中期'], ['H30527', '商品短期'], ['930666', '商品趋势'], ['930665', '商品动量'], 
               ['930775', '钢铁CFI'], ['930886', '煤炭CFI'], ['930906', '软商CFI'], ['930989', '油脂CFI'], ['930988', '粮食CFI'], 
               ['930952', '黑金CFI'], ['930940', 'CME商品'], ['931154', '能源CFI'], ['931337', '原油CFI']]
    return arr


def get_index(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.csindex.com.cn/zh-CN/indices/index-detail/H11069',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    params = (
        ('earnings_performance', '5\u5E74'),
        ('data_type', 'json'),
    )
    index_code_list = get_index_code_list()
    arr = []
    data = {}
    for info in index_code_list:
        url = f'http://www.csindex.com.cn/zh-CN/indices/index-detail/{info[0]}'
        response = requests.get(url, headers=headers, params=params, verify=False, timeout=300)
        if response.status_code != 200:
            continue
        decoded_data=response.text.encode().decode('utf-8-sig')
        for i in json.loads(decoded_data):
            ts = s2t(i['tradedate'])
            if ts not in data:
                data[ts] = {
                    'date': i['tradedate'].split(' ')[0]
                }
            if info[1] not in data[ts]:
                data[ts][info[1]] = {}
            data[ts][info[1]] = {
                'yesterday_close': i['lclose'],
                'today_close': i['tclose']
            }
    sorted(data.keys())
    for new_ts in data:
        if new_ts >= since and len(data[new_ts]) > 30:
            pfn(new_ts, data[new_ts])
        

def on_init():
    return ('INDEX', get_index)


# 测试
if __name__ == '__main__':
    get_index(0, None)
