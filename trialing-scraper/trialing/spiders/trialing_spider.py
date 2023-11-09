from typing import Any

import scrapy
from scrapy import Selector
from trialing.items import HospitalItem


class TrialingSpider(scrapy.Spider):
    name = "trialing_talent_spider"
    allowed_domains = ["trialing-talent.s3-website-eu-west-1.amazonaws.com"]
    start_urls = ["http://trialing-talent.s3-website-eu-west-1.amazonaws.com/"]

    def parse(self, response, **kwargs: Any):
        # Predefined DTO
        item = HospitalItem()
        # .card - main selector of each card on HTML page
        for card in response.css('.card'):
            # Extract the ID
            item['hospital_card_id'] = card.xpath('@id').get()
            # Extract the name
            item['name'] = card.css('h5::text').get()

            # Extract the address, ensuring it starts with '<strong>Address:</strong>'
            address_paragraph_html = card.css('.card-body p:contains("Address:")').get()
            address_paragraph = Selector(text=address_paragraph_html)
            address_data = " ".join(address_paragraph.css('::text').extract()).replace('Address:', '').strip()

            # Extract the Google Maps link and parse latitude and longitude
            maps_link = card.css('.card-body a::attr(href)').get()
            item['latitude'], item['longitude'] = maps_link.split('@')[1].split(',')[0:2]

            # Split the address to get country, region, and city
            address_parts = address_data.split(' | ')
            item['address'] = address_parts[0]
            item['region'], item['country'] = address_parts[-1].split(',')[0], address_parts[-1].split(',')[1].strip()
            item['city'] = address_parts[-2]

            # Extract the contact information if available
            phone = card.css('p strong::text').re(r'Phone:\s*(.*)')
            item['contact_data'] = phone[0] if phone else None

            yield item
