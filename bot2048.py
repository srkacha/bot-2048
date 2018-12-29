from scipy import spatial
from pynput.keyboard import Key, Controller
import imageutil as iu
import time
import cv2
import sys
import numpy as np
import pyautogui

#players
import greedy
import randomPlayer
import monotonicDecreasingPlayer as mdp
import alphabeta
import Board

#lookup table for storing base number representation values
digitsLookup = {
    (0.5876, 0.5948, 0.5632, 0.5648, 0.6136, 0.6208) : 0,
    (0.4348, 0.8968, 0.0392, 0.9372, 0.0, 0.9328) : 1,
    (0.5124, 0.6448, 0.1348, 0.568, 0.8452, 0.6116) : 2,
    (0.5052, 0.682, 0.2048, 0.7024, 0.5196, 0.706) : 3,
    (0.1524, 0.6624, 0.5328, 0.5232, 0.518, 0.7552) : 4,
    (0.6432, 0.4972, 0.5408, 0.6664, 0.5132, 0.6596) : 5,
    (0.5764, 0.4448, 0.7972, 0.684, 0.6376, 0.6628) : 6,
    (1, 1, 1, 1, 1, 1) : 7,
    (0.6144, 0.6156, 0.6768, 0.6568, 0.6624, 0.662) : 8,
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
        blackRatio = iu.blackSurfaceRatio(piece)
        representation = representation + (blackRatio, )
    return representation


#looks up the number based on its six point representation
#uses cosine similarity for determening the similarity between two vectors
def determineNumber(numRepresentation):
    # maxSimilarity = 0
    # bestMatchValue = -1
    # for key, value in digitsLookup.items():
    #     cosSimilarity = 1 - spatial.distance.cosine(numRepresentation, key)
    #     if cosSimilarity > maxSimilarity:
    #         maxSimilarity = cosSimilarity
    #         bestMatchValue = value
    minSsdSim = sys.maxsize
    bestMatchValue = -1
    for key, value in digitsLookup.items():
        ssdSim = ssd(numRepresentation, key)
        if ssdSim < minSsdSim:
            minSsdSim = ssdSim
            bestMatchValue = value
    
    return bestMatchValue

#fuction that calcualtes ssd
def ssd(a, b):
    return ((np.asarray(a) - np.asarray(b))**2).sum()

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
    gameField = cv2.resize(gameField, (1000, 1000))
    
    #then we resize the field by slicing of some of the border to make it more symetrical
    resizedGameField = iu.sliceImageFrame(gameField, 1)
    
    #we then extract the individual game blocks from the field
    gameBlocks = iu.getFieldBlocks(resizedGameField, dimension)
    gameStateTupple = ()

    #now that we have the game blocks, we are ready to start extracting the numbers
    #print(len(gameBlocks))
    for block in gameBlocks:
        digitImages = iu.getNumbers(block)
        blockValue = generateNumber(digitImages)
        #print(blockValue)
        #if we get None or some number that is not power of two, we return None
        if blockValue == None: return None
        if blockValue != 0 and blockValue not in [2,4,8,16,32,64,128,256,512,1024,2048, 4096, 8192]: return None

        gameStateTupple = gameStateTupple + (blockValue, )
    
    return gameStateTupple

#suggests a move to be made for the game, based on the game representation
#global keyborad object
keyboard = Controller()


score = 0
#function takes the game state tupple and dimension and plays the next move
def suggestNextMove(gameState, dimension, algorithm):
    if gameState == None: return
    move = -1
    
    #determining the move based on the algorithm
    if algorithm == 'Random':
        move = randomPlayer.randomMove(gameState, dimension)
    elif algorithm == 'Greedy':
        move = greedy.greedyMove(gameState, dimension)
    elif algorithm == 'Monotonic Decreasing':
        move = mdp.nextMove(gameState, dimension)
    elif algorithm == 'Minimax':
        global score
        gameState = np.asarray(gameState)
        gameState = np.reshape(gameState, (dimension,dimension))
        board = Board.Board(gameState,score)
    
        move,score = alphabeta.getDirection(board, 5)# mdp.nextMove(gameState, dimension)
    
    if move == 0:
        keyboard.press(Key.up)
    elif move == 1:
        keyboard.press(Key.right)
    elif move == 2:
        keyboard.press(Key.down)
    elif move == 3:
        keyboard.press(Key.left)


#fuctions that make it all run together
activeFlag = True

def startPlaying(dimension, algorithm):
    global activeFlag
    activeFlag = True

    while activeFlag:
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        gameState = getGameStateMatrix(screenshot, dimension)
        suggestNextMove(gameState, dimension, algorithm)

def stopPlaying():
    global activeFlag
    activeFlag = False