import requests
from lxml import etree
import time, datetime


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    'referer':'https://careers.tencent.com/search.html?keyword=python'
}


def get_detail_url(url):
    res = requests.get(url, headers=headers)
    text = res.json()
    urls = []
    ids = []
    for url in text['Data']['Posts']:
        id = url['PostId']
        url = 'http://careers.tencent.com/jobdesc.html?postId=' + id  # 有些url会ID=0 因此用这种方式拼接
        urls.append(url)
        ids.append(id)
    return urls, ids


def get_info_by_json(id):
    timestamp = int(round(time.time() * 1000))  # 时间戳
    url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp={}&postId={}&language=zh-cn'.format(
        timestamp, id)
    text = requests.get(url, headers=headers).json()
    CategoryName = text['Data']['CategoryName']
    LocationName = text['Data']['LocationName']
    RecruitPostName = text['Data']['RecruitPostName']
    Requirement = text['Data']['Requirement']
    Responsibility = text['Data']['Responsibility']
    LastUpdateTime = text['Data']['LastUpdateTime']
    print('职位名称:' + RecruitPostName)
    print('类型:' + CategoryName)
    print('地点:' + LocationName)
    print('时间:' + LastUpdateTime)
    # print('工作要求:' + Responsibility)
    # print('工作职责:' + Requirement)
    print('*' * 100)
    # print(int(round(time.time() * 1000)))


def main1(x):
    """使用json的方式获取职位信息 ， X 代表需要获取的页面数量"""
    for i in range(1, x + 1):
        print('*' * 50 + '第' + str(i) + '页' + '*' * 50)
        url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1591401487635&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(
            i)  # 腾讯招聘官网的职位信息 json
        urls, ids = get_detail_url(url)
        for id, url in zip(ids, urls):
            print(url)
            get_info_by_json(id)


def get_info_by_html(url):
    """通过网页代码获取信息"""
    pass


main1(3)