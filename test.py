import imageutil as iu
import cv2
import bot2048 as bot
import pyautogui
import numpy as np
import time

#file for testing 
#pozz djuka

#waiting so I can open the game
time.sleep(5)

while True:
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gameState = bot.getGameStateMatrix(screenshot, 4)
    print(gameState)
    bot.suggestNextMove(gameState, 4)
