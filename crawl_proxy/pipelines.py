# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from datetime import datetime
from crawl_proxy.custom_settings import mongo_settings


class CrawlProxyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self):
        self.mongo_uri = mongo_settings['URI']
        self.mongo_db = mongo_settings['DATABASE']
        self.mongo_collection = mongo_settings['PROXIES_COLLECTION']

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        for proxy in item['proxies']:
            proxy_item = {
                # 'url': item['url'],
                'spider': spider.name,
                'proxy': proxy,
                'updated_at': datetime.now()
            }

            if 'type' in item:
                proxy_item['type'] = item['type']

            self.db[self.mongo_collection].update_one(filter={'proxy': proxy_item['proxy']},
                                                      update={'$set': proxy_item},
                                                      upsert=True)
