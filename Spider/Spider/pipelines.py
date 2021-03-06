# -*- coding: utf-8 -*-
# 注意json文件以一个空的字典{}结尾！
import json
import codecs
import csv
import pymongo
from scrapy.conf import settings
from func_pack import get_current_day
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#此管道处理函数 用于处理 distinct_spider.py 中 的爬虫数据
class href_JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('href.json', 'w', encoding='utf-8')
        self.file.write('[')
        #print "Open the spider pipeline"

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    #要特别注意这两个函数名，因为框架需要调用 因此名字必须是open_spider 一点都不能错
    def open_spider(self,spider):
        pass
        #print "Spider start!"

    #同样 close_spider 的函数名也必须是这个，否则框架是无法识别的
    def close_spider(self, spider):
        #print "Close the spider pipeline"
        #注意Json文件以一个空的数据结构结尾
        self.file.write('{}]')
        self.file.close()

#此管道处理函数 用于处理 house_spider.py 中 的爬虫数据
class houseInfo_JsonWithEncodingPipeline(object):
    def __init__(self):
        fname = "./data/houseInfo_" + get_current_day() +".json"
        self.file = codecs.open(fname, 'w', encoding='utf-8')
        self.file.write('[')
        #print "Open the spider pipeline"

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    #要特别注意这两个函数名，因为框架需要调用 因此名字必须是open_spider 一点都不能错
    def open_spider(self,spider):
        pass
        #print "Spider start!"

    #同样 close_spider 的函数名也必须是这个，否则框架是无法识别的
    def close_spider(self, spider):
        #print "Close the spider pipeline"
        #注意Json文件以一个空的数据结构结尾
        self.file.write('{}]')
        self.file.close()

#此管道处理函数 用于处理 house_spider.py 中 的爬虫数据
class houseInfo_CsvWithEncodingPipeline(object):
    def __init__(self):
        src = './data/'
        fname = "houseInfo_" + get_current_day() +".csv"
        self.file = codecs.open(src + fname, 'wb',encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['introduction_house',
                              'community_house',
                              'href_house',
                              'unit_house',
                              'size_house',
                              'direction_house',
                              'decoration_house',
                              'elevator_house',
                              'type_house',
                              'years_house',
                              'area_house',
                              'interests_house',
                              'watch_times',
                              'submit_period',
                              'years_period',
                              'tax_free',
                              'total_price',
                              'smeter_price',
                              'region',
                              'info_cluster',
                              'info_flood',
                              'info_follow'])
        #print "Open the spider pipeline"

    def process_item(self, item, spider):
        self.writer.writerow((item['introduction_house'],
                              item['community_house'],
                              item['href_house'],
                              item['unit_house'],
                              item['size_house'],
                              item['direction_house'],
                              item['decoration_house'],
                              item['elevator_house'],
                              item['type_house'],
                              item['years_house'],
                              item['area_house'],
                              item['interests_house'],
                              item['watch_times'],
                              item['submit_period'],
                              item['years_period'],
                              item['tax_free'],
                              item['total_price'],
                              item['smeter_price'],
                              item['region'],
                              item['info_cluster'],
                              item['info_flood'],
                              item['info_follow']))
        return item

    #要特别注意这两个函数名，因为框架需要调用 因此名字必须是open_spider 一点都不能错
    def open_spider(self,spider):
        pass
        #print "Spider start!"

    #同样 close_spider 的函数名也必须是这个，否则框架是无法识别的
    def close_spider(self, spider):
        #print "Close the spider pipeline"
        #注意Json文件以一个空的数据结构结尾
        self.file.close()

class MongoDB_StoragePipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # 数据库登录需要帐号密码的话
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def open_spider(self,spider):
        logging.info("MongoDB_Pipeline has been opened.")

    def close_spider(self,spider):
        logging.info("MongoDB_Pipeline has been closed.")

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.insert(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写

class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item
