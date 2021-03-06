# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError

from appbee_crawler.manager.db_manager import DBManager
from appbee_crawler.spiders.parser.app_item_parser import AppItemParser


class UncrawledAppSpider(scrapy.Spider):
    name = "UncrawledAppSpider"
    allowed_domains = ["play.google.com"]

    def start_requests(self):
        uncrawled_package_names = DBManager.get_uncrawled_package_names_without_error_code()
        for package_name in uncrawled_package_names:
            if package_name == 'com.formakers.fomes':
                continue

            request = scrapy.Request('https://play.google.com/store/apps/details?id=' + package_name,
                                     callback=self.after_parsing, meta={'packageName': package_name},
                                     dont_filter=True, errback=self.error_handler)
            yield request

    @staticmethod
    def after_parsing(response):
        yield AppItemParser.parse(response)

    @staticmethod
    def error_handler(failure):
        if failure.check(HttpError):
            response = failure.value.response
            print(response.meta.get('packageName'), "/", response.status)
            DBManager.update_error_code_of_uncrawled_app(response.meta.get('packageName'), response.status)
