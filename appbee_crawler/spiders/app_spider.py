# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from appbee_crawler.app_items import AppItem
from appbee_crawler.util.date_util import DateUtil
from appbee_crawler.util.string_util import StringUtil

class AppSpider(scrapy.Spider):
    name = "AppSpider"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps/collection/topselling_free",
                    "https://play.google.com/store/apps/collection/topselling_paid",
                    "https://play.google.com/store/apps/collection/topgrossing",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_free",
                    "https://play.google.com/store/apps/category/GAME/collection/topselling_paid",
                    "https://play.google.com/store/apps/category/GAME/collection/topgrossing"]

    frmdata = {
        'start': '0',
        'num': '100',
        'numChildren': '0',
        'ipf': '1',
        'xhr': '1'
    }

    def start_requests(self):
        return_list = []

        for url in self.start_urls:
            return_list.append(scrapy.FormRequest(url, method='POST', callback=self.after_app_list_parsing))

        return return_list

    def after_app_list_parsing(self, response):
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

        appName = hxs.xpath("//div[@class='id-app-title']/text()[1]").extract()

        if len(appName) is 0:
            return None

        item['app_name'] = appName[0]
        item['star'] = float(hxs.xpath("//div[@class='score']/text()[1]").extract()[0])

        installs = StringUtil().getPureNumber(hxs.xpath("//div[@itemprop='numDownloads']/text()[1]").extract()[0])
        item['installs_min'] = int(installs.split('-')[0])
        item['installs_max'] = int(installs.split('-')[1])

        item['review_count'] = int(hxs.xpath("//span[@class='reviews-num']/text()[1]").extract()[0].replace(',', ''))
        item['updated_date'] = DateUtil().get_date_format(hxs.xpath("//div[@itemprop='datePublished']/text()[1]").extract()[0].replace(' ', ''))
        item['category_id'] = hxs.xpath("//span[@itemprop='genre']/text()[1]").extract()[0]
        item['contents_rating'] = hxs.xpath("//div[@itemprop='contentRating']/text()[1]").extract()[0]
        item['developer'] = hxs.xpath("//a[@class='document-subtitle primary']/span[@itemprop='name']//text()[1]").extract()[0]
        item['description'] = ''.join(hxs.xpath("//div[@itemprop='description']/div/text()").extract())

        appPrice = hxs.xpath("//div[@class='info-container']//button[@class='price buy id-track-click id-track-impression']/span[last()]/text()[1]").extract()[0].split('₩')

        if len(appPrice) == 2:
            item['app_price'] = int(appPrice[1].replace(',', ''))
        else:
            item['app_price'] = 0

        inappPriceListSize = len(hxs.xpath("//div[@class = 'content' and ../div/text()[1] = '인앱 상품']/text()[1]"))
        if inappPriceListSize > 0:
            in_app_price_string = hxs.xpath("//div[@class = 'content' and ../div/text()[1] = '인앱 상품']/text()[1]").extract()[0].replace(',', '')
            if '~' not in in_app_price_string:
                item['inapp_price_min'] = int(StringUtil().getPureNumber(in_app_price_string.split('₩')[1]))
            else:
                item['inapp_price_min'] = int(StringUtil().getPureNumber(in_app_price_string.split('~')[0].split('₩')[1]))
                item['inapp_price_max'] = int(StringUtil().getPureNumber(in_app_price_string.split('~')[1].split('₩')[1]))
        else:
            item['inapp_price_min'] = 0
            item['inapp_price_max'] = 0

        items.append(item)
        return items

