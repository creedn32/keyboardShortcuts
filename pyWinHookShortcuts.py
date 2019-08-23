import pyWinhook
import pythoncom
# import pyautogui
from pynput import keyboard


def functionComboDetected():
    print("Combo detected")
    keyDownInfoObj.autoKeyDown = keyboard.KeyCode(char="w")
    # hookManagerObj.UnhookKeyboard()
    keyboardControllerObj.press(keyboard.KeyCode(char="w"))
    # hookManagerObj.HookKeyboard()


def functionAutoKeyPress(event):

    print("Key pressed down automatically: " + event.Key)
    # print(str(currentPressedKeys))

    return True



def functionKeyPress(event):

    if event.Key in comboList:
        currentPressedKeys.append(event.Key)

    if list(dict.fromkeys(currentPressedKeys)) == comboList and keyDownInfoObj.comboReleased:
        keyDownInfoObj.comboReleased = False
        functionComboDetected()

    print("Key pressed down: " + event.Key)
    # print(str(currentPressedKeys))


    if comboList[0] in currentPressedKeys:
        return False
    else:
        return True



def functionKeyRelease(event):



    if event.Key in comboList:
        currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]

    if len(currentPressedKeys) == 0:
        keyDownInfoObj.comboReleased = True
        keyDownInfoObj.autoKeyDown = None


    if event.Key == keyDownInfoObj.autoKeyDown:
        pass

    print("Key released: " + event.Key)
    # print(str(currentPressedKeys))

    if comboList[0] in currentPressedKeys:
        return False
    else:
        return True




def OnKeyboardEvent(event):

    if event.MessageName == "key down" and keyDownInfoObj.autoKeyDown != None:
        return functionAutoKeyPress(event)
    elif event.MessageName == "key down":
        return functionKeyPress(event)
    elif event.MessageName == "key up":
        return functionKeyRelease(event)








class keyDownInfo():
    def __init__(self, comboReleased, autoKeyDown):
        self.comboReleased = comboReleased
        self.autoKeyDown = autoKeyDown




keyDownInfoObj = keyDownInfo(True, None)
comboList = ["Capital", "J"]
currentPressedKeys = []
keyboardControllerObj = keyboard.Controller()


hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
pythoncom.PumpMessages()












# print('MessageName: %s' % event.MessageName)
# print('Message: %s' % event.Message)
# print('Time: %s' % event.Time)
# print('Window: %s' % event.Window)
# print('WindowName: %s' % event.WindowName)
# print('Ascii: %s' % event.Ascii, chr(event.Ascii))
# print('Key: %s' % event.Key)
# print('KeyID: %s' % event.KeyID)
# print('ScanCode: %s' % event.ScanCode)
# print('Extended: %s' % event.Extended)
# print('Injected: %s' % event.Injected)
# print('Alt %s' % event.Alt)
# print('Transition %s' % event.Transition)
# print('---')


# return True to pass the event to other handlers
# return False to stop the event from propagating