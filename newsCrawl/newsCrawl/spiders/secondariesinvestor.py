import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os


class SecondariesinvestorSpider(scrapy.Spider):
    name = 'secondariesinvestor'
    start_urls = ['https://www.secondariesinvestor.com/news/fundraising/']

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('SecondariesinvestorSpider', 'pageNumberToScrapy').strip())
        
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Secondaries Investor"

        for i in response.css('.item-details'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            d = i.css('.td-post-date').xpath('.//time/@datetime').extract()
            if len(d) == 0:
                spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
            else:
                spiderItem['dates'] = d[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            yield spiderItem
            
        otherPageURLTemplate = 'https://www.secondariesinvestor.com/news/fundraising/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Secondaries Investor"

        for i in response.css('.item-details'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            d = i.css('.td-post-date').xpath('.//time/@datetime').extract()
            if len(d) == 0:
                spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
            else:
                spiderItem['dates'] = d[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            yield spiderItem


