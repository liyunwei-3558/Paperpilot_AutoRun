import autorun
import pandas as pd
import datetime

file_addr = "./records/" + str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')) + ".csv"
point_name_map = ["A", "B", "C", "wei0", "wei100", "ele0", "ele100", "wingOff", "wingOn", "Practice", "head",
                  "waist", "rect1", "rect2", "Config"]

def read_config():
    res = {}
    f = open("config.txt", 'r')
    lines = f.readlines()
    for index, line in enumerate(lines):
        x, y = line.split(',')
        x = int(x)
        y = int(y)
        res[point_name_map[index]] = (x, y)

    return res


if __name__ == "__main__":
    paradict = read_config()
    print(paradict)
    res = []
    df = pd.DataFrame(columns=('Type', 'Weight', 'Elevators', 'Winglets', 'theta', 'rou', 'result'))
    rows = 0
    # 从这里修改即可

    # nowres = autorun.autorun(paradict, "C", 6, 28, 1, 41, 100, 1, True)
    nowres = autorun.autorun(paradict, "C", 80, 41, 1, 50, 86, 1, True)
    nowres = autorun.autorun(paradict, "C", 55, 57, 1, 43, 105, 1, True)
    nowres = autorun.autorun(paradict, "C", 90, 50, 1, 51, 85, 1, True)
    nowres = autorun.autorun(paradict, "C", 76, 60, 1, 43, 105, 1, True)
    nowres = autorun.autorun(paradict, "C", 63, 45, 1, 38, 116, 1, True)
    nowres = autorun.autorun(paradict, "C", 21, 34, 1, 43, 95, 1, True)
    nowres = autorun.autorun(paradict, "C", 49, 41, 1, 43, 100, 1, True)
    nowres = autorun.autorun(paradict, "C", 15, 34, 1, 40, 100, 1, True)
    res.append(nowres)
    # df.loc[rows] = ["C", 10, ele, 1, 50, 50, nowres]
    # rows += 1
    # print(df)
    # df.to_csv(file_addr)
