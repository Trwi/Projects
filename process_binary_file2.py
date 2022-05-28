"""

*** Variable and function naming conventions were based on instructions at the beginning of the class ***

Instructions
An excerpt of a memory dump extracted by Access Data's FTK Imager (memdump.bin or test.bin) has been provided.

1) Copy the memory dump to the virtual desktop environment persistent storage area.

2) Develop a Python script to process the memory dump and identify unique strings of 5-12 characters along with the
number of occurrences of each unique string. Then display the resulting list of strings and occurrences in a
prettytable sorted by the highest number of occurrences.

REGULAR EXPRESSION HELP

word regx (more specifically continuous alpha string pattern)

wPatt = re.compile(b'[a-zA-Z]{5,15}')

"""

import re
import os
from prettytable import PrettyTable

# File Chunk Size
CHUNK_SIZE = 1024

# regular expressions
wPatt = re.compile(b'[a-zA-Z]{5,15}')

# Create empty dictionary, converted strings list, and pretty table.
stringDictionary = {}
convertedStringsList = []
resultTable = PrettyTable(['count', 'string'])

# Check which file the user wants to process
answer = input("What is the memory dump file you want to process to find email and url patterns contained within?: ")

print()

# Error handling for if the file does not exist. Also gives the option to safely exit the program by entering 'q'
while not os.path.isfile(answer) and answer != 'q':
    answer = input("No such file. What is the memory dump file you want to process to find email"
                   "and url patterns for? Or press 'q' to quit: ")
    print()

if answer != 'q':
    # Iterates through the binary file one chunk at a time. Uses regex to find relevant strings
    with open(answer, 'rb') as binaryFile:
        while True:
            chunk = binaryFile.read(CHUNK_SIZE)
            if chunk:
                byteStrings = wPatt.findall(chunk)

                # Converts byte strings to regular strings. Adds regular strings to new list.
                if byteStrings:
                    for string in byteStrings:
                        convertedString = str(string, 'utf-8').lower()
                        convertedStringsList.append(convertedString)

            else:
                break

    # Adds strings to dictionary with the value of 1 if key is not found in dictionary already, adds 1 to existing
    # value if key is found.
    for string in convertedStringsList:
        string.lower()
        if string in stringDictionary:
            stringDictionary[string] = stringDictionary[string] + 1
        else:
            stringDictionary[string] = 1

            # Adds a new for each key and value pair
    for key, value in stringDictionary.items():
        resultTable.add_row([value, key])

    # Formats the pretty table and sorts by count, highest to lowest.
    resultTable.align = 'l'
    resultTable.sortby = 'count'
    resultTable.reversesort = True
    print(resultTable.get_string())

    print("\nEnd of script")

else:

    print("\nEnd of script")
