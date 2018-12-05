# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import json, re


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
    revenue = scrapy.Field()
    business_registration = scrapy.Field()
    auditing_company = scrapy.Field()
    crawled_at = scrapy.Field()

    def getStreetAddress(self, data):
        return ' '.join(data[1].split())

    def getPhoneNumber(self, data):
        company_phone_number = list()
        company_phone_number.append(' '.join(data[2].split()))
        company_phone_number.append(' '.join(data[3].split()))
        return json.dumps(company_phone_number)

    def getEmail(self, data):
        return ' '.join(data[4].split())

    def getWebsite(self, data):
        return ' '.join(data[5].split())

    def getFinancialSummary(self, data):
        financial_summary = dict()
        for row in data:
            key = row.css('td:nth-child(1) ::text').extract_first()
            key = key.replace(' ', '_').lower().strip(':')
            financial_summary[key] = row.css('td:nth-child(2) ::text').extract_first()
        return financial_summary

    def getCompanyDetailDict(self, data):
        company_detail_dict = dict()
        data_list = list(filter(None, [ ' '.join(raw_token.split()) for raw_token in data ]))
        company_description = list()
        append_summary = True
        for data in data_list:
            result = re.match(r'^Auditing Company:', data)
            if result is None and append_summary:
                company_description.append(data)
            elif append_summary:
                append_summary = False
                auditing_company_index = data_list.index(data)
                company_detail_dict['auditing_company'] = data_list[auditing_company_index + 1]

            result = re.match(r'^Address:(.+)', data)
            if result:
                company_detail_dict['company_street_address'] = result.group(1)

            business_registration = dict()    
            result = re.match(r'^Established License:(.+)', data)
            if result:
                business_registration['establish_license'] = result.group(1)
            result = re.match(r'^Business License:(.+)', data)
            if result:
                business_registration['business_license'] = result.group(1)
            company_detail_dict['business_registration'] = json.dumps(business_registration)
        company_detail_dict['company_description'] = ' '.join(company_description)
        return company_detail_dict
