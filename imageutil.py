from imutils.perspective import four_point_transform
from imutils import contours
import cv2
import imutils
import numpy as np
import time

#returns game image object based on the screen capture of the game
#for now it works only with the game on: http://2048game.com/
#for now there is no resizing
def getGameField(gameImage):
    #grayscale filter
    gray = cv2.cvtColor(gameImage, cv2.COLOR_BGR2GRAY)
    #gaussian blur for removing noise
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    #canny edge detection for detecting contours
    canny = cv2.Canny(blur, 50, 200, 255)

    #finding the game contour
    contourList = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contourList = contourList[0] if imutils.is_cv2() else contourList[1]
    contourList = sorted(contourList, key = cv2.contourArea, reverse = True)

    gameContour = None

    #we know that the first contour from the list is the game field, so we take it out
    gameContour = contourList[0]

    #aproximating the rectangle around the game field
    peri = cv2.arcLength(gameContour, True)
    fourCornerApprox = cv2.approxPolyDP(gameContour, peri*0.02, True)

    #getting the game field based on the approximations above
    gameField = four_point_transform(gameImage, fourCornerApprox.reshape(4,2))

    return gameField

#returns list of block image objects for given game field image object
def getFieldBlocks(gameField, dimension):
    #dimesnion needs to be 4,5 or 6
    if dimension not in np.array((4,5,8)): return None
    fieldBlocks = []
    blockWidth = len(gameField)/dimension
    blockHeight = len(gameField)//dimension
    for y in range(dimension):
        for x in range(dimension):
            block = gameField[int(y*blockHeight):int((y + 1)*blockHeight), int(x*blockWidth):int((x+1)*blockWidth)]
            fieldBlocks.append(block)
    return fieldBlocks

#returns list of found number images if there are any on the game block image
def getNumbers(blockImage):
    #removing the field around the actual game block
    #noBorder = removeBlockBorder(blockImage)

    #increase the size of the image test
    blockImage = cv2.resize(blockImage, (600, 600))

    #removing the remainings of the field becaouse the previous method did not do it all, some edges stayed
    noBorder = sliceImageFrame(blockImage, 12)
    numbers = []

    #grayscale filter
    gray = cv2.cvtColor(noBorder, cv2.COLOR_BGR2GRAY)

    #converting grayscale to black and white only image
    bnw = blackAndWhite(gray)

    #gaussian blur for removing noise
    blur = cv2.GaussianBlur(bnw, (3,3), 0)

    #canny edge detection for detecting contours
    #still needs some work
    #180 was decided experimentaly
    canny = cv2.Canny(blur, 0, 180, 255)


    #finding the number contour
    contourList = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contourList = contourList[0] if imutils.is_cv2() else contourList[1]

    #sorting the contours from left to right
    if len(contourList) == 0: return numbers
    contourList = contours.sort_contours(contourList, method='left-to-right')[0]    

    #getting the numbers
    for c in contourList:
        # #aproximating the rectangle around the number shape
        (x,y,w,h) = cv2.boundingRect(c)
        number = noBorder[y: y + h, x: x + w]
        #resizing any number to a fixed size of 150x100
        number = cv2.resize(number, (100, 150))
        # cv2.imshow('sdfs', number)
        # cv2.waitKey(0)
        numbers.append(number)

    
    return numbers

def removeBlockBorder(blockImage):
    #increasing the contrast so we can detect the block border more easily
    hc = increaseContrast(blockImage)
    #grayscale filter
    gray = cv2.cvtColor(hc, cv2.COLOR_BGR2GRAY)
    #gaussian blur for removing noise
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    #canny edge detection for detecting contours
    canny = cv2.Canny(blur, 0, 0, 255)
    #finding the block border contour
    contourList = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contourList = contourList[0] if imutils.is_cv2() else contourList[1]
    contourList = sorted(contourList, key = cv2.contourArea, reverse = True)

    blockContour = None

    #the largest contour should be the block border
    #we know that the first contour from the list is the block field, so we take it out
    blockContour = contourList[0]

    #now we approximate the rectangular frame around the border we want to remove
    (x,y,w,h) = cv2.boundingRect(blockContour)
    noBorder = blockImage[y: y + h, x: x + w]

    #we return the borderless image
    return noBorder

#used for increasing the contrast of the image, helping us to see the borders more clearly in some cases
#default increase is 20%
def increaseContrast(image, alfa = 1.2):
    output = cv2.addWeighted(image, alfa, image, 0, 0)
    return output

#image needs to be grayscale
#converts a graycale image into a black and white image
#finds average pixel value
#replaces pixel values so the ones below the average become 0, the other ones become 255
def blackAndWhite(grayImage):
    grayImage = twoToneGrayscale(grayImage)
    #calculating the average
    average = int(grayImage.mean())

    #replacing the pixel values besad on the average
    #optimized with numpy direct indexing
    grayImage[grayImage>=average] = 255
    grayImage[grayImage<average] = 0

    return grayImage 

#image needs to be grayscale
#makes the image contain only two grayscale values
def twoToneGrayscale(grayscale):
    maxValue = grayscale.max()
    minValue = grayscale.min()

    #special case if the game block is empty
    if maxValue - minValue < 5: maxValue = minValue

    #now we set the new values
    grayscale[maxValue - grayscale <= grayscale - minValue] = maxValue
    grayscale[maxValue - grayscale > grayscale - minValue] = minValue
    return grayscale

#slices a percentual part of the image from all four sides
#calcualtes the offset based on the percent we want and returns us a new image croped by the offset on all four sides
def sliceImageFrame(image, percent):
    hOffset = len(image)*percent//100
    wOffset = len(image[0])*percent//100
    return image[hOffset:len(image) - hOffset, wOffset: len(image[0]) - wOffset]

#converts image to grayscale
def grayScaleImage(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#splits image into ...
def imageSplitter(image, wp=2, hp=3):
    parts = []
    blockHeight = len(image)//hp
    blockWidth = len(image[0])//wp
    for y in range(hp):
        for x in range(wp):
            block = image[int(y*blockHeight):int((y + 1)*blockHeight), int(x*blockWidth):int((x+1)*blockWidth)]
            parts.append(block)
    
    return parts

# black num, white background
# returns black to all ratio b/t
def blackSurfaceRatio(image):
    #optimized with numpy fuction
    blackPixels = (image == 0).sum()
    return blackPixels/(len(image)*len(image[0]))

#inverts the black and white color on a black and white image
def invertImage(image):
    return cv2.bitwise_not(image)