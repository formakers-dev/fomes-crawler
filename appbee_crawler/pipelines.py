# -*- coding: utf-8 -*-
from appbee_crawler.app_items import AppItem
from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.category_spider import CategoryItem


class AppBeeCrawlerPipeline(object):
    def __init__(self):
        print('### init Pipeline ###')

    def close_spider(self, spider):
        DBManager.close()

    def process_item(self, item, spider):
        if type(item) is CategoryItem:
            DBManager.upsert_categories(item)
        elif type(item) is AppItem:
            DBManager.upsert_apps(item)
            DBManager.delete_uncrawled_app(item['packageName'])

        return item
