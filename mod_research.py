'''
数据名称：中信期货研究报告
数据描述：中信期货提供金融期货、宏观研究、黑色建材、有色金属、能源、化工、策略研究、农产品、量化研究等最新期货分析数据报告。
数据来源：https://www.citicsf.com/e-futures/research/more?code
备注：因版权问题，故数据是PDF链接，而不是PDF文件；因研报有时效性，故只获取第一页数据，事实上除每日研报外，大部分只有一页数据。
'''


import requests
import json
import time


def t2s(t=None, fmt="%Y-%m-%d %H:%M:%S"):
    # 时间戳转日期
    if t is None:
        t = time.time()
    else:
        t /= 1000
    return time.strftime(fmt, time.localtime(t))


def get_research(since, pfn):
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.citicsf.com/e-futures/research/more?code',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    arr = []
    for x in range(1, 15):
        if x < 10:
            code = '00010' + str(x)
        else:
            code = '0001' + str(x)
        for y in range(1, 3):
            code1 = code + '0' + str(y)
            for z in range(1, 9):
                new_code = code1 + '0' + str(z)
                params = (
                    ('code', new_code),
                    ('page', '1'),
                )
                response = requests.get('https://www.citicsf.com/e-futures/research/getArticles', headers=headers, params=params, timeout=300)
                if response.status_code != 200:
                    data = []
                    continue
                else:
                    data = json.loads(response.text)['data']['result']['content']
                if len(data) == 0:
                    continue
                arr = arr + data
    arr.sort(key=lambda k: (k.get('postTime', 0)))
    for info in arr:
        ts = info['postTime']
        if ts >= since:
            id = info['id']
            columnCode = info['columnCode']
            dic = {
                'date': t2s(info['postTime'], '%Y-%m-%d'),
                'title': info['title'],
                'url': f'https://www.citicsf.com/e-futures/content/{columnCode}/{id}'
            }
            pfn(ts, dic)


def on_init():
    return ('RECH', get_research)


if __name__ == '__main__':
    get_research(1627784556000, None)
    pass
    