import sys
import Board
import numpy as np
import math

def getDirection(board, depth):
    test = 0
    direction, score = alphabeta(board, depth, -sys.maxsize, +sys.maxsize, 0)
    board.move(direction)
    score = board.get_score()
    return direction,score

weightMatrix = np.matrix([[14348907, 4782969, 1594323, 531441],
                                [6561,19683,59049,177147],
                                [2187, 729, 243, 81],
                                [1,3,9,27]])


def heuristicScore(board):
    # score = board.get_score()
   
    # maxVal = board.getMaxValue()
    # gameStateMatrix = board.get_gameStateMatrix()
    # clustScore = calculateClusteringScore(board.get_gameStateMatrix())
    # if maxVal != gameStateMatrix[0][0]:
    #    score /=2 
    #    clustScore /= 20
    # hs = int((score + math.log(score+1)*board.getNumberOfEmptyCells() - clustScore)) 
    score1 =  np.multiply(board.get_gameStateMatrix(), weightMatrix).sum()
    score2 =  np.multiply(board.get_gameStateMatrix(), np.transpose(weightMatrix)).sum()
    score3 =  np.multiply(board.get_gameStateMatrix(), np.flip(weightMatrix, 1)).sum()
    score4 =  np.multiply(board.get_gameStateMatrix(), np.flip(np.transpose(weightMatrix), 1)).sum()
    score5 =  np.multiply(board.get_gameStateMatrix(), np.flip(weightMatrix, 0)).sum()
    score6 =  np.multiply(board.get_gameStateMatrix(), np.flip(np.transpose(weightMatrix), 0)).sum()
    score7 =  np.multiply(board.get_gameStateMatrix(), np.flip(np.flip(weightMatrix, 1), 0)).sum()
    score8 =  np.multiply(board.get_gameStateMatrix(), np.flip(np.flip(np.transpose(weightMatrix), 1), 0)).sum()

    return np.max([score1, score2, score3, score4 ,score5, score6, score7, score8])

def calculateClusteringScore(gameStateMatrix):

    clusteringScore = 0
    
    neighbors = np.array([-1,0,1])
    
    for i,row in enumerate(gameStateMatrix):
        sum = 0
        numOfNeighbors=1
        for j,val in enumerate(row):
            if gameStateMatrix[i,j] == 0: continue
        
            numOfNeighbors=0
            sum = 0
            for k in neighbors:
                x = i+k
                if x<0 or x>=gameStateMatrix.shape[0]:
                    continue
                for l in neighbors:
                    y = j+l
                    if y < 0 or y>=gameStateMatrix.shape[0]:
                        continue
                    
                    if gameStateMatrix[x,y]>0:
                        numOfNeighbors+=1
                        sum+=abs(gameStateMatrix[i][j] - gameStateMatrix[x][y])
        
        clusteringScore += sum/numOfNeighbors;
    
    return clusteringScore
 
    
def alphabeta(board, depth, alpha, beta, player):
    
    bestDirection = -1
    bestScore = 0
    
    if board.isGameTerminated():
        if board.hasWon():
            bestScore=sys.maxsize
        else:
            bestScore = min(board.get_score(), 1)
    elif depth==0:
        bestScore = heuristicScore(board)
    else:
        if player==0:
            for m in range(0,4):
                if board.isMoveValid(m):
                    boardCopy = Board.Board(board.get_gameStateMatrix(), board.get_score())
                    boardCopy.move(m)
                    curDir, curScore = alphabeta(boardCopy,depth-1,alpha,beta,1)
                    
                    if curScore>alpha:
                        alpha=curScore
                        bestDirection = m
                    if beta<=alpha:
                        break  #cutoff
                    
            bestScore = alpha
        else:
            boardAsArray = board.get_gameStateMatrix().ravel()
            possibleValues = np.array([2,4])
            for ind, val in enumerate(boardAsArray):
                if val == 0:    
                    for pv in possibleValues:
                        boardCopy = Board.Board(board.get_gameStateMatrix(), board.get_score())
                        i = int(ind / board.get_gameStateMatrix().shape[0])
                        j = int(ind % board.get_gameStateMatrix().shape[0])
                        boardCopy.setCell(i, j, pv)
                        
                        curDir, curScore = alphabeta(boardCopy, depth-1, alpha, beta, 0)
                        
                        if curScore<beta:
                            beta=curScore
                        if beta<=alpha:
                            break
                    else:
                        continue
                    break
                        
            bestScore = beta
        
        
    return bestDirection, bestScore