# -*- coding: utf-8 -*-


try:
    from basketcompare.local_settings import *
except ImportError as e:
    pass


from datetime import datetime

BOT_NAME = 'basketcompare'

SPIDER_MODULES = ['basketcompare.spiders']
NEWSPIDER_MODULE = 'basketcompare.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True





# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'wickes.middlewares.WickesSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'wickes.middlewares.WickesDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html

EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'basketcompare.pipelines.ItemPipeline': 300,
# }

FEED_STORE_EMPTY = False # No exporting empty datasets
# FEED_URI =  "/tmp/%(name)s/" + datetime.today().strftime('%Y-%m-%d') + ".csv"
URI_SCHEME = "file"
FEED_FORMAT = "csv"
# FEED_STORAGES
# FEED_STORAGE_FTP_ACTIVE
# FEED_STORAGE_S3_ACL
# FEED_EXPORTERS
# FEED_STORE_EMPTY
# FEED_EXPORT_ENCODING
# FEED_EXPORT_FIELDS = ["date", "sku1", "sku2", "description", "price", "promotion", "url"]
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
#The initial download delay
AUTOTHROTTLE_START_DELAY = 5
#The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
#The average number of requests Scrapy should be sending in parallel to each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 300
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORTERS = {
    'csv': 'scrapy.exporters.CsvItemExporter',
}

LOCALIMAGESPIPELINE_IMAGES_EXPIRES = 180


