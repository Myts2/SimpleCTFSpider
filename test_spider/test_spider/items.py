# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *

db = MySQLDatabase("test",host='192.168.236.195',port=3306,user='root', passwd='qq784400047', charset='utf8')


class TestSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = scrapy.Field()
    ctf_name = scrapy.Field()
    task_class = scrapy.Field()
    task_name = scrapy.Field()
    wp_addr = scrapy.Field()
    task_files = scrapy.Field()

class CtfWikiItem(scrapy.Item):
    ctf_num = scrapy.Field()
    ctf_name = scrapy.Field()
    task_name = scrapy.Field()
    task_class = scrapy.Field()
    task_num = scrapy.Field()
    task_wp = scrapy.Field()
    task_url = scrapy.Field()
    wp_num = scrapy.Field()

class CtfWiki(Model):
    id = AutoField(primary_key = True)
    ctf_name = TextField()
    task_class = TextField()
    task_wp = TextField()
    task_name = TextField()

    class Meta:
        database = db