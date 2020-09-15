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

def getMaterials():


    time.sleep(5)

    x = threading.Thread(target=hoverFatigue)
    x.start()
    time.sleep(1)

    fatigueBox = None
    while fatigueBox == None:
        fatigueBox = pyautogui.locateOnScreen('images/fpPoints.png', confidence = 0.5)
        time.sleep(0.5)
    x.join()
    img = pyautogui.screenshot(region=fatigueBox)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.blur(img,(5,5))
    string = pytesseract.image_to_string(img)
    string =  string.split("/")[0]
    string = string.split(": ")[1]
    number = float(string)
    materials = math.ceil(number/8) * 5
    materials = int(materials)
    time.sleep(1)

    safeLocation = pyautogui.locateCenterOnScreen('images/safe.png', confidence = 0.55)

    pyautogui.moveTo(safeLocation)
    pressMouse()

    time.sleep(1)
    vaultLocation = pyautogui.locateCenterOnScreen('images/accountVault.png')
    pyautogui.moveTo(vaultLocation)
    pressMouse()
    time.sleep(1)
    removeLocation = pyautogui.locateCenterOnScreen('images/remove.png')
    pyautogui.moveTo(removeLocation)
    pressMouse()
    time.sleep(1)
    matLocation = pyautogui.locateCenterOnScreen('images/material.png')
    pyautogui.moveTo(matLocation)
    pressMouse()
    time.sleep(1)
    for x in range(len(str(materials))):
        pressButton(str(materials)[x])
        time.sleep(0.5)
    okLocation = pyautogui.locateCenterOnScreen('images/ok.png')
    pyautogui.moveTo(okLocation)
    pressMouse()
    time.sleep(1)
    pressButton('esc')


def buyTourney():
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("DOWN")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    x = threading.Thread(target=holdShift)
    x.start()
    itemLocation = pyautogui.locateCenterOnScreen('images/goldDragon.png')
    pyautogui.moveTo(itemLocation)
    pressMouse()
    x.join()
    time.sleep(0.5)
    pressButton("9")
    time.sleep(0.5)
    pressButton("9")
    okLocation = pyautogui.locateCenterOnScreen('images/ok.png')
    pyautogui.moveTo(okLocation)
    pressMouse()
    time.sleep(1)
    pressButton("space")
    pressButton("esc")

def main():
    tourney()

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
def tourney():
    try:
        for x in range(3):
            time.sleep(5)
            getMaterials()
            playActions("leaveSeria.json")
            time.sleep(1)
            playActions("toSiran.json")
            time.sleep(1)
            purpleQuest()
            time.sleep(1)
            playActions("siranToJun.json")
            time.sleep(1)
            glowQuest()
            time.sleep(1)
            buyTourney()
            time.sleep(1)
            playActions("junToTourney.json")
            time.sleep(1)

            schedule.every(2).seconds.do(run_threaded, pressButton, button = '0')
            schedule.every(0.75).seconds.do(pressButton, button = 'X')
            schedule.every(1.75).seconds.do(run_threaded, pressButton, button = 'F10')
            schedule.every(1).seconds.do(run_threaded, pressButton, button = 'SPACE')

            print("pass loop")

            while True:
                retryLocation = pyautogui.locateOnScreen('images/retry.png' , confidence= 0.99)

                if retryLocation is None:
                    schedule.run_pending()
                    time.sleep(1)

                else:
                    schedule.clear()
                    print("f while loop")
                    time.sleep(1)
                    pressButton("F12")
                    time.sleep(5)
                    pressButton("ESC")
                    characterLocation = pyautogui.locateCenterOnScreen('images/selectChar.png', confidence = 0.8)
                    pyautogui.moveTo(characterLocation)
                    pressMouse()
                    time.sleep(5)
                    pressButton("RIGHT")
                    time.sleep(1)
                    pressButton("SPACE")
                    break
    except KeyboardInterrupt:
        schedule.clear()
        sys.exit()


def pressButton(button):
    keys = Keys()
    keys.directKey(button)
    sleep(0.1)
    keys.directKey(button, keys.key_release)

def pressMouse():
    keys = Keys()
    keys.directMouse(buttons=keys.mouse_lb_press)
    sleep(0.1)
    keys.directMouse(buttons=keys.mouse_lb_release)

def run_threaded(job_func, *args, **kwargs):

   job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
   job_thread.start()

def purpleQuest():
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("DOWN")
    time.sleep(0.5)
    pressButton("DOWN")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    questLocation = pyautogui.locateCenterOnScreen('images/purpleQuest.png', confidence = 0.8)
    pyautogui.moveTo(questLocation)
    pressMouse()
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")

def glowQuest():
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("DOWN")
    time.sleep(0.5)
    pressButton("DOWN")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    questLocation = pyautogui.locateCenterOnScreen('images/glowingQuest.png', confidence = 0.8)
    pyautogui.moveTo(questLocation)
    pressMouse()
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(5)
    pressButton("ESC")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("SPACE")
    time.sleep(0.5)
    pressButton("ESC")
if __name__ == '__main__':

    main()




    #number of characters should be in range
