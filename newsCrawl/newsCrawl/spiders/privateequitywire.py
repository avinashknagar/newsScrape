import scrapy
from ..items import NewscrawlItem
import pandas as pd
import time
from configparser import ConfigParser
import os

class PrivateequitywireSpider(scrapy.Spider):
    name = 'privateequitywire'
    #allowed_domains = ['www.privateequitywire.co.uk/news']
    start_urls = ['http://www.privateequitywire.co.uk/news/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "Private Equity Wire"
        spiderItem['headlines'] = data['headline']
        spiderItem['dates'] = pd.Timestamp("today").strftime("%m/%d/%Y")
        spiderItem['links'] = data['fullLink']
        li = response.css('.field-name-body').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        pageNumberToScrapyForOldPost  = int(config_raw.get('PrivateequitywireSpider', 'pageNumberToScrapy').strip())
        
        
        headline =  response.css('.node--view-mode-preview').xpath('//div/section/h2/a/text()').extract()
        link = response.css('.node--view-mode-preview').xpath('//div/section/h2/a/@href').extract()
        spiderItem = NewscrawlItem()

        dt = list(zip(headline, link))
        df = pd.DataFrame(dt, columns=['headline', 'link'])
        df.drop_duplicates(inplace=True)
        df1 = df[~df.link.str.contains('http', case=False)]
        df1['fullLink'] = df1['link'].apply(lambda x: 'https://www.privateequitywire.co.uk'+str(x))

        for i in df1.index:
            data = df1.iloc[i]
            request = response.follow(df1['link'][i], callback = self.getContent)
            request.cb_kwargs['data'] = data
            yield request
        
        otherPageURLTemplate = 'https://www.privateequitywire.co.uk/news?page='
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+1):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        headline =  response.css('.node--view-mode-preview').xpath('//div/section/h2/a/text()').extract()
        link = response.css('.node--view-mode-preview').xpath('//div/section/h2/a/@href').extract()
        spiderItem = NewscrawlItem()

        dt = list(zip(headline, link))
        df = pd.DataFrame(dt, columns=['headline', 'link'])
        df.drop_duplicates(inplace=True)
        df1 = df[~df.link.str.contains('http', case=False)]
        df1['fullLink'] = df1['link'].apply(lambda x: 'https://www.privateequitywire.co.uk'+str(x))

        for i in df1.index:
            data = df1.iloc[i]
            request = response.follow(df1['link'][i], callback = self.getContent)
            request.cb_kwargs['data'] = data
            yield request
        
