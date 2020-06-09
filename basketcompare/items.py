# -*- coding: utf-8 -*-

import scrapy


class ScrapeItem(scrapy.Item):
	date = scrapy.Field()
	sku_1 = scrapy.Field()
	sku_2 = scrapy.Field()
	shelf_price = scrapy.Field()
	promo_price = scrapy.Field()
	promotion = scrapy.Field()


class AttrItem(scrapy.Item):
	date = scrapy.Field()
	sku_1 = scrapy.Field()
	sku_2 = scrapy.Field()
	description = scrapy.Field()
	url = scrapy.Field()
	taxonomy = scrapy.Field()
	attributes = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()
	image_name = scrapy.Field()





	
