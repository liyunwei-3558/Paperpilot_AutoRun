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
    for _ in range(30):

        nowres = autorun.autorun(paradict, "C", 6, 28, 1, 41, 100, 1, True)
        res.append(nowres)
        df.loc[rows] = ["C", 6, 28, 1, 41, 100, nowres]
        rows += 1

    print(df)
    df.to_csv(file_addr)