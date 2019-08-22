import pyautogui
import keyboard #also does mouse (pip install mouse, import mouse)

pyautogui.PAUSE = 0.001

PAUSED = 'paused'
CLICKING = 'clicking'
QUITTING = 'quitting'
state = PAUSED

positions = []
hotkeys = []
lastUserMouse = (pyautogui.position().x, pyautogui.position().y)

def dontQuit():
	print('Ready.')
	while True:
		loopPositions()
		if state == QUITTING:
			quit()

def doQuit():
	global state
	for key in hotkeys:
		try:
			keyboard.remove_hotkey(key)
		except KeyError as identifier:
			pass
	state = QUITTING

def addPosition():
	x, y = pyautogui.position()
	positions.append((x, y))
	print('learned {} {}'.format(x, y))

def loopPositions():
	global state
	for pos in positions:
		if state == CLICKING:
			pyautogui.click(pos[0], pos[1])
			print('clicked {} {}'.format(pos[0], pos[1]))
		if state == QUITTING:
			doQuit()

def clearPositions():
	positions.clear()
	toggleClicking()
	print('cleared')

def toggleClicking():
	global state
	global lastUserMouse

	def cleared():
		return len(positions) == 0

	if state == PAUSED and not cleared():
		lastUserMouse = lastUserMouse = (
			pyautogui.position().x, pyautogui.position().y)
		state = CLICKING
	else:
		state = PAUSED
		pyautogui.moveTo(lastUserMouse[0], lastUserMouse[1])

	print('state {}'.format(state))

hotkeys.append(keyboard.add_hotkey('alt+z', addPosition))
hotkeys.append(keyboard.add_hotkey('alt+x', toggleClicking))
hotkeys.append(keyboard.add_hotkey('alt+c', clearPositions))
hotkeys.append(keyboard.add_hotkey('alt+q', doQuit))

dontQuit()
