# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import ArticleItem
import re


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").extract()[0]
        author = response.xpath("//span[@class='name']/a/text()").extract()[0]
        avatar = response.xpath("//a[@class='avatar']/img/@src").extract()[0]
        pub_time = response.xpath("//span[@class='publish-time']/text()").extract()[0]
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split("/")[-1]
        content = response.xpath("//div[@class='show-content']").get()


        word_count = response.xpath("//span[@class='wordage']/text()").extract()[0]
        re_wc = re.match(".*?(\d+)", word_count)
        if re_wc:
            word_count = int(re_wc.group(1))

        like_count = response.xpath("//span[@class='likes-count']/text()").extract()[0]
        re_lc = re.match(".*?(\d+)", like_count)
        if re_lc:
            like_count = int(re_lc.group(1))

        read_count = response.xpath("//span[@class='views-count']/text()").extract()[0]
        re_rc = re.match(".*?(\d+)", read_count)
        if re_rc:
            read_count = int(re_rc.group(1))

        comments_count = response.xpath("//span[@class='comments-count']/text()").extract()[0]
        re_cc = re.match(".*?(\d+)", comments_count)
        if re_cc:
            comments_count = int(re_cc.group(1))

        subjects = ",".join(response.xpath("//div[@class='include-collection']/a/div/text()").extract())

        item = ArticleItem(
            title=title,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            origin_url=response.url,
            article_id=article_id,
            content=content,

            word_count=word_count,
            subjects=subjects,
            like_count=like_count,
            read_count=read_count,
            comments_count=comments_count

        )
        yield item


