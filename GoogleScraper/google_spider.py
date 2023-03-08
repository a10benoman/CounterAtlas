import scrapy

class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['cse.google.com']
    start_urls = ['https://cse.google.com/cse?cx=a3240aae15a61423c#gsc.tab=0&gsc.q=connect&gsc.sort=']

    def parse(self, response):
        for result in response.css('div.gs-webResult.gs-result'):
            link = result.css('a.gs-title::attr(href)').get()
            title = result.css('a.gs-title::text').get()
            description = result.css('div.gs-bidi-start-align.gs-snippet::text').get()
            if title and link and description:
                yield {
                    'link': link,
                    'title': title,
                    'description': description
                }
