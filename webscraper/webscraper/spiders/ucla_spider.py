import os
import scrapy
from urllib.parse import urlparse, unquote
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

class UclaSpider(scrapy.spiders.CrawlSpider):
    name = "ucla"
    allowed_domains = []
    start_urls = []
    exclude_patterns = ['.*\.(css|js|gif|jpg|jpeg|png)']

    custom_settings = {
        'DEPTH_LIMIT': 1  # Set your desired depth limit here
    }

    rules = (
        Rule(LinkExtractor(allow=('/')), callback='parse', follow=True),
    )

    # the following 4 functions are used to set the allowed_domains and start_urls properties to my massive 2000+ domain list
    # that actually got shortened to 130 domains
    def _loadDomains(self):
        domains = []
        with open('domains.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line.strip():
                    break 
                domains.append(line.strip())
        return domains
    def _loadStartURLs(self):
        urls = []
        with open('domains.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line.strip():
                    break 
                urls.append(f'https://{line.strip()}')
        return urls
    @property
    def allowed_domains(self):
        return self._loadDomains()
    @property
    def start_urls(self):
        return self._loadStartURLs()

    def parse(self, response):
        # Save response body as .txt in an organized folder structure
        self.save_response(response)

        # commenting this out b/c it just floods the terminal output
        # for sel in response.xpath('//ul/li'):
        #     item = UclaItem()
        #     item['title'] = sel.xpath('a/text()').extract()
        #     item['link'] = sel.xpath('a/@href').extract()
        #     item['description'] = sel.xpath('text()').extract()
        #     yield item


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
