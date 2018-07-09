# -*- coding: utf-8 -*-
import scrapy


class AppItem(scrapy.Item):
    # 항상 페이지 소스코드 안에 포함돼있는 정보
    packageName = scrapy.Field()
    appName = scrapy.Field()
    updatedDate = scrapy.Field()
    developer = scrapy.Field()
    description = scrapy.Field()
    appPrice = scrapy.Field()
    iconUrl = scrapy.Field()   # icon path
    categoryId1 = scrapy.Field()
    categoryName1 = scrapy.Field()
    contentsRating = scrapy.Field()    # 컨텐츠 등급

    # 항상 페이지에 포함되나 형태가 달라지는 정보
    installsMin = scrapy.Field()
    installsMax = scrapy.Field()

    # 값에 따라 페이지 소스코드에서 사라지는 정보
    star = scrapy.Field()
    reviewCount = scrapy.Field()
    categoryId2 = scrapy.Field()
    categoryName2 = scrapy.Field()
    inappPriceMin = scrapy.Field()      # 인앱결제 가격이 한 가지인 경우도 있음.
    inappPriceMax = scrapy.Field()
    similarApps = scrapy.Field()
