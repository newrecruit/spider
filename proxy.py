# -*- coding:UTF-8 -*-
import requests
import subprocess as sp
import re
import random
from lxml import etree


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'Referer': 'https://www.xicidaili.com/',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}


def get_proxy(page=1):
    proxies_list = []
    proxy_url = 'https://www.xicidaili.com/nn/{}'.format(page)
    response = requests.get(proxy_url, headers=headers)
    html = etree.HTML(response.text)
    info_list = html.xpath("//table[@id='ip_list']/tr")
    for info in info_list[1:]:
        ip = info.xpath('td[2]/text()')[0]
        port = info.xpath('td[3]/text()')[0]
        protocol = info.xpath('td[6]/text()')[0]
        proxies_list.append(protocol.lower()+'#'+ip+'#'+port)
    return proxies_list


def check_ip(ip):
    cmd = 'ping -n 3 -w 3 {}'.format(ip)
    info = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
    out = info.stdout.read().decode('gb18030')
    lose_sum = re.findall(u"丢失 = (\\d+)", out)
    if len(lose_sum) == 0:
        lose = 3
    else:
        lose = int(lose_sum[0])
    if lose > 2:
        return 1000
    else:
        average_time = re.findall(u"平均 = (\\d+)ms", out)
        if len(average_time) == 0:
            return 1000
        else:
            average_time = int(average_time[0])
            return average_time


if __name__ == '__main__':
    proxy_list = get_proxy(1)
    while True:
        proxy = random.choice(proxy_list)
        split_proxy = proxy.split('#')
        ip = split_proxy[1]
        average_time = check_ip(ip)
        if average_time >= 200:
            proxy_list.remove(proxy)
            print u'代理ip链接超时，重新获取中...'
        else:
            break

    proxy = {split_proxy[0]: split_proxy[1] + ':' + split_proxy[2]}
    print u"可使用代理ip：", proxy


