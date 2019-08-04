import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
print(sys)
import re
from basketcompare.spiders.price_bq import *
import json

class BQ_Attr_Spider(BQSpider):
	name = "bq_attr_spider"


	def parse(self, response):
		attr_dict = {}
		
		#Get JSON from script
		script_text = response.xpath("//script[contains(text(), 'window.__data')]/text()").extract_first().encode('utf-8')
		script_json = re.search('window.__data=(.*);', script_text).group(1)
		json_obj = json.loads(script_json)
		
		attributes = json_obj['product']['main']['product']['attributes']

		attr_dict['date'] = datetime.today().strftime('%Y-%m-%d')
		attr_dict['sku_1'] = attributes['ean']
		attr_dict['sku_2'] = re.search('([0-9]+_BQ)', response.url).group(1)
		attr_dict['description'] = attributes['name']
		attr_dict['url'] = response.url

		# For items not in a taxonomy
		try:
			attr_dict['taxonomy'] = re.search('departments\/(.*)\/diy', attributes['breadcrumbList'][0]['seoUrl'].lower()).group(1)
		except IndexError:
			pass

		#Get dynamic product attributes and add to dictionary
		product_attributes = attributes['technicalSpecifications']

		for i in product_attributes:
			attr_key = re.sub(r'\W+', ' ', i['name']).lower().replace(" ", "_")
			attr_value = i['value'].lower()
			attr_dict[attr_key] = attr_value
			# print(attr_key, attr_value)
			# attr_dict(attr_key) = attr_value
			# print(attr_dict)
							
		yield attr_dict

