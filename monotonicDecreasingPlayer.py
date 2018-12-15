import numpy as np
import random

#determines the future game state when a move is played
#returns game state matrix as np multi dim array
#direction can be 0 - up, 1 - right, 2- down and 3 - left
#gamestate matrix must be np array
def determineNextGameState(gameStateMatrix, dimension, direction, generateNewTile = True):
    nextMoveMatrix = 0
    if direction == 0:
        nextMoveMatrix = slideUp(gameStateMatrix, dimension)
    elif direction == 1:
        nextMoveMatrix = slideRight(gameStateMatrix, dimension)
    elif direction == 2:
        nextMoveMatrix = slideDown(gameStateMatrix, dimension)
    else: nextMoveMatrix = slideLeft(gameStateMatrix, dimension)

    #generating the new tile
    if generateNewTile and 0 in nextMoveMatrix:
        randomNumber = random.uniform(0, 1)
        generated = False
        while not generated:
            randomRow = random.randint(0, dimension - 1)
            randomCol = random.randint(0, dimension - 1)
            if nextMoveMatrix[randomRow][randomCol] == 0:
                nextMoveMatrix[randomRow][randomCol] = 2 if randomNumber<0.9 else 4
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
    rightSlide = slideRight(flipped, dimension)
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
def nextMove(gameStateMatrix, dimension, recursionDepth = 3):
    gameStateArray = np.asarray(gameStateMatrix)
    reshaped = gameStateArray.reshape((dimension, dimension))
    move, score = nextMoveRecursion(reshaped, dimension, recursionDepth, recursionDepth)
    return move

#recursivly calculates the heursitic score for a given depth and base parameter
#base parameter determines how much the score is affected the deeper the algorithm goes
def nextMoveRecursion(gameStateMatrix, dimension, depth, maxDepth, base = 0.9):
    bestScore = -1
    bestMove = 0
    for move in range(0, 4):
        #print(move)
        if isMoveValid(gameStateMatrix, dimension, move):
            newGameState = determineNextGameState(gameStateMatrix, dimension, move, generateNewTile=False)
            score = evaluateScore(newGameState, dimension)
            if depth != 0:
                result_move, result_score = nextMoveRecursion(newGameState, dimension, depth - 1, maxDepth)
                score += result_score*pow(base, maxDepth - depth + 1)
            
            if score > bestScore:
                bestScore = score
                bestMove = move
    return bestMove, bestScore

#determines if the move is valid or not
#move can be 0, 1, 2 or 3
def isMoveValid(gameStateMatrix, dimension, move ):
    result = 0
    if move == 0:
        result = slideUp(gameStateMatrix, dimension)
    elif move == 1:
        result = slideRight(gameStateMatrix, dimension)
    elif move == 2:
        result = slideDown(gameStateMatrix, dimension)
    else: result = slideLeft(gameStateMatrix, dimension)

    if (result == gameStateMatrix).sum() == dimension**2:
        return False
    else:
        return True


def evaluateScore(gameState, dimension, commonRatio=0.15 ):
    
    linearWeightedVal = 0
    weight = 1.
    invert = False
    
    for y in range(0,dimension):
            for x in range(0,dimension):
                b_x = x
                b_y = y
                if invert:
                    b_x = dimension - 1 - x
                #linearW
                currVal=gameState[b_y,b_x]
                
                linearWeightedVal += currVal*weight
                weight *= commonRatio
            invert = not invert
            
    linearWeightedVal2 = 0
    invert = False
    weight = 1.
    
    for x in range(0,dimension):
        for y in range(0,dimension):
            b_x = x
            b_y = y
            if invert:
                b_y = dimension - 1 - y
            #linearW
            currVal=gameState[b_y,b_x]
            
            linearWeightedVal2 += currVal*weight
            weight *= commonRatio
        invert = not invert
        
    
    # linearWeightedVal3 = 0
    # invert = False
    # weight = 1.
    
    # for y in range(0,dimension):
    #     for x in range(0,dimension):
    #         b_x = x
    #         b_y = dimension - 1 - y
    #         if invert:
    #             b_x = dimension - 1 - x
    #         #linearW
    #         currVal=gameState[b_y,b_x]
           
    #         linearWeightedVal3 += currVal*weight
    #         weight *= commonRatio
    #     invert = not invert
        
    # linearWeightedVal4 = 0
    # invert = False
    # weight = 1.
    
    # for x in range(0,dimension):
    #     for y in range(0,dimension):
    #         b_x = dimension - 1 - x
    #         b_y = y
    #         if invert:
    #             b_y = dimension - 1 - y
    #         #linearW
    #         currVal=gameState[b_y,b_x]
           
    #         linearWeightedVal4 += currVal*weight
    #         weight *= commonRatio
    #     invert = not invert
        
        
    # linearWeightedVal5 = 0
    # invert = True
    # weight = 1.
    
    # for y in range(0,dimension):
    #     for x in range(0,dimension):
    #         b_x = x
    #         b_y = y
    #         if invert:
    #             b_x = dimension - 1 - x
    #         #linearW
    #         currVal=gameState[b_y,b_x]
          
    #         linearWeightedVal5 += currVal*weight
    #         weight *= commonRatio
    #     invert = not invert
        
    # linearWeightedVal6 = 0
    # invert = True
    # weight = 1.
    

    # for x in range(0,dimension):
    #     for y in range(0,dimension):
    #         b_x = x
    #         b_y = y
    #         if invert:
    #             b_y = dimension - 1 - y
    #         #linearW
    #         currVal=gameState[b_y,b_x]
            
    #         linearWeightedVal6 += currVal*weight
    #         weight *= commonRatio
    #     invert = not invert
        
    
    # linearWeightedVal7 = 0
    # invert = True
    # weight = 1.
    
    # for y in range(0,dimension):
    #     for x in range(0,dimension):
    #         b_x = x
    #         b_y = dimension - 1 - y
    #         if invert:
    #             b_x = dimension - 1 - x
    #         #linearW
    #         currVal=gameState[b_y,b_x]
            
    #         linearWeightedVal7 += currVal*weight
    #         weight *= commonRatio
    #     invert = not invert
        
    # linearWeightedVal8 = 0
    # invert = True
    # weight = 1.
    
    # for x in range(0,dimension):
    #     for y in range(0,dimension):
    #         b_x = dimension - 1 - x
    #         b_y = y
            
    #         if invert:
    #             b_y = dimension - 1 - y
            
    #         #linearW
    #         currVal=gameState[b_y,b_x]
      
    #         linearWeightedVal8 += currVal*weight
    #         weight *= commonRatio
    #     invert = not invert
        
    
    maxVal = max(linearWeightedVal,linearWeightedVal2)#,linearWeightedVal3,linearWeightedVal4,linearWeightedVal5,linearWeightedVal6,linearWeightedVal7,linearWeightedVal8)

    return maxVal

