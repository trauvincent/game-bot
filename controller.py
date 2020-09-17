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
    x = threading.Thread(target=hoverFatigue)
    x.start()
    time.sleep(3)
    fatigueBox = pyautogui.locateOnScreen('images/fpPoints.png', confidence = 0.5)
    x.join()
    materials = processImg(fatigueBox)

    clickCenter('safe', 0.55)
    clickCenter('vault')
    clickCenter('remove')
    clickCenter('material')

    for x in range(len(str(materials))):
        pressButton(str(materials)[x])
        time.sleep(1)

    clickCenter('ok')
    pressButton('esc')

def processImg(box):
    img = pyautogui.screenshot(region=box)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.blur(img,(5,5))

    string = pytesseract.image_to_string(img)
    string =  string.split("/")[0]
    string = string.split(": ")[1]
    number = float(string)

    materials = math.ceil(number/8) * 5
    materials = int(materials)

    return materials

def buyTourney():
    pressButton("SPACE")
    time.sleep(1)
    pressButton("DOWN")
    time.sleep(1)
    pressButton("SPACE")
    time.sleep(1)
    x = threading.Thread(target=holdShift)
    x.start()
    clickCenter('goldDragon')
    x.join()

    pressButton("9")
    time.sleep(1)
    pressButton("9")
    clickCenter('ok')
    time.sleep(1)
    pressButton("space")
    pressButton("esc")

def main():
    time.sleep(5)
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
        for x in range(2):
            getMaterials()
            playActions("leaveSeria.json")
            playActions("toSiran.json")
            purpleQuest()
            playActions("siranToJun.json")
            glowQuest()
            buyTourney()
            playActions("junToTourney.json")

            schedule.every(1.1).seconds.do(run_threaded, pressButton, button = 'X')
            schedule.every(2).seconds.do(run_threaded, pressButton, button = 'SPACE')
            counter = 0

            while pyautogui.locateOnScreen('images/stop.png', confidence = 0.99) is None:
                retryLocation = None
                schedule.run_pending()
                emptyHpBar = pyautogui.locateOnScreen('images/enemyHp.png' , confidence= 0.99)

                if emptyHpBar:
                    pressButton("0")
                    time.sleep(0.5)
                    for x in range(5):
                        pressButton("X")
                        time.sleep(0.5)

                if(counter ==  3):
                    retryLocation = pyautogui.locateOnScreen('images/retry.png' , confidence= 0.99)
                    counter = 0

                if retryLocation:
                    pressButton("F10")

                counter = counter + 1
                time.sleep(1)

            schedule.clear()
            pressButton("F12")
            time.sleep(10)
            pressButton("ESC")
            clickCenter('selectChar', 0.8)
            time.sleep(5)
            pressButton("RIGHT")
            pressButton("SPACE")
            time.sleep(5)

    except KeyboardInterrupt:
        schedule.clear()
        sys.exit()

def pressButton(button):
    keys = Keys()
    keys.directKey(button)
    time.sleep(0.1)
    keys.directKey(button, keys.key_release)


def pressMouse():
    keys = Keys()
    keys.directMouse(buttons=keys.mouse_lb_press)
    time.sleep(0.1)
    keys.directMouse(buttons=keys.mouse_lb_release)
    time.sleep(1)

def run_threaded(job_func, *args, **kwargs):
   job_thread = threading.Thread(target=job_func, args=args, kwargs=kwargs)
   job_thread.start()

def purpleQuest():
    playActions("questWindow.json")
    clickCenter('purpleQuest', 0.9)
    playActions("finishQuest.json")

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
