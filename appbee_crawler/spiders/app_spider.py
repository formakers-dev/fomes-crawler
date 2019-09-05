# -*- coding: utf-8 -*-
import os

import scrapy
from scrapy.selector import Selector

from appbee_crawler.spiders.parser.app_item_parser import AppItemParser


class AppSpider(scrapy.Spider):
    name = "AppSpider"
    allowed_domains = ["play.google.com"]
    app_info_request_url = 'https://play.google.com/store/apps/details?id='
    app_counter = 0

    def __init__(self, urls=None, *args, **kwargs):
        super(AppSpider, self).__init__(*args, **kwargs)

        if urls is not None:
            if os.environ['PYTHON_ENV'] not in ['test']:
               self.start_urls = urls.split(';')

    @staticmethod
    def generate_form_data(page_number):
        return {
            'start': str(page_number * 60),
            'num': '60',
            'numChildren': '0',
            'ipf': '1',
            'xhr': '1'
        }

    def start_requests(self):
        return_list = []

        if self.packageName is not None:
            return_list.append(scrapy.FormRequest(url=self.app_info_request_url + self.packageName,
                               callback=self.after_parsing, meta={'packageName': self.packageName}))
        else:
            for url in self.start_urls:
                for page_number in range(0, 9):
                    return_list.append(scrapy.FormRequest(url=url, formdata=self.generate_form_data(page_number),
                                                      callback=self.after_app_list_parsing))
        return return_list

    def after_app_list_parsing(self, response):
        hxs = Selector(response)
        selects = hxs.xpath("//div[@class='details']/a[@class='card-click-target']")

        for sel in selects:
            package_name = sel.xpath("@href").extract()[0].split('=')[1]

            if package_name == 'com.formakers.fomes':
                continue

            self.app_counter += 1
            print('### [%5d] %s' % (self.app_counter, package_name))
            request = scrapy.Request(self.app_info_request_url + package_name,
                                     callback=self.after_parsing, meta={'packageName': package_name})
            yield request

    def after_parsing(self, response):
        parsed_app_item = AppItemParser.parse(response)

        if parsed_app_item.is_game():
            yield parsed_app_item

        generator = self.request_similar_apps(response)
        for request in generator:
            yield request

    def request_similar_apps(self, response):
        hxs = Selector(response)

        if 'depth' in response.meta:
            print('Referer=', response.request.headers.get('Referer'), ' depth=', response.meta['depth'])

        # 유사한 앱 목록
        selects = hxs.xpath("//div[@class='WHE7ib mpg5gc']//div[@class='b8cIId ReQCgd Q9MA7b']/a")

        for sel in selects:
            similar_package_name = sel.xpath("@href").extract()[0].split('=')[1]
            request = scrapy.Request(self.app_info_request_url + similar_package_name,
                                     callback=self.after_parsing, meta={'packageName': similar_package_name,
                                                                        'priority': -1})

            yield request
