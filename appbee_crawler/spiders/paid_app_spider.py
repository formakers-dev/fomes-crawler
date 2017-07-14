# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from appbee_crawler.app_items import AppItem
from appbee_crawler.util.date_util import DateUtil

class PaidAppSpider(scrapy.Spider):
    name = "PaidAppSpider"
    allowed_domains = ["play.google.com"]
    start_urls = "https://play.google.com/store/apps/collection/topselling_paid"
    frmdata = {
        'start': '180',
        'num': '60',
        'numChildren': '0',
        'ipf': '1',
        'xhr': '1'
    }

    def start_requests(self):
        return [scrapy.FormRequest(self.start_urls, method='POST', callback=self.after_app_parsing)]

    def after_app_parsing(self, response):
        hxs = Selector(response)
        selects = hxs.xpath("//div[@class='details']/a[@class='card-click-target']")
        for sel in selects:
            package_name = sel.xpath("@href").extract()[0].split('=')[1]
            request = scrapy.Request('https://play.google.com/store/apps/details?id=' + package_name, callback=self.after_parsing, meta = {'package_name' : package_name})
            yield request

    def after_parsing(self, response):
        hxs = Selector(response)
        items = []
        item = AppItem()
        item['package_name'] = response.meta.get('package_name')
        item['app_name'] = hxs.xpath("//div[@class='id-app-title']/text()[1]").extract()[0]
        item['star'] = hxs.xpath("//div[@class='score']/text()[1]").extract()[0]
        item['installs_min'] = hxs.xpath("//div[@itemprop='numDownloads']/text()[1]").extract()[0].split('-')[0].replace(',', '')
        item['installs_max'] = hxs.xpath("//div[@itemprop='numDownloads']/text()[1]").extract()[0].split('-')[1].replace(',', '')
        item['reviews'] = hxs.xpath("//span[@class='reviews-num']/text()[1]").extract()[0].replace(',', '')
        item['updated'] = DateUtil().get_date_format(hxs.xpath("//div[@itemprop='datePublished']/text()[1]").extract()[0].replace(' ', ''))
        item['category_id'] = hxs.xpath("//span[@itemprop='genre']/text()[1]").extract()[0]
        item['contents_rating'] = hxs.xpath("//div[@itemprop='contentRating']/text()[1]").extract()[0]
        item['developer'] = hxs.xpath("//a[@class='document-subtitle primary']/span[@itemprop='name']/text()[1]").extract()[0]
        item['description'] = ''.join(hxs.xpath("//div[@itemprop='description']/div/text()").extract())
        item['app_price'] = hxs.xpath("//div[@class='info-container']//button[@class='price buy id-track-click id-track-impression']/span[last()]/text()[1]").extract()[0].split(' ₩')[1].replace(',', '')

        inappListSize = len(hxs.xpath("//div[@class = 'content' and ../div/text()[1] = '인앱 상품']/text()[1]"))
        if inappListSize > 0:
            in_app_price_string = hxs.xpath("//div[@class = 'content' and ../div/text()[1] = '인앱 상품']/text()[1]").extract()[0].replace(',', '')
            if '~' not in in_app_price_string:
                item['inapp_price_min'] = in_app_price_string.split('₩')[1]
            else:
                item['inapp_price_min'] = in_app_price_string.split('~')[0].split('₩')[1]
                item['inapp_price_max'] = in_app_price_string.split('~')[1].split('₩')[1]
        else:
            item['inapp_price_min'] = 0
            item['inapp_price_max'] = 0

        items.append(item)
        return items





