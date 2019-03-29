# -*- coding: utf-8 -*-
'''
Create on 2019/1/23
@author: Max_Lyu
'''
import scrapy
import json
from onlineJudge.items import OnlinejudgeItem


class OjSpider(scrapy.Spider):
    name = 'oj'
    allowed_domains = ['oj.dgut.edu.cn']
    offset = 0
    url = 'http://oj.dgut.edu.cn/api/xproblem/?limit=20&offset='
    start_urls = [url + str(offset)]

    def parse(self, response):
        data = json.loads(response.text)['data']['results']
        if len(data):
            for i in range(len(data)):
                submissionNo = data[i]['submission_number']
                acceptedNo = data[i]['accepted_number']
                try:
                    passingRate = round((int(acceptedNo)/int(submissionNo)) * 100, 2)
                except ZeroDivisionError as e:
                    passingRate = 0
    
                strPR = str(passingRate) + "%"
    
                item = OnlinejudgeItem()
    
                item['id'] = data[i]['_id']
                item['title'] = data[i]['title']
                item['difficulty'] = data[i]['difficulty']
                item['submissionNo'] = submissionNo
                item['acceptedNo'] = acceptedNo
                item['passingRate'] = strPR
    
                yield item

                print(i)
            self.offset += 20
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
