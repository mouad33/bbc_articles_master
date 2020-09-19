# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy import Request
from bbc_articles.items import *
import logging
from pyquery import PyQuery as pq

from bs4 import BeautifulSoup
from readability import Document



import requests
requests.packages.urllib3.contrib.pyopenssl.extract_from_urllib3()

from datetime import datetime



class BbcSpider(CrawlSpider):
    name = 'bbc'
    start_urls = ['https://www.bbc.com/']

    rules=(Rule(LinkExtractor(restrict_xpaths="//li[contains(@class,'orb-nav-home')]//a",process_value=lambda x:x[0:15]+'.com'), callback='parse_item'),
        Rule(LinkExtractor(allow='bbc.com', restrict_xpaths='//div[contains(@class,"module__content")]'
                                                               '//div[contains(@class,"media") and not (contains(@class,"media--icon"))]'
                                                               '//a[contains(@class,"block-link__overlay-link")]'
                              , process_value=lambda x: 'https://www.bbc.com' + x if x[0:1] == "/" else x),
                callback='parse_item'),
           )
 
    @staticmethod
    def clean_article_text(raw_text):
        # readability library is not perfect,. sometimes unnecessary text is included.
        # remove those manually as follows.
        cleaned = raw_text
        removing_strings = ['Media playback is unsupported on your device ']
        for del_str in removing_strings:
            cleaned = cleaned.replace(del_str, '')

        return cleaned

 
#parse the home page of bbc and get the infomation of the media contents

    def reconcile_url_base(self, raw_urls):
        base_added_urls = [(self.start_urls[0] + x) if x[:4]!='http' else x for x in raw_urls ]

        return base_added_urls           
#parse the infomation of the articles on bbc home page

    def parse_item(self, response):
        
        
        if response.status==200:	
            # Extracting the content using css selectors
            urls = response.css('.media__link::attr(href)').extract()
            tag_texts = response.css('.media__tag::text').extract()
            tag_urls = response.css('.media__tag::attr(href)').extract()

            urls_cleansed = self.reconcile_url_base(urls)
            tag_urls_cleansed = self.reconcile_url_base(tag_urls)

            if len(urls_cleansed) != len(tag_urls_cleansed):
                raise Exception('Length Mismatch between article urls and tag urls')

            article_info_list = []

            for item in zip(urls_cleansed, tag_urls_cleansed, tag_texts):
                url = item[0]
                tag_url = item[1]
                tag_text = item[2]
                url_response = requests.get(url)
                doc = Document(url_response.text)
                soup = BeautifulSoup(url_response.text)
                date_info = soup.find('div', attrs={'class': 'date date--v2'})
                if date_info:
                    created_time_epoch = int(date_info['data-seconds'])
                    created_time_datetime = datetime.fromtimestamp(created_time_epoch)
                else:
                    created_time_datetime = None

                title = doc.title()
                cleansed_body = doc.summary()
            # Cannot scrap created time with scrapy nor with readability, so use BeautifulSoup for that.
                body_soup = BeautifulSoup(cleansed_body)
                cleansed_article_text = ' '.join([x.get_text().replace('\n', ' ') for x in body_soup.find_all('p')])
                cleansed_article_text = self.clean_article_text(cleansed_article_text)
				
                itemm=BbcArticlesItem()
                itemm['title']=doc.title()
                itemm['url']=url
                #itemm['time']=created_time_datetime
                #itemm['type']=tag_url
                itemm['related_topics']=tag_text
                itemm['article_text']=cleansed_article_text
            

				
               
                yield itemm
			
			
			
			
			
		      
		 
