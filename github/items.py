# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field() # 框架名称
    url = scrapy.Field()  # 框架主页路径
    star_number = scrapy.Field() # 框架的star数量
    update_time = scrapy.Field() # 更新时间
    clone_url = scrapy.Field()  # clone地址


