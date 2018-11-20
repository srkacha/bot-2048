from scipy import spatial
from pynput.keyboard import Key, Controller
import imageutil as iu
import random
import time
import cv2

#lookup table for storing base number representation values
digitsLookup = {
    (0.474, 0.4952, 0.5076, 0.5168, 0.5044, 0.5248) : 0,
    (0.2852, 0.72, 0.0884, 0.88, 0.0, 0.814) : 1,
    (0.4124, 0.5492, 0.1188, 0.548, 0.7064, 0.5388) : 2,
    (0.4688, 0.6232, 0.1952, 0.674, 0.4872, 0.6396) : 3,
    (0.0932, 0.58, 0.4856, 0.5136, 0.4004, 0.6852) : 4,
    (0.5348, 0.444, 0.4892, 0.6028, 0.4428, 0.5928) : 5,
    (0.4804, 0.4156, 0.708, 0.6248, 0.5556, 0.6176) : 6,
    (1, 1, 1, 1, 1, 1) : 7,
    (0.5212, 0.5392, 0.612, 0.612, 0.5988, 0.6188) : 8,
    (1, 1, 1, 1, 1, 1) : 9
}

#returns vector representation of the number based on the given image
#splits the image into 6 pieces, converts them to two color images and calculates the percentage of the black
#returns a vector with 6 values between 0 and 1
def calculateNumberRepresentation(numberImage):
    representation = ()

    #first we convert the imahe to two color image, black and white
    gray = iu.grayScaleImage(numberImage)
    bnw = iu.blackAndWhite(gray)
    
    #inverting image if the first pixel is black
    if bnw[0, 0] == 0: 
        bnw = iu.invertImage(bnw)

    #then we split the image into 6 equal pieces
    imagePieces = iu.imageSplitter(bnw)

    #now we calcualte the black percentages
    for piece in imagePieces:
        blackRatio = iu.colorRatio(piece)
        representation = representation + (blackRatio, )
    
    return representation


#looks up the number based on its six point representation
#uses cosine similarity for determening the similarity between two vectors
def determineNumber(numRepresentation):
    maxSimilarity = 0
    bestMatchValue = -1
    for key, value in digitsLookup.items():
        cosSimilarity = 1 - spatial.distance.cosine(numRepresentation, key)
        if cosSimilarity > maxSimilarity:
            maxSimilarity = cosSimilarity
            bestMatchValue = value
    
    return bestMatchValue

#returns a number based on the array of images of the number digits
def generateNumber(digitImages):
    #if the array is empty then the field was empty
    if len(digitImages) == 0: return 0
    
    number = ''
    for d in digitImages:
        numberRepresentation = calculateNumberRepresentation(d)
        digit = determineNumber(numberRepresentation)
        #if the number is not valid, that means that the recognition process was interrupted, so we return -1
        if digit == -1: return None
        #else we add it to the number
        number += str(digit)
    
    return int(number)

#for a given game screenshot determines the game state matrix (tupple for now)
def getGameStateMatrix(gameImage, dimension = 4):
    #first we extract the game field
    gameField = iu.getGameField(gameImage)
    
    #then we resize the field by slicing of some of the border to make it more symetrical
    resizedGameField = iu.sliceImageFrame(gameField, 1)
    
    #we then extract the individual game blocks from the field
    gameBlocks = iu.getFieldBlocks(resizedGameField, dimension)
    gameStateTupple = ()

    #now that we have the game blocks, we are ready to start extracting the numbers
    for block in gameBlocks:
        digitImages = iu.getNumbers(block)   
        blockValue = generateNumber(digitImages)
        #if we get None or some number that is not power of two, we return None
        if blockValue == None: return None
        if blockValue != 0 and blockValue not in [2,4,8,16,32,64,128,256,512,1024,2048]: return None

        gameStateTupple = gameStateTupple + (blockValue, )
    
    return gameStateTupple

#suggests a move to be made for the game, based on the game representation
#global keyborad object
keyboard = Controller()

def suggestNextMove(gameState):
    if gameState == None: return
    rand = random.uniform(0, 1)
    if rand < 0.6:
        keyboard.press(Key.up)
    elif rand < 0.9:
        keyboard.press(Key.right)
    elif rand <0.995:
        keyboard.press(Key.down)
    elif rand < 1:
        keyboard.press(Key.left)

def is_power(n):
    if not n == int(n):
        return False
    n = int(n)
    if n == 1:
        return True
    elif n > 2:
        return is_power(n/2.0)
    else:
        return False