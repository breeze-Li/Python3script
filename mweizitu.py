import requests
from lxml import etree
import os
from time import sleep

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
    "Referer": "https://www.mzitu.com/xinggan/"
}


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


def get_atlas_lnk():
    """获取图集链接和名称"""
    res = requests.get('https://www.mzitu.com/page/1', headers=headers)
    html = etree.HTML(res.text)
    atlas_lnk = html.xpath('//ul[@id="pins"]/li/a/@href')
    atlas_nm = html.xpath('//ul[@id="pins"]/li/a/img/@alt')
    # for link, name in zip(atlas_lnk, atlas_nm):
    #     print(link, name)
    return atlas_lnk, atlas_nm


def analytical_atlas(url):
    """解析图集"""
    res = requests.get(url, headers=headers)
    # print(res.text)
    html = etree.HTML(res.text)
    """先获取图集有多少张"""
    maximum_num_of_atlas = html.xpath('//div[@class="pagenavi"]/a[5]//text()')  # 第五个a标签下的文本即为最大图片数
    maximum_num_of_atlas = int(maximum_num_of_atlas[0]) + 1  # 转化为整形
    # print(maximum_num_of_atlas)
    """再获得图片链接,需要注意的是，xpath返回的是列表，但他的元素是etree对象，需要编码成字符串
    html.xpath('//div[@class="main-image"]/p/a/img/@src')[0].encode('utf-8').decode('utf-8')
    也可以直接转化为列表，更容易修改
    """
    img_lnk = list(html.xpath('//div[@class="main-image"]/p/a/img/@src')[0])
    return maximum_num_of_atlas, img_lnk


def get_imglink(altas_lnk):
    """每个图集的每张图片的链接"""
    urls = []
    maximum_num_of_atlas, img_lnk = analytical_atlas(altas_lnk)
    for i in range(1, maximum_num_of_atlas):
        if i < 10:
            img_lnk_t = ''.join(img_lnk[:-5]) + str(i) + ''.join(img_lnk[-4:])
            # img_lnk_t = ''.join(img_lnk)  # 将列表转化为字符串
        else:
            img_lnk_t = ''.join(img_lnk[:-6]) + str(i) + ''.join(img_lnk[-4:])
        urls.append(img_lnk_t)
    return urls


def download_img(title, urls):
    dirt = '妹子图\\' + title  # 图集文件夹名

    flags = '：:*?<>|！!'  # 文件夹名中的非法字符
    for flag in flags:
        f = dirt.find(flag)
        if f != -1:
            dirt = dirt.replace(dirt[f], '')  # 去除文件夹名中的非法字符

    judge = judge_dir(dirt)  # 创建图集文件夹
    if judge:
        for i in range(len(urls)):
            res = requests.get(urls[i], headers=headers)
            filename = dirt + '\\' + str(i) + '.jpg'
            with open(filename, 'wb') as f:
                print('正在保存{}/{}'.format(filename, len(urls)))
                f.write(res.content)
            sleep(2)  # 延时几秒，不要太嚣张
    else:
        print('图集{}已经下载'.format(dirt))
    sleep(1)


x = 6
atlas_lnk, atlas_nm = get_atlas_lnk()
for title, atlink in zip(atlas_nm[:x], atlas_lnk[:x]):  # 切片表示需要下载的图集数
    urls = get_imglink(altas_lnk=atlink)
    download_img(title, urls)
    sleep(1)
