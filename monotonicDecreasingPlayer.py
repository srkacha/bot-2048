import numpy as np
import random

#determines the future game state when a move is played
#returns game state matrix as np multi dim array
#direction can be 0 - up, 1 - right, 2- down and 3 - left
#gamestate matrix must be np array
def determineNextGameState(gameStateMatrix, dimension, direction, generateNewTile = False):
    nextMoveMatrix = 0
    if direction == 0:
        nextMoveMatrix = slideUp(gameStateMatrix, dimension)
    elif direction == 1:
        nextMoveMatrix = slideRight(gameStateMatrix, dimension)
    elif direction == 2:
        nextMoveMatrix = slideDown(gameStateMatrix, dimension)
    else: nextMoveMatrix = slideLeft(gameStateMatrix, dimension)

    #generating the new tile
    if generateNewTile:
        randomNumber = random.uniform(0, 1)
        generated = False
        while not generated:
            randomRow = random.randint(0, dimension - 1)
            randomCol = random.randint(0, dimension - 1)
            if nextMoveMatrix[randomRow][randomCol] == 0:
                nextMoveMatrix[randomRow][randomCol] = 2 if randomNumber<0.9 else 4
                print(generated, randomRow, randomCol)
                generated = True

    return nextMoveMatrix


def slideRight(gameStateMatrix, dimension):
    resultMatrix = np.zeros((dimension, dimension))
    for rowIndex, row in enumerate(gameStateMatrix):
        resultMatrix[rowIndex] = slide(row)
    return resultMatrix

def slide(row):
    result = np.zeros(len(row))
    skipFlag = False
    resultIndex = 0
    flippedRow = np.flip(row)
    filteredRow = flippedRow[flippedRow>0]
    for i, val in enumerate(filteredRow):
        if skipFlag == False and  i != len(filteredRow) - 1 and filteredRow[i] == filteredRow[i + 1]:
            result[resultIndex] = filteredRow[i]*2
            resultIndex += 1
            skipFlag = True
            continue
        elif skipFlag == False:
            result[resultIndex] = val
            resultIndex += 1
        if skipFlag: skipFlag = not skipFlag 

    return np.flip(result)

def slideUp(gameStateMatrix, dimension):
    transposed = np.transpose(gameStateMatrix)
    flipped = np.flip(transposed, 1)
    rightSlide = slideRight(transposed, dimension)
    flipped = np.flip(rightSlide, 1)
    transposed = np.transpose(flipped)
    return transposed

def slideDown(gameStateMatrix, dimension):
    transposed = np.transpose(gameStateMatrix)
    rightSlide = slideRight(transposed, dimension)
    transposed = np.transpose(rightSlide)
    return transposed

def slideLeft(gameStateMatrix, dimension):
    flipped = np.flip(gameStateMatrix, 1)
    rightSlide = slideRight(flipped, dimension)
    flipped = np.flip(rightSlide, 1)
    return flipped

#determines the next move to make
def nextMove(gameStateMatrix, recursionDepth = 3):
    return 0

def nextMoveRecursion():
    return 0


temp = (2, 8, 2, 0, 16, 2 ,0, 0, 2, 0, 0, 0, 0, 0, 2, 0)
temp = np.asarray(temp)
temp = temp.reshape(4,4)
result = determineNextGameState(temp, 4, 2, True)
print(result)