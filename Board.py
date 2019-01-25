# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 15:39:10 2018

@author: djuricic
"""
import numpy as np
import random

class Board:
    
    def __init__(self, gameStateMatrix, score):
        self.gameStateMatrix = gameStateMatrix
        self.score = score
        self.dimension = gameStateMatrix.shape[0]
        self.targetPoints = 2048
        self.minimumWinScore = 18432
        
    #determines the future game state when a move is played
    #returns game state matrix as np multi dim array
    #direction can be 0 - up, 1 - right, 2- down and 3 - left
    #gamestate matrix must be np array
    # returns new Board object with new game state
    def move(self, direction, generateNewTile = False):
        nextMoveMatrix = 0
        if direction == 0:
            nextMoveMatrix = self.slideUp(self.gameStateMatrix)
        elif direction == 1:
            nextMoveMatrix = self.slideRight(self.gameStateMatrix)
        elif direction == 2:
            nextMoveMatrix = self.slideDown(self.gameStateMatrix)
        else: nextMoveMatrix = self.slideLeft(self.gameStateMatrix)
        
        return 1
    
    
    def getMaxValue(self):
        return np.amax(self.gameStateMatrix)
        
    
        #generating the new tile
# =============================================================================
#         if generateNewTile and 0 in nextMoveMatrix:
#             randomNumber = random.uniform(0, 1)
#             generated = False
#             while not generated:
#                 randomRow = random.randint(0, self.dimension - 1)
#                 randomCol = random.randint(0,self.dimension - 1)
#                 if nextMoveMatrix[randomRow][randomCol] == 0:
#                     nextMoveMatrix[randomRow][randomCol] = 2 if randomNumber<0.9 else 4
#                     generated = True
# =============================================================================
    
    
    def slide(self, row):
        result = np.zeros(len(row))
        skipFlag = False
        resultIndex = 0
        flippedRow = np.flip(row)
        filteredRow = flippedRow[flippedRow>0]
        for i, val in enumerate(filteredRow):
            if skipFlag == False and  i != len(filteredRow) - 1 and filteredRow[i] == filteredRow[i + 1]:
                result[resultIndex] = filteredRow[i]*2
                self.score += result[resultIndex]
                resultIndex += 1
                skipFlag = True
                continue
            elif skipFlag == False:
                result[resultIndex] = val
                resultIndex += 1
            if skipFlag: skipFlag = not skipFlag 
    
        return np.flip(result)
    
    # returns new matrix
    def slideRight(self, gameState):
        resultMatrix = np.zeros((self.dimension, self.dimension))
        for rowIndex, row in enumerate(gameState):
            resultMatrix[rowIndex] = self.slide(row)
        self.gameStateMatrix = resultMatrix
        return resultMatrix
    
    # returns new matrix
    def slideUp(self, gameState):
        transposed = np.transpose(gameState)
        flipped = np.flip(transposed, 1)
        rightSlide = self.slideRight(flipped)
        flipped = np.flip(rightSlide, 1)
        transposed = np.transpose(flipped)
        self.gameStateMatrix = transposed
        return transposed
    
    # returns new matrix
    def slideDown(self, gameState):
        transposed = np.transpose(gameState)
        rightSlide = self.slideRight(transposed)
        transposed = np.transpose(rightSlide)
        self.gameStateMatrix = transposed
        return transposed
    
    # returns new matrix
    def slideLeft(self, gameState):
        flipped = np.flip(gameState, 1)
        rightSlide = self.slideRight(flipped)
        flipped = np.flip(rightSlide, 1)
        self.gameStateMatrix = flipped
        return flipped
    
    def get_score(self):
        return self.score

    def set_score(self, x):
        self.score = x
    
    def get_gameStateMatrix(self):
        return self.gameStateMatrix
    
    def hasWon(self):
        if self.score < self.minimumWinScore:
            return False
        if self.targetPoints in self.gameStateMatrix: return True
        return False
    
    def isGameTerminated(self):
        
        if self.hasWon():
            return True
        else:
            if self.getNumberOfEmptyCells() == 0:
                if self.isMoveValid(0) or self.isMoveValid(1) or self.isMoveValid(2) or self.isMoveValid(3):
                    return False
                return True
        return False

    def isMoveValid(self, move):
        result = 0
        bCopy = Board(self.gameStateMatrix, self.score)
        if move == 0:
            result = bCopy.slideUp(bCopy.get_gameStateMatrix())
        elif move == 1:
            result = bCopy.slideRight(bCopy.get_gameStateMatrix())
        elif move == 2:
             result = bCopy.slideDown(bCopy.get_gameStateMatrix())
        else: 
            result = bCopy.slideLeft(bCopy.get_gameStateMatrix())
        if (result == self.gameStateMatrix).sum() == self.dimension**2:
            return False
        else:
            return True   
        
    def getNumberOfEmptyCells(self):
        return self.dimension*self.dimension - np.count_nonzero(self.gameStateMatrix)


    def setCell(self, i, j, val):
        self.gameStateMatrix[i][j] = val