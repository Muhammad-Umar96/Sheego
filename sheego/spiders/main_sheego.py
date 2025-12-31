import scrapy
from scrapy_playwright.page import PageMethod
from sheego.items import SheegoItem


class MainSheegoSpider(scrapy.Spider):
    
    name = 'main_sheego_spider'
    
    def start_requests(self):
        url = 'https://sheego.de'
        yield scrapy.Request(url, meta={
            'playwright': True,
            'playwright_page_methods': [
                PageMethod('wait_for_selector', 'div.sc-b36a07fc-0.cAGgQf'),
                PageMethod('wait_for_timeout', 5000)
            ]
        })

    def parse(self, response):
        products = response.css('div.sc-b36a07fc-0.cAGgQf')
        for product in products:
            item = SheegoItem()
            id = product.css('a::attr(data-productid)').get()
            name = product.css('strong.sc-9b31f512-0.jxmwdC.sc-b36a07fc-4.jkHYzb::text').get()
            price = product.css('span.sc-d035325f-0.iFlODB.current-price::text').get()
            if not price:
                price = product.css('span.sc-d27b1efa-0.PmCZO::text').get()
            image = product.css('img::attr(src)').get()
            item['id'] = id
            item['name'] = name
            item['price'] = price
            item['image_urls'] = [image]
            
            yield item

        next_page = response.css('a.sc-5461739d-0.dSIkwe.sc-733a9301-1.gSqOdq::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, meta={
                'playwright': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', 'div.sc-b36a07fc-0.cAGgQf'),
                    PageMethod('wait_for_timeout', 5000)
                ]
            }, callback=self.next_parse)
    
    def next_parse(self, response):
        products = response.css('div.sc-b36a07fc-0.cAGgQf')
        for product in products:
            item = SheegoItem()
            id = product.css('a::attr(data-productid)').get()
            name = product.css('strong.sc-9b31f512-0.jxmwdC.sc-b36a07fc-5.iBWRpy::text').get()
            price = product.css('span.sc-d035325f-0.iFlODB.current-price::text').get()
            if not price:
                price = product.css('span.sc-8adda1b4-0.exaoql::text').get()
            image = product.css('img::attr(src)').get()
            item['id'] = id
            item['name'] = name
            item['price'] = price
            item['image_urls'] = [image]
            
            yield item


    # Checking a single Product Page
    #     next_page = response.css('a.sc-5461739d-0.cjHQnJ.sc-190dfbe2-0.hckJvJ.sc-57300b4e-1.LtXXN::attr(href)').get()
    #     next_page_url = response.urljoin(next_page)
    #     yield response.request(next_page_url, meta={
    #         'playwright': True,
    #         'playwright_page_methods': [
    #             PageMethod('wait_for_selector', 'h1.sc-238bf89e-0.bjNwot.sc-8024c401-0.hzWZaA'),
    #             PageMethod('wait_for_timeout', 5000)
    #         ]
    #     },callback=self.next_parse)

    # def next_parse(self,response):
    #     yield{
    #     'heading': response.css('h1.sc-238bf89e-0.bjNwot.sc-8024c401-0.hzWZaA::text').get()
    # }
