import win32gui
import sys
import os
import imageio
import time
import numpy as np
import cv2
from PIL import ImageGrab


def judge_save(img):
    here = cv2.resize(img, (16, 16), cv2.INTER_CUBIC)
    min_diff = 99999
    res = -1
    for i in range(10):
        mod = cv2.imread("./models/processed/" + str(i) + ".png", cv2.IMREAD_GRAYSCALE)

        w, h = mod.shape
        diff = cv2.absdiff(mod, here).sum()
        # print("diff with i = " + str(diff))
        if min_diff > diff:
            min_diff = diff
            res = i
    if min_diff >= 22000:
        res = -1
    if res != -1:
        return res
    else:
        return -1


def select_number(img):
    # cv2.namedWindow("look num", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("look num", img)
    # print("a number!!!")
    w, h = img.shape
    top = 0
    bottom = h
    res = -1
    f = 0
    for y in range(w):
        if f == 0 and img[y, :].sum() > 0:
            top = y
            f = 1
        elif f == 1 and img[y, :].sum() == 0:
            bottom = y
            f = 0
            res = judge_save(img[ top:bottom,:])
            break
    return res


def read_number(rect):
    lst = ImageGrab.grab(rect)
    lst = cv2.cvtColor(np.array(lst), cv2.COLOR_RGB2BGR)
    time.sleep(0.2)
    stable_count = 0
    while True:
        im = ImageGrab.grab(rect)  # 获得当前屏幕
        imm = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
        # video.write(imm)  # 写入
        cv2.namedWindow('imm', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('imm', imm)  # 显示
        # 先等稳定了再开始读
        if cv2.absdiff(imm, lst).sum() <= 5:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count == 4:
            print("start reading!")
            imggray = cv2.cvtColor(np.array(imm), cv2.COLOR_BGR2GRAY)
            thresh, imgthr = cv2.threshold(imggray, 230, 255, cv2.THRESH_BINARY)
            # cv2.namedWindow("threshold", cv2.WINDOW_AUTOSIZE)
            # cv2.imshow('threshold', np.array(imgthr))
            width, height = imgthr.shape
            f = 0
            # print(np.array(imgthr))
            num = str()
            for x in range(height):
                # print(x, imgthr[:, x].sum())
                if f == 0 and imgthr[:, x].sum() > 0:
                    left = x
                    f = 1
                elif f == 1 and imgthr[:, x].sum() == 0:
                    right = x
                    f = 0
                    temp = select_number(imgthr[:,left:right])
                    if temp == -1:
                        num += '.'
                    else:
                        num += str(temp)
                        if len(num) >= 4:
                            if num == "0.0.":
                                num = "0.0"

                            print("num is " + num)
                            return num

            print("num is " + num)
            # cv2.waitKey(0)
            return num

        lst = imm
        time.sleep(0.2)
