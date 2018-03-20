import csv, os
import time, datetime
from getUSDtoBRLexchangeRates import getCurrency
from WriteDictToCSV import  WriteDictToCSV
################################################################################


dataFolder = os.getcwd() + "\Data"
outputFolder = os.getcwd() + "\Output"
filename = ["ESTsoft Inc. - CRM - Daily Unique Purchaser.csv",
            "ESTsoft Inc. - CRM - Daily Unique Visitor.csv",
            "ESTsoft Inc. - CRM - Daily Peak Concurrent User.csv",
            "ESTsoft Inc. - CRM - Daily New Connecting Account.csv",
            "ESTsoft Inc. - CRM - Daily Revenue.csv"]

fieldnames = ["Date",
              "Daily New Connecting Account",
              "Daily Peak Concurrent User",
              "Daily Unique Visitor",
              "Daily Unique Purchaser",
              "Daily Revenue (BRL)"]
currency_txt = "USDBRL Historic  Exchange Rates.txt"


################################################################################
def transformDate(date, option):
    """
    #
    # @param
    # @return
    """
    # Different date formats accepted:
    date_patterns = ["%y%m%d", "%m/%d/%Y","%Y%m%d", "%A, %B %d, %Y", "%Y-%m-%d"]

    for pattern in date_patterns:
        try:
            if option == 1: # From String to String
                return datetime.datetime.strptime(date, pattern).strftime('%A, %B %d, %Y')
            elif option == 2: # From string to datetime
                return datetime.datetime.strptime(date, pattern)
            elif option == 3: # From Datetime to string
                return date.strftime('%A, %B %d, %Y')
        except:
            pass

    print("Date is not in expected format: %s" %(date))
    sys.exit(0)

################################################################################
def calculateNumberDays(data):
    t1 = time.mktime(time.strptime(data[fieldnames[1]][0][-1], '%A, %B %d, %Y'))
    t2 = time.mktime(time.strptime(data[fieldnames[1]][0][0], '%A, %B %d, %Y'))
    return datetime.timedelta(seconds=t2-t1).days
################################################################################
def calculatePercDiff(data_current, data_previous):
    try: # Get percentual difference
        return round(100*(data_current - data_previous)/data_previous,2)
    except: # if missing data, just add an empty cell.
        return []
################################################################################
def safeDivision(num,den):
    try:
        return num/den
    except:
        return []

def roundto(number,digits):
    try:
        return round(number, digits)
    except:
        return []
################################################################################
# Main program
def main():
    rows = []
    data = {}
    list_date = []
    list_entries = []

    for i in range (1,6):
        list_date = []
        list_entries = []
        with open(os.path.join(dataFolder, filename[i-1])) as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                list_date.append(transformDate(line['Date'], 1))
                list_entries.append(line['UserCount'])

        data[fieldnames[i]] = [list_date, list_entries]


    # Total number of days in data. From first entry to last entry
    numberDays = calculateNumberDays(data)

    ## Aggregates results per day on dataframe
    for i in range(0,numberDays+1):
        values = []
        values.append(transformDate(transformDate(data[fieldnames[1]][0][0], 2) - datetime.timedelta(days = i),3))
        for j in range(1,6):
            try: # If no missing data on the day, add row
                values.append(int(data[fieldnames[j]][1][data[fieldnames[j]][0].index(values[0])]))
            except: # If missing data, add empty cell
                values.append([])
        rows.append({field: value for (field, value) in zip(fieldnames,values)})

    ## Pre allocates space for all data to perform operations.
    data_organized =[ [], [], [], [], [], [],
                    numberDays*[None], numberDays*[None], numberDays*[None]
                    ,numberDays*[None],numberDays*[None]]

    # Entries on list are lists of dimension NumberOfDays
        # [[Date],[PU],[VU],[CCU],[DCA],[W%PU],[W%VT],[W%CCU],[W%DCA]]
        # [   0,    1,   2,   3,    4,     5,     6,     7,      8]
    for row in rows:
        for j,key in enumerate(row.keys()):
            data_organized[j].append(row[key])

    # Performs Math operations on lists
    for i in range(1,6):
        index = 0 # Go through the list, from the newest entry to oldest
        while index <= numberDays - 7: # Until it reaches last day on the list
            data_organized[i+5][index] = calculatePercDiff(data_organized[i][index], data_organized[i][index+7])
            index += 1 # Increment Index

    # ## Add new calculated fields to Data Dict
    # fieldnames.extend(('% Change (Week)','WVT','WCCU','WDCA','WR'))
    # k = 0
    # for a,b,c,d,e in zip(*data_organized[6:11]):
    #     rows[k].update({field: value for (field, value) in zip(fieldnames[6:11],[a,b,c,d,e])})
    #     k += 1;

    ## Add Exchange Rates & Financial Calc Fields to Data Dict:
    fieldnames.extend(["Daily Revenue (USD)","ARPPU (USD)","ARPU (USD)","Exchange Rate"])

    with open(os.path.join(dataFolder, currency_txt)) as currencyFile:
        for i, entry in enumerate(currencyFile):
            exg_rate = float(entry.split(' ')[1].split('\n')[0])
            rows[i].update({'Exchange Rate' : exg_rate})
            rows[i].update({'Daily Revenue (USD)' : roundto(rows[i]['Daily Revenue (BRL)']/exg_rate , 2)})
            rows[i].update({'ARPPU (USD)' : roundto(safeDivision(rows[i]['Daily Revenue (USD)'],rows[i]['Daily Unique Purchaser']) , 2)})
            rows[i].update({'ARPU (USD)' : roundto(safeDivision(rows[i]['Daily Revenue (USD)'],rows[i]['Daily Unique Visitor']) , 2)})


    ## Re-Organize Fieldnames:
    fields = [*fieldnames[0:5],*fieldnames[6:9],fieldnames[5],fieldnames[-1]]
    ## Write Dict to output folder
    WriteDictToCSV(outputFolder, 'output.csv', fields, rows)


################################################################################
if __name__ == '__main__':
    main()
