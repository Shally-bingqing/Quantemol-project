import scrapy
import os
import sys
sys.path.append('Janaf/mySpider/spiders')
from tools import  write_excel_xls as w2xl
from tools import write_excel_xls_append as a2xl

class janaf(scrapy.Spider):
    #all the element index
    element = ["C", "H", "Ac", "Ag", "Al", "Am", "Ar", "As", "At","Au", 
               "B", "Ba", "Be", "Bi", "Bk", "Br", "Ca", "Cd", "Ce", "Cf", "Cl",
               "Cm", "Co", "Cr", "Cs", "Cu", "D", "Dy", "Er", "Es", "Eu", "F", "Fe",
               "Fm", "Fr", "Ga", "Gd", "Ge", "He", "Hf", "Hg", "Ho", "I", "In", "Ir",
               "K", "Kr", "La", "Li", "Lr", "Lu", "Md", "Mg", "Mn", "Mo", "N", "Na",
               "Nb", "Nd", "Ne", "Ni", "No", "Np", "O", "Os", "P", "Pa", "Pb", "Pd",
               "Pm", "Po", "Pr", "Pt", "Pu", "Ra", "Rb", "Re", "Rh", "Rn", "Ru", "S",
               "Sb", "Sc", "Se", "Si", "Sm", "Sn", "Sr", "T", "Ta", "Tb", "Tc", "Te",
               "Th", "Ti", "Tl", "Tm", "U", "V", "W", "Xe", "Y", "Yb", "Zn", "Zr"]
    # store the attribute title
    # the data must be 2 demensions ,which would be stored
    title=[["Name","Formula","T/K","Cp°","S°"," -[G°-H°(Tr)]/T","H-H°(Tr)", "fH°","fG°","log Kf"]]
    # file path
    path="../dataset/janaf.xls"
    # name of spider & xls sheet
    name="janaf"
    # create & wtrite title into file
    w2xl(path,name,title)
    # the target domains allowed
    allow_domains = ['https://janaf.nist.gov/']
    # urls' common prefix
    prefix = "https://janaf.nist.gov/tables/"
    # urls' common endfix
    endfix = ".html"
    # urls' common connect char
    conn = "-"
    #the collection of the crawling weblink
    start_urls=[]
    #Construct all connections for each element
    for individual  in element:
        #Construct multiple serial number connection, no 000 page
        for i in range(1,999):
            # transfer int in2 string
            no=str(i)
            # fix string's length
            while(len(no)<3):
                #append "0" in the front of the string
                no="0"+no
                pass#while
            #Prefix + element name + - + ordinal of three characters + suffix
            #Verify that if it exists here
            tmp=prefix+individual+conn+no+endfix
            #join the list
            start_urls.append(tmp)
            pass#for i
        pass#for every

    def parse(self,response):
        #obtain the title of text
        #/html/body/p
        p = response.xpath("//p/text()").extract()
        #Determine if it can be crawled
        if p[0].find("not found")!=-1:
            #If there is a word "not found", it means not to crawl
            return
        else:
            #A list of stored values to be written
            value=[]
            #Declare the target value
            target=["298.15"]
            #obtain all lines
            rows = response.xpath("//tr")
            #travesal all lines
            for no,row in enumerate(rows):
                #Get each cell in each row
                everys = row.xpath(".//td")
                #Cache of per line 
                tmp=[]
                #Process each data
                for i,every in enumerate(everys):
                    #Get the value of each data cell
                    each = every.xpath(".//text()").extract()
                    #Get a cache for each row
                    tmp.append(each)
                    #Make a target value judgment on an element
                    pass# everys
                #process each row
                #judge the last element name in the first row is fetched
                #Do a non-null check first
                if tmp!=[]:
                    if no==0:
                        #Splices together the names of the elements
                        Name="".join(tmp[0])
                        value.append(Name)
                        #Splices together symbols of elements
                        Formula=''.join(tmp[-1])
                        value.append(Formula)
                        continue
                    #The non-null check is followed by a check
                    #to see if it matches the value
                    if tmp[0]==target :
                        #fill in a list of single values
                        line=[i for item in tmp for i in item]
                        for i in line:
                            value.append(i)
                            pass#for
                        value=[value]
                        break
                    pass#if tmp
                pass#for
            print("->",value,"<-")
            #store the value
            path="Janaf/mySpider/dataset/janaf.xls"
            #append every loop
            a2xl(path,value)

# scrapy crawl janaf -o ./dataset/janaf.csv