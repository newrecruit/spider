# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

response = requests.get(url='http://www.a-hospital.com/w/天津市医院列表')
soup = BeautifulSoup(response.text, 'lxml')
useful_info = soup.find(id='bodyContent')
useful_info = useful_info.find_all('ul')
for i in useful_info:
    info_raw = i.find_all('li')
    for j in info_raw:
        hospital_info = j.text
        try:
            address = re.search(u'医院地址：(.*?)\n', hospital_info).group(1)
        except:
            pass
        name = re.search('^(.*?)\n', hospital_info)
        if name:
            print name.group(1)






