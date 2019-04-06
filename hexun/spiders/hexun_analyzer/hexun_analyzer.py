# -*- coding: utf-8 -*-


def get_nav_url(response):
    tables = response.xpath("//div[@class='channelNav1']/a")
    urls = []
    stocks = []
    for table in tables[1:5]:
        urls.append(table.xpath('@href').extract()[0])
        stocks.append(table.xpath('text()').extract()[0])
    return urls, stocks


def get_line_url(response):
    urls = []
    titles = []
    if 'us' in response.url:
        url = response.xpath("//div[@class='infCon']")
    elif 'hk' in response.url:
        url = response.xpath("//ul[@class='text2a']/li")
    elif 'new' in response.url:
        url = response.xpath("//div[@class='pt_a']/ul[1]/li")
    else:
        url = response.xpath("//div[@class='left']/ul[1]/li")
    for url in url:
        titles.append(url.xpath("a/text()").extract()[0])
        urls.append(url.xpath("a/@href").extract()[0])
    return urls, titles
