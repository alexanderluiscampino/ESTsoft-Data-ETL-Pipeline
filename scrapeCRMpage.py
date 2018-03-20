from bs4 import BeautifulSoup
import requests
import time, datetime
from datetime import datetime
import sys, os, csv
from WriteDictToCSV import  WriteDictToCSV
from readPeriodDates import getDatePeriod
from authentication import readAuthenticationFile
from urlBuilder import urlBuilder_CRM_Login, urlBuilder_CRM_MetricCounts
################################################################################
dataFolder = os.getcwd() + "\Data"
outputFolder = os.getcwd() + "\Output"
################################################################################
def calculateNumberDays(start_date,end_date):
    # Different date formats accepted:
    date_patterns = ["%Y%m%d", "%y%m%d", "%m/%d/%Y","%Y%m%d", "%A, %B %d, %Y", "%Y-%m-%d"]
    for pattern in date_patterns:
        try:
            d1 = datetime.strptime(start_date, pattern)
            d2 = datetime.strptime(end_date, pattern)
            return abs((d2 - d1).days)
        except:# Exception as e: print(e)
            pass
################################################################################
def scrapeCRMdata():
    payload = readAuthenticationFile('CRM') # Authentication Data
    payload.update({'keepLogin': 1}) # Add Field
    # Metrics to Retrieve from CRM:
    metric_type = ["DailyNewConnectedAccount",
                   "PeakConcurrentUser",
                   "DailyUniqueVisitor",
                   "DailyUniquePurchaser"]

    start_date, end_date = getDatePeriod("%Y%m%d")
    data = {}
    with requests.Session() as s:
        url = urlBuilder_CRM_Login() # Logon page
        p = s.post(url, data=payload) # Requests log in
        # Metric URL:
        for metric in metric_type:
            url = urlBuilder_CRM_MetricCounts(start_date, end_date, metric)
            response = s.get(url)
            # Gets HMTL page on BS4
            soup = BeautifulSoup(response.text, "html.parser")

            # Looks for information within 'script' tag on position 39
            info = soup.findAll('script')[39].string
            # Initiate Variables
            date, count = [],[]
            for entry in info[info.find("[")+1:info.find("]")].split('},{'):
                date.append(entry.split('"')[1::2][0])
                count.append(int(entry.split('UserCount : ')[1].split('}')[0]))


            data.update({metric : {'date': date, 'count':count}})
            date, count = [],[]

    numberDays = calculateNumberDays(start_date,end_date) + 1
    values = []
    rows = []
    for i in range(0, numberDays):
        for metric in metric_type:
            values.append(data[metric]['count'][i])
        rows.append({'date': data[metric]['date'][i]})
        rows[i].update({field: value for (field, value) in zip(metric_type,values)})
        values = []


    metric_type.insert(0,'date')

    WriteDictToCSV(outputFolder, 'weeklyCRMData.csv', metric_type, rows)
################################################################################
if __name__ == '__main__':
    scrapeCRMdata()
