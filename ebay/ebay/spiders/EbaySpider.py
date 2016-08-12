# -*- coding: utf-8 -*-

import os
import yaml
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from ebay.items import EbayProduct

# http://www.ebay.com/sch/Computer-Components-Parts/175673/i.html?LH_Sold=1&LH_Complete=1&LH_LocatedIn=3&_pppn=r1&scp=ce0&_ipg=200
URL_TEMPLATE = 'http://www.ebay.com/sch/{section}/{section_id}/i.html?' \
               'LH_Sold=1' \
               '&LH_Complete=1' \
               '&LH_LocatedIn={location}' \
               '&_pppn=r1' \
               '&scp=ce0&_ipg=200' \
               '&rt=nc'

PATH = '/'.join(os.path.abspath(__file__).split('/')[:-3])
YAML_PATH = os.path.join(PATH, 'spider_target.yaml')


def get_start_urls(path=YAML_PATH):
    yaml_content = yaml.load(open(path, 'rb'))
    val = [section[:] + [location] for section in yaml_content.get('section')
           for location in yaml_content.get('location')]
    url_map = map(lambda x: dict(zip(['section', 'section_id', 'location'], x)), val)
    return list(set(URL_TEMPLATE.format(**data) for data in url_map))


def get_res(res):
    try:
        return res[0]
    except IndexError as exc:
        return None


def parse_price(price):
    if not price[0].isdigit():
        return price[1:]
    else:
        return price


class EbaySpider(CrawlSpider):
    name = "ebay"
    start_urls = get_start_urls()

    # rules = (
    #     Rule(
    #         LinkExtractor(
    #             restrict_xpaths='//w-root//ul[@id="ListViewInner"]/li//h3[@class="lvtitle"]/a'
    #         ),
    #         follow=True,
    #         callback='parse_detail'
    #     ),
    # )
    def parse(self, response):
        for url in response.xpath('//w-root//ul[@id="ListViewInner"]'
                                  '/li//h3[@class="lvtitle"]/a/@href').extract():
            yield Request(url, callback=self.parse_detail, errback=self.error_handle)

    def parse_detail(self, response):
        item = EbayProduct()
        item['section'] = response.xpath('//span[@itemprop="name"]/text()').extract()[1]
        item['name'] = get_res(response.xpath('//h1[@itemprop="name"]/text()').extract())
        item['href'] = response.url
        item['picture'] = get_res(response.xpath('//img[@itemprop="image"]/@src').extract())
        price_info = response.xpath('//span[@id="prcIsum"]/text()').extract()
        ship_info = response.xpath('//span[@id="fshippingCost"]/span/text()').extract()
        item['create_date'] = get_res(response.xpath('//span[@id="bb_tlft"]/text()').extract())
        if item['create_date']:
            item['create_date'] = item['create_date'].strip()
        try:
            item['price_unit'], item['price'] = get_res(price_info).split()
            item['price'] = parse_price(item['price'])
            item['shipping_unit'], item['shipping_price'] = get_res(ship_info).split()
            item['shipping_price'] = parse_price(item['shipping_price'])
            item['seller'] = get_res(response.xpath('//div[@class="mbg vi-VR-margBtm3"]/a/span/text()').extract())
            item['seller_href'] = get_res(response.xpath('//div[@class="mbg vi-VR-margBtm3"]/a/@href').extract())
        except Exception:
            pass
        yield item

    def error_handle(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
