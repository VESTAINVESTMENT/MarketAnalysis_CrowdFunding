#-*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
from selenium.common.exceptions import NoSuchElementException

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
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break
    def parse_listing(self, response):
    	title = response.xpath('//h2[@class="rich_media_title"]/text()').extract_first()
    	date=response.xpath('//em[@id="post-date"]/text()').extract_first()
    	author=response.xpath('//a[@id="post-user"]/text()').extract_first()
    	content=''.join(response.xpath('//div[@class="rich_media_content "]//text()').extract()).strip()
    	yield {'title':title,
    			'date':date,
    			'author':author,
    			'content':content}