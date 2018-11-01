# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class QiubaiproPipeline(object):
    # def __init__(self):
    #   self.fp = open('qiubai.txt', 'w', encoding='utf8')

    def open_spider(self, spider):
        self.fp = open('qiubai.txt', 'w', encoding='utf8')

    # 这个方法会自动调用，每次来一个item都会调用这个方法
    def process_item(self, item, spider):
        d = dict(item)
        string = json.dumps(d, ensure_ascii=False)
        self.fp.write(string + '\n')
        return item


    def close_spider(self, spider):
        self.fp.close()

# 存储到mysql的管道
import pymysql
from scrapy.utils.project import get_project_settings

class MysqlproPipeline(object):
    def open_spider(self, spider):
        # 从配置文件中获取参数
        settings = get_project_settings()
        # 链接数据库
        self.db = pymysql.connect(host=settings['HOST'], user=settings['USER'], password=settings['PWD'], db=settings['DB'], port=settings['PORT'], charset=settings['CHARSET'])

    # 这个方法会自动调用，每次来一个item都会调用这个方法
    def process_item(self, item, spider):
        self.save_to_mysql(item)
        return item

    def save_to_mysql(self, item):
        # 获取游标
        cur = self.db.cursor()
        # 执行sql语句
        sql = """insert into qiubai(image_url,name,age,content,haha_count,ping_count) values('%s','%s','%s','%s','%s','%s')""" % (item['image_url'], item['name'], item['age'], item['content'], item['haha_count'], item['ping_count'])
        try:
            cur.execute(sql)
            #提交
            self.db.commit()
        except Exception as e:
            print(e)
            #错误回滚
            self.db.rollback()


    def close_spider(self, spider):
        self.db.close()

from pymongo import MongoClient
class MongoproPipeline(object):
    # bind 127.0.0.1   注释这个选项即可
    def open_spider(self, spider):
        # 链接MongoDB服务器
        self.client = MongoClient('localhost', 27017)
        # 选择数据库
        db = self.client.qiubai
        # 选择集合
        self.conn = db.qiuqiu

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        d = dict(item)
        self.conn.insert(d)
        return item
        
