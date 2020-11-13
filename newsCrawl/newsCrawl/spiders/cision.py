import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class CisionSpider(scrapy.Spider):
    name = 'cision'
    start_urls = ['http://news.cision.com/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "businesswire : A BERKSHIRE HATHAWAY COMPANY"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.css('.card-large').xpath('.//article/time/@datetime').extract()
        spiderItem['links'] = data[1]
        li = response.css('span span::text').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('CisionSpider', 'pageNumberToScrapy').strip())
        
        for i in response.css('.card-item'):
            data = []
            data.append(i.xpath('.//article/a/h2/text()').extract_first())
            data.append(i.xpath('.//article/a/@href').extract_first())
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
        
        otherPageURLTemplate = 'https://news.cision.com/ListItems?pageIx='
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        for i in response.css('.card-item'):
            data = []
            data.append(i.xpath('.//article/a/h2/text()').extract_first())
            data.append(i.xpath('.//article/a/@href').extract_first())
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
    
    
