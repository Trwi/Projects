"""
*** Variable and function naming conventions were based on instructions at the beginning of the class ***

Instructions
An excerpt of a memory dump extracted by Access Data's FTK Imager (memdump.bin or test.bin) has been provided.

1) Copy the memory dump to the virtual desktop environment persistent storage area.

2) Develop a python script & regular expressions to extract and report ALL the e-mail & urls found in the memory dump.

REGULAR EXPRESSIONS HELP

e-mail and url patterns

ePatt = re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
uPatt = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')

"""

import re
import os
from prettytable import PrettyTable

# File Chunk Size
CHUNK_SIZE = 1024

# regular expressions
ePatt = re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
uPatt = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')

# Create empty lists
emailList = []
urlList = []
count = 0

# Check which file the user wants to process
answer = input("What is the memory dump file you want to process to find email and url patterns contained within?: ")

print()

# Error handling for if the file does not exist. Also gives the option to safely exit the program by entering 'q'
while not os.path.isfile(answer) and answer != 'q':
    answer = input("No such file. What is the memory dump file you want to process to find email"
                   "and url patterns for? Or press 'q' to quit: ")
    print()

if answer != 'q':
    # Iterates through the binary file one chunk at a time. Uses regex to find potential emails and urls
    with open(answer, 'rb') as binaryFile:
        while True:
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                emails = ePatt.findall(chunk)

                for eachEmail in emails:
                    eachEmail.lower()
                    emailList.append(eachEmail)

                urls = uPatt.findall(chunk)

                for eachUrl in urls:
                    eachUrl.lower()
                    urlList.append(eachUrl)

            else:
                break

    # Converts the byte string emails to regular strings        
    for eachPossibleEmail in emailList:
        emailString = str(eachPossibleEmail, 'utf-8')
        checkDomain = emailString[-4:-1]

        # Removes any extra characters at the end of found emails. Would need to be implemented differently to handle
        # more domains.
        if checkDomain == 'com' or checkDomain == 'org':
            emailString = emailString[:-1]
        emailList[count] = emailString
        count += 1

    count = 0

    # Converts url byte strings to regular strings        
    for eachPossibleUrl in urlList:
        urlString = str(eachPossibleUrl, 'utf-8')
        urlList[count] = urlString
        count += 1

        # Creates a pretty table for the results
    resultUrlTable = PrettyTable(['Urls'])
    resultEmailTable = PrettyTable(['Emails'])

    # Iterates through the emails in emailList, and creates a new row in its pretty table
    for eachPossibleEmail in emailList:
        resultEmailTable.add_row([eachPossibleEmail])

    # Iterates through the urls in urlList, and creates a new row in its pretty table
    for eachPossibleUrl in urlList:
        resultUrlTable.add_row([eachPossibleUrl])

    # Aligns the pretty table to the left, and prints each pretty table.        
    resultUrlTable.align = 'l'
    print(resultUrlTable.get_string())

    resultEmailTable.align = 'l'
    print(resultEmailTable.get_string())

    print("\nEnd of script")

else:

    print("\nEnd of script")
