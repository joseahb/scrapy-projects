# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
#import logging


class BanksSpider(scrapy.Spider):
    name = 'banksamerica'
    allowed_domains = ['www.banks-america.com']
    start_urls = ['https://banks-america.com/routing/b/']

    def parse(self, response):
        banks = response.xpath("//td/a").getall()
        for bank in banks:
            sel = Selector(text=bank)
            name = sel.xpath(".//text()").extract()
            link = sel.xpath(".//@href").extract()
            
            yield response.follow(url=link, callback=self.parse_banks, meta={'bank_name': name})
            
    def parse_banks(self, response):
        name = response.request.meta('bank_name')
        yield {
            'bank_name': name,
        }
