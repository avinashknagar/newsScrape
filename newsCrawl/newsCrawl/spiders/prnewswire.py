import scrapy
from ..items import NewscrawlItem
import pandas as pd
from configparser import ConfigParser
import os

class PrnewswireSpider(scrapy.Spider):
    name = 'prnewswire'
    start_urls = ['https://www.prnewswire.com/news-releases/news-releases-list/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "CISION PR Newswire"
        spiderItem['headlines'] = data[0]
        spiderItem['dates'] = response.css('.mb-no::text').extract_first()
        spiderItem['links'] = data[1]
        li = response.css('.release-body').xpath('.//p/text()').extract()
        content = ''.join(li).replace('/PRNewswire/','')
        spiderItem['content'] = content
        return spiderItem

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('PrnewswireSpider', 'pageNumberToScrapy').strip())
        
        
        for i in response.css('.col-sm-12'):
            data = []
            data.append(i.xpath('.//h3/a/text()').extract_first())
            data.append('https://www.prnewswire.com'+str(i.xpath('.//h3/a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                #print(data)
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
        
        for i in response.css('.col-sm-8'):
            data = []
            data.append(i.xpath('.//h3/a/text()').extract_first())
            data.append('https://www.prnewswire.com'+str(i.xpath('.//h3/a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                #print(data)
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
        
        otherPageURLTemplate = 'https://www.prnewswire.com/news-releases/news-releases-list/?page='
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)+'&pagesize=25'
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
        
    def parseRecursion(self, response):
        

        for i in response.css('.col-sm-12'):
            data = []
            data.append(i.xpath('.//h3/a/text()').extract_first())
            data.append('https://www.prnewswire.com'+str(i.xpath('.//h3/a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                #print(data)
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
        
        for i in response.css('.col-sm-8'):
            print(i)
            data = []
            data.append(i.xpath('.//h3/a/text()').extract_first())
            data.append('https://www.prnewswire.com'+str(i.xpath('.//h3/a/@href').extract_first()))
            if data[0] != None and data[1] != None:
                #print(data)
                request = response.follow(data[1], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request   
        
        


