# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from appbee_crawler.app_items import AppItem
from appbee_crawler.util.date_util import DateUtil
from appbee_crawler.util.string_util import StringUtil


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
        yield self.parse_app_item(response)

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
                                     callback=self.after_parsing, meta={'package_name': similar_package_name})
            yield request

    def parse_app_item(self, response):
        hxs = Selector(response)
        item = AppItem()
        item['package_name'] = response.meta.get('package_name')

        appName = hxs.xpath("//div[@class='id-app-title']/text()[1]").extract()

        if len(appName) is 0:
            return None

        item['app_name'] = appName[0]
        item['star'] = float(hxs.xpath("//div[@class='score']/text()[1]").extract()[0])

        installs = hxs.xpath("//div[@itemprop='numDownloads']/text()[1]").extract()[0].split('-')
        item['installs_min'] = StringUtil.parseNumber(installs[0])
        item['installs_max'] = StringUtil.parseNumber(installs[1])

        item['review_count'] = StringUtil.parseNumber(hxs.xpath("//span[@class='reviews-num']/text()[1]").extract()[0])
        item['updated_date'] = DateUtil.get_date_format(hxs.xpath("//div[@itemprop='datePublished']/text()[1]").extract()[0])

        category_ids = hxs.xpath("//a[@class='document-subtitle category']/@href[1]").extract()
        category_names = hxs.xpath("//span[@itemprop='genre']/text()[1]").extract()
        item['category1_id'] = category_ids[0]
        item['category1_name'] = category_names[0]

        if len(category_ids) > 1:
            item['category2_id'] = category_ids[1]
            item['category2_name'] = category_names[1]
        else:
            item['category2_id'] = ''
            item['category2_name'] = ''

        item['contents_rating'] = hxs.xpath("//div[@itemprop='contentRating']/text()[1]").extract()[0]
        item['developer'] = hxs.xpath("//a[@class='document-subtitle primary']/span[@itemprop='name']//text()[1]").extract()[0]
        item['description'] = ''.join(hxs.xpath("//div[@itemprop='description']/div/text()").extract())

        appPrice = hxs.xpath("//div[@class='info-container']//button[@class='price buy id-track-click id-track-impression']/span[last()]/text()[1]").extract()[0].split('₩')

        if len(appPrice) == 2:
            item['app_price'] = StringUtil.parseNumber(appPrice[1])
        else:
            item['app_price'] = 0

        in_app_price_list = hxs.xpath("//div[@class = 'content' and ../div/text()[1] = '인앱 상품']/text()[1]")
        in_app_price_min = '0'
        in_app_price_max = '0'
        if len(in_app_price_list) > 0:
            in_app_price = in_app_price_list.extract()[0]
            if '~' not in in_app_price:
                in_app_price_min = in_app_price.split('₩')[1]
            else:
                in_app_price_min = in_app_price.split('~')[0].split('₩')[1]
                in_app_price_max = in_app_price.split('~')[1].split('₩')[1]

        item['inapp_price_min'] = StringUtil.parseNumber(in_app_price_min)
        item['inapp_price_max'] = StringUtil.parseNumber(in_app_price_max)

        return item

