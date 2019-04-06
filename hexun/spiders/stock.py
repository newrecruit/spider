# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from hexun.items import HexunItem
from hexun_analyzer import hexun_analyzer

class StockSpider(scrapy.Spider):
    name = 'stock'
    allowed_domains = ['stock.hexun.com']
    start_urls = ['http://stock.hexun.com/']

    def parse(self, response):
        urls, stocks = hexun_analyzer.get_nav_url(response)
        for url, stock in zip(urls, stocks):
            yield Request(url=url, callback=self.lines, meta={'stock': stock}, dont_filter=True)

    def lines(self, response):
        urls, titles = hexun_analyzer.get_line_url(response)
        for url, title in zip(urls, titles):
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
