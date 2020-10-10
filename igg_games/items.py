import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Compose, MapCompose, Join, Identity


def filter_empty(value):
    if (value):
        return value


def filter_title(value):
    return value.replace('Free Download', '').replace('  ', ' ')


class IggItem(scrapy.Item):

    title = scrapy.Field(
        input_processor=Compose(TakeFirst(), filter_title, lambda v: v.strip()),
        output_processor=Join(''))

    developer = scrapy.Field(
        input_processor=MapCompose(lambda v: v.strip()),
        output_processor=Join(''))

    publisher = scrapy.Field(
        input_processor=MapCompose(lambda v: v.strip()),
        output_processor=Join(''))

    release_date = scrapy.Field(
        input_processor=MapCompose(lambda v: v.strip()),
        output_processor=Join(''))

    genre = scrapy.Field(
        input_processor=MapCompose(lambda v: v.strip(), filter_empty),
        output_processor=Identity())

    links = scrapy.Field(
        input_processor=MapCompose(lambda v: v.strip(), filter_empty),
        output_processor=Identity())
