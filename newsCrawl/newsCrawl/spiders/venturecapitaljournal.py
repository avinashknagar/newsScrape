import scrapy
from ..items import NewscrawlItem
import time
from configparser import ConfigParser
import os


class VenturecapitaljournalSpider(scrapy.Spider):
    name = 'venturecapitaljournal'
    start_urls = ['https://www.venturecapitaljournal.com/tag/fundraising/']

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('VenturecapitaljournalSpider', 'startDate').strip()
        endDate = config_raw.get('VenturecapitaljournalSpider', 'endDate').strip()
        pageNumberToScrapyForOldPost  = int(config_raw.get('VenturecapitaljournalSpider', 'pageNumberToScrapy').strip())
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Venture Capital Journal"

        for i in response.css('.td-block-span6'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            spiderItem['dates'] = i.css('.td-post-date').xpath('.//time/@datetime').extract()[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            dateobj = time.strptime(spiderItem['dates'], "%Y-%m-%d")
            if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                yield spiderItem
        
        otherPageURLTemplate = 'https://www.venturecapitaljournal.com/tag/fundraising/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+2):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'/'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('VenturecapitaljournalSpider', 'startDate').strip()
        endDate = config_raw.get('VenturecapitaljournalSpider', 'endDate').strip()
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Venture Capital Journal"

        for i in response.css('.td-block-span6'):
            spiderItem['headlines'] = i.css('.entry-title').xpath('.//a/text()').extract_first()
            spiderItem['dates'] = i.css('.td-post-date').xpath('.//time/@datetime').extract()[0].split('T')[0]
            spiderItem['links'] = i.css('.entry-title').xpath('.//a/@href').extract_first()
            dateobj = time.strptime(spiderItem['dates'], "%Y-%m-%d")
            if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                yield spiderItem
            
    
    
    
