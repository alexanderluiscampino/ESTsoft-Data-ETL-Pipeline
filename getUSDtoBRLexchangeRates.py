import json, urllib.request
import time, datetime
import sys

def transformDate(s_date):
    """
    #
    # @param
    # @return
    """
    date_patterns = ["%y%m%d", "%m/%d/%Y","%Y%m%d", "%A, %B %d, %Y", "%Y-%m-%d"]
    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(s_date, pattern).strftime('%Y-%m-%d')
        except:
            pass

    print("Date is not in expected format: %s" %(date))
    sys.exit(0)

def getCurrency(date):
    urlExchange = ("https://api.fixer.io/{}?base=USD".format(date))
    with urllib.request.urlopen(urlExchange) as url:
        info = json.loads(url.read())
        return info["rates"]["BRL"]

def functionCallCurrency(dates):
    """
    #
    # @param
    # @return
    """
    currency_values = []
    num_request = 1 # To limit HTTPs requests
    for date in dates:
        currency_values.append(getCurrency(transformDate(date)))
        if num_request == 60: # Avoid HTTPs request deny due to Spam
            time.sleep(120) # Rest for 120seconds before another HTTP request
            num_request = 0 # Reset Requests Number
        num_request += 1
    return currency_values

def main():
    date = ["2018-02-28","2018-02-27"]
    print(functionCallCurrency(date))
################################################################################
if __name__ == '__main__':
    main()
