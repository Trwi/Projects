"""

*** Variable and function naming conventions were based on instructions at the beginning of the class ***

Instructions:

After participating in this weeks live webinar, employ the concepts provided to create simple covert communication
capability within the true color image provided.  You will be using the Python Image Library (PIL),  the true color
bmp file provided and the simple code book provided here.

"""

import random  # Will be used to pick random pixels for hiding message

from PIL import Image  # pip install pillow

# Holds the messages in a dictionary to match the user's input
messageDict = {"0": "Dead Drop @", "1": "Corner of Lexington Ave and E 48th Street",
               "2": "Corner of Madison Ave and E 34th Street", "3": "Drop Package in Potted Plant outside Wells Fargo",
               "4": "Drop Package in Gold Gargage Can", "5": "12 PM Sharp", "6": "7 AM Sharp",
               "7": "Abort if you see a Red Rose"}

# Allows me to perform math operations to alter the least significant bit of each color in pixel by appropriate number
conversionDict = {"0": [1, 1, 1], "1": [0, 0, 1], "2": [0, 1, 0], "3": [0, 1, 1], "4": [1, 0, 0], "5": [1, 0, 1],
                  "6": [1, 1, 0], "7": [1, 1, 1]}
answer = "0"
answerList = []  # Holds the user's answers
allowedAnswers = ["0", "1", "2", "3", "4", "5", "6", "7"]  # List for Input Validation

while answer != "55" and answer != "99":
    print()
    print("[0] Dead Drop @\n[1] Corner of Lexington Ave and E 48th Street\n[2] Corner of Madison Ave and E 34th Street")
    print("[3] Drop Package in Potted Plant outside Wells Fargo\n[4] Drop Package in Gold Gargage Can")
    print("[5] 12 PM Sharp\n[6] 7 AM Sharp\n[7] Abort if you see a Red Rose\n")

    print("[55] Create Covert Image")
    print("[99] To abort mission and exit program\n")

    answer = input("Enter your choice now: ")  # records the user's answer

    if answer in allowedAnswers and answer not in answerList:  # adds answer to answerList with input validation
        answerList.append(answer)

# Pixel tuple index pseudo constants
RED = 0
GREEN = 1
BLUE = 2

if answer != "99":  # Allows safe exit from program if so chosen
    try:
        # Obtain the Basic image information
        img = Image.open('monalisa.bmp')
        y = img.height
        x = img.width
        pix = img.load()

        cnt = 0
        pixelListZeros = []  # Holds a list of the pixels if the last bit of each color is 0
        pixelListOther = []  # Holds a list of the pixels if the last bit of each color is 1, Used for message '000'
        changedPixelList = []  # Holds a list of the pixels that have been changed

        for row in range(0, y):

            for col in range(0, x):

                cnt += 1
                pixel = pix[col, row]  # Pixel values

                redPx = pixel[RED]  # Extract the RGB
                grnPx = pixel[GREEN]
                bluPx = pixel[BLUE]

                singlePixelList = [col, row, redPx, grnPx, bluPx]  # Holds each individual pixel

                if redPx % 2 == 0 and grnPx % 2 == 0 and bluPx % 2 == 0:  # If true, the last bit of each color is '0'
                    pixelListZeros.append(singlePixelList)
                else:
                    pixelListOther.append(
                        singlePixelList)  # Else, the last bit of each color is '1', used for ans '000'

        for answer in answerList:
            # Since the last bit of each color is 1, I need to change the bit to 0 through subtraction
            if answer == "0":
                randomInt = random.randint(0, len(pixelListOther) - 1)  # Helps pick random pixel
                pixelListOther[randomInt][2] = pixelListOther[randomInt][2] - 1
                pixelListOther[randomInt][3] = pixelListOther[randomInt][3] - 1
                pixelListOther[randomInt][4] = pixelListOther[randomInt][4] - 1
                changedPixelList.append(pixelListOther[randomInt])  # Adds changed pixel to changedPixelList
            else:
                # Since the last bit of each color is 0, I need to add 1 only where needed with the use of
                # conversionDict
                randomInt = random.randint(0, len(pixelListZeros) - 1)  # Helps pick random pixel
                pixelListZeros[randomInt][2] = pixelListZeros[randomInt][2] + conversionDict[answer][0]
                pixelListZeros[randomInt][3] = pixelListZeros[randomInt][3] + conversionDict[answer][1]
                pixelListZeros[randomInt][4] = pixelListZeros[randomInt][4] + conversionDict[answer][2]
                changedPixelList.append(pixelListZeros[randomInt])  # Adds changed pixel to changedPixelList

        for changedPixel in changedPixelList:
            pixel = (changedPixel[2], changedPixel[3], changedPixel[4])  # Grabs the altered color number for each color
            pix[changedPixel[0], changedPixel[1]] = pixel  # Changes each pixel's colors to their new color number

        img.save('monaLisaSteg.bmp')  # Saves image in current directory

        print("\nALTERED PIXELS")
        for changedPixel in changedPixelList:  # Prints the positions of the altered pixels
            print(f"({changedPixel[0]}, {changedPixel[1]})")

    except Exception as err:  # Handles any errors. For example, if the image is not found in directory
        print("Steg Failed: ", str(err))

print("\nEnd of Script")
