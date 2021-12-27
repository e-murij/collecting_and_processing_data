import scrapy
from itemloaders.processors import TakeFirst, Compose

def price_to_float(price):
    price = price[0].replace(' ', '')
    return float(price)

class LeroymerlinParserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(), input_processor= Compose(price_to_float))
    pass
