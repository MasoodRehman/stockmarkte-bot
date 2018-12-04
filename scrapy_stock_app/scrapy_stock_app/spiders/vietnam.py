# -*- coding: utf-8 -*-
import scrapy
import json, re
from scrapy_stock_app.items import VietnamItem

class VietnamSpider(scrapy.Spider):
    name = 'vietnam'
    allowed_domains = ['stock.vietnammarkets.com']
    start_urls = ['http://stock.vietnammarkets.com/vietnam-stock-market.php']

    def parse(self, response):
        rows = response.css('#VNMC_contentinner .fullbox .results tr:nth-child(n+2)')
        for row in rows:
            item = VietnamItem()
            item['ticker_symbol'] = row.css('td:nth-child(1) a::text').extract_first()
            item['business'] = row.css('td:nth-child(3) ::text').extract_first()
            item['listing_bourse'] = row.css('td:nth-child(4) ::text').extract_first()
            item['company_name'] = row.css('td:nth-child(2) ::text').extract_first()
            item['company_url'] = row.css('td:nth-child(1) a::attr(href)').extract_first()
            item['country'] = "Vietnam"
            yield scrapy.Request(
                item['company_url'],
                callback = self.company_detail, 
                meta = {
                    'item': item
                },
                dont_filter = True
            )
    
    def company_detail(self, response):
        company_profile = response.css('#VNMC_contentinner .fullbox .inner .results table:first-of-type tr:nth-child(1)>td:first-child')[0]
        company_profile_tokens = company_profile.css('td::text').extract()
        
        item = response.meta.get('item')

        # item['company_name'] = ' '.join(company_profile_tokens[0].split())
        item['company_street_address'] = ' '.join(company_profile_tokens[1].split())
        
        company_phone_number = list()
        company_phone_number.append(' '.join(company_profile_tokens[2].split()))
        company_phone_number.append(' '.join(company_profile_tokens[3].split()))
        item['company_phone_number'] = json.dumps(company_phone_number)
        
        item['company_email'] = ' '.join(company_profile_tokens[4].split())
        item['company_website'] = ' '.join(company_profile_tokens[5].split())
        # item['business'] = ' '.join(company_profile_tokens[6].split())
        
        financial_summary = dict()
        financial_summary_rows = response.css('#VNMC_contentinner .fullbox .inner .results table:first-of-type table tr')
        for row in financial_summary_rows:
            key = row.css('td:nth-child(1) ::text').extract_first()
            value = row.css('td:nth-child(2) ::text').extract_first()
            financial_summary[key] = value.strip(':')
        item['financial_summary'] = json.dumps(financial_summary)
        
        business_summary = response.css('#VNMC_contentinner .fullbox .inner .results table:nth-of-type(1)  tr:nth-of-type(2)')[1]
        business_summary_raw_tokens = business_summary.css('td ::text').extract()
        data_list = filter(None, [ ' '.join(raw_token.split()) for raw_token in business_summary_raw_tokens ])
        company_description = list()
        append_summary = True
        for data in data_list:
            result = re.match(r'^Auditing Company:', data)
            if result is None and append_summary:
                company_description.append(data)
            elif append_summary:
                append_summary = False
                auditing_company_index = data_list.index(data)
                item['auditing_company'] = data_list[auditing_company_index + 1]

            result = re.match(r'^Address:(.+)', data)
            if result:
                item['company_street_address'] = result.group(1)

            business_registration = dict()    
            result = re.match(r'^Established License:(.+)', data)
            if result:
                business_registration['establish_license'] = result.group(1)
            result = re.match(r'^Business License:(.+)', data)
            if result:
                business_registration['business_license'] = result.group(1)
            item['business_registration'] = json.dumps(business_registration)
        item['company_description'] = ' '.join(company_description)

        return item
