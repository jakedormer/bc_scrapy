import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #Needed to be able to import from parent directory.
import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
import re
from items import ScrapeItem
from basketcompare.spiders.main import *



class BQSpider(MainSpider):
    name = "price_bq"

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["date", "sku_1", "sku_2", "description", "shelf_price", "promo_price", "promotion"],
        'FEED_URI': "/tmp/" + name + "/" + datetime.today().strftime('%Y-%m-%d') + ".csv"
    }

    allowed_domains = ["diy.com"]

    sitemap_urls = [
        'https://www.diy.com/sitemap/sitemap-index-diy.xml',
        # 'https://www.diy.com/departments/it-kitchens-chilton-white-country-style-full-height-standard-cabinet-door-500mm/37447_BQ.prd'
    ]

    sitemap_rules = [
        ('_BQ', 'parse')
    ]



    def parse(self, response):
        # Data stored in a JSON script and so must parse this instead.

        script_text = response.xpath("//script[contains(text(), 'window.__data')]/text()").extract_first().encode('utf-8')
        script_json = re.search('window.__data=(.*);', script_text).group(1)
        json_obj = json.loads(script_json)
        attributes = json_obj['product']['main']['product']['attributes']

        f = open("demo.json", "w")
        f.write(script_json)
        f.close()

        l = ItemLoader(item=ScrapeItem(), response=response)
        l.add_value('date', datetime.today().strftime('%Y-%m-%d'))
        l.add_value('sku1', attributes['ean'])
        l.add_value('sku2', re.search('([0-9]+_BQ)', response.url)).group(1)
        l.add_value('description', attributes['name'])
        l.add_value('shelf_price', attributes['pricing']['currentPrice']['amountIncTax'])
        l.add_value('promo_price', None)

        try:
            l.add_value('promotion', attributes['promotion'])
        except KeyError:
            pass

        return l.load_item()

