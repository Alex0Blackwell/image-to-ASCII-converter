from PIL import Image
import time as t
import glob, random, curses


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
    """ convert rgb to ansi (closest of 15 default colours) """
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

    def __init__(self, filename, colourChoice):
        self.colourChoice = colourChoice
        self.ref = Image.open(filename)
        self.rgb = self.ref.convert("RGB")
        self.wXh = self.ref.size


    def genAscii(self):
        """ The method to print the ASCII image. """
        darkToBright = ['#', '$', '&', '%', 'x', 'v', '=', '+', '*', '~', '`']

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
                # ascii color light gray
                if(self.colourChoice == 1):  # grayscale
                    print(darkToBright[totalBrightness//70], end='')
                else:
                    print('\033[07m', end='')  # reverse color
                    if(self.colourChoice == 2):  # 8-bit
                        print(f"\033[47m{rgbToAnsi(r, g, b)+darkToBright[totalBrightness//70]}\033[0m", end='')
                    elif(self.colourChoice == 3):  # true colour
                        print(f"\x1b[38;2;{r};{g};{b}m{darkToBright[totalBrightness//70]}\x1b[0m", end='')
            print()


def main():

    exts = ["jpg", "jpeg", "JPG", "JPEG", "png", "PNG"]
    possibleImages = []
    imageNames = []

    for ext in exts:
        possibleImages += glob.glob(f"imgs/*.{ext}")

    for img in possibleImages:
        imageNames.append(img.split('imgs/')[1].split('.')[0])

    print("Hello, type the associated number to make an ASCII image of one of the following images.")
    c = 1
    for img in imageNames:
        print(f"({c}) {img} image")
        c += 1
    print("If you don't see your image listed, drop it into the ./imgs/ folder")

    userNum = ""
    while(not (userNum.isdigit() and 1 <= int(userNum) <= len(possibleImages))):
        if(userNum.isdigit()):
            if(not(1 <= int(userNum) <= len(possibleImages))):
                print(f"Make sure the number is between or equal to 1 and {len(possibleImages)}")
        userNum = input("Enter the number: ")
    userNum = int(userNum)

    print("Type the associated number to choose what type of colour to use.")
    colourChoices = ["Grayscale", "8-Bit Colour", "True Colour"]
    c = 1
    for type in colourChoices:
        print(f"({c}) {type}")
        c += 1

    colorChoice = ""
    while(not (colorChoice.isdigit() and 1 <= int(colorChoice) <= 3)):
        if(colorChoice.isdigit()):
            if(not(1 <= int(colorChoice) <= 3)):
                print("Make sure the number is between or equal to 1 and 3")
        colorChoice = input("Enter the number: ")
    colorChoice = int(colorChoice)
    bruteAnim("Generating your ", "ASCII Image");
    print()
    t0 = t.time()
    selectedImage = Picture(possibleImages[userNum-1], colorChoice)
    selectedImage.genAscii()
    print('\033[0m')  # reset colors
    timeElapsed = round(t.time() - t0, 2)
    print(f"The image was generated in {timeElapsed} seconds.")
    print("It might look like a bunch of random text now\nbut zoom out to see the picture!")


if __name__ == '__main__':
    main()
