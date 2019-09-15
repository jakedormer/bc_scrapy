from basketcompare.spiders.main import *


class WickesSpider(MainSpider):
    name = "price_wickes"
    scrape_type = name.split("_")[0]
    scrape_retailer = name.split("_")[1]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["date", "sku_1", "sku_2", "shelf_price", "promo_price", "promotion"],
        'FEED_URI': "file:///tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".csv",
        'ITEM_PIPELINES': {
            'basketcompare.pipelines.PriceItemPipeline': 300,
        },
    }

    allowed_domains = ["wickes.co.uk"]

    sitemap_urls = [
        'https://www.wickes.co.uk/sitemap.xml',
    ]

    sitemap_rules = [
        ('\/p\/', 'parse'),
        # ('\/p\/122428', 'parse'),
        # ('\/p\/220056', 'parse'),
    ]


    def parse(self, response):

        l = ItemLoader(item=ScrapeItem(), response=response)

        l.add_value('date', self.date)

        sku_1 = response.css('strong#product-code-val::text').extract_first()
        l.add_value('sku_1', sku_1)

        l.add_value('sku_2', '')

        shelf_price = re.search('(\d+\.?\d*)', response.css('div.pdp-price__new-price::text').extract_first()).group(1)
        l.add_value('shelf_price', shelf_price)

        l.add_value('promo_price', '')

        # Promotions list needed as Wickes keep promotions in 2 places.
        
        promotions = []
        try:
            promotions.append(" ".join(response.css('.pdp-price__description::text').extract()).strip().replace("  ", " "))
            promotions.append(response.css('.pdp__badge::text').extract_first().strip())
            promotion_text = " ".join(promotions)
        except AttributeError: # strip() fails when it doesn not find a promotion.
            promotion_text = ''

        l.add_value('promotion', promotion_text)
        
        if self.counter < 500:
            if shelf_price == None or sku_1 == None:
                self.counter += 1
            else:
                return l.load_item()        
        else:
            self.gcs = False
            raise CloseSpider(reason='No Prices or sku_1')

