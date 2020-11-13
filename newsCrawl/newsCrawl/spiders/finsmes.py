import scrapy
from ..items import NewscrawlItem
import pandas as pd
import time
from configparser import ConfigParser
import os

class FinsmesSpider(scrapy.Spider):
    name = 'finsmes'
    #allowed_domains = ['https://www.finsmes.com/']
    start_urls = ['https://www.finsmes.com/']

    def getContent(self, response, data):
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "FINSMES : Real Time VC & Private Equity Deals and News"
        spiderItem['headlines'] = data['headline']
        spiderItem['dates'] = data['date']
        spiderItem['links'] = data['link']
        li = response.css('.entry-content').xpath('.//p/text()').extract()
        spiderItem['content'] = ' '.join(li)
        return spiderItem

    def parse(self, response):
        print('Function parse is called!')
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('FinsmesSpider', 'startDate').strip()
        endDate = config_raw.get('FinsmesSpider', 'endDate').strip()
        pageNumberToScrapyForOldPost  = int(config_raw.get('FinsmesSpider', 'pageNumberToScrapy').strip())
        
        print('Start to FinsmesSpider from '+startDate+' to '+endDate+' for '+str(pageNumberToScrapyForOldPost)+' pages')
 
        headline = response.xpath('//div[@class="post-module-content"]/header/h2/a/text()').extract()
        link = response.xpath('//div[@class="post-module-content"]/header/h2/a/@href').extract()
        date = response.css('.published::text').extract()
        
        print(date)

        dt = list(zip(headline, link, date))
        df = pd.DataFrame(dt, columns=['headline', 'link', 'date'])
        
        for i in df.index:
            #data['site'] = "FINSMES : Real Time VC & Private Equity Deals and News"
            print(df['link'][i])
            dateobj = time.strptime(df['date'][i], "%B %d, %Y")
            if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                data = df.iloc[i]
                request = response.follow(df['link'][i], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
        
        otherPageURLTemplate = 'https://www.finsmes.com/older-posts/page/'
        
        for pagenumber in range(2,pageNumberToScrapyForOldPost+2):
            otherPageURL = otherPageURLTemplate + str(pagenumber)
            request = response.follow(otherPageURL, callback = self.parseRecursion)
            yield request
    
    def parseRecursion(self, response):
        print('Function parseRecursion is called!')
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('FinsmesSpider', 'startDate').strip()
        endDate = config_raw.get('FinsmesSpider', 'endDate').strip()

        headline = response.xpath('//div[@class="post-module-content"]/header/h2/a/text()').extract()
        link = response.xpath('//div[@class="post-module-content"]/header/h2/a/@href').extract()
        date = response.css('.published::text').extract()
        
        dt = list(zip(headline, link, date))
        df = pd.DataFrame(dt, columns=['headline', 'link', 'date'])
        
        for i in df.index:
            #data['site'] = "FINSMES : Real Time VC & Private Equity Deals and News"
            print(df['link'][i])
            dateobj = time.strptime(df['date'][i], "%B %d, %Y")
            if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                data = df.iloc[i]
                request = response.follow(df['link'][i], callback = self.getContent)
                request.cb_kwargs['data'] = data
                yield request
