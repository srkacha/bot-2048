import numpy as np
import time 

def determineNextGameState(gameStateMatrix, dimension, direction):
    nextMoveMatrix = 0
    #startTime = time.time_ns()
    if direction == 0:
        nextMoveMatrix = slideUp(gameStateMatrix, dimension)
    elif direction == 1:
        nextMoveMatrix = slideRight(gameStateMatrix, dimension)
    elif direction == 2:
        nextMoveMatrix = slideDown(gameStateMatrix, dimension)
    else: nextMoveMatrix = slideLeft(gameStateMatrix, dimension)
    #endTime = time.time_ns()
    #print(endTime - startTime)
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

def isMoveValid(gameStateMatrix, dimension, move):
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

def generateWeightedMatrix(dimension = 4, alpha = 0.25):
    maxWeight = 1
    flip = False
    matrix = np.zeros((dimension, dimension))
    for row in matrix:
        for index in range(0, dimension):
            row[index] = maxWeight
            maxWeight = maxWeight*alpha
        if flip:
            row = np.flip(row)
        flip = not flip
    return matrix

#weighted matrixes for different game dimensions
wmat4 = generateWeightedMatrix(alpha = 0.25)
wmat5 = generateWeightedMatrix(5, alpha = 0.25)
wmat8 = generateWeightedMatrix(8, alpha = 0.25)

cornerMat = np.matrix([[10,8,7,6.5],
 [.5,.7,1,3],
 [-.5,-1.5,-1.8,-2],
 [-3.8,-3.7,-3.5,-3]])

cornerMat2 = np.matrix([[512, 128, 32, 8],[128, 32, 8, 2],[0.5, 0.125, 0, -4],[0.125, 0, -4, -32]])

def evaluateScore(gameState, dimension = 4):
    if dimension == 4: weightMatrix = wmat4
    elif dimension == 5: weightMatrix = wmat5
    else: weightMatrix = wmat8
    
    freeSpace = (gameState == 0).sum()
    finalScore = 0

    #weights
    penaltyWeight = 0.05
    freeSapceBonusWeigth = 0.7
   
    #monotonicity property
    score1 =  np.multiply(gameState, weightMatrix).sum()
    score2 =  np.multiply(gameState, np.transpose(weightMatrix)).sum()

    #calculating the penalty
    penalty = 0
    for rowIndex, row in enumerate(gameState):
        for colIndex, element in enumerate(row):
            if rowIndex<dimension - 1:
                penalty += abs(gameState[rowIndex][colIndex] - gameState[rowIndex + 1][colIndex])
            if colIndex < dimension - 1:
                penalty += abs(gameState[rowIndex][colIndex] - gameState[rowIndex][colIndex + 1])
            if rowIndex>0:
                penalty += abs(gameState[rowIndex][colIndex] - gameState[rowIndex - 1][colIndex])
            if colIndex >0:
                penalty += abs(gameState[rowIndex][colIndex] - gameState[rowIndex][colIndex - 1])

    score = np.max([score1, score2])
    finalScore = score

    if gameState.max() != gameState[0][0]: finalScore = score/100
    return finalScore


def expectimax(gameStateMatrix, dimension = 4, player = 1, depth = 4, lastGenerated = -1):
    bestMove = -1
    bestScore = -1
    if depth == 0:
        return evaluateScore(gameStateMatrix, dimension), -1
    if player == 1: #human player
        for move in range(0, 4):
            if isMoveValid(gameStateMatrix, dimension, move):
                newGameState = determineNextGameState(gameStateMatrix, dimension, move)
                score, dumpMove = expectimax(newGameState, dimension, 0, depth - 1, lastGenerated)
                if score > bestScore:
                    bestScore = score
                    bestMove = move
    elif player == 0: #computer generating random tile
        averageScore = 0
        for randomTileValue in [2, 4]:
            if lastGenerated == randomTileValue and lastGenerated == 4: break
            gameStateAsArray = gameStateMatrix.ravel()
            for index in np.where(gameStateAsArray == 0)[0]:
                    freeSpace = (gameStateMatrix == 0).sum()
                    gameStateAsArrayCopy = np.copy(gameStateAsArray)
                    gameStateAsArrayCopy[index] = randomTileValue
                    gameStateMatrixReshaped = np.reshape(gameStateAsArrayCopy, (dimension, dimension))
                    scoreB, moveB = expectimax(gameStateMatrixReshaped, dimension, 1, depth - 1, randomTileValue)
                    
                    if randomTileValue == 2:
                        averageScore += scoreB*(1/freeSpace)*0.9
                    else:
                        averageScore += scoreB*0.1*(1/freeSpace)
        return averageScore, -1
    return bestScore, bestMove

def nextMove(gameStateMatrix, dimension):
    gameStateMatrix = np.asarray(gameStateMatrix)
    gameStateMatrix = np.reshape(gameStateMatrix, (dimension,dimension))
    freeSpace = (gameStateMatrix == 0).sum()
    if freeSpace > 4:
        score, move = expectimax(gameStateMatrix, dimension, depth=3)
    elif freeSpace > 2:
        score, move = expectimax(gameStateMatrix, dimension, depth=4)
    else: score, move = expectimax(gameStateMatrix, dimension, depth=5)
    return move