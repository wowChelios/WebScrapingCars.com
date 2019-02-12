# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarscomItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    year = scrapy.Field()
    made = scrapy.Field()
    model = scrapy.Field()
    price = scrapy.Field()
    slrzip = scrapy.Field()
    slreview = scrapy.Field()
    fuel = scrapy.Field()
    cty = scrapy.Field()
    hwy = scrapy.Field()
    drive = scrapy.Field()
    eng = scrapy.Field()
    mileage = scrapy.Field()
    exter = scrapy.Field()
    inter = scrapy.Field()
    tran = scrapy.Field()



