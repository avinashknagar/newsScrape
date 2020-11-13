import scrapy
from ..items import NewscrawlItem
import pandas as pd
import time
from configparser import ConfigParser
import os

class PrivateequityinternationalSpider(scrapy.Spider):
    name = 'privateequityinternational'
    start_urls = ['https://www.privateequityinternational.com/news-analysis/fundraising/']

    
    def parse(self, response):
        print('Function parse is called!')
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('PrivateequityinternationalSpider', 'startDate').strip()
        endDate = config_raw.get('PrivateequityinternationalSpider', 'endDate').strip()
        pageNumberToScrapyForOldPost  = int(config_raw.get('PrivateequityinternationalSpider', 'pageNumberToScrapy').strip())
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Private Equity International"
        for i in response.xpath('//div[@class="item-details"]'):
            h = i.xpath('.//div[@class="item-header"]/h2/a/text()').extract()
            if len(h) > 0:
                spiderItem['headlines'] = h[0]
                spiderItem['dates'] = i.xpath('.//div/span/time/text()').extract_first()
                spiderItem['links'] = i.xpath('.//div[@class="item-header"]/h2/a/@href').extract_first()
                dateobj = time.strptime(spiderItem['dates'], "%d %B %Y")
                if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                    yield spiderItem
        
        otherPageURLTemplate = 'https://www.privateequityinternational.com/news-analysis/fundraising/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
            
        
    
    def parseRecursion(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('PrivateequityinternationalSpider', 'startDate').strip()
        endDate = config_raw.get('PrivateequityinternationalSpider', 'endDate').strip()
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Private Equity International"
        for i in response.xpath('//div[@class="item-details"]'):
            h = i.xpath('.//div[@class="item-header"]/h2/a/text()').extract()
            if len(h) > 0:
                spiderItem['headlines'] = h[0]
                spiderItem['dates'] = i.xpath('.//div/span/time/text()').extract_first()
                spiderItem['links'] = i.xpath('.//div[@class="item-header"]/h2/a/@href').extract_first()
                dateobj = time.strptime(spiderItem['dates'], "%d %B %Y")
                if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                    yield spiderItem
    
   
