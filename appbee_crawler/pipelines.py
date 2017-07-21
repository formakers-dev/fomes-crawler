# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from pymongo import MongoClient
from appbee_crawler.spiders.app_spider import AppItem
from appbee_crawler.spiders.category_spider import CategoryItem


class AppBeeCrawlerPipeline(object):
    def __init__(self):
        print('### init Pipeline ###')

    def open_spider(self, spider):
        self.mongo_client = MongoClient(os.environ['MONGO_URL'])
        self.db = self.mongo_client['appbee']

    def close_spider(self, spider):
        self.mongo_client.close()

    def process_item(self, item, spider):
        if type(item) is CategoryItem:
            self.db.categories.update({'id':item['id']}, dict(item), upsert=True)
        elif type(item) is AppItem:
            self.db.apps.update({'package_name':item['package_name']}, dict(item), upsert=True)

        return item
