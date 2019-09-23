import scrapy
from test_spider.items import TestSpiderItem


def debug(func):
    print(func)
    return func


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'github-susers'
    domain = "https://github.com"
    start_urls = [
        'https://github.com/susers/Writeups',
    ]

    def parse_github(self, response):
        file_label = response.xpath('./td[@class="icon"]/svg/@aria-label').extract()
        text = response.xpath('./td[@class="content"]/span/a[@class="js-navigation-open"]/text()').extract()
        next_url = response.xpath('./td[@class="content"]/span/a/@href').extract()
        return file_label[0], text[0], next_url[0]

    def parse(self, response):
        for file in response.xpath('//*[@class="js-navigation-item"]'):
            file_label, year, next_url = self.parse_github(file)
            if file_label == "directory":
                tmp_dict = {"year": year}
                yield scrapy.Request(self.domain + next_url, meta={'item': tmp_dict}, callback=self.deal_ctf_name)

    def deal_ctf_name(self, response):
        tmp_dict = response.meta['item']
        for file in response.xpath('//*[@class="js-navigation-item"]'):
            file_label, ctf_name, next_url = self.parse_github(file)
            if file_label == "directory":
                tmp_dict["ctf_name"] = ctf_name
                yield scrapy.Request(self.domain + next_url, meta={'item': tmp_dict}, callback=self.task_class)

    def task_class(self, response):
        tmp_dict = response.meta['item']
        for file in response.xpath('//*[@class="js-navigation-item"]'):
            file_label, task_class, next_url = self.parse_github(file)
            if file_label == "directory":
                tmp_dict["task_class"] = task_class.split("/")[0]
                yield scrapy.Request(self.domain + next_url, meta={'item': tmp_dict}, callback=self.task_name)

    def task_name(self, response):
        tmp_dict = response.meta['item']
        for file in response.xpath('//*[@class="js-navigation-item"]'):
            file_label, task_name, next_url = self.parse_github(file)
            if file_label == "directory":
                tmp_dict["task_name"] = task_name.split("/")[0]
                yield scrapy.Request(self.domain + next_url, meta={'item': tmp_dict}, callback=self.task_parse)

    def task_parse(self, response):
        tmp_dict = response.meta['item']
        for file in response.xpath('//*[@class="js-navigation-item"]'):
            file_label, filename, next_url = self.parse_github(file)
            if "up" in filename:
                tmp_dict["wp_addr"] = self.domain + next_url
            if "attachment" in filename:
                next_url_attach = next_url
                content_list = response.xpath('//div[@class="Box-body"]/article/p')
                for i in range(len(content_list)):
                    if "offline" in content_list[i]:
                        tmp_dict["flag"] = content_list[i+1]
                        break
                yield scrapy.Request(self.domain + next_url_attach, meta={'item': tmp_dict}, callback=self.attach_parse)

    def attach_parse(self,response):
        tmp_dict = response.meta['item']
        download_url = []
        for file in response.xpath('//*[@class="js-navigation-item"]'):
            file_label, filename, next_url = self.parse_github(file)
            if file_label != "directory" :
                download_url.append(self.domain+next_url.replace("blob", "raw"))
        tmp_dict["task_files"] = download_url
        item = TestSpiderItem()
        for key in tmp_dict:
            item[key] = tmp_dict[key]

        yield item


