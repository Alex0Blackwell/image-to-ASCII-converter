from PIL import Image
import glob


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

        imgSize = 250  # max number of columns/rows
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
                totalBrightness = r + g + b;  # 0-765
                print(darkToBright[totalBrightness//70], end='')  # 0->0, 765->10
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

    selectedImage = Picture(possibleImages[userNum-1])
    selectedImage.genAscii()
    print("It might look like a bunch of random text now\nbut zoom out to see the picture!")


if __name__ == '__main__':
    main()
