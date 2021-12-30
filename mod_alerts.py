# -*- coding: UTF-8 -*-


'''
数据名称：同花顺期货快讯
数据描述：提供专业、全面、准确的7X24小时期货资讯及期货行情报价服务，内容覆盖国内、国际主要市场期货品种，帮助投资者把握期货市场投资先机。
数据来源：http://goodsfu.10jqka.com.cn/qhkx_list/
'''

import requests
from lxml import etree
import time


def s2t(s, fmt='%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(time.strptime(s, fmt))*1000)


group_code = ''
last_title = ''
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://goodsfu.10jqka.com.cn/qhkx_list/index_2.shtml',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def get_content(url):
    response = requests.get(url, headers=headers, verify=False)
    response.encoding="gbk"
    selector = etree.HTML(response.text)
    content = selector.xpath('//div[@class="main-text atc-content"]//*/text()')
    if len(content) < 10:
        new_content = ''
        for i in range(len(content)):
            if '关注' in content[i]:
                new_content = content[:i]
        new_content = ''.join(new_content).split()
        if len(new_content) > 1:
            all_content = ''
            for v in new_content:
                all_content = all_content + v + ' '
            return all_content
        else:
            return new_content[0]


def get_alerts(since, pfn):
    news_time_arr = []
    title_arr = []
    href_arr = []
    # 因快讯有时效性，固只爬取最新的10页数据，大概2天内的数据
    for page in range(10, 0, -1):
        response = requests.get(f'http://goodsfu.10jqka.com.cn/qhkx_list/index_{page}.shtml', headers=headers, verify=False, timeout=300)
        if response.status_code != 200:
            continue
        selector = etree.HTML(response.text)
        if selector is None:
            continue
        news_time = selector.xpath('//span[@class="arc-title"]/span/text()')
        title = selector.xpath('//span[@class="arc-title"]/a/text()')
        href = selector.xpath('//span[@class="arc-title"]/a/@href')
        news_time_arr = news_time_arr + news_time[::-1]
        title_arr = title_arr + title[::-1]
        href_arr = href_arr + href[::-1]
    now_year = time.strftime("%Y", time.localtime())
    news_time_arr = [now_year + '年' + i for i in news_time_arr]
    for num in range(len(news_time_arr)):
        ts = s2t(news_time_arr[num], '%Y年%m月%d日 %H:%M')
        if ts >= since:
            content = get_content(href_arr[num])
            if not content:
                continue
            dic = {
                'date': news_time_arr[num],
                'title': '【' + title_arr[num] + '】',
                'url': href_arr[num],
                'content': content
            }
            pfn(ts, dic)


def on_init():
    return ('ALTS', get_alerts)


if __name__ == "__main__":
    get_alerts(0, None)
    pass
