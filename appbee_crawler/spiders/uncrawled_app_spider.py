# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError

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
            request_list.append(scrapy.Request('https://play.google.com/store/apps/details?id=' + packageName, callback=self.after_parsing, meta={'packageName': packageName}, dont_filter=True, errback=self.error_handler))
        return request_list

    def after_parsing(self, response):
        yield AppItemParser.parse(response)

    def error_handler(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            print(response.meta.get('packageName'), "/", response.status)
            DBManager.update_uncrawled_apps(response.meta.get('packageName'), response.status)