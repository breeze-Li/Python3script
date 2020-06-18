'''
爬取虎牙LOL首页中主播的 信息 和 人气 并进行排名
'''


import requests
from urllib import request
import re

class Spider():
    url = 'https://www.huya.com/g/lol'
    root_patten = '<i class="nick" title=([\s\S]*?)</li>'
    name_patten = '">([\s\S]*?)</i>\r\n'
    num_patten = '<i class="js-num">([\s\S]*?)</i></span>'
    
    def __catah_content(self):                  #抓取页面
        r = request.urlopen(Spider.url)
        htmls = r.read()
        #htmls.decode('utf8','ignore')
        htmls = str (htmls,encoding = 'utf-8')
        
        return htmls
    
    def __analysis(self,htmls):               #正则匹配
        root_html = re.findall(Spider.root_patten , htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_patten,html)
            num = re.findall(Spider.num_patten,html)
            anchor = {'name':name,'num':num}
            anchors.append(anchor)
            #print(anchors)
        return anchors
        

    def __refine(self,anchors):                     #
        l = lambda anchor:{
            'name':anchor['name'][0],
            'num':anchor['num'][0]
            }    
        return list(map(l , anchors))

    def __sort(self,anchors):                       #排序
        anchors  = sorted(anchors, key = self.__sort_seed,reverse = True)
        return anchors


    def __sort_seed(self,anchors):                  #排序种子
        r = re.findall('\d*',anchors['num'])
        num = float(r[0])
        if '万' in anchors['num']:
            num =num*10000
        return num

 
    def show(self,anchors):                             #显示最后结果
        for i in range(0,len(anchors)):
            print('第' + str (i + 1) + '名'
            + '   :   '  + anchors[i]['name']+'-----'+
            anchors[i]['num'])



    def go(self):                                       #入口函数
       htmls = self.__catah_content()
       anchors = self.__analysis(htmls)
       anchors = self.__refine(anchors)
       anchors = self.__sort(anchors)
       self.show(anchors)

spider = Spider()               #实例化
spider.go()                     #调用入口函数



