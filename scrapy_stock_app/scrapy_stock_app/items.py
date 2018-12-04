# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VietnamItem(scrapy.Item):
    # define the fields for your item here:
    ticker_symbol = scrapy.Field()
    business = scrapy.Field()
    listing_bourse = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_street_address = scrapy.Field()
    country = scrapy.Field()
    company_description = scrapy.Field()
    company_phone_number = scrapy.Field()
    company_website = scrapy.Field()
    company_email = scrapy.Field()
    financial_summary = scrapy.Field()
    business_registration = scrapy.Field()
    auditing_company = scrapy.Field()
    crawled_at = scrapy.Field()
