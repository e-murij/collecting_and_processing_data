import requests
from bs4 import BeautifulSoup as bs


def parser_item(item):
    vacancy_date = {}
    vacancy_name_link = item.find('span', {'class': 'resume-search-item__name'})
    vacancy_date['vacancy_name'] = vacancy_name_link.getText().replace(u'\xa0', ' ')
    vacancy_date['vacancy_link'] = vacancy_name_link.find('a')['href']
    company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').getText().replace(
        u'\xa0', ' ')
    vacancy_date['company_name'] = company_name
    salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace('\u202f', '')
        salary = salary.split(' ')
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
            salary_currency = salary[2]
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
            salary_currency = salary[2]
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[2])
            salary_currency = salary[3]
    vacancy_date['salary_min'] = salary_min
    vacancy_date['salary_max'] = salary_max
    vacancy_date['salary_currency'] = salary_currency
    return vacancy_date


def parser_hh(vacancy, link):
    vacancy_date = []
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    html = requests.get(
        link + f'/search/vacancy?area=4&fromSearchLine=true&st=searchVacancy&text={vacancy}&from=suggest_post',
        headers=headers)
    if html.ok:
        html_bs = bs(html.text, 'lxml')
        page_block = html_bs.find('div', {'data-qa': 'pager-block'})
        if not page_block:
            last_page = 1
        else:
            last_page = int(page_block.find_all('a', {'class': 'bloko-button'})[-2].getText())

    for page in range(0, last_page):
        html = requests.get(
            link + f'/search/vacancy?area=4&fromSearchLine=true&st=searchVacancy&text={vacancy}&from=suggest_post&page={page}',
            headers=headers)
        if html.ok:
            html_bs = bs(html.text, 'lxml')
            vacancy_items = html_bs.find('div', {'data-qa': 'vacancy-serp__results'}) \
                .find_all('div', {'class': 'vacancy-serp-item'})
            for item in vacancy_items:
                vacancy_date.append(parser_item(item))
    return vacancy_date
