# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class pttPipeline(object):
    def process_item(self, item, spider):
        self.db.article.insert_one(dict(item))
        return item

    def open_spider(self, spider):
        self.db_client = MongoClient('mongodb://localhost:27017')
        self.db = self.db_client["bbbb"]


    def close_spider(self, spider):
        self.db_client.close()

