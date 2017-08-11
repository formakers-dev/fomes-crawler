# -*- coding: utf-8 -*-
import scrapy

from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.parser.app_item_parser import AppItemParser


class UncrawledAppSpider(scrapy.Spider):
    name = "UncrawledAppSpider"
    allowed_domains = ["play.google.com"]

    def start_requests(self):
        user_apps_list = DBManager.select_user_apps()
        request_list = []
        for user_apps in user_apps_list:
            apps = user_apps['apps']
            for app in apps:
                packageName = app['packageName']
                crawled_apps = DBManager.select_apps(packageName)
                if crawled_apps.count() <= 0:
                    request_list.append(scrapy.Request('https://play.google.com/store/apps/details?id=' + packageName,
                                                                                    callback=self.after_parsing, meta={'package_name': packageName}))
        return request_list

    def after_parsing(self, response):
        yield AppItemParser.parse(response)


