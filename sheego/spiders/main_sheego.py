import scrapy

from scrapy.loader import ItemLoader
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
            loader = ItemLoader(item=SheegoItem(), selector=product)
            loader.add_css('id', 'a::attr(data-productid)')
            loader.add_css('name','strong.sc-9b31f512-0.jxmwdC.sc-b36a07fc-4.jkHYzb')
            loader.add_css('price','span.sc-d035325f-0.iFlODB.current-price')
            loader.add_css('price','span.sc-d27b1efa-0.PmCZO')
            loader.add_css('image_urls', 'img::attr(src)')
            
            yield loader.load_item()

        next_page = response.css('a.sc-5461739d-0.dSIkwe.sc-733a9301-1.gSqOdq::attr(href)').get()
        next_page_url = response.urljoin(next_page)
        yield scrapy.Request(next_page_url, meta={
                'playwright': True,
                'playwright_page_methods': [
                    PageMethod('wait_for_selector', 'div.sc-b36a07fc-2.iqkLkG'),
                    PageMethod('wait_for_timeout', 5000)
                ]
            }, callback=self.next_parse)
    
    def next_parse(self, response):
        products = response.css('div.sc-b36a07fc-0.cAGgQf')
        for product in products:
            loader = ItemLoader(item=SheegoItem(), selector=product)
            loader.add_css('id','a::attr(data-productid)')
            loader.add_css('name', 'strong.sc-9b31f512-0.jxmwdC.sc-b36a07fc-5.iBWRpy')
            loader.add_css('price', 'span.sc-d035325f-0.iFlODB.current-price')
            loader.add_css('price', 'span.sc-8adda1b4-0.exaoql')
            loader.add_css('image_urls', 'img::attr(src)')
            
            yield loader.load_item()


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
