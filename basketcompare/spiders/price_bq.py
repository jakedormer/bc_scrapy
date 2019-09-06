import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #Needed to be able to import from parent directory.
from basketcompare.spiders.main import *




class BQSpider(MainSpider):
    name = "price_bq"
    scrape_type = name.split("_")[0]
    scrape_retailer = name.split("_")[1]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["date", "sku_1", "sku_2", "description", "shelf_price", "promo_price", "promotion"],
        'FEED_URI': "file:///tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".json",
        'ITEM_PIPELINES': {
            'basketcompare.pipelines.PriceItemPipeline': 300,
        },
    }

    allowed_domains = ["diy.com"]

    sitemap_urls = [
        'https://www.diy.com/sitemap/sitemap-index-diy.xml',
        # 'https://www.diy.com/departments/it-kitchens-chilton-white-country-style-full-height-standard-cabinet-door-500mm/37447_BQ.prd'
    ]

    sitemap_rules = [
        ('_BQ', 'parse'),
        # ('243748_BQ', 'parse'),
    ]



    def parse(self, response):
        # Data stored in a JSON <script> and so must parse this instead.

        script_text = response.xpath("//script[contains(text(), 'window.__data')]/text()").extract_first()
        script_json = re.search('window.__data=(.*);', script_text).group(1)
        json_obj = json.loads(script_json)
        attributes = json_obj['product']['main']['product']['attributes']

        l = ItemLoader(item=ScrapeItem(), response=response)
        l.add_value('date', self.date)

        sku_1 = re.search('([0-9]+_BQ)', response.url).group(1)
        l.add_value('sku_1', sku_1)

        l.add_value('sku_2', attributes['ean'])

        shelf_price = attributes['pricing']['currentPrice']['amountIncTax']
        l.add_value('shelf_price', shelf_price)

        l.add_value('promo_price', None)

        try:
            l.add_value('promotion', attributes['promotion'])
        except KeyError:
            l.add_value('promotion', '')

        if self.counter < 3000: # Cancel the scrape if >= 100 missing prices or sku_1's
            if shelf_price == None or sku_1 == None:
                self.counter += 1
            else:
                return l.load_item()        
        else:
            self.gcs = False # Do not send data to google cloud storage
            raise CloseSpider(reason='No Prices or sku_1')

