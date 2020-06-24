import requests
# 引用requests模块
from bs4 import BeautifulSoup
import os
from time import sleep

header = {
    'Referer': 'https://tu.acgbox.org/index.php/category/saki/Sec-Fetch-Dest: document',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
}


def save_html(url):
    """保存图集url的html代码"""
    res = requests.get(url, headers=header)
    with open('ACG.html', 'w')as f:
        f.write(res.text)


def save_img():
    with open('ACG.html', 'r') as f:
        html = BeautifulSoup(f, 'html.parser')
        # print(html)
        list_content = html.find_all('img', class_='post-item-img lazy')
        for i in list_content:
            # print(i['alt'], ':', i['data-original'])
            img = requests.get(i['data-original'], headers=header)
            # print(type(img))
            dirt = 'ACG/' + i['alt'][:-4].strip()  # 图集文件夹
            judge_dir(dirt)  # 创建图集文件夹
            filename = i['alt'] + '.jpg'
            path = dirt + '/' + filename
            print('正在保存：{}/{}'.format(filename, len(list_content)))
            with open(path, 'wb') as ff:
                ff.write(img.content)
            sleep(3)




def judge_dir(dirt):
    """判断及创建目录"""
    isExists = os.path.exists(dirt)
    # print(isExists)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(dirt)
        print(dirt + '创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print(dirt + '目录存在')
        return False


def get_urls(root_url):
    """利用用户url获取图集链接"""
    res = requests.get(root_url, headers=header)
    html = BeautifulSoup(res.text, 'html.parser')
    item_link = html.find_all('a', class_="item-link")
    urls = [item['href'] for item in item_link]
    # save_html(root_url)
    return urls


root_url = 'https://tu.acgbox.org/index.php/category/xinkoudao/'
urls = get_urls(root_url)
for url in urls:
    save_html(url)
    save_img()

