import scrapy
from test_spider.items import TestSpiderItem


def debug(func):
    print(func)
    return func


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'github-ctfs'
    domain = "https://github.com"
    start_urls = [
        'https://github.com/ctfs/write-ups-2013',
    ]

    def parse_github(self, response):
        file_label = response.xpath('./td[@class="icon"]/svg/@aria-label').extract()
        text = response.xpath('./td[@class="content"]/span/a[@class="js-navigation-open"]/text()').extract()
        next_url = response.xpath('./td[@class="content"]/span/a/@href').extract()
        return file_label[0], text[0], next_url[0]
