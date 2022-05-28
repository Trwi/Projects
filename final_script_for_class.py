"""

*** Variable and function naming conventions were based on instructions at the beginning of the class ***
*** Code will not run as I have removed the website we were authorized to scrape. Tested and works as of 05/27/2022 ***
*** I can ask for permission if you would like to see it run, or you can use a website of your choice ***
*** Script has only been tested on website we were authorized to scrape ***

Your Final Scripting Project Details:

Your final script will scrape the given website within CyberApolis.

IMPORTANT you will not follow any links that veer outside of CyberApolis

IMPORTANT you are allowed to use standard python libraries and any 3rd party library that we have used during the class.

Your script will generate a report that contains the following information.

1) Unique URLs of all the pages found on the website

2) Unique URL links to images found on the website

3) Extract and phone numbers found on the website

4) Extract all text content from each of the pages and store them in a string variable

5) Extract any Zip Codes

NOTE for Items 6-8 you will be utilizing NLTK to process all the text found on the website, using the text content you
extracted during item 4 above.

6) A list of all unique vocabulary found on the website

7) A list of all possible verbs

8) A list of all possible nouns

"""

# Python Standard Libraries
import requests  # Python Standard Library for url requests
import re
import nltk
import math
import string
from unidecode import unidecode

# Python 3rd Party Libraries
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def printSimplePrettyTable(header, rows):
    """ Prints out a basic pretty table with a header and single entries for the rows """

    table = PrettyTable([header])

    for row in rows:
        table.add_row([row])

    table.align = 'c'
    print(table.get_string())
    print("\n")


def printModifiedTable(header, rows):
    """ Creates and prints a custom table that is similar to a pretty table to hold all words, nouns, and verbs """

    group = ""

    if header == 'Verbs' or header == 'Vocabulary':
        n = 11
    else:
        n = 10

    # segList divides rows list into separate, ten item lists for printing
    segList = [rows[i:i + n] for i in range(0, len(rows), n)]
    length = math.floor(50 - len(header) / 2) - 1
    centered = length + len(header)

    print("+" + ("=" * 100) + "+")
    print("|" + " " * 100 + "|")
    print("|" + (" " * length) + header + (" " * (100 - centered)) + "|")
    print("+" + "=" * 100 + "+")

    for segment in segList:
        for word in segment:
            group = group + " " + word
        firstPrint = "|" + group
        spaces = 101 - len(firstPrint)
        print(firstPrint + " " * spaces + "|")
        group = ""

    print("+" + "=" * 100 + "+")
    print("\n")


def processWebScrape():
    """
    Scrapes a website for text and images, grabs links on the site within CyberApolis, and scrapes those pages as well.
    REGEX is used to extract found phone numbers and zip codes. All URLs to pages, all image URLs, zip codes, and phone
    numbers are printed inside a pretty table with printSimplePrettyTable method. Returns all found text to main to
    send to nltkResults method.

    """

    url = 'https://*****.********/'  # Decided to obfuscate the website we were given since it is accessible
    base = 'https://******.******'   # Obfuscated the base of the website as well
    page = requests.get(url)  # retrieve a page from your favorite website
    soup = BeautifulSoup(page.text, 'html.parser')  # convert the page into soup
    text = soup.get_text()
    imageURLS = []
    links = []

    for link in soup.find_all('a'):
        link = str(link.get('href'))
        if link != 'None':  # If the value of link is not None
            if link[0:4] != 'http':  # If URL path is relative
                link = base + link  # Prepend the base url
            links.append(link)

    for link in links:
        baseReg = r'^http[s]?:\/\/[^\/]+'  # Regex for getting the base of a URL
        base = re.search(baseReg, link).group()
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        images = soup.findAll('img')
        text = text + soup.get_text()
        for image in images:
            imageURL = base + image['src']
            if imageURL not in imageURLS:
                imageURLS.append(imageURL)

    usZip = r'(\d{5}\-?\d{0,4})'  # zip code regex
    phoneNumber = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'  # phone number regex
    zipCodes = re.findall(usZip, text)
    phoneNumbers = re.findall(phoneNumber, text)
    phoneNumbers = list(set(phoneNumbers))
    zipCodes = list(set(zipCodes))

    printSimplePrettyTable('Unique URLs', links)
    printSimplePrettyTable('Image URLs', imageURLS)
    printSimplePrettyTable('Phone Numbers', phoneNumbers)
    printSimplePrettyTable('Zip Codes', zipCodes)

    removeDigits = r'[0-9]'
    text = re.sub(removeDigits, '', text)

    return text


def nltkResults(text):
    """
    Uses nltk to process text from web scrape. Prints unique vocab, possible verbs, and possible nouns with
    printModifiedTable method

    """
    text = unidecode(text)  # The only way I could get rid of specific bad chars. I tried every other way.
    punctSet = set(string.punctuation)
    badChars = ['+00', "'s", 'c', '//', "''", "'ll", '``', "..", "...", "n't",
                "'d"]  # Characters in the results that I did not want
    punctSet.update(badChars)
    vocab = nltk.word_tokenize(text)
    vocabSet = set(vocab)
    vocabSet -= punctSet
    vocab = list(vocabSet)
    verbsList = []
    nounsList = []

    posTagged = nltk.pos_tag(vocab)

    VERBTAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP',
                'VBZ']  # I was not sure how many of the types of verbs and nouns were needed.
    NOUNTAGS = ['NN', 'NNP', 'NNS',
                'NNPS']  # I chose all. Would just need to remove whatever was not necessary if that is wrong.

    for pos in posTagged:
        if pos[1] in VERBTAGS:
            verbsList.append(pos[0])
        elif pos[1] in NOUNTAGS:
            nounsList.append(pos[0])
        else:
            continue

    verbsSet = set(verbsList)
    nounsSet = set(nounsList)
    verbsSet -= punctSet
    nounsSet -= punctSet
    verbsList = list(verbsSet)
    nounsList = list(nounsSet)

    printModifiedTable('Vocabulary', vocab)
    printModifiedTable('Verbs', verbsList)
    printModifiedTable('Nouns', nounsList)


if __name__ == '__main__':

    text = processWebScrape().lower()
    nltkResults(text)
