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

        app_name = hxs.xpath("//h1[@itemprop='name']/span/text()").extract()

        if len(app_name) is 0:
            return None

        item['appName'] = app_name[0]

        package_name = response.url.split('=')

        if len(package_name) > 1:
            item['packageName'] = response.url.split('=')[1]

        score_data = hxs.xpath("//meta[@itemprop='ratingValue']/@content").extract()
        if len(score_data) > 0:
            item['star'] = float(score_data[0])
        else:
            item['star'] = 0

        installs = hxs.xpath("//div[@class='hAyfc']/div[@class='BgcNfc' and text()='설치 수']/"
                             "../span[@class='htlgb']/div/span[@class='htlgb']/text()").extract()
        if len(installs) > 0:
            installs_parse = installs[0].split('+')
            item['installsMin'] = StringUtil.parseNumber(installs_parse[0])

            if installs_parse[0][0] == '5':
                item['installsMax'] = item['installsMin'] * 2
            elif installs_parse[0][0] == '1':
                item['installsMax'] = item['installsMin'] * 5
            else:
                item['installsMax'] = 0
        else:
            item['installsMin'] = 0
            item['installsMax'] = 0

        review_count = hxs.xpath("//meta[@itemprop='reviewCount']/@content").extract()
        if len(review_count) > 0:
            item['reviewCount'] = StringUtil.parseNumber(review_count[0])
        else:
            item['reviewCount'] = 0

        update_date = hxs.xpath("//div[@class='hAyfc']/div[@class='BgcNfc' and text()='업데이트 날짜']/ ../span["
                                "@class='htlgb']/div/span[@class='htlgb']/text()").extract_first()
        item['updatedDate'] = DateUtil.get_date_format(update_date)

        category_selector = hxs.xpath("//a[@itemprop='genre']")
        category_ids = category_selector.xpath("@href").extract()
        category_names = category_selector.xpath("text()").extract()

        item['categoryId1'] = category_ids[0].split('/')[-1]
        item['categoryName1'] = category_names[0]

        if len(category_ids) > 1:
            item['categoryId2'] = category_ids[1].split('/')[-1]
            item['categoryName2'] = category_names[1]
        else:
            item['categoryId2'] = ''
            item['categoryName2'] = ''

        item['contentsRating'] = hxs.xpath("//meta[@itemprop='contentRating']/@content").extract_first()
        item['developer'] = hxs.xpath("//a[@class='hrTbp R8zArc' and starts-with(@href, "
                                      "'https://play.google.com/store/apps/dev')]/text()").extract_first()
        item['description'] = ''.join(hxs.xpath("//meta[@itemprop='description']/@content").extract())

        app_price = hxs.xpath("//meta[@itemprop='price']/@content").extract_first()

        if app_price is not None:
            app_price = app_price.split('₩')

            if len(app_price) == 2:
                item['appPrice'] = StringUtil.parseNumber(app_price[1])
            else:
                item['appPrice'] = 0
        else:
            item['appPrice'] = 0

        in_app_price = hxs.xpath("//div[@class='BgcNfc' and text()='인앱 상품']/../span/div/span/text()").extract_first()

        in_app_price_min = '0'
        in_app_price_max = '0'

        # 인앱구매 가격이 범위가 아닐경우 min과 max를 통일.
        # min, max 둘 중 하나에만 값이 있으면 범위로 오인할 수도 있음.
        if in_app_price is not None:
            in_app_price_list = in_app_price.split(' ')
            in_app_price_min = in_app_price_list[1].split('₩')[1]

            if '-' in in_app_price:
                in_app_price_max = in_app_price_list[3].split('₩')[1]
            else:
                in_app_price_max = in_app_price_min

        item['inappPriceMin'] = StringUtil.parseNumber(in_app_price_min)
        item['inappPriceMax'] = StringUtil.parseNumber(in_app_price_max)

        similar_app_hreps = hxs.xpath(
            "//div[@class='WHE7ib mpg5gc']//div[@class='b8cIId ReQCgd Q9MA7b']/a/@href").extract()
        item['similarApps'] = list(map(lambda hrep: hrep.split("=")[1], similar_app_hreps))

        icon_path_str = hxs.xpath("//img[@itemprop='image' and @alt='포스터']/@src").extract()

        if len(icon_path_str) > 0:
            item['iconUrl'] = icon_path_str[0]
        else:
            item['iconUrl'] = ''

        item['imageUrls'] = cls.parse_image_urls(hxs)

        return item

    @classmethod
    def parse_image_urls(cls, html_xpath_selector):
        img_tag_selectors = html_xpath_selector.xpath("//button/img[@itemprop='image']")
        image_urls = []

        for img_tag_selector in img_tag_selectors:
            data_src = img_tag_selector.re(r'\sdata-src="(\S+)"')

            if len(data_src) > 0:
                image_urls.append(data_src[0])
            else:
                src = img_tag_selector.re(r'\ssrc="(\S+)"')
                if len(src) > 0:
                    image_urls.append(src[0])

        return image_urls
