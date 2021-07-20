import win32gui
import sys
import os
import imageio
import time
import numpy as np
import cv2
from Mytest import read_config
from PIL import ImageGrab
import math

if __name__ == "__main__":

    params = read_config()

    (x1, y1) = params["wei0"]
    (x2, y2) = params["waist"]
    K = params['wei100'][0] - params['wei0'][0]
    # K /= 15217
    K /= 227
    theta = 41
    rou = 100
    rou *= K
    rect = (x1, y1, x2, y2)
    h = abs(y1 - y2)
    w = abs(x1 - x2)
    lst = ImageGrab.grab(rect)
    lst = cv2.cvtColor(np.array(lst), cv2.COLOR_RGB2BGR)
    time.sleep(0.2)
    stable_count = 0
    (cx, cy) = params["waist"]
    (hx, hy) = params["head"]
    (dx, dy) = (hx - cx, cy - hy)
    # nowd = pow(dx,2)+pow(dy,2)
    #     # nowd = math.sqrt(nowd)
    dx *= K
    dy *= K
    dy += rou
    # 逆时针旋转
    theta = theta * math.pi / 180
    finalx = dx * math.cos(theta) - dy * math.sin(theta) + w - 12 * K
    finaly = - dx * math.sin(theta) - dy * math.cos(theta) + h - 12 * K
    finalx = round(finalx)
    finaly = round(finaly)
    print(finalx, finaly)
    while True:
        im = ImageGrab.grab(rect)  # 获得当前屏幕
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        # video.write(imm)  # 写入
        cv2.namedWindow('imm', cv2.WINDOW_AUTOSIZE)
        cv2.circle(imm, (finalx, finaly), 5, (0, 0, 255), 1)
        cv2.imshow('imm', imm)  # 显示
        cv2.waitKey(10)
