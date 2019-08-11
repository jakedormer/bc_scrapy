# -*- coding: utf-8 -*-

# Scrapy settings for wickes project
from datetime import datetime

BOT_NAME = 'basketcompare'

SPIDER_MODULES = ['basketcompare.spiders']
NEWSPIDER_MODULE = 'basketcompare.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

CREDENTIALS = {"type": "service_account",   "project_id": "basketcompare-247312",   "private_key_id": "b5af00a9075c2b3788c6a7c9e04372435e24f00e",   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDKgNyOHS14r46/\nRwT0ULFRhkNumzqtSdulqCi4nSSc5T4ic07BbbZJYyqZZH8girB9qcMfrLB7tXhW\nquR4qa8DEjnpiZVnc2lVR4CumzYE8bsksFCb5kyYScriQ+AJPJYfoQ60asKDqxkD\nbjCWYNl4bvSMMt33R0bGwarP2cl7nz5Ftri/pnY//GQR4C6qrSy+kzXJvOO6U3sm\n2f2eX43UUOjUtSGi4GvKAnE/ngCGDAsfwx8HqmeR83MHlPosrl2OSxSM/ikKqrpx\nRg/7ODiwsXOHeBkcocyUSlineBtUAFdgNnBXmjtAP1hrwSHrGZ6BUCb433qbCw5i\nDDy++dsnAgMBAAECggEAC8b1zNAWmmu/ZhF30Mu2nFKuLksZ3QUsIJTIlYASJovQ\nkslY/bfnP5pkWlp1aEuYmx5Z6kgtVWyG7KdwtTHNK2UOeC4XwdX8/Mg1TDJbsGrs\nouQcNAzvTHYSNhmTeIYNBxbjV4vT9ztmr4PjkINecnolf9fff+elzp5p1D/Kz4Un\nY/wNZYJEM+acqQ73rI0xGsLQ2skZJYj0bGFQ2Umkp/AuNdc52H1ni9BPwo4EzKUU\nWt0eaCXMyO8w/S2l5/ymkgW9+bo/nVb+VLcjWXZ42RuGEaHtg07PFd5za/IaAYoY\nHNTGT/7Z5UHWaGt7qGldeIabyJtEDzrrajI9jDCFSQKBgQDt+4XUuOsKXcWnKp7y\nhlSK/wgdTnHNMixv3ABMWVN/9l0mthudcMGlPMKWkMMeJcTNSdF7TxZwqGE3pnJd\nbD2g/GfGcxjI+lzsbu081xiquv/R+PSadUChiEjEn27YECRtZIeKsRBTCYbgtZ3D\nhqAwrWfoQKlUmcZwbRU6ZQapSQKBgQDZ1bJkpLoqJrwXGD5DmJWkEY6uYy8m4Ktc\nvcD+b376P9KiyRpLBhOfrptC1OKm0rxgqidrr/eKl8QBqORYM1ssOGcmgmPTAsvl\nVcSncYJvMVhbUzUAotueDicr1ONrHj1k3ecr/ObwKmFPS1pWkycPEKcbi07r1xb3\n808UdQNQ7wKBgQCdjqGbJVZPRaf/NcOH85FzeMdph67mWGp9IF1+LsGOfZBMedKs\nmKNL/38g6fSUOBMkitPK3KCRs5ixnFwpJ+lhdNpL05W8Ma1lx0b/ubSWDDokTLu8\nqxZAG5d5vchH+d/0INNv6ixRnYQTr4okkjPqJlQduvmgjjKH6mBcidgwKQKBgQC3\npv/49Bx0LyYCvpC4AqueoKLPiZWWTHKNBPnySWQfbbGTRsMhH2VqChaiOMNB7Ief\nY7VKiBfGQ/+fepnRdrLWTFNC10l7/G6U0kOy+/MA9fRNQpB8EdHgpoQF4z088UjH\ngoJExrqZHtHdvWTTesrCW8LXaRLHqRaXQw2X7LM4BwKBgQDGQ1ldpUvyzzXs5dUa\nwHSm1udaCjl3cxv8ryl0aIbyaRXrTvO1RcJku8hGYTNjLEie+eNCcYZreHv7X8DL\n2EEHAmu2Uk2Ys9kAYn3S32xwczxkck39nrKEwGXqFU2Gbi97ktID9yvXySxSskGp\n46kI8e9cI8Hq6zTIVKs4K+7FQQ==\n-----END PRIVATE KEY-----\n",   "client_email": "cloud-storage@basketcompare-247312.iam.gserviceaccount.com",   "client_id": "101975648539855159771",   "auth_uri": "https://accounts.google.com/o/oauth2/auth",   "token_uri": "https://oauth2.googleapis.com/token",   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-storage%40basketcompare-247312.iam.gserviceaccount.com"}


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
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'basketcompare.pipelines.ItemPipeline': 300,
}

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
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORTERS = {
    'csv': 'scrapy.exporters.CsvItemExporter',
}
