# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class OnlinejudgePipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active                # 激活工作簿
        self.ws.append(['编号', '标题', '难度', '提交量', '正确数', '正确率'])    # 设置表头

    def process_item(self, item, spider):
        line = [item['id'], item['title'], item['difficulty'],
                item['submissionNo'], item['acceptedNo'], item['passingRate']]
        self.ws.append(line)
        self.wb.save('oj.xlsx')
        return item
