# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from hexun.items import HexunItem


class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['stock.hexun.com']
    start_urls = ['http://stock.hexun.com/']

    def parse(self, response):
        tables = response.xpath("//div[@class='channelNav1']/a")
        for table in tables[1:5]:
            url = table.xpath('@href').extract()[0]
            stock = table.xpath('text()').extract()[0]
            yield Request(url=url, callback=self.lines, meta={'stock': stock}, dont_filter=True)

    def lines(self, response):
        urls = []
        if 'us' in response.url:
            urls = response.xpath("//div[@class='infCon']")
        elif 'hk' in response.url:
            urls = response.xpath("//ul[@class='text2a']/li")
        elif 'new' in response.url:
            urls = response.xpath("//div[@class='pt_a']/ul[1]/li")
        else:
            urls = response.xpath("//div[@class='left']/ul[1]/li")
        for url in urls:
            title = url.xpath("a/text()").extract()[0]
            url = url.xpath("a/@href").extract()[0]
            yield Request(url=url, callback=self.data, meta={'title': title, 'stock': response.meta['stock']})

    def data(self, response):
        item = HexunItem()
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['stock'] = response.meta['stock']
        item['time'] = response.xpath("//span[@class='pr20']/text()").extract()[0]
        item['author'] = response.xpath("//*[@rel='nofollow']/text()").extract()[0]
        item['text'] = ''.join(response.xpath("//div[@class='art_contextBox']/p/text()").extract())
        yield item

