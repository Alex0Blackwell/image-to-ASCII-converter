from PIL import Image
import time as t
import glob, random


def bruteAnim(sentence, word):
    letters = ['a','c','d','f','g','i','k','m','o','q','s','u','w','y']
    write = sentence+''
    for a in range(0, len(word)):
        for b in range(0,5):
            print(write+letters[random.randint(0,len(letters)-1)], end='\r')
            t.sleep(0.05)
        write = write + word[a]
    print(sentence+word)


### making this public considerably speeds up the run time (70% faster)
# black:\033[30m, red:\033[31m, green:\033[32m ,orange:\033[33m
# blue:\033[34m, purple:\033[35m, cyan:\033[36m ,lightgrey:\033[37m
# darkgrey:\033[90m, lightred:\033[91m, lightgreen:\033[92m, yellow:\033[93m
# lightblue:\033[94m, pink:\033[95m, lightcyan:\033[96m
colorList = [[(28, 28, 28), '\033[30m'], [(224, 52, 52), '\033[31m'], [(42, 209, 75), '\033[32m'],
[(219, 141, 46), '\033[33m'], [(53, 48, 217), '\033[34m'], [(156, 43, 227), '\033[35m'],
[(53, 214, 219), '\033[36m'], [(171, 171, 171), '\033[90m'], [(99, 99, 99), '\033[90m'],
[(255, 163, 163), '\033[91m'], [(130, 255, 145), '\033[92m'], [(255, 251, 5), '\033[93m'],
[(150, 227, 255), '\033[94m'], [(255, 140, 230), '\033[95m'], [(204, 249, 255), '\033[96m']]

def rgbToAnsi(r, g, b):
    # assume minDifference is the first pixel
    ansiIndex = 0
    minDifference = abs(colorList[0][0][0] - r)
    minDifference += abs(colorList[0][0][1] - g)
    minDifference += abs(colorList[0][0][2] - b)

    for i in range(1, len(colorList)):
        thisDifference = abs(colorList[i][0][0] - r)
        thisDifference += abs(colorList[i][0][1] - g)
        thisDifference += abs(colorList[i][0][2] - b)
        if(thisDifference < minDifference):
            minDifference = thisDifference
            ansiIndex = i


    return colorList[ansiIndex][1]


class Picture():
    """
    Used for converting an jpg or png image to a text image.

    Attributes:
        filename (string): The location of the jpg/png file
    """

    def __init__(self, filename):
        self.ref = Image.open(filename)
        self.rgb = self.ref.convert("RGB")
        self.wXh = self.ref.size


    def genAscii(self):
        """ The method to print the ASCII image. """
        darkToBright = ['#', '$', '&', '%', 'w', 'x', '=', '+', '*', '~', '`']

        imgSize = 160  # max number of columns/rows
        if(self.wXh[0] >= self.wXh[1]):
            # landscape
            xStep = imgSize
            yStep = int(self.wXh[1]*imgSize/self.wXh[0])
        else:
            # portrait
            xStep = int(self.wXh[0]*imgSize/self.wXh[1])
            yStep = imgSize

        incrementX = self.wXh[0] // xStep
        incrementY = self.wXh[1] // (yStep//2)  # divide by 2 because of terminal line height

        for row in range(0, self.wXh[1], incrementY):
            for col in range(0, self.wXh[0], incrementX):
                (r, g, b) = self.rgb.getpixel((col, row))
                totalBrightness = r + g + b  # 0-765
                print(rgbToAnsi(r, g, b)+darkToBright[totalBrightness//70], end='')  # 0->0, 765->10
            print()


def main():
    exts = ["jpg", "jpeg", "png", "PNG"]
    possibleImages = []
    imageNames = []

    for ext in exts:
        possibleImages += glob.glob(f"imgs/*.{ext}")

    for img in possibleImages:
        imageNames.append(img.split('imgs/')[1].split('.')[0])

    print("Hello, type the associated number to make an ASCII image of one of the following images. ")
    c = 1
    for img in imageNames:
        print(f"({c}) {img} image")
        c += 1
    print("If you don't see your image listed, drop it into the ./imgs/ folder")

    userNum = ""
    while(not (userNum.isdigit() and 0 <= int(userNum) <= len(possibleImages))):
        if(userNum.isdigit()):
            if(not(0 <= int(userNum) <= len(possibleImages))):
                print(f"Make sure the number is between 0 and {len(possibleImages)}")
        userNum = input("Enter the number: ")
    userNum = int(userNum)
    bruteAnim("Generating your ", "ASCII Image");

    print('\033[47m')  # set the background color
    t0 = t.time()
    selectedImage = Picture(possibleImages[userNum-1])
    selectedImage.genAscii()
    print('\033[0m')  # reset colors
    print("It might look like a bunch of random text now\nbut zoom out to see the picture!")
    timeElapsed = round(t.time() - t0, 2)
    print(f"The image was generated in {timeElapsed} seconds.")


if __name__ == '__main__':
    main()
