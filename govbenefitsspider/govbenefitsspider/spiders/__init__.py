# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
# from govbenefitsspider.items import BenefitProgramItem
# from govbenefitsspider.items import BenefitProgramDetail


# Scraper to save the entire response to a file
class BenefitProgramSpider(scrapy.Spider):
    name = "benefitprograms"
    allowed_domains = ["benefits.gov"]
    start_urls = [
        "http://www.benefits.gov/benefits/browse-by-category/category/FOO",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)


# Scraper to grab only the listing page
# class BenefitProgramSpider(scrapy.Spider):
#     name = "benefitprograms"
#     allowed_domains = ["benefits.gov"]
#     start_urls = [
#         "http://www.benefits.gov/benefits/browse-by-category/category/FOO",
#     ]

#     def parse(self, response):
#         # filename = response.url.split("/")[-2]
#         # with open(filename, 'wb') as f:
#         #     f.write(response.body)

#         for sel in response.xpath('//div[@class="top"]'):
#             item = BenefitProgramItem()
            
#             item['title'] = sel.xpath(
#                 'span[@class="benefit-header"]/a/text()').extract()

#             item['details_link'] = sel.xpath(
#                 'span[@class="benefit-header"]/a/@href').extract()

#             item['description'] = sel.xpath(
#                 'span[@class="benefit-description hidden-phone"]/text()').extract()
            
#             yield item


# Full on looping spider
# class BenefitProgramSpider(scrapy.Spider):
#     name = "benefitprograms"
#     allowed_domains = ["benefits.gov"]
#     start_urls = [
#         "http://www.benefits.gov/benefits/browse-by-category/category/FOO",
#     ]

#     def parse(self, response):
#         for href in response.css("span.benefit-header > a::attr('href')"):
#             url = response.urljoin(href.extract())
#             yield scrapy.Request(url, callback=self.parse_dir_contents)

#     def parse_dir_contents(self, response):
#         item = BenefitProgramDetail()
#         item['title'] = response.xpath(
#             '//div[@class="span8 benefit-detail-title"]/text()').extract()
#         item['agency'] = response.xpath(
#             '//div[@class="span4 benefit-detail-agency"]/span[2]/text()').extract()
#         item['state_link'] = response.xpath(
#             '//div[@class="span4 benefit-detail-agency"]/span[3]/a/@href').extract()
#         yield item
