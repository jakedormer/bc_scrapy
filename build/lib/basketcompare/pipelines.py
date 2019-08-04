# -*- coding: utf-8 -*-

import os


class ItemPipeline(object):

	def process_item(self, item, spider):
		return item

	def close_spider(self, spider):
		from google.cloud import storage
		dir_path = os.path.dirname(os.path.realpath(__file__))
		credentials = os.path.join(dir_path, 'basketcompare-ac7c8362ee1f.json')

		# Explicitly use service account credentials by specifying the private key
		client = storage.Client.from_service_account_json(credentials)

		# Make an authenticated API request
		bucket = client.get_bucket('basketcompare')
		file_path = "/tmp/wickes/2019-08-04.csv"
		blob = bucket.blob("price_scrape/wickes/wickes_20190801")
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