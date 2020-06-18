# coding:utf-8
import os
import pprint
import requests, re
from lxml import etree
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",

}


def get_page():
    url = 'https://www.ximalaya.com/yinyue/20380455/'  # 地址
    res = requests.get(url, headers=headers).text
    alt = re.findall(r'<h1 class="title lO_">(.*?)</h1>', res, re.S)  # 文件夹名称
    # print(alt)
    return res, alt[0]  # re返回的是一个列表 取出[0]


def get_id(res):
    html = etree.HTML(res)
    lis = html.xpath('//*[@id="anchor_sound_list"]/div[2]/ul/li')
    sum = str(len(lis))  # 一页作品总数 （30）
    print('总数；' + sum)
    titles = []
    ids = []
    for li in lis:
        title = li.xpath('./div[2]/a//text()')[0]
        href = li.xpath('./div[2]/a/@href')[0]
        song_id = href.split('/')[-1]  # 接口url的id
        titles.append(title)
        ids.append(song_id)
        # print(title, href, i)
    return titles, ids, sum


def get_song_url(ids):
    """提供音频链接的api，从中取出音频链接"""
    song_urls = []
    for id in ids:
        api = 'https://www.ximalaya.com/revision/play/v1/audio?id={}&ptype=1'.format(str(id))  # api
        data = requests.get(api, headers=headers).json()  # 返回的json
        song_url = data['data']['src']  # 取出音频链接
        song_urls.append(song_url)
        sleep(1)
    return song_urls


def download_song(titles, song_urls, sum, alt):
    i = 1
    if not os.path.exists(alt):  # 创建文件夹
        os.mkdir(alt)
    for title, song_url in zip(titles, song_urls):
        res = requests.get(song_url, headers=headers)
        print('正在下载:' + title + '{}/{}'.format(str(i), sum))
        with open('{}\{}.mp3'.format(alt, title), 'wb') as f:
            f.write(res.content)
        sleep(3)
        i += 1
    print('下载完成')


res, alt = get_page()
titles, ids, sum = get_id(res)
song_urls = get_song_url(ids)
download_song(titles, song_urls, sum, alt)
