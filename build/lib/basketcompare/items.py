# -*- coding: utf-8 -*-

import scrapy


class ScrapeItem(scrapy.Item):
	date = scrapy.Field()
	sku_1 = scrapy.Field()
	sku_2 = scrapy.Field()
	shelf_price = scrapy.Field()
	promo_price = scrapy.Field()
	promotion = scrapy.Field()






	
