#/usr/bin/python
#coding:utf-8
import json
import requests
'''
关键字搜索
'''

class POIController(object):
    def __init__(self,key):
        self.key = key
        self.keyword = ''
        self.city = ''
        self.offset = ''
        self.page = ''
        self.extension = 'all'
        self.url = ''
        self.json = ''
        self.file = ''
        print('-------初始化成功-------')
    '''
    设置属性：爬取参数
    '''
    def setproperties(self,city,keyword,offset,page,extension='all'):
        self.keyword = keyword
        self.city = city
        self.offset = offset
        self.page = page
        self.extension = extension
        self.url = 'http://restapi.amap.com/v3/place/text?&keywords='+self.keyword+'&city='+self.city+'&output=json&offset='+str(self.offset)+'&page='+str(self.page)+'&key='+self.key+'&extensions='+self.extension
        print('爬取内容:%s %s 页码-%d'%(city,keyword,page))
    '''
    返回文本
    '''
    def url2text(self):
        req = requests.get(self.url)
        text = json.loads(req.text)
        return text

    '''
    返回json
    '''
    def text2json(self,text):
        self.poi = self.url2text().get('pois')
        print('poi字典大小：%d'%len(self.poi))
        return self.poi

    '''
    把POI的数据进行整理
    '''
    def json2plain(self,p):
        name = p.get('name')
        type = p.get('type')
        address = p.get('address')
        location = p.get('location')
        try:
            result = name + ',' + type + ',' + location + ',' + address + '\n'
        except TypeError:
            print('错误：%s'%type)
        return result

    def poi2txt(self,fname='test.txt'):
        f = open(fname,'w+')
        for p in self.poi:
            f.write(self.json2plain(p))
        f.close()
    def poi2txt_page(self,mpage):
        self.url = 'http://restapi.amap.com/v3/place/text?&keywords='+self.keyword+'&city='+self.city+'&output=json&offset='+str(self.offset)+'&page='+str(mpage)+'&key='+self.key+'&extensions='+self.extension
        text = self.url2text()
        poi = self.text2json(text)
        for p in poi:
            self.file.write(self.json2plain(p))

    def poi2txt_page_file(self,pages,fname='poires.txt'):
        self.file = open(fname,'a+')

        if(len(pages)<0):
            print('数组数目错误')
        for p in pages: #对于每一页，都爬取下来
            self.poi2txt_page(p)
        pass

    def poi2file(self, mpage,poitype):
        self.url = 'http://restapi.amap.com/v3/place/text?&keywords=' + poitype + '&city=' + self.city + '&output=json&offset=' + str(
            self.offset) + '&page=' + str(mpage) + '&key=' + self.key + '&extensions=' + self.extension
        text = self.url2text()
        poi = self.text2json(text)
        for p in poi:
            self.file.write(self.json2plain(p))
    def poi2txtplus(self, pages, poitype,fname):
        self.file = open(fname, 'a+')
        # if (len(pages) < 0):
        #     print('数组数目错误')
        for type in poitype:
            for p in pages:  # 对于每一页，都爬取下来
                print('爬取内容:%s %s 页码-%d' % (city, type, p))

                self.poi2file(p,str(type))

key='9f99fc570ccaf6abc209780433d9f4c1'

mpages = range(6)
poitype = ['出入口','房地产','公司','购物','行政地标','交通设施','教育培训','金融','酒店','旅游景点','美食','汽车服务','生活服务','文化传媒','休闲娱乐','运动健身','政府机构']
fnametype = ['出入口','房地产','公司','购物','行政地标','交通设施','教育培训','金融','酒店','旅游景点','美食','汽车服务','生活服务','文化传媒','休闲娱乐','运动健身','政府机构']

index = 4
# keywords=poitype[index]
# fpath = fnametype[index]+'.txt'
city = '上海'
offset = 200
page = 1;
print(mpages)
print(poitype)

#*****************************************************
controller = POIController(key)
for i in range(16,len(poitype)):
    keywords = poitype[i]
    fpath = fnametype[i] + '.txt'
    controller.setproperties(city,keywords,offset,page)
    text = controller.url2text()
    controller.text2json(text)
    controller.poi2txt_page_file(mpages,fpath)
#*****************************************************

#*****************************************************


# fpath = '../resources/poi.txt'
# controller.poi2txtplus(mpages,poitype,fpath)