import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class UnquoteSpider(scrapy.Spider):
    name = 'unquote'
    start_urls = ['http://www.unquote.com/category/funds/']

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('UnquoteSpider', 'pageNumberToScrapy').strip())
        
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Unquote: An Acuris Company"

        for i in response.css('article'):
            h = i.css('.listings-article-title').xpath('.//a/text()').extract()
            d = i.css('.article-meta-details').xpath('.//li/time/@datetime').extract()
            if len(h) > 0:
                spiderItem['headlines'] = h[0]
                if len(d) == 0:
                    spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
                else:
                    spiderItem['dates'] = d[0].split('T')[0]
                spiderItem['links'] = i.css('.listings-article-title').xpath('.//a/@href').extract_first()
                yield spiderItem
        
        otherPageURLTemplate = 'https://www.unquote.com/category/funds/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Unquote: An Acuris Company"

        for i in response.css('article'):
            h = i.css('.listings-article-title').xpath('.//a/text()').extract()
            d = i.css('.article-meta-details').xpath('.//li/time/@datetime').extract()
            if len(h) > 0:
                spiderItem['headlines'] = h[0]
                if len(d) == 0:
                    spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
                else:
                    spiderItem['dates'] = d[0].split('T')[0]
                spiderItem['links'] = i.css('.listings-article-title').xpath('.//a/@href').extract_first()
                yield spiderItem
                
    
    
