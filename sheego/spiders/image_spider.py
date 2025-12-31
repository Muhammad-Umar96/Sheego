import scrapy
from scrapy_playwright.page import PageMethod


class MainSheegoSpider(scrapy.Spider):
    name = "image_spider"
    def start_requests(self):
        url = "https://sheego.de"
        yield scrapy.Request(url, meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod("wait_for_selector", "a.sc-5461739d-0.cjHQnJ.sc-190dfbe2-0.hckJvJ.sc-e0459f27-1.fzjwJR"),
                PageMethod("wait_for_timeout", 5000)
            ]
        })


    def parse(self, response):
        items = response.css("a.sc-5461739d-0.cjHQnJ.sc-190dfbe2-0.hckJvJ.sc-e0459f27-1.fzjwJR")
        for item in items:                      
            image = item.css("img::attr(src)").get()
            yield {
                "image_urls": [image]
        }
            