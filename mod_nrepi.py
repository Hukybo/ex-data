# -*- coding: UTF-8 -*-


'''
数据名称：新房价指数(New Real estate price index)
数据描述：房屋销售价格指数是反映一定时期房屋销售价格变动程度和趋势的相对数，它通过百分数的形式来反映房价在不同时期的涨跌幅度。包括商品房、公有房屋和私有房屋各大类房屋的销售价格的变动情况。
数据来源：http://data.eastmoney.com/cjsj/newhouse.html
'''


import json
import time
import requests


def s2t(s, fmt="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(s, fmt))*1000)


def str_to_num(s):
    if s == '' or s == '-' or s == None:
        return 'NaN'
    else:
        return s
    

def format_date(old_arr):
    new_arr = []
    for i in old_arr:
        arr = i.split('/')
        new_arr.append(arr[2] + '-' + arr[0] + '-' + arr[1])
    return new_arr
        

def get_nrepi(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://data.eastmoney.com/cjsj/newhouse.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    citys = ['北京', '上海', '安庆', '蚌埠', '包头', '北海', '长春', '长沙', '德州', '成都', '大理', '大连', '丹东', '福州', '赣州', '广州', '贵阳', '桂林', 
            '哈尔滨', '海口', '杭州', '合肥', '呼和浩特', '惠州', '吉林', '济南', '济宁', '金华', '锦州', '九江', '昆明', '兰州', '泸州', '洛阳', '牡丹江',
            '南昌', '南充', '南京', '南宁', '宁波', '平顶山', '秦皇岛', '青岛', '泉州', '三亚', '韶关', '深圳', '沈阳', '石家庄', '太原', '唐山', '天津', 
            '温州', '乌鲁木齐', '无锡', '武汉', '西安', '西宁', '厦门', '襄樊', '徐州', '烟台', '扬州', '宜昌', '银川', '岳阳', '湛江', '郑州', '重庆', '遵义']
    all_data = {}
    dates = None
    for city in citys:
        all_data[city] = []
        for stat in range(1, 4):
            for mkt in range(1, 4):
                params = (
                    ('mkt', mkt),
                    ('stat', stat),
                    ('city1', city),
                    ('city2', city),
                )
                url = 'http://data.eastmoney.com/dataapi/cjsj/getnewhousechartdata'
                res = requests.get(url, headers=headers, params=params, timeout=300)
                if res.status_code != 200:
                    continue
                info = json.loads(res.text)
                if 'chart' in info and 'graphs' in info['chart'] and 'graph' in info['chart']['graphs']:
                    all_data[city].append(info['chart']['graphs']['graph'][0]['value'])
                    if not dates:
                        dates = format_date(info['chart']['series']['value'])
    for x in range(len(dates)):
        data = {}
        data['日期'] = dates[x]
        for city in all_data:
            data[city] = {}
            data[city]['新建住宅价格指数'] = {}
            data[city]['新建商品住宅价格指数'] = {}
            data[city]['二手住宅价格指数'] = {}
            data[city]['新建住宅价格指数']['环比'] = str_to_num(all_data[city][0][x])
            data[city]['新建住宅价格指数']['同比'] = str_to_num(all_data[city][1][x])
            data[city]['新建住宅价格指数']['定基'] = str_to_num(all_data[city][2][x])
            data[city]['新建商品住宅价格指数']['环比'] = str_to_num(all_data[city][3][x])
            data[city]['新建商品住宅价格指数']['同比'] = str_to_num(all_data[city][4][x])
            data[city]['新建商品住宅价格指数']['定基'] = str_to_num(all_data[city][5][x])
            data[city]['二手住宅价格指数']['环比'] = str_to_num(all_data[city][6][x])
            data[city]['二手住宅价格指数']['同比'] = str_to_num(all_data[city][7][x])
            data[city]['二手住宅价格指数']['定基'] = str_to_num(all_data[city][8][x])
        ts = s2t(data['日期'], "%Y-%m-%d")
        if ts >= since:
            pfn(ts, data)


def on_init():
    return ('NREPI', get_nrepi)


if __name__ == '__main__':
    get_nrepi(1439136000000, None) # 测试
    pass
    