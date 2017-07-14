# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from appbee_crawler.repository.setup import Category, App, Setup
from appbee_crawler.spiders.category_spider import CategoryItem
from appbee_crawler.spiders.free_app_spider import AppItem

class AppbeeCrawlerPipeline(object):
    def __init__(self):
        self.engine = Setup().getEngine()

    def open_spider(self, spider):
        Session = sessionmaker(bind=self.engine)
        self.db_session = Session()

    def process_item(self, item, spider):
        if type(item) is CategoryItem:
            category = Category(**item)
            self.db_session.add(category)
        elif type(item) is AppItem:
            app = App(**item)
            self.db_session.add(app)
        self.db_session.commit()
        return item

