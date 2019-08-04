from scrapy.spiders import SitemapSpider

class MainSpider(SitemapSpider):
	name = "MainSpider"


	def promo_regex(self):
		return self.shelf_price

