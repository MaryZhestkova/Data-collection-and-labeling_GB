import scrapy
from scrapy.http import HtmlResponse
from labirint.items import LabirintItem

class LabirintSpider(scrapy.Spider):
    name = "labirint"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/genres/2791/"]

    def parse(self, response: HtmlResponse):
        # Переход на следующую страницу
        next_page = response.xpath('//a[@class="pagination-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        # Получение ссылок на книги
        books = response.xpath('//span[@class="product-title"]/../@href').getall()
        for book in books:
            yield response.follow(book, callback=self.books_parse)
    

    def books_parse(self, response: HtmlResponse):
        # Извлечение названия книги
        title = response.xpath('//span[@class="product-title"]/text()').get()
        
        # Извлечение автора книги
        author = response.xpath('//div[@class="product-author"]/a/span/text()').get()
        
        # Извлечение цены книги
        price = response.xpath('//span[@class="price-val"]/span/text()').get()

        # Отладочная информация
        self.logger.info(f'Title: {title}, Author: {author}, Price: {price}')

        # Обработка случаев отсутствия данных
        title = title.strip() if title else 'Не найдено'
        author = author.strip() if author else 'Не найдено'
        price = price.strip() if price else 'Не найдено'

        url = response.url
        yield LabirintItem(title=title, author=author, price=price, url=url)