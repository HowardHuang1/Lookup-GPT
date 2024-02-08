import scrapy
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
        #print(type(url), url)
        if url is None or url in self.accessed_urls:
            return False
        for domain in self.disallowed_domains:
            if domain in url:
                return False
        return True


    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            item = UclaItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['description'] = sel.xpath('text()').extract()
            yield item

            # Extract the URLs of the next pages to scrape
            next_pages = response.xpath('//a/@href').extract()
            for next_page in next_pages:
                next_page = response.urljoin(next_page)
                if self.valid_next_page(next_page):
                    yield scrapy.Request(next_page, callback=self.parse)
                    self.accessed_urls.add(next_page)