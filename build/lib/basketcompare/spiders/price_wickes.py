import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #Needed to be able to import from parent directory.
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
import re
from items import ScrapeItem
from basketcompare.spiders.main import *


class WickesSpider(MainSpider):
    name = "price_wickes"
    scrape_type = name.split("_")[0]
    scrape_retailer = name.split("_")[1]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["date", "sku_1", "sku_2", "description", "shelf_price", "promo_price", "promotion"],
        'FEED_URI': "/tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".csv"
    }

    allowed_domains = ["wickes.co.uk"]

    sitemap_urls = [
        'https://www.wickes.co.uk/sitemap.xml',
    ]

    sitemap_rules = [
        # ('\/p\/', 'parse'),
        ('\/p\/107177', 'parse'),
    ]

    def parse(self, response):

        l = ItemLoader(item=ScrapeItem(), response=response)

        l.add_value('date', datetime.today().strftime('%Y-%m-%d'))
        l.add_css('sku1', 'strong#product-code-val::text')
        l.add_value('sku2', '')
        l.add_css('description', 'h1.pdp__heading::text')
        l.add_value('shelf_price', re.search('(\d+\.?\d*)', response.css('div.pdp-price__new-price::text').extract_first()).group(1)),
        l.add_value('promo_price', None)
        l.add_value('promotion', " ".join(response.css('.pdp-price__description::text').extract()))

        return l.load_item()

