import wx
import imageutil as iu
import cv2
import bot2048 as bot
import pyautogui
import numpy as np
from threading import Thread
import time

#cao goca

#flag for knowing if the bot is active or not
botActive = True

#fuction to be executed when the button is pressed
def startPlayer():
    botActive = True
    time.sleep(5)
    while botActive:
        try:
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            gameState = bot.getGameStateMatrix(screenshot)
            bot.suggestNextMove(gameState)
        except:
            botActive = False
        

class BotGUI(wx.Frame):

    def __init__(self, *args, **kw):
        super(BotGUI, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        startButton = wx.Button(panel, label='Start', pos = (20, 20))
        startButton.Bind(wx.EVT_BUTTON, self.start)

        self.SetSize(400,200)
        self.SetTitle('2048 Bot')
        self.Centre()

    def start(self, e):
        Thread(target=startPlayer).start()

def main():
    app = wx.App()
    bot = BotGUI(None)
    bot.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()