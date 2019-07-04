# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class Definition(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = Field()
    word_text = Field()
    word_html = Field()
    header = Field()
    definition_html = Field()
    definition_text = Field()
    see_also = Field()

