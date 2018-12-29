import imageutil as iu
import cv2
import bot2048 as bot
import pyautogui
import numpy as np
import time
import imageio

#file for testing 
#pozz djuka

#waiting so I can open the game
time.sleep(5)

dim = 4

while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gameState = bot.getGameStateMatrix(screenshot, dim)
    #print(gameState)
    bot.suggestNextMove(gameState, dim, 'Monotonic Decreasing')

