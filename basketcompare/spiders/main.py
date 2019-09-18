import scrapy
from scrapy.spiders import SitemapSpider
from datetime import datetime
from scrapy.loader import ItemLoader
from basketcompare.items import ScrapeItem
import re
from scrapy.exceptions import CloseSpider
import json

class MainSpider(SitemapSpider):
	name = "MainSpider"
	custom_settings = {
	
	}
	
	date = datetime.today().strftime('%Y-%m-%d')
	yyyymmdd = datetime.today().strftime('%Y%m%d')
	counter = 0
	gcs = True


