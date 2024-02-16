import os
import scrapy
from urllib.parse import urlparse, unquote
from ..items import UclaItem

class UclaSpider(scrapy.Spider):
    name = "ucla"
    allowed_domains = ["ucla.edu"]
    disallowed_domains = ["digital.library.ucla.edu", "medschool.ucla.edu", "law.ucla.edu", "frontera.library.ucla.edu",
                          "anderson.ucla.edu", "ugedication.edu", "oralhistory.library.ucla.edu",
                          "alumni.ucla.edu/travel/tours/", "dentistry.ucla.edu"]
    start_urls = ["https://www.ucla.edu/"]

    accessed_urls = set(start_urls)

    def valid_next_page(self, url):
        if url is None or url in self.accessed_urls:
            return False
        for domain in self.disallowed_domains:
            if domain in url:
                return False
        return True

    def parse(self, response):
        # Save response body as .txt in an organized folder structure
        self.save_response(response)

        for sel in response.xpath('//ul/li'):
            item = UclaItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['description'] = sel.xpath('text()').extract()
            yield item

            # CUSTOMIZE depth limit in scrapy to work
            '''
            # Extract and follow the URLs of the next pages to scrape (DFS) 
            next_pages = response.xpath('//a/@href').extract()
            for next_page in next_pages:
                next_page = response.urljoin(next_page)
                if self.valid_next_page(next_page):
                    self.accessed_urls.add(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
            '''

    def save_response(self, response):
        parsed_url = urlparse(response.url)
        path_segments = parsed_url.path.strip('/').split('/')
        decoded_segments = [unquote(segment) for segment in path_segments]
        file_path = os.path.join('data', parsed_url.netloc, *decoded_segments)

        if not file_path.endswith('.txt'):
            file_path += '.txt'

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {file_path}')
