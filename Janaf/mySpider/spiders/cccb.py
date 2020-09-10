import scrapy
from .tools import write_excel_xls as w2xl

class ApiSpider(scrapy.Spider):
    # spider name 
    name = 'cccb'
    # the target domains which allowed
    allowed_domains = ['https://cccbdb.nist.gov/']
    # the list of urls will be scrapied
    start_urls = ['https://cccbdb.nist.gov/pollistx.asp',]
                      
    def parse(self, response): 
        # data will store into Excel file
        #get all the tables in target url
        tables = response.xpath("//table")
        #dataset
        cccb=[]
        #the target table is no.2
        for number, table in enumerate(tables):
            #the no.2 table which store data
            if number ==1:
                # get all the rows in target table
                rows = table.xpath(".//tr")
                # deal with every row in rows we get , which contains all data
                for no,row in enumerate(rows):
                    #tempory to save one line value
                    one=[]
                    if no==0:
                        #the 1st row is ths
                        everys = row.xpath(".//th")
                    else:
                        # get all element data in every row 
                        everys = row.xpath(".//td")
                    #deal with every element data in  one row
                    for i, every in enumerate(everys):
                        #append every value in line
                        one.append(every.xpath("string(.)").extract()[0])
                        pass#for every
                    ##test capture
                    #print("------------",one,"--------------")
                    if one!=[]:
                        #null value check
                        cccb.append(one)
                        pass#if one
                    pass#for everys
                pass#for rows
            pass#for tables
        #file path , here u can choose which type(.csv or .xls) 2 save 
        path ="./dataset/cccb.xls"
        #sheet name
        name="CCCB"
        #write 2 xls file
        w2xl(path,name,cccb)
  
#cmd run this bellow
'''
scrapy crawl cccb
'''