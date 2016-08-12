# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayProduct(scrapy.Item):
    section = scrapy.Field()
    name = scrapy.Field()
    picture = scrapy.Field()
    create_date = scrapy.Field()
    price = scrapy.Field()
    price_unit = scrapy.Field()
    seller = scrapy.Field()
    seller_href = scrapy.Field()
    shipping_price = scrapy.Field()
    shipping_unit = scrapy.Field()
    href = scrapy.Field()

