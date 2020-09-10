import csv
from tools import  write_excel_xls as w2xl
import os
import pandas

#definition to judge the head
#Consider deleting the head directly 
#by looking if it has key word during traversal
def isHead(x,key):
    #if find key word
    if x.find(key)!=-1:
        #if find
        return True
        pass#if
    else:
        return False
        pass#else
    pass#def

#make each line as a single element
#calculate the length of the expression page number string
#whether <3 or not
def isTail(x,length):
    #get the length of string
    if len(x)<=length:
        #if it's less than the desired length
        return True
        pass #if
    else:
        return False
        pass#else
    pass#else

#Join all the columns into one column
def connect(list):
    y=""
    for i in list:
        y+=i
        pass#for
    return [y]
    pass#def connect

#To determine the element information row
#look for both ( and ) in a row
def isTitle(x,key):
    y=0
    for i in key:
        #if find 
        if x.find(i)!=-1:
            #then add 1
            y=y+1
            pass#if
        pass#for
    #if can't find both ( and )
    if y<len(key):
        #then it's not the element information row
        return False
        pass#if
    else:
        return True
        pass#else
    pass#def 

'''
Processing each row, since each row is a scientific count,
But they are signed numbers, which means that every number is preceded by either a minus sign,
Or not. So we starting with scientific counting,
The scientific count of E is always followed by three, the first symbol,
The last two digits of each line represent the count, and the last character of each line is the line number,
We can choose to abandon it or leave it at the end
'''
def separation(x,char):
    #save the result
    y=[]
    #get rid of the last data
    tail=x[-1]
    #from the original
    x=x[:-2]
    #delete all blank spaces first
    x=x.replace(" ","")
    #drop all the newline symbols
    x=x.replace("\t","")
    while(len(x)>3):
        #split it by looking
        #print("x:",x)
        if x.index(char)!=-1:
            #the last three digits of E represent the end of a number
            y.append([x[:x.index(char)+4]])
            #print("y:",y)
            #Subtract the value of the added result
            x=x[x.index(char)+4:]
            pass #if
        else:
            if len(x)<3:
                break
        pass #while
    y.append([tail])
    return y
    pass#def

def read(path,name):
    #Record the number of pages and processing
    flag=0
    record=[]
    page=[]
    filepath = path + name
    #Open the file as read-only
    with open(filepath,'r') as f:
        #Converts the file to a CSV reader object
        reader = csv.reader(f)
        #Turn the data into a 2-dimensional list
        data = list(reader)
        #Store the formatted data
        y=[]
        #get each line
        for no, i in enumerate(data):
            #print each line
            print(no,":",i)
            
            #first, combine all the rows into one column
            tmp=connect(i)
            #Second, judge whether it is a title
            #print("************",flag,":",record,"**********")
            if isHead(tmp[0],"THERMODYNAMIC"):
                #If so, write the start tag
                if flag==0 or len(record)<=flag:
                    record.append(no)
                    pass
                else:
                    record[flag]=no
                    pass
                continue
            #Determine if it is a subheading
            if isHead(tmp[0],"CETPC"):
                if flag==0 or len(record)<=flag:
                    record.append(no)
                    pass
                else:
                    record[flag]=no
                    pass
                continue
            #Determine if it is a page number
            if isTail(tmp[0],3):
                #record the page number
                page.append(tmp[0])
                #The beginning and end of a page may have no title, 
                #but the page number
                if record[flag]!="" and record!=[]:
                    #Subtracting the current page number coordinates 
                    #from the latest title coordinates
                    #it is the number of processes
                    record[flag]=no-record[flag]
                    pass#if record
                else:
                    #Records a page that processes the current
                    record[flag]=no
                    pass#else
                #Then proceed to the processing record on the next page
                flag=flag+1
                continue
            mark=["(",")"]
            #Determines whether it is the title of the element
            if isTitle(tmp[0],mark):
                #Divide the header elements by spacing
                tmp=tmp[0].replace(" ",'\t').split("\t")
                #There's an empty element in there that needs to be replaced
                for i in tmp:
                    #Is null or is a newline
                    if i==" " or i=="":
                        #delete the element
                        tmp.remove(i)
                        pass#if
                    pass#for
                #The small problem is that the second partition value may stick to the third
                if len(tmp[1])>4:
                    #Determine if each character is a number
                    for i in tmp[1]:
                        #if it's a number
                        if i.isdigit():
                            #Returns the index of the character if it is
                            separatrix=tmp[1].index(i)
                            #Divide by bounds
                            #Get the first half
                            second=tmp[1][:separatrix]#J
                            #get the second half
                            third=tmp[1][separatrix:]
                            #refill
                            tmp[1]=second
                            tmp.insert(2,third)
                            break
                        pass#for
                    pass#for
                #write into the result
                y.append(tmp)
                continue
            else:
                #To the exclusion of all other possibilities, non-element titles are data
                y.append(separation(tmp[0],"E"))
            pass#for no
        pass#with
    #write the output into the file
    save_path = 'Janaf/mySpider/dataset/output_49-51.xls'
    sheet_name="NASA_poly"
    return w2xl(save_path,sheet_name,y)

if __name__ =="__main__":
    # #test isTail
    # x="TABLE II. - THERMODYNAMIC DATA COEFFICIENTS"
    # key="TABLE"
    # print(isHead(x,key))
    # x = "10"
    # length=3
    # print(isTail(x,length))
   #l=["ZrN(L)	J 6/61ZR	l.N	1.	0.	0.C	3225.000	5000.000	106","23074	1"]
   #print(connect(l))
   #l=['ZrN(L)\tJ 6/61ZR\tl.N\t1.\t0.\t0.C\t3225.000\t5000.000\t10623074\t1']
   #key=["(",")"]
   #print(isTitle(l[0],key))
   #x=["0.00000000E+00 0.00000000E+00-7.45375000E+02-1.17208122E+01 0.00000000E+00	4"]
    #x=["-1.284274B0E+05-5.45922640E+01 1.05676750E+01	0.00000000E+00	0.00000000E-f00	3"]
    #x=["0.00000000E+00 0.00000000E+00-1.28427450E+05-5.45922640E+01 0.00000000E-(-00	4"]
    #char="E"
    #print(x[0].index(char))
    #print(separation(x[0],char))
    
    #name = get_filename(csvdir)
    path='Janaf/mySpider/spiders/source_data/'
    #the name of file
    name='NASA_poly49-51.csv'
    read(path,name)