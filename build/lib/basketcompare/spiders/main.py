from scrapy.spiders import SitemapSpider
from datetime import datetime

class MainSpider(SitemapSpider):
	name = "MainSpider"
	custom_settings = {
	
	}
	
	date = datetime.today().strftime('%Y-%m-%d')
	counter = 0
	gcs = True


	def promo_regex(self):
		return self.shelf_price

