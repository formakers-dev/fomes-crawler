# -*- coding: utf-8 -*-
import scrapy

from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.parser.app_item_parser import AppItemParser

class UncrawledAppSpider(scrapy.Spider):
    name = "UncrawledAppSpider"
    allowed_domains = ["play.google.com"]

    def start_requests(self):
        uncrawled_apps_list = DBManager.select_uncrawled_apps()
        request_list = []
        for app in uncrawled_apps_list:
            packageName = app['packageName']
            request_list.append(scrapy.Request('https://play.google.com/store/apps/details?id=' + packageName, callback=self.after_parsing, meta={'packageName': packageName}))
        return request_list

    def after_parsing(self, response):
        yield AppItemParser.parse(response)
