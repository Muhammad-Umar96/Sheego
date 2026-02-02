# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

class SheegoItem(scrapy.Item):
    
    id = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    image_urls = scrapy.Field()     # Field for image URLs to be downloaded
    # images = scrapy.Field()         # Field to store information about downloaded images
    