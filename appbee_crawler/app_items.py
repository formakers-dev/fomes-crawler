# -*- coding: utf-8 -*-
import scrapy

class AppItem(scrapy.Item):
    package_name = scrapy.Field()
    app_name = scrapy.Field()
    star = scrapy.Field()
    installs_min = scrapy.Field()
    installs_max = scrapy.Field()
    reviews = scrapy.Field()
    updated = scrapy.Field()
    category_id = scrapy.Field()
    contents_rating = scrapy.Field()
    developer = scrapy.Field()
    description = scrapy.Field()
    app_price = scrapy.Field()
    inapp_price_min = scrapy.Field()
    inapp_price_max = scrapy.Field()





