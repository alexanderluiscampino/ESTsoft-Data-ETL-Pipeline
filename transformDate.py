import datetime
import sys

def transformDate(s_date, outputPattern):
    """
    # Receives the patterm required for output and the date read from file.
    # Returns de date on the required pattern
    # @param S_date -> Date in string formats
    #        outputPattern -> output pattern desired
    # @return date in the required format
    """
    # Different date formats accepted:
    date_patterns = ["%y%m%d", "%m/%d/%Y","%Y%m%d", "%A, %B %d, %Y", "%Y-%m-%d"]

    for pattern in date_patterns:
        try:
            return datetime.datetime.strptime(s_date, pattern).strftime(outputPattern)
        except: # Exception as e:
            pass #print(e)

    print("Date is not in expected format: %s" %(date))
    sys.exit(0)


if __name__ == '__main__':
    exampleDate = '20180315'
    exmaplePattern = '%A, %B %d, %Y'
    print(transformDate(exampleDate, exmaplePattern))
