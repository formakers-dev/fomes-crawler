# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from appbee_crawler.spiders.parser.app_item_parser import AppItemParser


class AppSpider(scrapy.Spider):
    name = "AppSpider"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps/collection/topselling_free?authuser=0",
                    "https://play.google.com/store/apps/collection/topselling_paid?authuser=0",
                    "https://play.google.com/store/apps/collection/topgrossing?authuser=0",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_free?authuser=0",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_paid?authuser=0",
                    "https://play.google.com/store/apps/category/GAME/collection/topgrossing?authuser=0"]

    def get_form_data(self, page_number):
        return {
            'start': str(page_number*60),
            'num': '60',
            'numChildren': '0',
            'ipf': '1',
            'xhr': '1'
        }

    def start_requests(self):
        return_list = []

        for url in self.start_urls:
            for page_number in range(0, 9):
                return_list.append(scrapy.FormRequest(url=url, formdata=self.get_form_data(page_number), callback=self.after_app_list_parsing))
        return return_list

    def after_app_list_parsing(self, response):
        hxs = Selector(response)
        selects = hxs.xpath("//div[@class='details']/a[@class='card-click-target']")
        for sel in selects:
            package_name = sel.xpath("@href").extract()[0].split('=')[1]
            request = scrapy.Request('https://play.google.com/store/apps/details?id=' + package_name,
                                     callback=self.after_parsing, meta={'package_name': package_name})
            yield request

    def after_parsing(self, response):
        yield AppItemParser.parse(response)

        generator = self.request_similar_apps(response)
        for request in generator:
            yield request

    def request_similar_apps(self, response):
        hxs = Selector(response)

        # 유사한 앱 목록
        selects = hxs.xpath("//div[@class='id-cluster-container details-section recommendation']//a[@class='title']")
        for sel in selects:
            similar_package_name = sel.xpath("@href").extract()[0].split('=')[1]
            request = scrapy.Request('https://play.google.com/store/apps/details?id=' + similar_package_name,
                                     callback=self.after_parsing, meta={'package_name': similar_package_name,
                                                                        'priority': -1})
            yield request


