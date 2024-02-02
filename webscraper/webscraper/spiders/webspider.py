import scrapy


class WebspiderSpider(scrapy.Spider):
    name = "webspider"
    allowed_domains = ["registrar.ucla.edu"]
    start_urls = ["https://registrar.ucla.edu/registration-classes"]

    def parse(self, response):
        html_content = response.body
        with open('output.html', 'wb') as f:
            f.write(html_content)

        next_page = response.css('li')

        # hardcoded next page as classes page
        if next_page is not None:
            next_page_url = "https://registrar.ucla.edu/registration-classes"
            yield response.follow(next_page_url, callback=self.parse)
