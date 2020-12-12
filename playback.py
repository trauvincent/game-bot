import pyautogui
from time import sleep, time
import os
import json
from keys import *



def main():

    initializePyAutoGUI()
    countdownTimer()

    playActions("leaveSeria.json")
    playActions("tourney.json")


    print("Done")


def initializePyAutoGUI():
    # Initialized PyAutoGUI
    # https://pyautogui.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pyautogui.FAILSAFE = True


def countdownTimer():
    # Countdown timer
    print("Starting", end="", flush=True)
    for i in range(0, 4):
        print(".", end="", flush=True)
        sleep(1)
    print("Go")


def playActions(filename):
    # Read the file
    keys = Keys()
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir,
        'recordings',
        filename
    )
    with open(filepath, 'r') as jsonfile:
        # parse the json
        data = json.load(jsonfile)

        # loop over each action
        # Because we are not waiting any time before executing the first action, any delay before the initial
        # action is recorded will not be reflected in the playback.
        for index, action in enumerate(data):
            action_start_time = time()



            # perform the action
            if action['type'] == 'press':
                key = convertKey(action['button'])
                keys.directKey(key)
                print("press on {}".format(key))
            elif action['type'] == 'release':
                key = convertKey(action['button'])
                keys.directKey(key, keys.key_release)
                print("release on {}".format(key))
            elif action['type'] == 'click':
                pyautogui.click(action['pos'][0], action['pos'][1], duration=0.25)
                print("click on {}".format(action['pos']))

            # then sleep until next action should occur
            try:
                next_action = data[index + 1]
            except IndexError:
                # this was the last action in the list
                break
            elapsed_time = next_action['time'] - action['time']

            # if elapsed_time is negative, that means our actions are not ordered correctly. throw an error
            if elapsed_time < 0:
                raise Exception('Unexpected action ordering.')

            # adjust elapsed_time to account for our code taking time to run
            elapsed_time -= (time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print('sleeping for {}'.format(elapsed_time))
            sleep(elapsed_time)
    sleep(1.5)


# convert pynput button keys into pyautogui keys
# https://pynput.readthedocs.io/en/latest/_modules/pynput/keyboard/_base.html#Key
# https://pyautogui.readthedocs.io/en/latest/keyboard.html
def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_gr': 'altright',

        'alt_l': 'lalt',
        'alt_r': 'ralt',
        'caps_lock': 'caps',
        'ctrl_l': 'lcontrol',
        'ctrl_r': 'rcontrol',
        'page_down': 'pgdn',
        'page_up': 'pgup',
        'shift_l': 'lshift',
        'shift_r': 'rshift',
        'num_lock': 'numlock',
        'print_screen': 'printscreen',
        'scroll_lock': 'scroll',
    }

    # example: 'Key.F9' should return 'F9', 'w' should return as 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key


if __name__ == "__main__":
    main()
