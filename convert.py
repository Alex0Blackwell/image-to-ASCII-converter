from PIL import Image
import glob


class Picture():
    """docstring for Picture."""

    def __init__(self, filename):
        self.ref = Image.open(filename)
        self.rgb = self.ref.convert("RGB")
        self.wXh = self.ref.size


    def genAscii(self):
        darkToBright = ['#', '$', '&', '%', 'w', 'x', '=', '+', '*', '~', '`']

        if(self.wXh[0] >= self.wXh[1]):
            # landscape
            xStep = 150
            yStep = int(self.wXh[1]*150/self.wXh[0])
        else:
            xStep = int(self.wXh[0]*150/self.wXh[1])
            yStep = 150

        incrementX = self.wXh[0] // xStep
        incrementY = self.wXh[1] // (yStep//2)

        for row in range(0, self.wXh[1], incrementY):
            # for every 'increment'th column
            for col in range(0, self.wXh[0], incrementX):
                # for every 'increment'th row
                (r, g, b) = self.rgb.getpixel((col, row))
                totalBrightness = r + g + b;  # 0-765
                #index = totalBrightness // 70  # 0->0, 765->10
                print(darkToBright[totalBrightness//70], end='')
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


if __name__ == '__main__':
    main()
