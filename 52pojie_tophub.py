import requests, os
import datetime
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
}


def name(titles):
    """去除文件夹名中的非法字符"""
    flags = '：:*?<>|！!'  # 文件夹名中的非法字符
    for flag in flags:
        f = titles.find(flag)
        if f != -1:
            titles = titles.replace(titles[f], '')  # 去除文件夹名中的非法字符
    return titles


def geturl_and_title():
    url = 'https://tophub.today/n/NKGoRAzel6'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    todays = soup.find('tbody').find_all('td', class_='al')  # 所有包含链接的标签
    update_time = soup.find('h2', class_='cc-dc-Cb').text  # 更新时间
    print('*' * 50, update_time, '*' * 50, sep='\n')

    hrefs = []
    titles = []
    for today in todays:
        href = today.find('a')['href']  # 链接
        title = today.find('a').string  # 标题
        hrefs.append(href)
        titles.append(title)
    return hrefs, titles


def makedir():
    """以今天的日期为目录明"""
    dirt = str(datetime.date.today())  # 今天的日期 用作目录明 目录为str格式
    if not os.path.exists(dirt):
        os.makedirs(dirt)
    else:
        print('今日已经运行')
        exit()
    return dirt


def download(titles, hrefs, dirt):
    """下载网页"""
    for title, href in zip(titles, hrefs):
        text = requests.get(href, headers=headers).text
        # print(text)

        title = name(title)  #
        with open(dirt + '\\' + title + '.html', 'w') as f:
            f.write(text)
            print('{}->->->->->->->->保存完毕'.format(title))
        # print('{}:{}'.format(title, href))  # title.ljust(len_str) >> 左对齐 len_str 个字符


def main():
    hrefs, titles = geturl_and_title()
    dirt = makedir()
    download(titles, hrefs, dirt)


main()
