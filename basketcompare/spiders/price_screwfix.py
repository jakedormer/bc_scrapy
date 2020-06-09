from basketcompare.spiders.main import *


class ScrewfixSpider(MainSpider):
    name = "price_screwfix"
    scrape_type = name.split("_")[0]
    scrape_retailer = name.split("_")[1]

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["date", "sku_1", "sku_2", "shelf_price", "promo_price", "promotion"],
        'FEED_URI': "file:///tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".csv",
        'ITEM_PIPELINES': {
            'basketcompare.pipelines.PriceItemPipeline': 300,
        },
    }

    allowed_domains = ["screwfix.com"]

    sitemap_urls = [
        'https://www.screwfix.com/sitemap-en-gb.xml',
        # 'https://www.screwfix.com/p/makita-dlx2336s-18v-3-0ah-li-ion-lxt-cordless-twin-pack/896hy',
        # 'https://www.screwfix.com/p/mk-logic-plus-13a-2-gang-dp-switched-socket-2a-2-outlet-usb-charger-white/5541x'
    ]

    sitemap_rules = [
        ('\/p\/', 'parse'),
        # ('\/p\/.*\/896hy', 'parse'),
        # ('\/p\/.*\/5541x', 'parse'),
    ]


    def parse(self, response):

        l = ItemLoader(item=ScrapeItem(), response=response)

        l.add_value('date', self.date)

        sku_1 = response.request.url.split('/')[-1]
        l.add_value('sku_1', sku_1)

        l.add_value('sku_2', '')

        shelf_price = response.css('div.pr__price::attr(content)').extract_first()
        l.add_value('shelf_price', shelf_price)

        #Bulk savings table
        try:
            bulk_price = response.css('td.bigBulkBlk>strong::text').extract_first().replace("£", "")
            l.add_value('promo_price', bulk_price)
        except AttributeError:
            l.add_value('promo_price', '')

        # Promotions list needed as Wickes keep promotions in 2 places.
        
        promotions = []
        try:
            # Promotions
            promotion_text = response.css('.pr__infobox::text').extract_first().strip().replace("  ", " ")

        except AttributeError: # strip() fails when it doesn not find a promotion.
            promotion_text = ''

        promotions.append(promotion_text)

        l.add_value('promotion', promotions)
        

        # For stopping spider if nothing captured
        if self.counter < 500:
            if shelf_price == None or sku_1 == None:
                self.counter += 1
            else:
                return l.load_item()        
        else:
            self.gcs = False
            raise CloseSpider(reason='No Prices or sku_1')

