"""

This Virus Total API program followed the instructions of an assignment in my Violent Python course. Variable
and function naming conventions were based on instructions at the beginning of the class.

"""

import json
import hashlib
import os
import math
from prettytable import PrettyTable
from virus_total_apis import PublicApi as VirusTotalPublicApi

print()
print('=' * 73)
print('The final output from Virus Total is formatted best for a size 14 font')
print('=' * 73)
print('\n')

API_KEY = input('What is your Virus Total API key?: ')  # Holds the API key for your VT account
loop = 'Y'     # While loop control
fileList = []  # Holds the files inside the directory
md5List = []   # Holds the hashes of each file
count = 0      # Helps with iteration

''' 

While loop below sets a list of all the files in the directory provided by the user. If directory does not exist,
program informs the user and prompts them again. Gives the user the option to safely exit the program if needed.

'''
while loop == 'Y':
    directory = input("What directory are the files located to upload to Virus Total?: ")
    
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                fileList.append(file)
        
        loop = 'Moving on'
            
    else:
        loop = input(f"\n{directory} is not a valid directory. Press "
                     f"'y' to try again or 'q' to exit the program: ").upper()
        print()   

"""

If statement below ensures that the user can exit the program above if directory is not valid. Gets the full path of
file, reads file in byte form, hashes file, and adds hash to md5List.

"""

if loop == 'Moving on': 
    
    for file in fileList: 
        path = os.path.join(root, file)
        fullPath = os.path.abspath(path)
        readFile = open(fullPath, "rb")
        fileContent = readFile.read()
        md5Hash = hashlib.md5(fileContent).hexdigest()
        md5List.append(md5Hash)                
    
    ''' Prepares the pretty table to output the file alongside their hashes and prints the pretty table '''
    md5Table = PrettyTable(['File', 'MD5 Hash'])
    
    for file in fileList:
        md5Table.add_row([fileList[count], md5List[count]])
        count += 1
    
    md5Table.align = 'l'
    print()
    print('Printing your files and their corresponding MD5 hashes...\n')
    print(md5Table.get_string())
    print('\n')
    
    ''' 
    Sends each hash to Virus Total for processing, receives results, formats output,
    and outputs the results of each file/hash 
    '''
    print('Printing the responses from Virus Total...\n\n')
    
    count = 0
    vt = VirusTotalPublicApi(API_KEY)
    
    for md5 in md5List:
        response = vt.get_file_report(md5)
        fileString = f'Virus Total Response For {fileList[count]}'
        length = math.floor(len(fileString) / 2)
        distance = 73 - length
        print(' ' * distance + fileString)
        print('=' * 146)
        print(json.dumps(response, sort_keys=False, indent=4)) 
        print('=' * 146)
        print('\n\n')
        count += 1

print('End of Script')
