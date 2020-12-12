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

    fatigueBox = pyautogui.locateOnScreen('images/fpPoints.png', confidence = 0.7, region = box)


    x.join()
    materials = processImg1(fatigueBox)


    materials = subtractInvMaterials(box, materials)



    pyautogui.moveTo(554, 630)
    pressMouse()

    pressButton('tab')
    clickCenter('remove')
    clickCenter('material')
    for x in range(len(str(materials))):
        pressButton(str(materials)[x])



    clickCenter('ok')
    pressButton('esc')

    time.sleep(1)
    return materials/5



def subtractInvMaterials(box, materials):
    pressButton("i")
    if pyautogui.locateOnScreen('images/questMaterial.png', confidence = 0.8, region = box) is None:
        clickCenter('questTab')

    number = pyautogui.locateOnScreen('images/questMaterial.png', confidence = 0.7, region = box)
    print(number)
    if number:
        region = (int(number.left + 0.45*number.width), number.top, int(0.55 *number.width), int(number.height*0.4))
        invMaterials = processImg2(region) * 5
    else:
        invMaterials = 0

    materials = materials - invMaterials
    if materials <= 0:
        materials = 0
    pressButton("i")
    time.sleep(1)
    return materials

def processImg1(box):


    string = prepareImg(box)
    string = string.split(": ")[1]
    string =  string.split("/")[0]


    number = float(string)
    materials = math.ceil(number/8) * 5
    materials = int(materials)
    return materials

def processImg2(box):
    string = prepareImg(box)
    print(string)
    string = ''.join(char for char in string if char.isdigit())
    if string:
        invMaterials = int(string)
    else:
        invMaterials = 0
    return invMaterials

def whiteMask(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    # change it according to your need !
    lower_white = np.array([0,0,0], dtype=np.uint8)
    upper_white = np.array([0,0,255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    image = cv2.bitwise_and(image,image, mask= mask)



    return image

def prepareImg(box):
    img = pyautogui.screenshot(region=box)

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = whiteMask(img)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.blur(img,(2,2))

    string = pytesseract.image_to_string(img)

    return string

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
    tourney(int(sys.argv[1]))

def holdShift():
    keys = Keys()
    keys.directKey("lshift")
    sleep(5)
    keys.directKey("lshift", keys.key_release)

def hoverFatigue():
    barLocation = pyautogui.locateCenterOnScreen('images/fpBar2.png' , confidence= 0.9)
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
            time.sleep(1)
            #purpleQuest()
            playActions("siranToJun.json")
            #glowQuest()
            buyTourney(runs)
            playActions("junToTourney.json")

            bot(box)
            exitTourney()
            changeCharacter()
    except KeyboardInterrupt:
        sys.exit()

def bot(box):
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

def exitTourney():
    pressButton("F12")
    time.sleep(10)
    pressButton("space")


def changeCharacter():
    pressButton("ESC")
    clickCenter('selectChar', 0.8)
    time.sleep(5)
    pressButton("RIGHT")
    pressButton("SPACE")
    time.sleep(15)

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
    clickCenter('acceptQuest', 0.9)
    time.sleep(3)
    clickCenter('complete', 0.9)
    pressButton("space")

def glowQuest():
    playActions("questWindow.json")
    clickCenter('glowQuest', 0.9)
    playActions("questChat.json")
    playActions("finishQuest.json")


def clickCenter(imgName, con = 0.95):
    location = pyautogui.locateCenterOnScreen(f'images/{imgName}.png', confidence = con)
    pyautogui.moveTo(location)
    pressMouse()

if __name__ == '__main__':
    main()
