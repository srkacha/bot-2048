import imageutil as iu
import cv2
import bot2048 as bot
import pyautogui
import numpy as np
import time

#testing the essentials

#waits so i can open the game
time.sleep(5)

while True:
    
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    time1 = time.time_ns()
    gameState = bot.getGameStateMatrix(image)
    print(gameState)
    timediff = (time.time_ns() - time1)/1000000000
    print(timediff)
    #time.sleep(1)
    bot.suggestNextMove(gameState)
