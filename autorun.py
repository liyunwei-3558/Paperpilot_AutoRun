# create by liyunwei-3558 7/6/2021
import cv2
import math
import time
import pyautogui
import datetime
from Utils import read_number




def autorun(params, pType, pWeight, pEle, pWing, theta, rou, times=1, replace=True):
    # setting params
    # type
    results = []
    pyautogui.click(x=params[pType][0], y=params[pType][1], clicks=1, interval=0.1, button='left')
    # weight
    wei_y = params["wei0"][1]
    st = params["wei0"][0]
    ed = params["wei100"][0]
    dwx = round(((ed - st) * pWeight) / 100)

    pyautogui.moveTo(st, wei_y, duration=0)
    pyautogui.dragRel(dwx, 0, duration=0.1, button='left')
    (weight_afterx, weight_aftery) = (st + dwx, wei_y)

    # Ele
    ele_y = params["ele0"][1]
    st = params["ele0"][0]
    ed = params["ele100"][0]
    dex = round((ed - st) * pEle / 100)

    pyautogui.moveTo(st, ele_y, duration=0)
    pyautogui.dragRel(dex, 0, duration=0, button='left')
    (ele_afterx, ele_aftery) = (st + dex, ele_y)

    # Winglet
    if pWing == 1:
        pyautogui.moveTo(params["wingOff"][0], params["wingOff"][1])
        pyautogui.dragTo(params["wingOn"][0], params["wingOn"][1], duration=0.1, button='left')

    pyautogui.click(params["Practice"][0], params["Practice"][1], button='left')
    time.sleep(0.3)

    (cx, cy) = params["waist"]
    (hx, hy) = params["head"]
    (dx, dy) = (hx - cx, cy - hy)
    dy += rou
    # 逆时针旋转
    theta = theta * math.pi / 180
    finalx = dx * math.cos(theta) - dy * math.sin(theta)
    finaly = - dx * math.sin(theta) - dy * math.cos(theta)
    finalx += cx
    finaly += cy

    for _ in range(times):
        pyautogui.moveTo(hx, hy)
        pyautogui.dragTo(finalx, finaly, duration=0.4, button='left')
        # time.sleep(7)
        (x1, y1) = params["rect1"]
        (x2, y2) = params["rect2"]
        roi = (x1, y1, x2, y2)
        temp_num = read_number.read_number(roi)
        # time.sleep(0.7)
        if 3 <= len(temp_num) <= 5 and temp_num[-1] != '.':
            results.append(float(temp_num))

        if times > 1:
            pyautogui.click(button='left')

    if replace:
        pyautogui.click(params["Config"][0], params["Config"][1], button='left')
        time.sleep(0.3)
        pyautogui.moveTo(params["wingOn"][0], params["wingOn"][1])
        pyautogui.dragTo(params["wingOff"][0] - 10, params["wingOff"][1], duration=0.1, button='left')
        pyautogui.moveTo(weight_afterx, weight_aftery, duration=0.1)
        pyautogui.dragTo(params["wei0"][0] - 10, params["wei0"][1], duration=0.1, button='left')
        pyautogui.moveTo(ele_afterx, ele_aftery, duration=0.1)
        pyautogui.dragTo(params["ele0"][0], ele_aftery, duration=0.1, button='left')
        pyautogui.click(params["A"][0], params["A"][1], button='left')

    if times > 1:
        return results
    else:
        return results[0]
