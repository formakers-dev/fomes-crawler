# -*- coding: utf-8 -*-
import scrapy

class AppItem(scrapy.Item):
    package_name = scrapy.Field()
    app_name = scrapy.Field()
    star = scrapy.Field()
    installs_min = scrapy.Field()
    installs_max = scrapy.Field()
    review_count = scrapy.Field()
    updated_date = scrapy.Field()
    category_id = scrapy.Field()
    contents_rating = scrapy.Field()    # 컨텐츠 등급
    developer = scrapy.Field()
    description = scrapy.Field()
    app_price = scrapy.Field()
    inapp_price_min = scrapy.Field()
    inapp_price_max = scrapy.Field()