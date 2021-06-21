import pyautogui
import keyboard #also does mouse (pip install mouse, import mouse)
from time import sleep

#pyautogui.PAUSE = 0.4

positions = []
hotkeys = []
lastUserMouse = (pyautogui.position().x, pyautogui.position().y)
quitting = 0

def message():
    print('Ready.\n'
          'ctrl+alt+z Learn position\n'
          'ctrl+alt+a Pause\n'
          'ctrl+alt+x Click positions\n'
          'ctrl+alt+c Save\n'
          'ctrl+alt+v Clear positions\n'
          'ctrl+alt+q Quit'
    )

def load():
    global positions
    with open('positions.txt','r') as f:
        positions = [
            (tuple([int(y) for y in x.rstrip().split(',')]) if ',' in x else x.rstrip())
            for x in f.readlines()]
    print('loaded')
    print(positions)
    
def addPosition():
    x, y = pyautogui.position()
    positions.append((x, y))
    print(f'learned {x} {y}')

def addPause():
    positions.append((-1, -1))
    print('added a pause')

def clickPositions():
    for pos in positions:
        if type(pos) is tuple:
            if (pos[0] > -1):
                pyautogui.moveTo(pos[0], pos[1], 0.15, pyautogui.easeInOutQuad)
                pyautogui.click(pos[0], pos[1])
                print(f'clicked {pos[0]} {pos[1]}')
            else:
                print('pause.', end='')
                sleep(1)
                print('.', end='')
                sleep(1)
                #print('.')
                #sleep(1)
        else:
            keyboard.press_and_release(pos)
            print(f'pressed {pos}')

def save():
    with open('positions.txt','w') as f:
        f.writelines([f'{x[0]},{x[1]}\n' for x in positions])
    print('saved\n')

def clearPositions():
    s = input('Are you sure?! [y/N]')
    if (s.upper() == 'Y'):
        positions.clear()
        print('cleared')

def keepRunning():
    while (not quitting):
        pass

def doQuit():
    global quitting
    for key in hotkeys:
        try:
            keyboard.remove_hotkey(key)
        except KeyError as _:
            pass
    print('Done.\n')
    quitting = 1

hotkeys.append(keyboard.add_hotkey('ctrl+alt+z', addPosition))
hotkeys.append(keyboard.add_hotkey('ctrl+alt+a', addPause))
hotkeys.append(keyboard.add_hotkey('ctrl+alt+x', clickPositions))
hotkeys.append(keyboard.add_hotkey('ctrl+alt+c', save))
hotkeys.append(keyboard.add_hotkey('ctrl+alt+v', clearPositions))
hotkeys.append(keyboard.add_hotkey('ctrl+alt+q', doQuit))

message()
load()
keepRunning()
