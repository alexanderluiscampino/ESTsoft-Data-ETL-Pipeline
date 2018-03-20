import os, sys
import time, datetime
cwd = os.getcwd()
filename = "period.txt"
from transformDate import transformDate

def getDatePeriod(reqPattern):
    with open(os.path.join(cwd, filename)) as periodFile:
        for line in periodFile:
            if line.find('##') == -1: #if it is not a comment line
                if line.find('InitialDate') > -1: # Initial Date
                    initialDate = line.split(':')[1].split('\n')[0].replace(" ", "")
                elif line.find('FinalDate') > -1: # Final Date
                    finalDate = line.split(':')[1].split('\n')[0].replace(" ", "")

    return transformDate(initialDate, reqPattern), transformDate(finalDate, reqPattern)

if __name__ == '__main__':
    print(getDatePeriod())
