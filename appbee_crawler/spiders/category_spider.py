# -*- coding: utf-8 -*-
import scrapy
from appbee_crawler.category_items import CategoryItem
from scrapy.selector import Selector


class CategorySpider(scrapy.Spider):
    name = "CategorySpider"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps"]

    def parse(self, response):
        hxs = Selector(response)
        selects = hxs.xpath("//a[@class='child-submenu-link']")
        items = []
        for sel in selects:
            item = CategoryItem()
            item['id'] = sel.xpath("@href").extract()[0]
            item['title'] = sel.xpath("@title").extract()[0]
            items.append(item)
        return items
