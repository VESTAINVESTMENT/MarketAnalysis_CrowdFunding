#-*- coding: utf-8 -*-
import os
import csv
import glob
import MySQLdb
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from sqlalchemy import *

class ResultsSpider(scrapy.Spider):
    name = 'results'
    allowed_domains = ["weixin.sogou.com","mp.weixin.qq.com"]
    def start_requests(self):
        self.driver = webdriver.Chrome('C://Users/USER/Desktop/sougou/chromedriver')
        self.driver.get('http://weixin.sogou.com')
        
        pauser=input(print('ready?'))

        sel = Selector(text=self.driver.page_source)
        listings = sel.xpath('//h3/a[@target="_blank"]/@href').extract()
        for listing in listings:
            yield Request(listing, callback=self.parse_listing)
    
        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[@id="sogou_next"]')
                sleep(2)
                self.logger.info('Sleeping for 2 seconds.')
                next_page.click()

                sel = Selector(text=self.driver.page_source)
                listings = sel.xpath('//h3/a[@target="_blank"]/@href').extract()
                for listing in listings:
                    yield Request(listing, callback=self.parse_listing)
            except NoSuchElementException:
                self.logger.info('No more pages to load?')
                manual=input(print('right?'))
                if manual=='yes':
                    self.driver.quit()
                    break
                else:
                    sel = Selector(text=self.driver.page_source)
                    listings = sel.xpath('//h3/a[@target="_blank"]/@href').extract()
                    for listing in listings:
                        yield Request(listing, callback=self.parse_listing)
    def parse_listing(self, response):
        title = response.xpath('//h2[@class="rich_media_title"]/text()').extract_first().encode('utf-8')
        pubdate=response.xpath('//em[@id="post-date"]/text()').extract_first().encode('utf-8')
        author=response.xpath('//a[@id="post-user"]/text()').extract_first().encode('utf-8')
        content=''.join(response.xpath('//div[@class="rich_media_content "]//text()').extract()).strip().encode('utf-8')
        if title==None:
            print("WARNING:It's not a typical link, try redirect.")
            sharelink=response.xpath('//a[@id="js_share_source"]/@href').extract_first()
            yield Request(sharelink, callback=self)
        else:
            yield {'title':title,'pubdate':pubdate,'author':author,'content':content}
    def close(self, reason):
        data=pd.read_csv('C://Users/USER/Desktop/sougou/items.csv')
        engine = create_engine("mysql+mysqldb://root:psswd@localhost:3306/sougou_db?charset=utf8&use_unicode=1",encoding='utf-8')
        meta = MetaData(bind=engine)
        table_actors = Table('sougou_table', meta,Column('title', VARCHAR),Column('date', VARCHAR),Column('author', VARCHAR),Column('content', VARCHAR),mysql_charset='utf-8')
        meta.create_all(engine)
        meta.create_all(engine)
        data.to_sql('sougou_table',con=engine, if_exists='replace',index=False)
