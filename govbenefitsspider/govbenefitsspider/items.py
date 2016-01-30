# -*- coding: utf-8 -*-

import scrapy


class BenefitProgramItem(scrapy.Item):
    title = scrapy.Field()
    details_link = scrapy.Field()
    description = scrapy.Field()


class BenefitProgramDetail(scrapy.Item):
    title = scrapy.Field()
    agency = scrapy.Field()
    state_link = scrapy.Field()
