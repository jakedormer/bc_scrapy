# -*- coding: utf-8 -*-

import os
from datetime import datetime
import re
import json
import smtplib
from scrapy.mail import MailSender
from email.message import EmailMessage
from scrapy.pipelines.images import ImagesPipeline, FilesPipeline
from scrapy.pipelines.files import GCSFilesStore
from scrapy.utils.project import get_project_settings
from basketcompare.items import ScrapeItem, AttrItem
from scrapy.http.request import Request
from scrapy.exceptions import DropItem


class PriceItemPipeline(object):

	def __init__(self):
		self.items_seen = set()
		self.date_count = 0
		self.sku_1_count = 0
		self.sku_2_count = 0
		self.description_count = 0
		self.shelf_price_count = 0
		self.promotion_count = 0

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

	def send_email(self, spider):


		gmail_user = spider.settings.get('GMAIL_USER')
		gmail_password = spider.settings.get('GMAIL_PASSWORD')
		

		msg = EmailMessage()
		msg['Subject'] = spider.name + " - " + spider.date
		msg['From'] = gmail_user
		msg['To'] = spider.settings.get('EMAIL_TO')
		body = "date_count: " + str(self.date_count) + "\n"
		body += "sku_1_count: " + str(self.sku_1_count) + "\n"
		body += "sku_2_count: " + str(self.sku_2_count) + "\n"
		body += "promotion_count: " + str(self.promotion_count) + "\n"
		body += "shelf_price_count: " + str(self.shelf_price_count)

		msg.set_content(str(body))


		
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.send_message(msg)
		server.close()


	def process_item(self, item, spider):
		# Check for duplcates first.

		# Check for duplcates first.
		if item['sku_1'][0] in self.items_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.items_seen.add(item['sku_1'][0]) # Add item to set

		# To Remove lists & Add Counts
		item['date'] = item['date'][0]
		if item['date'] != '':
			self.date_count +=1

		item['sku_1'] = item['sku_1'][0]
		if item['sku_1'] != '':
			self.sku_1_count += 1
		
		item['sku_2'] = item['sku_2'][0]
		if item['sku_2'] != '':
			self.sku_2_count += 1

		item['promotion'] = item['promotion'][0]
		if item['promotion'] != '':
			self.promotion_count += 1

		item['shelf_price'] = round(float(item['shelf_price'][0]), 2)
		if item['shelf_price'] != '':
			self.shelf_price_count += 1
		
		if item['promo_price']:
			pass
		else:
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
			settings_credentials = str(spider.settings.get('CREDENTIALS')).replace("'", '"')
			# dumped = json.dumps(spider.settings.get('CREDENTIALS'))
			loaded = json.loads(settings_credentials.replace("\'", "\""))
			# loaded = json.loads(spider.settings.get('CREDENTIALS'))
			credentials = service_account.Credentials.from_service_account_info(loaded) # Dumps = data to json, loads = json to python.

			# Explicitly use service account credentials by specifying the private key
			client = storage.Client(project="basketcompare-247312", credentials=credentials)

			# Make an authenticated API request

			bucket = client.get_bucket('basketcompare')
			file_path = spider.scrape_type + "/" + spider.scrape_retailer + "/" + spider.scrape_retailer + "_" + spider.yyyymmdd + ".csv"
			local_file_path = "/tmp/" + file_path
			# blob = bucket.blob("/" + scrape_type + "/" + scrape_retailer + "/" scrape_retailer + "_" + yyyymmdd)
			blob = bucket.blob(file_path)
			blob.upload_from_filename(local_file_path)

		self.send_email(spider)

class AttrItemPipeline(object):

	def process_item(self, item, spider):
		return item


class GCSImagesPipeline(GCSFilesStore):

	GCS_PROJECT_ID = "basketcompare-247312"


	def __init__(self):
	  from google.cloud import storage
	  from google.oauth2 import service_account
	  settings = get_project_settings()
	  settings_credentials = settings['CREDENTIALS']
	  loaded = json.loads(str(settings_credentials).replace("\'", "\""))
	  credentials = service_account.Credentials.from_service_account_info(loaded)
	  bucket = "basketcompare_images/products/wickes/"
	  client = storage.Client(project="basketcompare-247312", credentials=credentials)

class GCSFilePipeline(FilesPipeline):
	def __init__(self, store_uri, download_func=None, settings=None):
		super(GCSFilePipeline, self).__init__(store_uri,download_func,settings)
  

class LocalImagesPipeline(ImagesPipeline):

	# def process_item(self, item, spider):

		# # To Remove lists & Add Counts
		# item['date'] = item['date'][0]

		# item['sku_1'] = item['sku_1'][0]
		
		# item['sku_2'] = item['sku_2'][0]

		# item['description'] = item['description'][0]

		# item['url'] = item['url'][0]

		# item['taxonomy'] = item['taxonomy'][0]

		# item['attributes'] = item['attributes']

		# # item['image_urls'] = item['image_urls'][0]

		# # item['image_name'] = item['image_name'][0]

		# return item

	# def __init__(self):
	# 	self.items_seen = set()
	# 	self.date_count = 0
	# 	self.sku_1_count = 0
	# 	self.sku_2_count = 0
	# 	self.description_count = 0
	# 	self.url_count = 0
	# 	self.taxonomy_count = 0
	# 	self.attributes_count = 0
	# 	self.image_urls_count = 0

	def get_media_requests(self, item, info):

		# To Remove lists
		item['date'] = item['date'][0]

		item['sku_1'] = item['sku_1'][0]
		
		item['sku_2'] = item['sku_2'][0]

		item['description'] = item['description'][0]

		item['url'] = item['url'][0]

		item['taxonomy'] = item['taxonomy'][0]

		try:
			item['attributes'] = item['attributes']
		except KeyError:
			item['attributes'] = ''

		# item['image_urls'] = item['image_urls'][0]

		item['image_name'] = item['image_name'][0]

		if item['image_urls']:
			return [Request(x, meta={'image_name': item["image_name"]})
					for x in item.get('image_urls', [])]

	def file_path(self, request, response=None, info=None):
		return '%s' % request.meta['image_name']



	# def get_media_requests(self, item, info):
	#     img_url = item.meta['image_name']
	#     meta = {'filename': item['sku_1']}
	#     yield scrapy.Request(url=img_url, meta=meta)
