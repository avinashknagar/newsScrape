import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class GlobenewswireSpider(scrapy.Spider):
    name = 'globenewswire'
    start_urls = ['http://www.globenewswire.com/en/Index/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "businesswire : A BERKSHIRE HATHAWAY COMPANY"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.xpath('.//span[@itemprop="datePublished"]/em/time/@datetime').extract()
        spiderItem['links'] = data[1]
        li = response.css('.article-body').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('GlobenewswireSpider', 'pageNumberToScrapy').strip())
        
        for i in response.css('.post-title16px'):
            data = []
            data.append(i.xpath('.//a/text()').extract_first())
            data.append('https://www.globenewswire.com'+str(i.xpath('.//a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
        
        otherPageURLTemplate = 'http://www.globenewswire.com/en/Index?page='
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'#pagerPos'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        for i in response.css('.post-title16px'):
            data = []
            data.append(i.xpath('.//a/text()').extract_first())
            data.append('https://www.globenewswire.com'+str(i.xpath('.//a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
    
    

