import pyWinhook, pythoncom, pyautogui, win32gui, time


import sys
sys.path.append("..")
from creed_modules import creedFunctions



def functionComboDetected(outputCombo, **otherArg):

    # print(keyDownInfoObj.autoKeyDown)

    if not keyDownInfoObj.autoKeyDown:

        for outKey in outputCombo:
            keyDownInfoObj.autoKeyDown.append(outKey)
            pyautogui.keyDown(creedFunctions.convertKey(outKey, pyHookToAutoGui))


        for outKey in reversed(outputCombo):
            pyautogui.keyUp(creedFunctions.convertKey(outKey, pyHookToAutoGui))

        if otherArg:
            time.sleep(.07)

            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":

                for list in otherArg["outputString"]:

                    for outKey in list:
                        keyDownInfoObj.autoKeyDown.append(outKey)

                        pyautogui.keyDown(creedFunctions.convertKey(outKey, pyHookToAutoGui))

                    for outKey in reversed(list):
                        pyautogui.keyUp(creedFunctions.convertKey(outKey, pyHookToAutoGui))




def functionAutoKeyPress(event):


    # print("Key pressed down automatically: " + event.Key.lower())
    # print("Allowed to send automatic press to OS? " + str(True))
    return True


def functionKeyPress(event):

    # print(str(event.Key))

    toReturn = True

    if event.Key == "Tab":
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":
            # print("tabbed")
            pyautogui.press("right")
            toReturn = False



    for combo in comboList:

        if event.Key.lower() in combo["inputKeys"] and event.Key.lower() not in currentPressedKeys:
            currentPressedKeys.append(event.Key.lower())


        if currentPressedKeys == combo["inputKeys"]:
            if "outputComboKeys" in combo.keys():
                if "outputString" in combo.keys():
                    functionComboDetected(combo["outputComboKeys"], outputString=combo["outputString"])
                else:
                    functionComboDetected(combo["outputComboKeys"])
            elif "printToScreen" in combo.keys():
                print(combo["printToScreen"])


    if event.Key.lower() not in keyDownInfoObj.autoKeyDown and "capital" in currentPressedKeys:
        toReturn = False


    # print("Key pressed: " + event.Key.lower())
    # print("Allowed to send press to OS? " + str(toReturn))

    return toReturn



def functionKeyRelease(event):

    toReturn = True


    if event.Key.lower() not in keyDownInfoObj.autoKeyDown and event.Key.lower() in currentPressedKeys:

        currentPressedKeys.remove(event.Key.lower())
        toReturn = False


        # for combo in comboList:

            # if event.Key.lower() in combo["inputKeys"]:

                #remove that key from currentPressedKeys

                # currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]

        # if "capital" in currentPressedKeys:
        #     toReturn = False


    elif event.Key.lower() in keyDownInfoObj.autoKeyDown:
        keyDownInfoObj.autoKeyDown.remove(event.Key.lower())

    # print(str(currentPressedKeys))
    # print("Key released: " + event.Key.lower())
    # print("Allowed to send release to OS? " + str(toReturn))
    return toReturn




def OnKeyboardEvent(event):


    if event.MessageName in ["key sys down", "key down"]:

        if event.Key.lower() in keyDownInfoObj.autoKeyDown:
            # print("event.Key: " + event.Key)
            # print("keyDownInfoObj.autoKeyDown: " + str(keyDownInfoObj.autoKeyDown))
            return functionAutoKeyPress(event)
        else:
            return functionKeyPress(event)

    elif event.MessageName in ["key up", "key sys up"]:
        return functionKeyRelease(event)



def createPathList(path):

    pathList = []

    for key in path:

        keyToAppend = []

        for i in autoGuiToPyHook:
            if i[1] == key:
                keyToAppend = i[0]

        if not keyToAppend:
            for i in pyHookToAutoGui:
                if i[1] == key:
                    keyToAppend.append(i[0])

        if not keyToAppend:
            for i in characterToDesc:
                if i[1] == key:
                    keyToAppend.append(i[0])


        if not keyToAppend:
            keyToAppend.append(key)

        pathList.append(keyToAppend)

    pathList.insert(0, ["back"])
    pathList.insert(0, ["lcontrol", "a"])
    # print(str(pathList).replace("'", "\""))

    return pathList




class keyDownInfo():
    def __init__(self, autoKeyDown):
        self.autoKeyDown = autoKeyDown





pyHookToAutoGui = [
    ["lmenu", "alt"],
    ["oem_1", ":"],
    ["oem_5", "\\"],
    ["lshift", "shift"],
    ["back", "backspace"],
    ["lcontrol", "ctrl"],
]


characterToDesc = [
    ["space", " "]
]


autoGuiToPyHook = [
    [["lshift", "oem_1"], ":"]
]




comboList = [
                {"inputKeys": ["capital", "j"], "outputComboKeys": ["left"]},
                {"inputKeys": ["capital", "k"], "outputComboKeys": ["right"]},
                {"inputKeys": ["capital", "u"], "outputComboKeys": ["up"]},
                {"inputKeys": ["capital", "m"], "outputComboKeys": ["down"]},
                {"inputKeys": ["capital", "c"], "outputComboKeys": ["lmenu", "space"], "outputString": createPathList("c:\\users\\creed\\")},
                {"inputKeys": ["capital", "s"], "outputComboKeys": ["lmenu", "space"], "outputString": createPathList("c:\\users\\creed\\nas\\synologydrive\\computer\\setup files\\")},
                {"inputKeys": ["capital", "h"], "printToScreen": "hi"}
            ]



keyDownInfoObj = keyDownInfo([])
currentPressedKeys = []
pyautogui.PAUSE = 0



hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
print("ready")
pythoncom.PumpMessages()





#
# win32guiObj = win32gui
#     win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
#     processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
#     # print(psutil.Process(processID[-1]))
#
#     if psutil.Process(processID[-1]).name() == "Executor.exe":
#         keyDownInfoObj.notAllowedToRelease = "Tab"
#         pyautogui.press("right")
#         toReturn = False


# def functionOtherComboDetected(outputKeys):
#
#
#k     # windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
#     # systemTrayObj = windowsExplorerApp.window(class_name="Shell_TrayWnd")
#     # systemTrayObj.child_window(title="Executor").click()
#
#     # windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
#     print(1)
#
#
#     # for outKey in outputKeys:
#     #     pyautogui.press(outKey.lower())

