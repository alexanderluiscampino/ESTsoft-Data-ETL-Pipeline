import sys, os, csv

def WriteDictToCSV(outputFolder, outputfile, fieldnames, dict_data):
    """
    #
    # @param
    # @return
    """
    try:
        with open(os.path.join(outputFolder, outputfile), 'w+') as outputcsv:
            writer = csv.DictWriter(outputcsv, delimiter=',',
                                               lineterminator='\n',
                                               fieldnames=fieldnames)
            writer.writeheader()
            for entry in dict_data:
                writer.writerow(entry)
    #except IOError as (errno, strerror):
    except IOError as err:
            print("I/O error({0}): {1}".format(errno, strerror))
    return

if __name__ == '__main__':
    WriteDictToCSV(outputFolder, outputfile, fieldnames, dict_data)
