import pyautogui
import time
print(pyautogui.size())
try:
    while True:

        print(pyautogui.position())
        time.sleep(0.1)

except KeyboardInterrupt:
    print("User quit!\n")