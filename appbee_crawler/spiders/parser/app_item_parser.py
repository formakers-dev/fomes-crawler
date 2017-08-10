# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from appbee_crawler.app_items import AppItem
from appbee_crawler.util.date_util import DateUtil
from appbee_crawler.util.string_util import StringUtil

class AppItemParser(object):

    @classmethod
    def parse(cls, response):
        hxs = Selector(response)
        item = AppItem()
        item['package_name'] = response.meta.get('package_name')

        appName = hxs.xpath("//div[@class='id-app-title']/text()[1]").extract()

        if len(appName) is 0:
            return None

        item['app_name'] = appName[0]
        score_data = hxs.xpath("//div[@class='score']/text()[1]").extract()
        if(len(score_data) > 0):
            item['star'] = float(score_data[0])
        else:
            item['star'] = 0

        installs = hxs.xpath("//div[@itemprop='numDownloads']/text()[1]").extract()
        if len(installs) > 0:
            installs_parse = installs[0].split('-')
            item['installs_min'] = StringUtil.parseNumber(installs_parse[0])
            item['installs_max'] = StringUtil.parseNumber(installs_parse[1])
        else:
            item['installs_min'] = 0
            item['installs_max'] = 5

        review_count = hxs.xpath("//span[@class='reviews-num']/text()[1]").extract()
        if(len(review_count) > 0):
            item['review_count'] = StringUtil.parseNumber(review_count[0])
        else:
            item['review_count'] = 0

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

        app_price = hxs.xpath("//div[@class='info-container']//button[@class='price buy id-track-click id-track-impression']/span[last()]/text()[1]").extract()[0].split('₩')

        if len(app_price) == 2:
            item['app_price'] = StringUtil.parseNumber(app_price[1])
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

        similar_app_hreps = hxs.xpath("//div[@class='id-cluster-container details-section recommendation']//div[@class='card no-rationale square-cover apps small' and  ../../h1/a/text()[1] = '유사한 콘텐츠']//a[@class='title']/@href").extract()
        item['similar_apps'] = list(map(lambda hrep: hrep.split("=")[1], similar_app_hreps))

        return item