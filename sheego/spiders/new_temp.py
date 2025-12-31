import scrapy
from scrapy_playwright.page import PageMethod
from sheego.items import SheegoItem


class MainSheegoSpider(scrapy.Spider):
    name = "new_spider"
    def start_requests(self):
        url = "https://sheego.de"
        yield scrapy.Request(url, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", 'a.sc-5461739d-0.cjHQnJ.sc-190dfbe2-0.hckJvJ.sc-e0459f27-1.gtituF'),
                PageMethod("wait_for_timeout", 10000)
            ]
        })


    def parse(self, response):
        item = SheegoItem()
        products = response.css('a.sc-5461739d-0.cjHQnJ.sc-190dfbe2-0.hckJvJ.sc-e0459f27-1.gtituF')
        for product in products:
            item['name'] = product.css("strong.sc-7fb6a9ee-0.jWelwM.sc-e0459f27-4.boIJCF::text").get()                        
            # item['price'] = product.css("span.sc-d035325f-0.KIDBo.current-price::text").get()
            
            # if not price:
            #     price = item.css("span.sc-d27b1efa-0.PmCZO::text").get()

            # item['image_product'] = product.css("img::attr(src)").get()
            yield item

