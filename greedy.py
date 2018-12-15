import numpy as np

nextMove = 0
previousGameState = 0
firstMove = True

#function takes game state tupple and returns one of the folowing values
# 0 - up
# 1 - right
# 2 - down
# 3 - left
def greedyMove(gameStateTupple, dimension):
    global previousGameState
    global nextMove
    global firstMove

    #if it's the first move
    if firstMove: 
        previousGameState = np.full((dimension, dimension), 0)
        firstMove = not firstMove
    
    gameStateArray = np.asarray(gameStateTupple)
    reshapedArray = np.reshape(gameStateArray, (dimension,dimension))

    lastNum = 0 #helps to skip summing middle twos in the 2,2,2,2 situation

    #now we determine the sums
    rowSum = 0
    colSum = 0

    #row sum
    for row in reshapedArray:
        filteredRow = row[row>0] #filtered values without zeros
        for index, element in enumerate(filteredRow):
            if index != len(filteredRow) - 1 and filteredRow[index] == filteredRow[index+1] and lastNum != filteredRow[index]:
                rowSum += 2*filteredRow[index]
                lastNum = filteredRow[index + 1]
            else:
                lastNum = 0 #we skipped the repeating number so we reset the lastNUm value

    #column sum
    lastNum = 0
    transGameState = reshapedArray.transpose()
    for row in transGameState:
        filteredRow = row[row>0] #filtered values without zeros
        for index, element in enumerate(filteredRow):
            if index != len(filteredRow) - 1 and filteredRow[index] == filteredRow[index+1] and lastNum != filteredRow[index]:
                colSum += 2*filteredRow[index]
                lastNum = filteredRow[index + 1]
            else:
                lastNum = 0 #we skipped the repeating number so we reset the lastNUm value

    
    #now we have the sums, next we determine the move

    if rowSum != 0 or colSum !=0:
        if colSum >= rowSum: nextMove = 0
        else: nextMove = 1
    else: #this means that row and col sum is 0
        if (reshapedArray == previousGameState).sum() == dimension**2:
            nextMove = nextMove + 1
        else:
            nextMove = 0
    
    previousGameState = reshapedArray

    return nextMove
