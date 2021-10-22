import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://novosibirsk.hh.ru/search/vacancy?area=4&fromSearchLine=true&text=Python&from=suggest_post']

    def parse(self, response: HtmlResponse):
        next_page = 'https://novosibirsk.hh.ru' + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib[
            'href']
        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').get()
        salary = ''.join(response.css('span[class="bloko-header-2 bloko-header-2_lite"]::text').getall())
        if salary == 'з/п не указана':
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.replace(u'\xa0', '').split(' ')
            if salary[0] == 'от' and salary[2] == 'до':
                salary_min = int(salary[1])
                salary_max = int(salary[3])
                salary_currency = salary[4]
            elif salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
                salary_currency = salary[2]
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
                salary_currency = salary[2]

        yield JobparserItem(name=name, link=response.url, salary_min=salary_min, salary_max=salary_max,
                            salary_currency=salary_currency)
