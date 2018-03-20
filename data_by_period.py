import sys, os, csv
import time, datetime
from WriteDictToCSV import  WriteDictToCSV
from getUSDtoBRLexchangeRates import functionCallCurrency
from transformDate import transformDate
from scrapeCRMpage import scrapeCRMdata
from scrapeBillingPage import scrapeBillingData
from scrapeCRMtopItems import scrapeTopItems

dataFolder = os.getcwd() + "\Data"
outputFolder = os.getcwd() + "\Output"
outputfile = 'weeklyData.csv'
# Main program
def main(numberTopItems):
    print("\n******** Routine is Now Running ********\n")
    print("******** Scraping Billing Page Data ********\n")
    scrapeBillingData()

    print("******** Scraping CRM Page Data ********\n")
    scrapeCRMdata()

    print("******** Scraping Top {} Items ********\n".format(numberTopItems))
    scrapeTopItems(numberTopItems)

    print("\n******** All Info is Now gathered ********\n")
    data = []

    with open(os.path.join(outputFolder,"weeklyCRMData.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            data.append(line)

    with open(os.path.join(outputFolder,"weeklyRevenue.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for i,line in enumerate(reader):
            exchangeRate = functionCallCurrency([line['date']])[0]
            data[i].update({'Revenue (USD)' : round(float(line['Revenue (BRL)'])/exchangeRate, 2) })
            data[i].update(line)
            data[i].update({'Exchange Rate' : exchangeRate })
            data[i].update({'date' : transformDate(line['date'], "%A, %B %d, %Y") })


    # Write Final File:
    WriteDictToCSV(outputFolder, outputfile, list(data[0].keys()) , data)
    # Remove Extra Files:
    os.remove(os.path.join(outputFolder,"weeklyCRMData.csv"))
    os.remove(os.path.join(outputFolder,"weeklyRevenue.csv"))

    print("******** Please Find All Information on File: {} and top{}Items.csv********\n".format(outputfile,numberTopItems))
################################################################################
if __name__ == '__main__':
    numberTopItems = 10
    main(numberTopItems)
