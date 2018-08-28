# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from datetime import datetime
from crawl_proxy.helper.db import get_mysql_connection


class MongoPipeline(object):

    def __init__(self):
        self.db = get_mysql_connection()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        print('insert {} proxies'.format(len(item['proxies'])))
        for proxy in item['proxies']:
            current_time = datetime.now()

            with self.db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO proxies (ip, updated_at) VALUE (%s, %s)
                    ON DUPLICATE KEY UPDATE updated_at=%s
                """, (proxy, current_time, current_time))
                self.db.commit()
