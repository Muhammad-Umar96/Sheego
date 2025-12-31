# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class SheegoPricePipeline:
    def process_item(self, item, spider):
        item["price"] = item["price"].replace(" ", " ").replace(",", ".")
        return item
    
class SheegoImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):

        filename = request.url.split('/')[-2]
        name = request.url.split('/')[-1].split('?')[0]

        return f"full/{filename}_{name}"
    
class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Item ID already seen: {adapter['id']}")
        else:
            self.ids_seen.add(adapter["id"])
            return item

class SavingToMySQLPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Um@r94566666',
            database='sheego'
            )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                            id VARCHAR(255) ,
                            name VARCHAR(255),
                            price VARCHAR(50),
                            urls TEXT
                            )""")
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item 

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO products 
                            (id, name, price, urls) VALUES (%s, %s, %s, %s)""", (
            item['id'],
            item['name'],
            item['price'],
            ','.join(item['image_urls'])
        ))

    def close_spider(self, spider):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()