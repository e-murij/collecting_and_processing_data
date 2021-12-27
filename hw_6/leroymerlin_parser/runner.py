from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroymerlin_parser.spiders.leroymerlin import LeroymerlinParserSpider
from leroymerlin_parser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinParserSpider, category='стулья')
    process.start()
