import scrapy
from igg_games.items import IggItem
from scrapy.loader import ItemLoader


class IggSpider(scrapy.Spider):
    name = 'igg'
    allowed_domains = 'igg-games.com'

    start_urls = ['https://igg-games.com']

    def parse(self, response):
        href = response.xpath('//li/a[contains(text(), "GAME LIST")]/@href').extract_first()
        yield scrapy.Request(href, callback = self.parse_urls, dont_filter = True)

    def parse_urls(self, response):
        for sel in response.xpath('//div[@class="uk-margin-medium-top"]/ul/li'):
            url = sel.xpath('a/@href').extract_first()
            yield scrapy.Request(url, callback = self.parse_dir_content, dont_filter = True)

    def parse_dir_content(self, response):
        il = ItemLoader(item=IggItem(), response=response)

        il.add_value('title', response.xpath(
            '//h1[@class="uk-margin-large-top uk-margin-remove-bottom uk-article-title ogiua"]/text()').get())
        il.add_value('developer', response.xpath(
            '//span[contains(text(), "Developer: ")]/../text()').getall())
        il.add_value('publisher', response.xpath(
            '//span[contains(text(), "Publisher: ")]/../text()').getall())
        il.add_value('release_date', response.xpath(
            '//span[contains(text(), "Release Date: ")]/../text()').getall())
        il.add_value('genre', response.xpath(
            '//span[contains(text(), "Genre: ")]/../text()').getall())
        il.add_value('links', response.xpath(
            '//a[contains(text(), "Download HERE")]/@href').getall())
        return il.load_item()
