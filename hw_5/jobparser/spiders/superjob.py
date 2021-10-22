import re

import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SuperJobSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://nsk.superjob.ru/vakansii/menedzher.html']

    def parse(self, response: HtmlResponse):
        next_page = 'https://nsk.superjob.ru' + response.css('a[rel="next"]').attrib['href']
        response.follow(next_page, callback=self.parse)
        vacancy = response.xpath('//div[@class="_2rfUm _2hCDz _21a7u"]/a/@href').getall()
        for link in vacancy:
            yield response.follow(f'https://nsk.superjob.ru{link}', callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[class ="rFbjy _2dazi _2hCDz _1RQyC"]::text').get()
        salary = response.css('span[class ="_2Wp8I _2rfUm _2hCDz"]::text').getall()
        if salary[0] == 'По договорённости':
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            if salary[0] == 'от':
                str_salary = salary[2].replace(u'\xa0', '')
                salary_min = int(re.search(r'^\d*', str_salary)[0])
                salary_max = None
                salary_currency = re.search(r'\D*$', str_salary)[0]
            elif salary[0] == 'до':
                str_salary = salary[2].replace(u'\xa0', '')
                salary_max = int(re.search(r'^\d*', str_salary)[0])
                salary_min = None
                salary_currency = re.search(r'\D*$', str_salary)[0]
            else:
                salary_min = int(salary[0].replace(u'\xa0', ''))
                salary_max = int(salary[1].replace(u'\xa0', ''))
                salary_currency = salary[3]

        yield JobparserItem(name=name, link=response.url, salary_min=salary_min, salary_max=salary_max,
                            salary_currency=salary_currency)
