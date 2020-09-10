# coding=UTF-8
import xlrd
import xlwt
from xlutils.copy import copy  # Modify (append write)：xlutils
import os

##ref 
# https://blog.csdn.net/u013250071/article/details/81911434

def write_excel_xls(path, sheet_name, value):
    index = len(value)  # Gets the number of rows to write to
    workbook = xlwt.Workbook()  # Create a new workbook
    sheet = workbook.add_sheet(sheet_name)  # Create a new table in the workbook
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # Writes data to the table (corresponding rows and columns)
    workbook.save(path)  # save the workbook
    print("Table in xls format writes data successfully！")
 
 
def write_excel_xls_append(path, value):
    index = len(value)  # Gets the number of rows to write to
    workbook = xlrd.open_workbook(path)  # open the workbook
    sheets = workbook.sheet_names()  # obtain all tables in the workbook
    worksheet = workbook.sheet_by_name(sheets[0])  # obtain the first table in the workbook
    rows_old = worksheet.nrows  # obtain the number of rows in the table which alreafy have the data
    new_workbook = copy(workbook)  # copy the xlrd object and convert it to xlwt object
    new_worksheet = new_workbook.get_sheet(0)  # obtain the first converted table in the workbook
    for i in range(0, index):
        for j in range(0, len(value[i])): # Appends the write data,
            new_worksheet.write(i+rows_old, j, value[i][j])  #noting that the write starts with the 'i +rows_old' line
    new_workbook.save(path)  # save the workbook
    print("XLS format table [append] writes data successfully！")
 
 
def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # open the workbook
    sheets = workbook.sheet_names()  # get all tables in the workbook
    worksheet = workbook.sheet_by_name(sheets[0])  # obtain the first table in the workbook
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # read the data row by row, column by column
        print()

def checkFile(filePath,fileName):
    #Gets all file names under the file path
    allFileName = os.listdir(filePath)
    fileState = False
    #Under the specified path, determines whether the specified file exists
    for file in allFileName:
    #Output all files and folders
    #print("existFile:==>",file)
        if file == fileName:
            #print("file:",file)
            #print("fileName:",fileName)
            fileState = True
            break
    return fileState
