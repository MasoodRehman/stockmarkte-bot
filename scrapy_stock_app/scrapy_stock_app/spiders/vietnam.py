# -*- coding: utf-8 -*-
import scrapy
import json, re
from scrapy_stock_app.items import VietnamItem

class VietnamSpider(scrapy.Spider):
    name = 'vietnam'
    allowed_domains = ['stock.vietnammarkets.com']
    start_urls = ['http://stock.vietnammarkets.com/vietnam-stock-market.php']

    def parse(self, response):
        """
        Main parser method.
        =============================================
        This is the parsing method that called by default by scrapy framework for process the response 
        return by the start_url page.
        
        Contract that check the following constraints of the current callback method.

        url: 
            sets the sample url used when checking other contract conditions for this spider. 
            This contract is mandatory. All callbacks lacking this contract are ignored when running the checks.
        
        return: 
            sets lower and upper bounds for the items and requests returned by the spider. 
            The upper bound is optional
        
        scrapes: 
            checks that all the items returned by the callback have the specified fields. This contract is now
            override with our custom contract called `itemAttributesCheck` so that we can send an email if our 
            custom contract become failed.
        
        @url http://stock.vietnammarkets.com/vietnam-stock-market.php
        @returns items 0
        @returns requests 0
        @itemAttributesCheck ticker_symbol business listing_bourse company_name company_url
        """
        rows = response.css('#VNMC_contentinner .fullbox .results tr:nth-child(n+2)')
        for row in rows:
            # Load item object
            item = VietnamItem()
            
            # Feed data to item parameters
            item['ticker_symbol'] = row.css('td:nth-child(1) a::text').extract_first()
            item['business'] = row.css('td:nth-child(3) ::text').extract_first()
            item['listing_bourse'] = row.css('td:nth-child(4) ::text').extract_first()
            item['company_name'] = row.css('td:nth-child(2) ::text').extract_first()
            item['company_url'] = row.css('td:nth-child(1) a::attr(href)').extract_first()
            item['country'] = "Vietnam"

            # Nested request to company detail page and parse the response data into seperate method.
            # Pass the response and the item object so we can fill the remaining parameters by the response
            # return from the company detail page, that's way we will get whole company data from two different pages
            # with in a single iteration.
            yield scrapy.Request(
                item['company_url'],
                callback = self.company_detail, 
                meta = {
                    'item': item
                },
                dont_filter = True
            )
    
    def company_detail(self, response):
        """
        Company detail page parser
        =============================================
        This is the parsing method that parse compnay details page. The main parsing method collect data from the start url and then 
        for each company url which is collected by that inital page a new request called for each company detail page and pass the 
        response to this `company_detail` method for parsing the detail page response and collect data for the remaining item parameters 
        and return it to the yield which pass the item to the item pipeline class for storing into data store in our case it is json file.
        """
        company_profile = response.css('#VNMC_contentinner .fullbox .inner .results table:first-of-type tr:nth-child(1)>td:first-child')[0]
        company_profile_tokens = company_profile.css('td::text').extract()
        financial_summary_rows = response.css('#VNMC_contentinner .fullbox .inner .results table:first-of-type table tr')

        # get item object which passed by parsing method for feeding the remaining parameters.
        item = response.meta.get('item')

        item['company_street_address'] = item.getStreetAddress(company_profile_tokens)
        item['company_phone_number'] = item.getPhoneNumber(company_profile_tokens)
        item['company_email'] = item.getEmail(company_profile_tokens)
        item['company_website'] = item.getWebsite(company_profile_tokens)
        # Finanical summary parameters
        financial_summary = item.getFinancialSummary(financial_summary_rows)
        item['revenue'] = financial_summary.get('market_cap')
        item['financial_summary'] = json.dumps(financial_summary)
        # Business summary parameters
        business_summary = response.css('#VNMC_contentinner .fullbox .inner .results table:nth-of-type(1)  tr:nth-of-type(2)')[1]
        business_summary_raw_tokens = business_summary.css('td ::text').extract()
        company_detail_dict = item.getCompanyDetailDict(business_summary_raw_tokens)
        item['auditing_company'] = company_detail_dict.get('auditing_company')
        item['company_street_address'] = company_detail_dict.get('company_street_address')
        item['business_registration'] = company_detail_dict.get('business_registration')
        item['company_description'] = company_detail_dict.get('company_description')

        return item
