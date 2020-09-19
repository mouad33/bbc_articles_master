# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class BbcArticlesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	
    title=scrapy.Field()
    
    url=scrapy.Field()
    
    related_topics=scrapy.Field()
    article_text=scrapy.Field()


