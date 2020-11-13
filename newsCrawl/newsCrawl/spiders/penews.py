import scrapy
from ..items import NewscrawlItem
from configparser import ConfigParser
import os
import time


class PenewsSpider(scrapy.Spider):
    name = 'penews'
    start_urls = ['https://www.penews.com/funds/']

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('PenewsSpider', 'startDate').strip()
        endDate = config_raw.get('PenewsSpider', 'endDate').strip()
        pageNumberToScrapyForOldPost  = int(config_raw.get('PenewsSpider', 'pageNumberToScrapy').strip())
        
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "PRIVATE EQUITY NEWS"

        for i in response.xpath('//article'):
            spiderItem['headlines'] = i.xpath('.//div/h2/a/text()').extract_first()
            spiderItem['dates'] = i.xpath('.//div/p/text()').extract_first()
            spiderItem['links'] = i.xpath('.//div/h2/a/@href').extract_first()
            dateobj = time.strptime(spiderItem['dates'], "%A %B %d, %Y %I:%M%p")
            if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                    yield spiderItem

        
        otherPageURLTemplate = 'https://www.penews.com/funds/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('PenewsSpider', 'startDate').strip()
        endDate = config_raw.get('PenewsSpider', 'endDate').strip()
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "PRIVATE EQUITY NEWS"

        for i in response.xpath('//article'):
            spiderItem['headlines'] = i.xpath('.//div/h2/a/text()').extract_first()
            spiderItem['dates'] = i.xpath('.//div/p/text()').extract_first()
            spiderItem['links'] = i.xpath('.//div/h2/a/@href').extract_first()
            dateobj = time.strptime(spiderItem['dates'], "%A %B %d, %Y %I:%M%p")
            if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                yield spiderItem
    
    
