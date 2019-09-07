# -*- coding: utf-8 -*-

import os
from datetime import datetime
import re
import json


class PriceItemPipeline(object):

	def __init__(self):
		self.items_seen = set()

	def regex_promo(self, shelf_price, promotion):
	# print("£",shelf_price,", ", promotion)
	# x for £xx
		x = re.search('(?!.*?each)([0-9]+) for £(\d*\.?\d*).*', promotion, re.IGNORECASE)
		if x:
			x1 = round(float(x.group(2)) / float(x.group(1)), 2)
			print(x1)
			return x1
			
		 # x or more for £x.xx?
		x = re.search('.*[0-9]+ or more for £(\d*\.?\d*).*', promotion, re.IGNORECASE)
		if x:
			x1 = round(float(x.group(1)), 2)
			print(x1)
			return x1
			
			
		# £x.xx each when you buy x or more
		x = re.search('.*£(\d*\.?\d*) each', promotion, re.IGNORECASE)
		if x:
			x1 = round(float(x.group(1)), 2)
			print(x1)
			return x1

		# Buy 1 get 1 free
		x = re.search('(buy (one|1) get (one|1) free|bogof)', promotion, re.IGNORECASE)
		if x:
			x1 = round(shelf_price / 2, 2)
			print(x1)
			return x1


		# x for (the price of)? x
		x = re.search('.*([3-5]) for (the price of )?([2-4]).*', promotion, re.IGNORECASE)
		if x:
			if x.group(3):
				x1 = round(shelf_price * (float(x.group(3)) / float(x.group(1))), 2)
				print(x1)
				return x1
			else:
				x1 = round(shelf_price * (float(x.group(2)) / float(x.group(1))), 2)
				print(x1)
				return x1

		# xx% off when you spend £x +
		x = re.search('([0-9]+)% off.*when you spend.* £(\d*\.?\d*).*', promotion, re.IGNORECASE)
		if x:
			if shelf_price > float(x.group(2)):
				x1 = round(shelf_price * (1 - float(x.group(1)) / 100), 2)
				print(x1)
				return x1
			else:
				print(shelf_price)
				return shelf_price

		# £x off when you spend £x +
		x = re.search('£(\d*\.?\d*).*when you spend.*£(\d*\.?\d*).*', promotion, re.IGNORECASE)
		if x:
			if shelf_price > float(x.group(2)):
				x1 = round(shelf_price - float(x.group(1)), 2)
				print(x1)
				return x1
			else:
				print(shelf_price)
				return shelf_price

		# Buy 1 get 1 half price
		x = re.search('buy (one|1).*half price.*', promotion, re.IGNORECASE)
		if x:
			x1 = round(shelf_price * 0.75, 2)
			print(x1)
			return x1

		# xx% off, discount applied at checkout
		x = re.search('([0-9]+)% off.*checkout.*', promotion, re.IGNORECASE)
		if x:
			x1 = round(shelf_price * (1 - float(x.group(1)) / 100), 2)
			print(x1)
			return x1
		else:
			print(shelf_price)
			return shelf_price

	def process_item(self, item, spider):
		if item['sku_1'][0] in self.items_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.items_seen.add(item['sku_1'][0]) # Add item to set

			# To Remove lists
			item['date'] = item['date'][0]
			item['sku_1'] = item['sku_1'][0]
			item['sku_2'] = item['sku_2'][0]
			# item['description'] = item['description'][0]
			item['promotion'] = item['promotion'][0]
			item['shelf_price'] = round(float(item['shelf_price'][0]), 2) # Because item loader returns a list. Convert string to float.
			try:
				item['promo_price'] = self.regex_promo(item['shelf_price'], item['promotion'])
			except TypeError: # For when promotion == None
				item['promo_price'] = item['shelf_price']


			return item

	def close_spider(self, spider):
		if spider.gcs == True:

			from google.cloud import storage
			from google.oauth2 import service_account


			# Create json object from Credentials Dict
			settings_credentials = str(spider.settings.get('CREDENTIALS'))
			# dumped = json.dumps(spider.settings.get('CREDENTIALS'))
			loaded = json.loads(settings_credentials.replace("\'", "\""))
			# loaded = json.loads(spider.settings.get('CREDENTIALS'))
			credentials = service_account.Credentials.from_service_account_info(loaded) # Dumps = data to json, loads = json to python.

			# Explicitly use service account credentials by specifying the private key
			client = storage.Client(project="basketcompare-247312", credentials=credentials)

			# Make an authenticated API request
			scrape_type = spider.name.split("_")[0]
			scrape_retailer = spider.name.split("_")[1]
			yyyymmdd = datetime.today().strftime('%Y%m%d')

			bucket = client.get_bucket('basketcompare')
			file_path = scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + yyyymmdd + ".json"
			local_file_path = "/tmp/" + file_path
			# blob = bucket.blob("/" + scrape_type + "/" + scrape_retailer + "/" scrape_retailer + "_" + yyyymmdd)
			blob = bucket.blob(file_path)
			blob.upload_from_filename(local_file_path)

class AttrItemPipeline(object):

	def process_item(self, item, spider):
		return item