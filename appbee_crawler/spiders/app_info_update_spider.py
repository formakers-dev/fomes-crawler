# -*- coding: utf-8 -*-
import scrapy

from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.parser.app_item_parser import AppItemParser


class AppInfoUpdateSpider(scrapy.Spider):
    name = "AppInfoUpdateSpider"
    allowed_domains = ["play.google.com"]

    def start_requests(self):
        package_names = DBManager.get_package_names_to_update_info()
        for package_name in package_names:
            if package_name == 'com.formakers.fomes':
                continue

            request = scrapy.Request('https://play.google.com/store/apps/details?id=' + package_name,
                                     meta={'packageName': package_name}, dont_filter=True)
            yield request

    def parse(self, response):
        yield AppItemParser.parse(response)
