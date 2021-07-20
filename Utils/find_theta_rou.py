import pyautogui
import math
# import Mytest
point_name_map = ["A", "B", "C", "wei0", "wei100", "ele0", "ele100", "wingOff", "wingOn", "Practice", "head",
                  "waist", "rect1", "rect2", "Config"]
f = open("../config.txt", 'r')
lines = f.readlines()
params = {}
for index, line in enumerate(lines):
    x, y = line.split(',')
    x = int(x)
    y = int(y)
    params[point_name_map[index]] = (x, y)

while True:
    theta = int(input("theta:"))
    rou = int(input("rou"))
    # params = Mytest.read_config()

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

    pyautogui.moveTo(finalx, finaly)
