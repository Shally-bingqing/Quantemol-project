import scrapy

# /html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody
#/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[7]/td/table
##s1n2c0\ i1\ CAS1333-74-0
#
class ApiSpider(scrapy.Spider):
    name = 'atct'
    allowed_domains = ['atct.anl.gov/']
    start_urls = ['https://atct.anl.gov/Thermochemical%20Data/version%201.122g/index.php',]

    def parse(self, response):
        print("-------------")
        items=response.xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody//tr")
        for no,item in enumerate(items):
            print(items.xpath("/@id").extract_first())

#


