from robobrowser import RoboBrowser
from functools import wraps
from robobrowser.forms import form
from robobrowser.forms.fields import Submit, Input
import sys, os, csv
from WriteDictToCSV import  WriteDictToCSV
from readPeriodDates import getDatePeriod
from urlBuilder import urlBuilder_Billing_statsPeriod
from transformDate import transformDate
################################################################################
dataFolder = os.getcwd() + "\Data"
outputFolder = os.getcwd() + "\Output"
################################################################################
# Class definition to press submit button:
class ImageSubmit(Submit):
    def serialize(self):
        return {self.name + '.x': '0', self.name + '.y': '0'}

def include_image_submit(parse_field):
    @wraps(parse_field)
    def wrapper(tag, tags):
        field = parse_field(tag, tags)
        if type(field) is Input:  # not a subclass, exactly this class
            if field._parsed.get('type') == 'image':
                field = ImageSubmit(field._parsed)
                #print(field._parsed)
        return field
    return wrapper
# This allows button type image to be clicked:
form._parse_field = include_image_submit(form._parse_field)
################################################################################
def authBillingPage():
    # Login page:
    url = urlBuilder_Billing_statsPeriod('Revenue')
    # Authentication:
    username = "alexcampino"
    password = "PIJcig243"
    # Creates Browser object:
    browser = RoboBrowser(history=True, parser='html.parser')
    # Opens Login Page:
    browser.open(url)
    # This retrieves __VIEWSTATE and parsed data:
    signin = browser.get_form(id='form1')
    # Give values to parsed information:
    signin["adminid"].value = username
    signin["pswd"].value = password
    # Login:
    browser.submit_form(signin, 'btnSubmit')
    return browser, url
################################################################################
def getRevenueValues(browser, url, initialDate, finalDate):
    ### Get Values from Revenue:
    # Opens Purchase Period Page:
    browser.open(url)
    signin = browser.get_form(id='form1')
    signin['fromymd'] = initialDate
    signin['toymd'] =  finalDate
    signin['drpSiteCode'] = "ESTBR"
    # Refresh button image submit:
    submit_field = signin['imgSearch']
    submit_field.value = 'imgSearch'
    # Submit Form:
    browser.submit_form(signin, submit=submit_field)
    ## Retrieve values of interest:
    info = browser.parsed # Parses the resulting URL html
    # Information is fetched:
    info = info.find_all('table')[2].find_all('tr')[2:-2]
    dates, revenue = [], []
    for j, entry in enumerate(info):
        value = entry.find_all('td')
        dates.append(transformDate(value[0].text, "%y%m%d"))
        revenue.append(int(value[6].text.replace(',','')))

    return dates, revenue
################################################################################
def getUniquePurchasers(browser, url, initialDate, finalDate):
    ## Get Unique Purchasers function
    url = urlBuilder_Billing_statsPeriod('UniquePurchasers') # Obtain URL
    browser.open(url) # Open URL

    # Assigning values to form:
    signin = browser.get_form(id='form1')
    signin['fromymd'] = initialDate
    signin['toymd'] =  finalDate
    signin['drpSitecode'] = "ESTBR"
    # Refresh button image submit:
    submit_field = signin['imgSearch']
    submit_field.value = 'imgSearch'
    # Submit Form:
    browser.submit_form(signin, submit=submit_field)
    # Retrieve values of interest:
    info = browser.parsed
    # Returns Unique Purchasers Number:
    return info.find_all('table')[3].find_all('font')[2].text

################################################################################
def scrapeBillingData():
    initialDate, finalDate = getDatePeriod("%Y%m%d")

    browser, url = authBillingPage()
    dates, revenue = getRevenueValues(browser, url, initialDate, finalDate)
    uniquePurchasers = getUniquePurchasers(browser, url, initialDate, finalDate)

    print("Number of Unique Purchasers in this Period is: {}".format(uniquePurchasers))

    ###############################################################################
    # Write data to file:
    rows = []
    fieldnames = ['date', 'Revenue (BRL)']
    for date, dailyRevenue in zip(dates,revenue):
        rows.append({field: value for (field, value) in zip(fieldnames,[date,dailyRevenue])})

    WriteDictToCSV(outputFolder, 'weeklyRevenue.csv', fieldnames, rows)
################################################################################
if __name__ == '__main__':
    scrapeBillingData()
