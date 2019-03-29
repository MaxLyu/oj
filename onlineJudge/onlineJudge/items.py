# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OnlinejudgeItem(scrapy.Item):

    id = scrapy.Field()                     # 题目编号
    title = scrapy.Field()                  # 标题
    difficulty = scrapy.Field()             # 难度
    submissionNo = scrapy.Field()      # 提交量
    acceptedNo = scrapy.Field()        # 正确数
    passingRate = scrapy.Field()           # 正确率

    pass
