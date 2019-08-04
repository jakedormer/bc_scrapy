# -*- coding: utf-8 -*-

import scrapy


class ScrapeItem(scrapy.Item):
	date = scrapy.Field()
	sku1 = scrapy.Field()
	sku2 = scrapy.Field()
	description = scrapy.Field()
	shelf_price = scrapy.Field()
	promo_price = scrapy.Field()
	promotion = scrapy.Field()






	
