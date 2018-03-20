from WriteDictToCSV import  WriteDictToCSV
import os
################################################################################
dataFolder = os.getcwd() + "\Data"
outputFolder = os.getcwd() + "\Output"

def getTopItems(topNumber, text):
    topItems = []
    fieldnames = ['Product', 'Price', 'Quantity']

    for j, line in enumerate(text):
        if j < topNumber:
            line = line.replace('[','').replace(']','').split(', ')
            product = line[2].split('Shop')[1]
            price = line[6]
            quantity = line[7]
            topItems.append({field:value for field,value in zip(fieldnames, [product, price, quantity])})
        else:
            break


    WriteDictToCSV(outputFolder, 'topItems.csv', fieldnames, topItems)
################################################################################
if __name__ == '__main__':
    with open('content.txt') as textFile:
        for line in textFile:
            text = line
    text = text.split('],[')

    getTopItems(10, text)
