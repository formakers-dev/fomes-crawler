# -*- coding: utf-8 -*-
import scrapy

from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.parser.app_item_parser import AppItemParser


class UncrawledAppSpider(scrapy.Spider):
    name = "UncrawledAppSpider"
    allowed_domains = ["play.google.com"]

    def start_requests(self):
        app_list = DBManager.select_uncrawled_apps()
        request_list = []
        for app in app_list:
            request_list.append(scrapy.Request('https://play.google.com/store/apps/details?id=' + app['packageName'],
                                     callback=self.after_parsing, meta={'package_name': app['packageName']}))
        return request_list

    def after_parsing(self, response):
        yield AppItemParser.parse(response)
        DBManager.delete_uncrawled_app(response.meta.get('package_name'))


