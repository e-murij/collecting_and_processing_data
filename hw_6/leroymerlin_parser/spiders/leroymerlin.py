import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroymerlin_parser.items import LeroymerlinParserItem


class LeroymerlinParserSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, category):
        self.start_urls = [f'https://novosibirsk.leroymerlin.ru/search/?q={category}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="bex6mjh_plp b1f5t594_plp p5y548z_plp pblwt5z_plp nf842wf_plp"]'
                                   '//@href').getall()
        for link in ads_links:
            yield response.follow('https://novosibirsk.leroymerlin.ru' + link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinParserItem(), response=response)
        loader.add_xpath("name", '//h1[@slot ="title"]//text()')
        loader.add_xpath("photos", '//img[@slot="thumbs"]//@src')
        loader.add_xpath("price", '//span[@slot="price"]//text()')
        yield loader.load_item()
