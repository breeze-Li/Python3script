# 作者：娶一个骚的名字
# 日期：2019/7/28 11:39
# 工具：PyCharm
import requests
from lxml import etree
import os


class BiZhi(object):

    def first_request(self, headers, number):
        for j in range(1, 2):
            url = 'http://www.win4000.com/mobile_' + str(number) + '_0_0_' + str(j) + '.html'
            response = requests.get(url, headers=headers)
            html = etree.HTML(response.content.decode())
            Bigtit_list = html.xpath('//ul[@class="clearfix"]/li/a/@title')
            Biglink_list = html.xpath('//div[@class=""]/ul/li/a/@href')
            for Bigtit, Biglink in zip(Bigtit_list, Biglink_list):
                if os.path.exists(Bigtit) == False:
                    os.mkdir(Bigtit)
                biglink = str(Biglink).replace('.html', '')
                self.second_request(Bigtit, biglink, headers)

    def second_request(self, Bigtit, biglink, headers):  # ,Bigtit,Biglink,
        for i in range(1, 10):
            try:
                url = biglink + '_' + str(i) + '.html'
                # if url == biglink+'_'+str(i+1)+'.html':
                #     break
                response = requests.get(url, headers=headers)
                html = etree.HTML(response.content.decode())
                img_link = ''.join(html.xpath('//div[@class="main-wrap"]/div/a/img/@src'))
                print(img_link)
                # 请求图片下载地址
                resp = requests.get(img_link, headers=headers)
                data = resp.content
                img_name = img_link[-10:]
                # print(img_name)
                file_name = Bigtit + '\\' + img_name
                print('正在下载的图片为：', img_name)
                with open(file_name, 'wb') as f:
                    f.write(data)
            except Exception as err:
                if err == 'string index out of range':
                    continue


spider = BiZhi()
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'}
print('''
以下为分类对应数字，输入是请输入数字！……^^_^^……
明星：2338  节日：2339  美女：2340
风景：2341  汽车：2342  可爱：2343
唯美：2344  动漫：2346  爱情：2347
动态：2348  卡通：2349  高翔：2350
影视：2354  动物：2355  植物：2356  美食：2362
 
 
''')
number = input('请输入您要下载类目对应的数字：')
spider.first_request(headers, number)
