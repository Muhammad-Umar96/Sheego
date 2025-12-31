# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SheegoItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()     # Field for image URLs to be downloaded
    # images = scrapy.Field()         # Field to store information about downloaded images
    