from basketcompare.spiders.price_bq import *

class BQ_Attr_Spider(BQSpider):
	name = "attr_bq"
	scrape_type = name.split("_")[0]
	scrape_retailer = name.split("_")[1]

	custom_settings = {
		'FEED_URI': "file:///tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".json",
		'FEED_FORMAT': 'json',
		'FEED_EXPORTERS': {
    		'jsonlines': 'scrapy.exporters.CsvItemExporter',
		},
		'ITEM_PIPELINES': {
			'basketcompare.pipelines.AttrItemPipeline': 300,
		},
	}


	def parse(self, response):
		attr_dict = {}
		
		#Get JSON from script
		script_text = response.xpath("//script[contains(text(), 'window.__data')]/text()").extract_first()
		script_json = re.search('window.__data=(.*);', script_text).group(1)
		json_obj = json.loads(script_json)
		
		attributes = json_obj['product']['main']['product']['attributes']

		attr_dict['date'] = datetime.today().strftime('%Y-%m-%d')
		attr_dict['sku_1'] = re.search('([0-9]+_BQ)', response.url).group(1)
		attr_dict['sku_2'] = attributes['ean']
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
			attr_key = re.sub(r'\W+', ' ', i['name']).strip().lower().replace(" ", "_") #Spaces wont be accepted in an SQL table.
			attr_value = i['value'].strip().lower()
			attr_dict[attr_key] = attr_value
			# print(attr_key, attr_value)
			# attr_dict(attr_key) = attr_value
			# print(attr_dict)
							
		yield attr_dict

