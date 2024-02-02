import scrapy


class ExtractHtmlSpider(scrapy.Spider):
    name = "extract_html"

    def start_requests(self):
        # Get user-input URL from command line for website to scrape
        user_input_url = getattr(self, 'url', None)
        if user_input_url:
            yield scrapy.Request(url=user_input_url, callback=self.parse)

    def parse(self, response):
        # Extract HTML code from the page
        yield {
            'url': response.url,
            'html_code': response.body.decode('utf-8'),
        }
