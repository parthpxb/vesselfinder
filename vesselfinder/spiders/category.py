import requests
import scrapy
from parsel import Selector
from scrapy.cmdline import execute


class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        url = "https://www.vesselfinder.com/news"
        url = url
        url = url

        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '_ga_0MB1EVE8B7=GS1.1.1681130340.1.0.1681130340.0.0.0; _ga=GA1.1.1494201586.1681130340; _gcl_au=1.1.685194021.1681130341',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        count = 0

        response = requests.request("GET", url, headers=headers, data=payload)
        data=Selector(response.text)
        print()




if __name__ == '__main__':
    execute('scrapy crawl category'.split())