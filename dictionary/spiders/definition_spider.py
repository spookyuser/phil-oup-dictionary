import scrapy
from scrapy import FormRequest
from scrapy.item import Item, Field
from bs4 import BeautifulSoup
from scrapy.spiders.init import InitSpider
from ..items import Definition
from scrapy.shell import inspect_response


class DefinitionSpider(scrapy.Spider):
    name = "definition"
    alt_headers = {
        "User-Agent": "Dictionary Scraping Bot",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.5",
    }
    headers = {"User-Agent": "Dictionary Scraping Bot"}
    url = "https://0-www-oxfordreference-com.innopac.wits.ac.za/view/10.1093/acref/9780198735304.001.0001/acref-9780198735304-e-{}"
    login_url = "https://innopac.wits.ac.za/wamvalidate?url=https%3A%2F%2F0-www-oxfordreference-com.innopac.wits.ac.za"
    login_form = {
        "name": "", #TODO: Add name
        "code": "", #TODO: Add code
        "pin": "", #TODO: Add pin
        "pat_submit": "xxx", #This is actually meant to be 'xxx'
    }
    login_count = 0

    def start_requests(self):
        for i in range(int(self.start), int(self.end)):
            yield scrapy.Request(url=self.url.format(i), callback=self.parse, headers=self.alt_headers)

    def parse(self, response):
        if "validate" in response.url:
            return self.login(response)
        else:
            return self.get_data(response)

    def login(self, response):
        self.login_count = self.login_count + 1
        self.log("Login page... Posting username & password. Login count:" + str(self.login_count))
        self.crawler.stats.set_value('login count', self.login_count)

        return FormRequest.from_response(
            response,
            formdata=self.login_form,
            headers=self.alt_headers,
            callback=self.parse,
            dont_filter=True,
        )

    def get_data(self, response):
        word_selector = response.xpath('//*[@id="pagetitle"]/span[1]//text()')
        header_selector =  response.css("#pagetitle > span.headwordInfo *::text")
        definition_selector = response.xpath('//div[@class="div1"]/p')
        see_also_selector = response.css("#contentRoot > p")

        index = response.url.split("-e-")[1]
        word_text = word_selector.get()
        word_html = response.xpath('//*[@id="pagetitle"]/span[1]').get()
        header = "".join(header_selector.extract())
        definition_html = "".join(definition_selector.extract())
        definition_text = BeautifulSoup(definition_html).get_text()
        see_also = see_also_selector.get()
        yield Definition(
            index=index,
            word_text=word_text,
            word_html=word_html,
            header=header,
            definition_html=definition_html,
            definition_text=definition_text,
            see_also=see_also,
        )
