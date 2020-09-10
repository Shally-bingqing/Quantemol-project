import scrapy
from .tools import write_excel_xls_append as a2xl
from .tools import write_excel_xls as w2xl
from ..items import Nist

class NistSpider(scrapy.Spider):
    #contruct the urls of crawling
    name = 'nist'
    start_urls = ['https://webbook.nist.gov/cgi/formula/',]
    prefix="https://webbook.nist.gov"
    output=[]
    next_url=[]

    #definition for getting all urls of species page
    def parse(self, response):
        #create a list for writting the url
        urls=[]
        #obtain the Xpath of each species
        items=response.xpath('//*[@id="main"]//ul//li')
        #get the url of each species information page
        for no,item in enumerate(items):
            element=item.xpath("string(.)").extract_first()
            url=self.prefix+item.xpath("./a/@href").extract_first()
           #collect the urls if can't find "species" in the Xpath
            if element.find("species")!=-1:
                self.next_url.append(url)
            else:#transfer the urls of information pages to "idea_parse" function
                yield scrapy.Request(url,callback=self.idea_parse)
        if self.next_url!=[]:#traverse the collection of non-information pages' urls 
            for i in self.next_url:#get all urls from the collection
                url=i
                self.next_url.remove(url)
                yield scrapy.Request(url,callback=self.parse)

    def idea_parse(self, response):
        #go to the page of each urls
        items=response.xpath('//*[@id="main"]//ul//li')
        for no,item in enumerate(items):#traverse the text part of the web page
            tmp=item.xpath("./strong/text()").extract_first()
            if  tmp!=None and tmp.find("Other data")!=-1:
                eachs = item.xpath(".//li")#get the url when the page has "other data"
                for each in eachs:#get new text part
                    temp=each.xpath("./a/text()").extract_first()
                    #obtain the final urls when find the "ion energetics"
                    if temp!=None and temp.find("ion energetics")!=-1:
                        url=self.prefix+each.xpath("./a/@href").extract_first()
                        #get the final urls and transfer them to "data_parse" function
                        yield scrapy.Request(url,callback=self.data_parse)
    
    #function for getting each species' IE value
    def data_parse(self, response):
        data=[]
        y=Nist()
        items= response.xpath("//table")#get the Xpath of table
        for no,item in enumerate(items):
            tmp=item.xpath("./@aria-label").extract_first()
            if tmp !=None and tmp.find("Ionization energy")!=-1:
                eachs=item.xpath(".//tr")
                for nu,each in enumerate(eachs):
                    if nu==1:
                        everys= each.xpath(".//td")
                        tmp=[]
                        for every in everys:
                            text=every.xpath("./text()").extract_first()
                            if text!=None:
                                tmp.append(text)
                            else:
                                text=every.xpath("./a/text()").extract_first()
                                if text != None:
                                    tmp.append(text)
                                else:
                                    text= every.xpath("./em/text()").extract_first()
                                    tmp.append(text)
                        #obtain the data from each cell
                        if len(tmp)>0:
                            y['IE'] = tmp[0]
                        if len(tmp)>1:
                            y['Method']=tmp[1]
                        if len(tmp)>2:
                            y['Refer']=tmp[2]
                        if len(tmp)>3:
                            y['Comment']=tmp[3]
                        if y['IE']!="":
                            y['Name']=response.xpath('//*[@id="Top"]/text()').extract_first()
                            items= response.xpath('//*[@id="main"]//ul//li')
                            #get the foemula and CAS NO. of each species
                            for no,item in enumerate(items):
                                tmp=item.xpath("./strong/text()").extract_first()
                                if no==0:
                                    y['Formula']=item.xpath("./text()").extract_first()
                                if tmp!=None and tmp.find("CAS")!=-1:
                                    y['CAS']=item.xpath("./text()").extract_first()
                        yield y