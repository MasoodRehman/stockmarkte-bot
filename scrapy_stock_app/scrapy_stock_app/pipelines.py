# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class ScrapyStockAppPipeline(object):

    def open_spider(self, spider):
        # Open a file for saving data as json line.
        self.file = open('./../store/company_profiles.jl', 'w')

    def close_spider(self, spider):
        # close file.
        self.file.close()

    def process_item(self, item, spider):
        item['crawled_at'] = json.dumps(datetime.now(), default=json_serial)
        line = json.dumps(dict(item)) + "\n"
        # Save data in a file as json line.
        self.file.write(line)
        return item
        