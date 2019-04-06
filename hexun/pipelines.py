# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import sys
import pymysql

reload(sys)
sys.setdefaultencoding('utf8')


class HexunPipeline(object):

    def __init__(self):
        #链接数据库
        self.connect = pymysql.connect(
            host='localhost',
            port=3306,
            db='run',
            user='root',
            charset='utf8',
            passwd='123',
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        path = 'E:\\PycharmProjects\\stock'
        title = re.sub(r"[\/\\\:\*\?\"\<\>\|\s]", '', item['title'])
        text = re.sub(r'\s', '', item['text'])
        if not os.path.exists(path):
            os.makedirs(path)
        adress = r'E:\PycharmProjects\\stock\\'+title+'.txt'
        with open(adress, 'w') as fp:
            fp.write('title:' + title + '\n')
            fp.write('author:' + item['author'] + '\n')
            fp.write('time:' + item['time'] + '\n')
            fp.write('stock:' + item['stock'] + '\n')
            fp.write('url:' + item['url'] + '\n')
            fp.write('text:' + text)

        self.cursor.execute(
            """create table if not exists stock(
            id INT AUTO_INCREMENT,
            title varchar(100) not null unique,
            time varchar(20) not null,
            primary key(id)
            )engine=innodb default charset=utf8;
            """
        )
        self.connect.commit()
        self.cursor.execute(
            """insert into stock(title,time)values(%s,%s)""", (item['title'], item['time'])
        )
        self.connect.commit()
        return item



