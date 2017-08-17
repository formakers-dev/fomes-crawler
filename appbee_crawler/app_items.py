# -*- coding: utf-8 -*-
import scrapy

class AppItem(scrapy.Item):
    packageName = scrapy.Field()
    appName = scrapy.Field()
    star = scrapy.Field()
    installsMin = scrapy.Field()
    installsMax = scrapy.Field()
    reviewCount = scrapy.Field()
    updatedDate = scrapy.Field()
    categoryId1 = scrapy.Field()
    categoryName1 = scrapy.Field()
    categoryId2 = scrapy.Field()
    categoryName2 = scrapy.Field()
    contentsRating = scrapy.Field()    # 컨텐츠 등급
    developer = scrapy.Field()
    description = scrapy.Field()
    appPrice = scrapy.Field()
    inappPriceMin = scrapy.Field()
    inappPriceMax = scrapy.Field()
    similarApps = scrapy.Field()