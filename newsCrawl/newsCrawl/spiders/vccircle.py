import scrapy
from ..items import NewscrawlItem
import re
from configparser import ConfigParser
import os

class VccirclePeSpider(scrapy.Spider):
    name = 'vccircle'
    start_urls = ['https://www.vccircle.com/deal-type/pe/','https://www.vccircle.com/deal-type/venture-capital/']

    def parse(self, response):
        
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('VccirclePeSpider', 'pageNumberToScrapy').strip())
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "VCCiRCLE : "+response.css('.page-title::text').get()
        for i in response.css('.article-details'):
            t = i.xpath('.//div[@class="title"]/a/text()').extract()
            d = i.xpath('.//span[@class="publish-time"]/text()').extract()
            for x in t:
                if re.search('[a-zA-Z]+',x) is not None:
                    spiderItem['headlines'] = str(x).strip("\n").strip(" ")
            for x in d:
                if re.search('[a-zA-Z]+',x) is not None:
                    spiderItem['dates'] = str(x).strip("\n").strip(" ")
            spiderItem['links'] = i.xpath('.//div[@class="title"]/a/@href').extract_first()
            print(spiderItem['dates'])
            yield spiderItem
        
        otherPageURLTemplate = 'https://www.vccircle.com/deal-type/pe/all/'
       
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
            
        
        otherPageURLTemplate = 'https://www.vccircle.com/deal-type/venture-capital/all/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
        
#response.css('.card-body').css('.card-title::text').extract()
# response.css('.card-body').xpath('.//a/@href').extract()
    
    def parseRecursion(self, response):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "VCCiRCLE : "+response.css('.page-title::text').get()
        for i in response.css('.article-details'):
            t = i.xpath('.//div[@class="title"]/a/text()').extract()
            d = i.xpath('.//span[@class="publish-time"]/text()').extract()
            for x in t:
                if re.search('[a-zA-Z]+',x) is not None:
                    spiderItem['headlines'] = str(x).strip("\n").strip(" ")
            for x in d:
                if re.search('[a-zA-Z]+',x) is not None:
                    spiderItem['dates'] = str(x).strip("\n").strip(" ")
            spiderItem['links'] = i.xpath('.//div[@class="title"]/a/@href').extract_first()
            print(spiderItem['dates'])
            yield spiderItem
    

