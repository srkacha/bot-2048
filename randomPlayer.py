import random
import numpy as np

repeatedMoves = 0
previousGameState = 0
firstMove = True

#random move generator based on simple logic, going up is the best, followed by right, then down and left at the end
def randomMove(gameStateTupple, dimension):
    global previousGameState
    global repeatedMoves
    global firstMove

    nextMove = 0

    gameStateArray = np.asarray(gameStateTupple)
    reshapedArray = np.reshape(gameStateArray, (dimension,dimension))

    #if it's the first move
    if firstMove: 
        previousGameState = np.full((dimension, dimension), 0)
        firstMove = not firstMove
    
    randomNumber = random.uniform(0, 1)

    if (previousGameState == reshapedArray).sum() == dimension**2:
        repeatedMoves += 1
    else: repeatedMoves = 0

    if repeatedMoves == 0:
        if randomNumber < 0.75: nextMove = 0
        elif randomNumber < 0.9: nextMove = 1
        elif randomNumber < 0.995: nextMove = 2
        else: nextMove = 3
    elif repeatedMoves == 1:
        if randomNumber < 0.80: nextMove = 1
        elif randomNumber < 0.5: nextMove = 2
        else: nextMove = 3
    elif repeatedMoves == 2:
        if randomNumber < 0.95: nextMove = 2
        else: nextMove = 3
    else: nextMove = 3

    previousGameState = reshapedArray

    return nextMove
