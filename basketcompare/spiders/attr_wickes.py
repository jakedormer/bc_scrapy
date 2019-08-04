from datetime import datetime
import re
import sys
from basketcompare.spiders.price_wickes import *


class Wickes_Attr_Spider(WickesSpider):
	name = "attr_wickes"
	custom_settings = {

	}


	def parse(self, response):
		attr_dict = {}
		attr_dict['date'] = datetime.today().strftime('%Y-%m-%d')
		attr_dict['sku_1'] = response.css('strong#product-code-val::text').extract()
		attr_dict['sku_2'] = ''
		attr_dict['description'] = response.css('h1.pdp__heading::text').extract()
		attr_dict['url'] = response.url

		breadcrumb_links = response.css('.breadcrumbs__item>a::attr(href)').extract() 
		attr_dict['taxonomy'] = re.search('products\/(.*)\/c\/', breadcrumb_links[len(breadcrumb_links)-1].lower()).group(1) #Count breadcrumb links and then choose n-1 link.

		attributes = response.selector.css('ul.info__lists-not-bullets>li')

		for i in attributes:
			attr_key_raw = re.search('([a-z0-9 ]+):', i.css('strong::text').extract_first().lower()).group(1).encode('utf-8')
			attr_key = re.sub(r'\W+', ' ', attr_key_raw).lower().replace(" ", "_")
			attr_value = i.css('li::text').extract()[1].encode('utf-8').replace('"', '').strip().lower()
			attr_dict[attr_key] = attr_value
			# print(attr_key, attr_value)
			# attr_dict(attr_key) = attr_value
			# print(attr_dict)
							
		yield attr_dict
