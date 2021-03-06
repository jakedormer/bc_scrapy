from basketcompare.spiders.price_wickes import *


class Wickes_Attr_Spider(WickesSpider):
    name = "attrraw_wickes"
    scrape_type = name.split("_")[0]
    scrape_retailer = name.split("_")[1]

    custom_settings = {
        'FEED_URI': "file:///tmp/" + scrape_type + "/" + scrape_retailer + "/" + scrape_retailer + "_" + datetime.today().strftime('%Y%m%d') + ".json",
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
        },
        'ITEM_PIPELINES': {
            'basketcompare.pipelines.AttrItemPipeline': 300,
            'basketcompare.pipelines.LocalImagesPipeline': 1,
        },

        # 'IMAGES_STORE': 'gs://basketcompare_images/products/wickes/',
        'IMAGES_STORE': '/home/jake/Pictures/products/wickes',
        # 'GCS_PROJECT_ID': 'basketcompare-247312',
    }

    sitemap_rules = [
        ('\/p\/', 'parse'),
        # ('\/p\/160087', 'parse'),
        # ('\/p\/107177', 'parse'),
    ]


    def parse(self, response):
        attr_dict = {}
        attr_dict['date'] = self.date
        sku_1 = response.css('strong#product-code-val::text').extract_first()
        attr_dict['sku_1'] = sku_1
        attr_dict['sku_2'] = ''
        attr_dict['description'] = response.css('h1.pdp__heading::text').extract_first()
        attr_dict['url'] = response.url

        breadcrumb_links = response.css('.breadcrumbs__item>a::attr(href)').extract() 
        attr_dict['taxonomy'] = re.search('products\/(.*)\/c\/', breadcrumb_links[len(breadcrumb_links)-1].lower()).group(1) #Count breadcrumb links and then choose n-1 link.

        attributes = response.selector.css('ul.info__lists-not-bullets>li')

        for i in attributes:
            attr_key_raw = re.search('([a-z0-9 ]+):', i.css('strong::text').extract_first().lower()).group(1)
            attr_key = re.sub(r'\W+', ' ', attr_key_raw).lower().strip().replace(" ", "_")
            attr_value = i.css('li::text').extract()[1].replace('"', '').strip().lower()
            attr_dict[attr_key] = attr_value
            # print(attr_key, attr_value)
            # attr_dict(attr_key) = attr_value
            # print(attr_dict)
                            
        yield attr_dict

        # Images

        img_url = response.xpath("//div[@class='s7staticimage']/img/@src").extract_first() # 107177

        if not img_url:
            img_url = response.xpath("//div[@id='noScriptProductS7Image']/img/@src").extract_first()

        if "https:" not in img_url:
            img_url = "https:" + img_url

        yield ImageItem(image_urls=[img_url], image_name=sku_1)
       
