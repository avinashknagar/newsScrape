import scrapy
import pandas as pd
from ..items import NewscrawlItem
from scrapy.http import FormRequest
import json
from lxml import etree
import time
from configparser import ConfigParser
import os


class AltassetsSpider(scrapy.Spider):
    name = 'altassets'
    start_urls = ['https://www.altassets.net/category/private-equity-news/by-news-type/fund-news']

    def parse(self, response):
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('AltassetsSpider', 'startDate').strip()
        endDate = config_raw.get('AltassetsSpider', 'endDate').strip()
        pageNumberToScrapyForOldPost  = int(config_raw.get('AltassetsSpider', 'pageNumberToScrapy').strip())
        
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "AltAssets : The Alternative Assets Network"
        for i in response.xpath('//div[@class="item-details"]'):
            if len(i.xpath('.//div/span/time/text()').extract()) > 0:
                spiderItem['headlines'] = i.xpath('.//h3/a/text()').extract_first()
                spiderItem['dates'] = i.xpath('.//div/span/time/text()').extract_first()
                spiderItem['links'] = i.xpath('.//h3/a/@href').extract_first()
                dateobj = time.strptime(spiderItem['dates'], "%B %d, %Y")
                if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                    yield spiderItem
        
        url = 'https://www.altassets.net/wp-admin/admin-ajax.php?td_theme_name=Newspaper&v=7.0.1'
        for i in range(3,pageNumberToScrapyForOldPost+1):
            formdata = {"action":"td_ajax_loop",
                         "loopState[sidebarPosition]":"",
                         "loopState[moduleId]":"6",
                         "loopState[currentPage]":str(i),
                         "loopState[max_num_pages]":"1301",
                         "loopState[atts][category_id]":"3",
                         "loopState[atts][offset]":"7",
                         "loopState[ajax_pagination_infinite_stop]":"3",
                         "loopState[server_reply_html_data]":""
                         }
            request = FormRequest(url,callback=self.parseRecursion,formdata=formdata)
            yield request
    
    def parseRecursion(self, response):
        print('Function parseRecursion is called!')
        
        work_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(work_dir,'spiders.cfg')
        print(filepath)
        config_raw = ConfigParser()
        config_raw.read(filepath)
        startDate = config_raw.get('AltassetsSpider', 'startDate').strip()
        endDate = config_raw.get('AltassetsSpider', 'endDate').strip()
        
        spiderItem = NewscrawlItem()
        spiderItem['site'] = "AltAssets : The Alternative Assets Network"
        
        jsonBody = json.loads(response.body.decode('gbk').encode('utf-8'))
        htmlcode = jsonBody['server_reply_html_data']
        

        
        dom = etree.HTML(htmlcode)

        for i in dom.xpath('//div[@class="item-details"]'):
            if len(i.xpath('.//div/span/time/text()')) > 0:
                spiderItem['headlines'] = i.xpath('.//h3/a/text()')[0]
                spiderItem['dates'] = i.xpath('.//div/span/time/text()')[0]
                spiderItem['links'] = i.xpath('.//h3/a/@href')[0]
                dateobj = time.strptime(spiderItem['dates'], "%B %d, %Y")
                if dateobj >= time.strptime(startDate,"%Y-%m-%d") and dateobj <= time.strptime(endDate,"%Y-%m-%d"):
                    yield spiderItem

