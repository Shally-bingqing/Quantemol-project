# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Cccb(scrapy.Item):
    #accroding to the html table
    Molecule = scrapy.Field()
    Name = scrapy.Field()
    State = scrapy.Field()
    Conformation = scrapy.Field()
    Alpha = scrapy.Field()
    Squib =scrapy.Field()
    Commment = scrapy.Field()
    pass

class Nist(scrapy.Item):
    Name = scrapy.Field()
    Formula = scrapy.Field()
    CAS = scrapy.Field()
    IE=scrapy.Field()
    Method=scrapy.Field()
    Refer=scrapy.Field()
    Comment=scrapy.Field()