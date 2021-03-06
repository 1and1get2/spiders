            # -*- coding: utf-8 -*-

from os import linesep

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from tutorial.items import BookItem

class GroupSpider(CrawlSpider):
    name = "douban_book"
    allowed_domains = ["douban.com"]
    start_urls = [
        #u'http://book.douban.com/tag/?view=type'
        u'http://book.douban.com/tag/小说'
    ]

    rules = [
        # 规则 获得页面里面的下一页，follow爬下去
        Rule(SgmlLinkExtractor(
                allow=('/subject/\d+/$',),
                restrict_xpaths=('//*[@id="subject_list"]/*',),
            ),
            callback='parse_book',
            process_request='add_cookie',
        ),
        # 规则 获得页面里面的下一页，follow爬下去
        Rule(SgmlLinkExtractor(
                allow=('/tag/[^/]+\?start=',),
                restrict_xpaths=('//*[@id="subject_list"]/'
                                 'div[@class="paginator"]/span[@class="next"]/a',),
            ),
            callback='parse_book_tag',
            follow=True,
            process_request='add_cookie',
        ),
    ]


    def add_cookie(self, request):
        request.replace(cookies=[
            {'name': 'COOKIE_NAME',
             'value': 'VALUE',
             'domain': '.book.douban.com',
             'path': '/'},
            ]);
        return request;

    def parse_book(self, response):
        sel = Selector(response)
        title = sel.css("#wrapper > h1 > span").xpath('text()').extract()[0]
        p_article = sel.css(".article")
        #url = response.url
        #self.log(url)
        #with open('./data/book', 'a') as f:
            #f.write(url)
            #f.write(linesep)
        item = BookItem()
        item['title'] = title
        return item

    def parse_book_tag(self, response):
        url = response.url
        self.log(url)
        with open('./data/book_tag', 'a') as f:
            f.write(url)
            f.write(linesep)
