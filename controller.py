from keys import *
import time
import cv2
import pyautogui
from playback import playActions
import schedule
import sys




def main():
    try:
        for x in range(1):
            time.sleep(5)
            playActions("leaveSeria.json")
            time.sleep(1)
            playActions("tourney.json")
            time.sleep(1)

            schedule.every(2).seconds.do(pressButton, button ='0')
            schedule.every(1.75).seconds.do(pressButton, button = 'F10')
            schedule.every(0.75).seconds.do(pressButton, button = 'X')
            schedule.every(1).seconds.do(pressButton, button= 'SPACE')

            print("pass loop")

            while True:
                retryLocation = pyautogui.locateOnScreen('images/retry.png')

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

if __name__ == '__main__':

    main()




    #number of characters should be in range
