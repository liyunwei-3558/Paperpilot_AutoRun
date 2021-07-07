import cv2
import numpy as np

files_addr = "../models/origin/"
save_addr = "../models/processed/"


def process(ori_img):
    img = cv2.cvtColor(np.array(ori_img), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
    # cv2.namedWindow('imm', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('imm', ori_img)  # 显示
    imggray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    thresh, imgthr = cv2.threshold(imggray, 230, 255, cv2.THRESH_BINARY)
    # cv2.namedWindow("threshold", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('threshold', np.array(imgthr))

    w, h = imgthr.shape
    left = top = right = bottom = 0
    f = 0
    for x in range(w):

        if f == 0 and imgthr[x, :].sum() > 0:
            left = x
            f = 1
        elif f == 1 and imgthr[x, :].sum() == 0:
            right = x
            f = 0
            break
    for y in range(h):
        if f == 0 and imgthr[:, y].sum() > 0:
            top = y
            f = 1
        elif f == 1 and imgthr[:, y].sum() == 0:
            bottom = y
            f = 0
            break

    roi = (left, top, right, bottom)
    img_final = imgthr[left:right, top:bottom]
    # cv2.namedWindow("roi", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("roi", img_final)
    # cv2.waitKey(0)
    img_final = cv2.resize(img_final, (16, 16), interpolation=cv2.INTER_CUBIC)

    return img_final


for i in range(10):
    src = cv2.imread(files_addr + str(i) + ".png")
    proimg = process(src)
    print("size of " + str(i))
    print(proimg.shape)
    cv2.imwrite(save_addr + str(i) + ".png", img=proimg)
