# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from test_spider.items import CtfWiki
import json


class TestSpiderPipeline(object):
    def process_item(self, item, spider):
        if not CtfWiki.table_exists():
            CtfWiki.create_table()
        try:
            CtfWiki.create(ctf_name=item['ctf_name'],task_class=json.dumps(item['task_class']),task_name = item["task_name"], task_wp=item['task_wp'])
        except Exception as e:
            if str(e.args[0]) == '1062':
                print ('重复数据，跳过。')
            else:
                print (e.args[0],e.args[1])

        return item
