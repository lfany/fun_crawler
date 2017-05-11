# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy


# from scrapy.loader import ItemLoader
from spy.fun_crawler.fun.items import CoserItem


class CoserSpider(scrapy.Spider):
    name = "coser"
    allowed_domains = ["bcy.net"]
    base_url = 'http://bcy.net'
    item = ''
    start_urls = (
        'http://bcy.net/cn125101',
        'http://bcy.net/cn126487',
        'http://bcy.net/cn126173'
    )

    def parse(self, response):
        sel = Selector(response)

        for link in sel.xpath(
                "//div[@class='tab-nav tab-nav--space']/a[@class='tab-nav__item ']/@href").extract():
            if link.find('post') != -1:
                link = 'http://bcy.net%s' % link
                # print(link)
                request = scrapy.Request(link, callback=self.parse_item)
                yield request

    def parse_item(self, response):

        for i in response.xpath('//ul[@class="l-grid__inner"]/div[@id="js-postTpl"]/li[@class="l-grid__item "]'):
            self.item = CoserItem()
            self.item['url'] = response.url
            self.item['post_url'] = self.base_url + i.xpath('//a[@class="postWorkCard__link"]/@href').extract_first()
            self.item['name'] = i.xpath('//span[@class="l-left fz14 w220 cut"]/text()').extract_first()
            self.item['info'] = i.xpath('//footer[@class="bgG bottom db full ph10 text-shadow postWorkCard__ft cut"]/text()') \
                .extract_first()
            self.item['image'] = i.xpath('//div[@class="postWorkCard__img ovf"]/img/@src').extract_first()
            if self.item['post_url']:
                yield scrapy.Request(url=self.item['post_url'], callback=self.parse_post)

            # print(i.xpath('*'))

            # yield item

    def parse_post(self, response):
        self.item['image_urls'] = response.xpath('//img[@class="detail_std detail_clickable"]/@src').extract()
        yield self.item
