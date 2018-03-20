import os, sys
cwd = os.getcwd()

def readAuthenticationFile(page):
    """
    # Reads Authentication data from file authenticate.txt
    # params: @page - website to retrieve configs from
    # returns: @payload to be used with HTTP requests library
    """
    filename = "authenticate.txt"
    data = [] # Temp File to store data
    payload = {} # Return payload with authentication fields
    with open(os.path.join(cwd, filename)) as authFile:
        for line in authFile:
            if line.find('##') == -1: #if it is not a comment line
                if line.find('*{}'.format(page)) > -1: # If header matches
                    read = True
                    while read: # read next lines after the header
                        data = authFile.readline() # Read next line
                         # Creates condition to stop when hits empty line or EOF
                        read = not(data == '' or data =='\n')
                        data = data.split('\n')[0].replace(' ','').split(':')
                        if not read: # Leaves file reading if condition is met
                            break
                        payload.update({data[0] : data[1]})
    return payload


if __name__ == '__main__':
        print(readAuthenticationFile('Billing'))
