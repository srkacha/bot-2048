import sys
import Board
import numpy as np
import math

globalScore = 0

def getDirection(gameState, dimension, depth):
    global globalScore
    gameState = np.asarray(gameState)
    gameState = np.reshape(gameState, (dimension,dimension))
    board = Board.Board(gameState,globalScore)
    direction, globalScore = alphabeta(board, dimension, depth, -sys.maxsize, +sys.maxsize, 0)
    board.move(direction)
    score = board.get_score()
    return direction,score



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

def heuristicScore(board, dimension, prob):
    if dimension == 4: weightMatrix = wmat4
    elif dimension == 5: weightMatrix = wmat5
    else: weightMatrix = wmat8

    score1 =  np.multiply(board.get_gameStateMatrix(), weightMatrix).sum()
    score2 =  np.multiply(board.get_gameStateMatrix(), np.transpose(weightMatrix)).sum()

    scores = np.array([score1, score2])
    score = np.max(scores)

    if board.get_gameStateMatrix()[0][0] != board.get_gameStateMatrix().max():
        score = score/100

    return score
 
    
def alphabeta(board, dimension, depth, alpha, beta, player, prob = 1):
    
    bestDirection = -1
    bestScore = 0
    
    if board.isGameTerminated():
        if board.hasWon():
            bestScore=sys.maxsize
        else:
            bestScore = min(board.get_score(), 1)
    elif depth==0:
        bestScore = heuristicScore(board, dimension, prob)
    else:
        if player==0:
            for m in range(0,4):
                if board.isMoveValid(m):
                    boardCopy = Board.Board(board.get_gameStateMatrix(), board.get_score())
                    boardCopy.move(m)
                    curDir, curScore = alphabeta(boardCopy, dimension,depth-1,alpha,beta,1, prob)
                    
                    if curScore>alpha:
                        alpha=curScore
                        bestDirection = m
                    if beta<=alpha:
                        break  #cutoff
                    
            bestScore = alpha
        else:
            boardAsArray = board.get_gameStateMatrix().ravel()
            possibleValues = np.array([2])
            for ind, val in enumerate(boardAsArray):
                if val == 0:    
                    for pv in possibleValues:
                        boardCopy = Board.Board(board.get_gameStateMatrix(), board.get_score())
                        i = int(ind / board.get_gameStateMatrix().shape[0])
                        j = int(ind % board.get_gameStateMatrix().shape[0])
                        boardCopy.setCell(i, j, pv)
                        
                        curDir, curScore = alphabeta(boardCopy,dimension, depth, alpha, beta, 0, prob*0.9 if pv == 2 else prob*0.1)
                        
                        if curScore<beta:
                            beta=curScore
                        if beta<=alpha:
                            break
                    else:
                        continue
                    break
                        
            bestScore = beta
        
        
    return bestDirection, bestScore