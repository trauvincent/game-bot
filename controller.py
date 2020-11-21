from keys import *
import time
import cv2
import pyautogui
from playback import playActions
import schedule
import sys
import threading
import pytesseract
import numpy as np
import math
from win32gui import FindWindow, GetWindowRect

def getMaterials(box):
    x = threading.Thread(target=hoverFatigue)
    x.start()
    time.sleep(3)

    fatigueBox = pyautogui.locateOnScreen('images/fpPoints.png', confidence = 0.8, region = box)
    x.join()
    materials = processImg(fatigueBox)

    pyautogui.moveTo(554, 630)
    pressMouse()

    pressButton('tab')
    clickCenter('remove')
    clickCenter('material')
    for x in range(len(str(materials))):
        pressButton(str(materials)[x])


    barLocation = pyautogui.locateCenterOnScreen('images/fpBar.png' , confidence= 0.9)
    pyautogui.moveTo(barLocation)
    clickCenter('ok')
    pressButton('esc')
    return materials/5

    return materials/5


def processImg(box):
    img = pyautogui.screenshot(region=box)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.medianBlur(img, 3)

    string = pytesseract.image_to_string(img)
    string = string.split(": ")[1]
    string =  string.split("/")[0]


    number = float(string)
    materials = math.ceil(number/8) * 5
    materials = int(materials)
    return materials

def buyTourney(runs):
    pressButton("SPACE")
    pressButton("DOWN")
    pressButton("SPACE")
    x = threading.Thread(target=holdShift)
    x.start()
    clickCenter('goldDragon')
    x.join()

    for digit in str(runs):
        pressButton(digit)

    clickCenter('ok')

    pressButton("space")
    pressButton("esc")


def main():
    time.sleep(10)
    tourney(9)

def holdShift():
    keys = Keys()
    keys.directKey("lshift")
    sleep(5)
    keys.directKey("lshift", keys.key_release)

def hoverFatigue():
    barLocation = pyautogui.locateCenterOnScreen('images/fpBar.png' , confidence= 0.9)
    pyautogui.moveTo(barLocation)
    pyautogui.move(50,0)
    pyautogui.move(100,0,10)

def gameWindow():
    gameHandle = FindWindow(None, "Dungeon Fighter Online")
    gameWindow = GetWindowRect(gameHandle)
    gameBox = (gameWindow[0], gameWindow[1], gameWindow[2]-gameWindow[0], gameWindow[3]-gameWindow[1])
    return gameBox

def tourney(characters):
    box = gameWindow()
    try:
        for x in range(characters):
            runs = getMaterials(box)
            playActions("leaveSeria.json")

            playActions("toSiran.json")

            purpleQuest()

            playActions("siranToJun.json")

            glowQuest()
            buyTourney(runs)
            playActions("junToTourney.json")
            while pyautogui.locateOnScreen('images/stop.png', confidence = 0.99, region = box) is None:
                emptyHpBar = pyautogui.locateOnScreen('images/enemyHp.png' , confidence= 0.9, region = box)
                if emptyHpBar:
                    pressButton("0")
                    for x in range(5):
                        pressButton("X")
                    time.sleep(1)
                    pressButton("F10")
                else:
                    pressButton('SPACE')
                    playActions("basicAttack.json")
            pressButton("F12")
            time.sleep(10)
            pressButton("space")
            pressButton("ESC")
            clickCenter('selectChar', 0.8)
            time.sleep(5)
            pressButton("RIGHT")
            pressButton("SPACE")
            time.sleep(15)
    except KeyboardInterrupt:
        sys.exit()

def pressButton(button):
    keys = Keys()
    keys.directKey(button)
    time.sleep(0.1)
    keys.directKey(button, keys.key_release)
    time.sleep(1)

def pressMouse():
    keys = Keys()
    keys.directMouse(buttons=keys.mouse_lb_press)
    time.sleep(0.1)
    keys.directMouse(buttons=keys.mouse_lb_release)
    time.sleep(1)

def purpleQuest():
    playActions("questWindow.json")
    clickCenter('purpleQuest', 0.9)
    clickCenter('complete', 0.9)
    pressButton("space")

def glowQuest():
    playActions("questWindow.json")
    clickCenter('glowQuest', 0.9)
    playActions("questChat.json")
    playActions("finishQuest.json")


def clickCenter(imgName, con = 0.99):
    location = pyautogui.locateCenterOnScreen(f'images/{imgName}.png', confidence = con)
    pyautogui.moveTo(location)
    pressMouse()

if __name__ == '__main__':
    main()
