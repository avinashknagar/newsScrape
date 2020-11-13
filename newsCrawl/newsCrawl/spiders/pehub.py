import scrapy
import pandas as pd
from ..items import NewscrawlItem
from configparser import ConfigParser
import os

class PehubSpider(scrapy.Spider):
    name = 'pehub'
    start_urls = ['https://www.pehub.com/news-and-analysis/pe-deals/']

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('PehubSpider', 'pageNumberToScrapy').strip())
        
        
        spiderItem = NewscrawlItem()

        spiderItem['site'] = "PE Hub"
        for i in response.css('.td-animation-stack'):
            h = i.xpath('.//div/div[@class="item-details"]/div/h2/a/text()').extract()
            d = i.xpath('.//div/div[@class="td-module-meta-info"]/span[@class="td-post-date"]/time/@datetime').extract()
            if len(d)>0 and len(h)>0:
                spiderItem['headlines'] = h[0]
                spiderItem['dates'] = list(d[0].split('T'))[0]
                spiderItem['links'] = i.xpath('.//div/div[@class="item-details"]/div/h2/a/@href').extract_first()
                yield spiderItem
        
        otherPageURLTemplate = 'https://www.pehub.com/news-and-analysis/pe-deals/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        spiderItem = NewscrawlItem()

        spiderItem['site'] = "PE Hub"
        for i in response.css('.td-animation-stack'):
            h = i.xpath('.//div/div[@class="item-details"]/div/h2/a/text()').extract()
            d = i.xpath('.//div/div[@class="td-module-meta-info"]/span[@class="td-post-date"]/time/@datetime').extract()
            if len(d)>0 and len(h)>0:
                spiderItem['headlines'] = h[0]
                spiderItem['dates'] = list(d[0].split('T'))[0]
                spiderItem['links'] = i.xpath('.//div/div[@class="item-details"]/div/h2/a/@href').extract_first()
                yield spiderItem
    
    
    
