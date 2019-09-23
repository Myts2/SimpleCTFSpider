# -*- coding: utf-8 -*-
import scrapy
from test_spider.items import CtfWikiItem

import urllib
import requests
from lxml import etree

class CtfTimesSpider(scrapy.Spider):
    name = 'ctf-times'
    allowed_domains = ['ctftime.org']
    start_id = 841
    start_urls = ['https://ctftime.org/event/%d/tasks/' % i for i in range(1, 841)]
    event_template = "https://ctftime.org/event/%d/tasks/"
    task_template = "https://ctftime.org/task/%d"
    wp_template = "https://ctftime.org/writeup/%d"
    current_id = start_id

    def parse(self, response):
        # if response.url == self.start_urls[0]:
        #     yield scrapy.Request(self.event_template % self.start_id)
        # self.current_id = self.current_id - 1

        # task available test
        if response.xpath('//div[@class="well"]/p'):
            yield scrapy.Request(self.event_template % self.current_id)
        task_list = response.xpath('//table/tr')[1:]
        for single_task in task_list:
            item = CtfWikiItem()
            item["ctf_num"] = self.current_id
            item["ctf_name"] = response.xpath('//ul[@class="breadcrumb"]/li/a/text()')[2].extract()
            item["task_name"] = single_task.xpath("./td/a/text()").extract_first()
            item["task_class"] = single_task.xpath("./td/span/text()").extract()
            item["task_num"] = single_task.xpath("./td/a/@href").extract_first().split("/")[-1]
            item["task_url"] = self.task_template % int(item["task_num"])
            yield scrapy.Request(item['task_url'], meta={'item': item}, callback=self.task_parse)
        if self.current_id >= 1:
            yield scrapy.Request(self.event_template % self.current_id)

    def task_parse(self,response):
        item = response.meta['item']
        if response.xpath("//table/tr"):
            wp_list = response.xpath("//table/tr")[1:]
            wp_num_list = []
            for single_wp in wp_list:
                wp_num_list.append(single_wp.xpath("./td/a/@href").extract_first().split("/")[-1])
            for single_wp_num in wp_num_list:
                url = self.wp_template % int(single_wp_num)
                item["wp_num"] = single_wp_num
                yield scrapy.Request(url, meta={'item': item}, callback=self.wp_parse)
            #     wp_response = self.wp_parse(self.wp_template % int(single_wp_num))
            #     single_wp_url = wp_response.xpath("//div[@class='well']/a/@href")
            #     task_wp_list.append(single_wp_url)
            # yield item

    def wp_parse(self, response):
        # response = requests.get(url).text
        # selector = etree.HTML(response)
        # return selector
        item = response.meta['item']
        single_wp_url = response.xpath("//div[@class='well']/a/@href").extract_first()
        item["task_wp"] = single_wp_url
        yield item

