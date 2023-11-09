import scrapy


class HospitalItem(scrapy.Item):
    """
    HospitalItem used as a DTO to define structure of parsed data
    """
    hospital_card_id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    contact_data = scrapy.Field()
