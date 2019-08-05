# -*- coding: utf-8 -*-

import os
from datetime import datetime


class ItemPipeline(object):

	def process_item(self, item, spider):
		item['promo_price'] = "hello"
		return item

	def close_spider(self, spider):
		from google.cloud import storage
		dir_path = os.path.dirname(os.path.realpath(__file__))
		credentials = os.path.join(dir_path, 'basketcompare-ac7c8362ee1f.json')

		# Explicitly use service account credentials by specifying the private key
		client = storage.Client.from_service_account_json(credentials)

		# Make an authenticated API request
		scrape_type = spider.name.split("_")[0]
		scrape_retailer = spider.name.split("_")[1]
		yyyymmdd = datetime.today().strftime('%Y%m%d')

		bucket = client.get_bucket('basketcompare/')
		file_path = "/tmp/"+ spider.name + "_" + yyyymmdd + ".csv"
		# blob = bucket.blob("/" + scrape_type + "/" + scrape_retailer + "/" scrape_retailer + "_" + yyyymmdd)
		blob = bucket.blob("/" + scrape_type)
		blob.upload_from_filename(file_path)


# class GCSFilesStore(GCSFilesStore):

# 	def process_item(self, item, spider):
#         return item

#     def close_spider(self, spider):
#         from google.cloud import storage
#         client = storage.Client.from_service_account_json('basketcompare-ac7c8362ee1f.json')
#         bucket, prefix = uri[5:].split('/', 1)
#         self.bucket = client.bucket(bucket)
#         self.prefix = prefix

# def explicit():
#     from google.cloud import storage

#     credentials = 'basketcompare-ac7c8362ee1f.json'

#     # Explicitly use service account credentials by specifying the private key
#     # file.
#     storage_client = storage.Client.from_service_account_json('basketcompare-ac7c8362ee1f.json')

#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)

# explicit()