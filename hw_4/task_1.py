from lxml import html
import requests
import datetime
from pymongo import MongoClient


def get_news_mail_ru():
    news = []
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

    keys = ('title', 'link', 'date')
    link = 'https://mail.ru/'

    request = requests.get(link, headers=headers)
    root = html.fromstring(request.text)
    news_links = root.xpath("//a[@class='news-visited svelte-15lqz3c']/@href")
    news_text = root.xpath("//a[@class='news-visited svelte-15lqz3c']/text()")

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', ' ')

    news_date = []
    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//*[@datetime]/@datetime')
        news_date.append(date)

    news_date = [item for sublist in news_date for item in sublist]

    for item in list(zip(news_text, news_links, news_date)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
        news_dict['source'] = 'mail.ru'
        news.append(news_dict)

    return news


def get_news_yandex():
    news = []
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

    keys = ('title', 'link', 'date')
    link = 'https://yandex.ru/news'

    request = requests.get(link, headers=headers)
    root = html.fromstring(request.text)
    news_links = root.xpath("//div[@class='mg-card__text']/a/@href")
    news_text = root.xpath("//*[@class='mg-card__title']/text()")

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', ' ')

    news_date = root.xpath('//span[@class="mg-card-source__time"]/text()')
    for i, item in enumerate(news_date):
        if len(item) == 5:
            news_date[i] = f'{datetime.date.today()} {item}'
        else:
            news_date[i] = f'{datetime.date.today() - datetime.timedelta(days=1)} {item[-5:]}'

    for item in list(zip(news_text, news_links, news_date)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
        news_dict['source'] = 'yandex.ru'
        news.append(news_dict)

    return news


def get_news_lenta_ru():
    news = []

    keys = ('title', 'date', 'link')
    link = 'https://lenta.ru/'

    request = requests.get(link)

    root = html.fromstring(request.text)
    root.make_links_absolute(link)

    news_links = root.xpath('//div[@class="item"]/a/@href')
    news_links.append(root.xpath('//div[@class="first-item"]/h2/a/@href')[0])
    news_text = root.xpath('//div[@class="item"]/a/text()')
    news_text.append(root.xpath('//div[@class="first-item"]/h2/a/text()')[0])
    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', ' ')
    news_date = []
    for item in news_links:
        request_item = requests.get(item)
        root = html.fromstring(request_item.text)
        news_date.append(root.xpath('//div[contains(@class, "b-topic__info")]/time/@datetime'))

    news_date = [item for sublist in news_date for item in sublist]

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)

    return news


def print_news_to_db(news, mongodb_url):
    client = MongoClient(mongodb_url)
    db = client['news_database']
    collection = db['news']
    collection.insert_many(news)


if __name__ == "__main__":
    mongodb_url = 'mongodb://localhost:27017/'
    print_news_to_db(get_news_mail_ru(), mongodb_url)
    print_news_to_db(get_news_lenta_ru(), mongodb_url)
    print_news_to_db(get_news_yandex(), mongodb_url)
