from basketcompare.spiders.price_bq import *

class BQ_Attr_Spider(Price_BQ):
	name = "attrraw_bq"
	scrape_type = name.split("_")[0]
	scrape_retailer = name.split("_")[1]

	custom_settings = {
		'FEED_URI': "file:///tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".json",
		'FEED_FORMAT': 'json',
		'FEED_EXPORTERS': {
    		'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
		},
		'ITEM_PIPELINES': {
		    'basketcompare.pipelines.AttrItemPipeline': 300,
		    'basketcompare.pipelines.LocalImagesPipeline': 1,
		},

		'IMAGES_STORE': '/home/jake/Pictures/products/bq',
	}


	def parse(self, response):
		l = ItemLoader(item=AttrItem(), response=response)
		
		#Get JSON from script
		script_text = response.xpath("//script[contains(text(), 'window.__data')]/text()").extract_first()
		script_json = re.search('window.__data=(.*);', script_text).group(1)
		json_obj = json.loads(script_json)
		
		attributes = json_obj['product']['main']['product']['attributes']

		l.add_value('date', self.date)
		sku_1 = re.search('([0-9]+_BQ)', response.url).group(1)
		l.add_value('sku_1', sku_1)
		l.add_value('sku_2', attributes['ean'])
		l.add_value('description', attributes['name'])
		l.add_value('url', response.url)

		# For items not in a taxonomy
		try:
			l.add_value('taxonomy', re.search('departments\/(.*)\/diy', attributes['breadcrumbList'][0]['seoUrl'].lower()).group(1))
		except IndexError:
			pass

		#Get dynamic product attributes and add to dictionary
		product_attributes = attributes['technicalSpecifications']

		for i in product_attributes:
			attr_key = re.sub(r'\W+', ' ', i['name']).strip().lower().replace(" ", "_") #Spaces wont be accepted in an SQL table.
			attr_value = i['value'].strip().lower()
			l.add_value('attributes', {attr_key: attr_value})
			# print(attr_key, attr_value)
			# attr_dict(attr_key) = attr_value
			# print(attr_dict)


		#Images
		try:
			img_url = response.xpath("//img[contains(@src, 'media')]").extract_first()
			img_code = re.search('([0-9]+_0[0-9][a-zA-Z]+)(&|\?)', img_url).group(1)
			url =  "https://media.diy.com/is/image/Kingfisher/" + img_code + "?$MOB_PREV$&$width=200&$height=200"	
			l.add_value('image_urls', url)
			l.add_value('image_name', sku_1)
		except TypeError:
			l.add_value('image_urls', '')
			l.add_value('image_name', '')


		return l.load_item()

		

