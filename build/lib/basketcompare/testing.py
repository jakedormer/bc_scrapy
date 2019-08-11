import os
from datetime import datetime



def close_spider(spider):
	from google.cloud import storage
	dir_path = os.path.dirname(os.path.realpath(__file__))
	credentials = os.path.join(dir_path, 'basketcompare-ac7c8362ee1f.json')

	# Explicitly use service account credentials by specifying the private key
	client = storage.Client.from_service_account_json(credentials)

	# Make an authenticated API request
	scrape_type = spider.split("_")[0]
	scrape_retailer = spider.split("_")[1]
	yyyymmdd = datetime.today().strftime('%Y%m%d')

	bucket = client.get_bucket('basketcompare')
	file_path = "/tmp/"+ scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + yyyymmdd + ".csv"
	blob = bucket.blob(scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + yyyymmdd + ".csv")
	blob.upload_from_filename(file_path)

price_wickes = "price_wickes"

close_spider(price_wickes)