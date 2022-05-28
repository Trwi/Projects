""" Variable and function naming conventions were based on instructions at the beginning of the class """

from PIL import Image

# Pixel tuple index psuedo constants
RED = 0
GREEN = 1
BLUE = 2

''' Obtain the Basic image information '''
try:
    img = Image.open('monalisa.bmp')  # Open original picture
    img2 = Image.open('monaLisaSteg.bmp')  # Open picture with hidden message

    imgList = []  # Creates a list of pixels from original picture
    img2List = []  # Creates a list of pixels from altered picture
    imgSet = set()  # Creates a set of pixels from original picture. This makes it easier to compare images.
    img2Set = set()  # Creates a set of pixels from altered picture. Allows for easier comparison.

    y = img.height
    x = img.width

    y1 = img2.height
    x2 = img2.width

    pix = img.load()
    pix2 = img2.load()

    for row in range(0, y):  # Iterates through original image's pixels and adds them to a list

        for col in range(0, x):
            pixel = pix[col, row]  # Pixel values

            redPx = pixel[RED]  # Extract the RGB
            grnPx = pixel[GREEN]
            bluPx = pixel[BLUE]

            imgList.append([col, row, redPx, grnPx, bluPx])  # Adds pixel to original picture imgList

    for row in range(0, y):  # Iterates through altered image's pixels and adds them to a separate list

        for col in range(0, x):
            pixel = pix2[col, row]  # Pixel values

            redPx = pixel[RED]  # Extract the RGB
            grnPx = pixel[GREEN]
            bluPx = pixel[BLUE]

            img2List.append([col, row, redPx, grnPx, bluPx])  # Adds pixel to altered picture img2List

    ''' I needed to create a set for each images pixel's to later compare them to find altered pixels '''
    for pixel in imgList:
        imgSet.add(tuple(pixel))

    for pixel in img2List:
        img2Set.add(tuple(pixel))

    ''' I was having trouble sorting a list with binary representation to print message in correct order.
    This conversionDictionary allowed me to sort since I converted the binary values to an integer. '''

    conversionDict = {"-1-1-1": 0, "001": 1, "010": 2, "011": 3, "100": 4, "101": 5, "110": 6, "111": 7}

    # Holds the messages for later printing    
    messageDict = {0: "Dead Drop @", 1: "Corner of Lexington Ave and E 48th Street",
                   2: "Corner of Madison Ave and E 34th Street", 3: "Drop Package in Potted Plant outside Wells Fargo",
                   4: "Drop Package in Gold Garbage Can", 5: "12 PM Sharp", 6: "7 AM Sharp",
                   7: "Abort if you see a Red Rose"}

    newSet = img2Set.difference(imgSet)  # Creates a new set of the differences between the two sets
    newList = list(newSet)  # converts the newSet to a list for easier processing
    codeList = []  # Holds the message in binary form '001' etc. for further processing, used with conversionDict
    messageList = []  # Holds the message in int form for easier processing, used with messageDict

    for pixel in newList:  # Extracts the binary message from each pixel in newList
        pixelCode = pix[pixel[0], pixel[1]]  # Grabs the pixel from original image with col, row
        redPixel = pixelCode[RED]  # Sets the value for RED pixel
        greenPixel = pixelCode[GREEN]  # Sets the value for GREEN pixel
        bluePixel = pixelCode[BLUE]  # Sets the value for BLUE pixel
        redCode = pixel[2] - redPixel  # Altered pixel - Original pixel
        greenCode = pixel[3] - greenPixel  # Altered pixel - Original pixel
        blueCode = pixel[4] - bluePixel  # Altered pixel - Original pixel
        code = str(redCode) + str(greenCode) + str(
            blueCode)  # Creates a string of the binary representation for lookup in conversionDict
        codeList.append(code)  # Adds the binary code to codeList

    for code in codeList:  # Converts the binary message to an int through conversionDictionary for easier processing
        messageNumber = conversionDict[code]
        messageList.append(messageNumber)  # Adds the converted int to messageList for lookup in messageDictionary

    messageList.sort()  # Sorts the messages so they print in order

    for message in messageList:  # prints each message with use of messageDictionary
        print(messageDict[message])


except Exception as err:  # Handles any errors that might occur during processing
    print("Extract Failed: ", str(err))

print("\nEnd of Script. Good luck.")
