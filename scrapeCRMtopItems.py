from bs4 import BeautifulSoup
import requests
import time, datetime
import sys, os, csv
from WriteDictToCSV import  WriteDictToCSV
from readPeriodDates import getDatePeriod
from urlBuilder import urlBuilder_CRM_TopItems, urlBuilder_CRM_Login
from authentication import readAuthenticationFile
################################################################################
dataFolder = os.getcwd() + "\Data"
outputFolder = os.getcwd() + "\Output"
################################################################################
def cleanTableFile(text):
    # Clean clustered text from unnecessary entries:
    str_to_remove = ['stlye=', 'span','u0027', 'u003', 'text-align:', 'right','left','center','\\c','\\e', '/','\\','"']
    for string in str_to_remove:
        text = text.replace(string,'')

    text = text.split(":[")[1].split("]}")[0]
    # Returns text in list form. One entry per item
    return text.split('],[')
################################################################################
def getTopItems(topNumber, text):
    topItems = []
    fieldnames = ['Product', 'Price', 'Quantity']

    for j, line in enumerate(text):
        if j < topNumber: # Return Top# Items
            line = line.replace('[','').replace(']','').split(', ') # Clean Text
            # Assigns text entries to categories:
            product = line[2].split('Shop')[1]
            price = line[6]
            quantity = line[7]
            # Adds entries to parsed List:
            topItems.append({field:value for field,value in zip(fieldnames, [product, price, quantity])})
        else:
            break

    return topItems, fieldnames
################################################################################
def scrapeTopItems(numberTopItems):
    payload = readAuthenticationFile('CRM') # Authentication Data
    payload.update({'keepLogin': 1}) # Add Field
    start_date, end_date = getDatePeriod("%Y%m%d")
    data = {}
    with requests.Session() as s:
       url = urlBuilder_CRM_Login() # Logon page
       p = s.post(url, data=payload) # Requests log in
       url = urlBuilder_CRM_TopItems(start_date,end_date)
       response = s.get(url)
       # Gets HMTL page on BS4:
       soup = BeautifulSoup(response.text, "html.parser")
       # Cleans the data returned from the Page:
       topItems, fieldnames = getTopItems(numberTopItems, cleanTableFile(soup.text))

       WriteDictToCSV(outputFolder, 'top{}Items.csv'.format(numberTopItems), fieldnames, topItems)
################################################################################
if __name__ == '__main__':
    numberTopItems = 15;
    scrapeTopItems(numberTopItems)
