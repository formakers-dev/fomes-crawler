# -*- coding: utf-8 -*-
from appbee_crawler.app_items import AppItem
from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.category_spider import CategoryItem
import re

from appbee_crawler.util.string_util import StringUtil


class AppBeeCrawlerPipeline(object):
    game_category_id_pattern = re.compile("^GAME")

    def __init__(self):
        print('### init Pipeline ###')

    def close_spider(self, spider):
        print('### Close Spider ###')
        DBManager.close()

    def process_item(self, item, spider):
        print('### Process Item ###')

        StringUtil.trim(item)

        if type(item) is CategoryItem:
            DBManager.upsert_category(item)
        elif type(item) is AppItem:

            if self.game_category_id_pattern.match(item['categoryId1']):
                DBManager.upsert_app(item)
            else:
                DBManager.upsert_other_app(item)

            DBManager.delete_uncrawled_app(item['packageName'])

        return item
