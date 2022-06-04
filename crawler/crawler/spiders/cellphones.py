import scrapy

class CellPhonesSpider(scrapy.Spider):
    name: 'CellPhones'
    start_urls = ['']

    def parse(self, response):
        yield
