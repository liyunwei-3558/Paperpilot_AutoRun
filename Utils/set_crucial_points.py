def set_points():
    point_dict = dict()
    print("请按提示输入如下坐标,格式为x,y")
    pointnames = ["Plane Type A", "Plane Type B", "Plane Type C", "Paper Weight为0时的红色滑块中心",
                  "Paper Weight为100时的红色滑块中心", "Elevators为0时的红色滑块中心", "Elevators为100时的红色滑块中心",
                  "Winglets为Off时红色滑块中心", "Winglets为On时红色滑块中心", "Practice按钮中心", "小人的头部中心", "小人腰部中心",
                  "距离显示框的左上角", "距离显示框的右下角", "Configuration Mode按钮"]
    point_name_map = ["A", "B", "C", "wei0", "wei100", "ele0", "ele100", "wingOff", "wingOn", "Practice", "head",
                      "waist", "rect1", "rect2", "Config"]

    for index, name in enumerate(pointnames):
        now = input(name + ":")
        x, y = now.split(',')
        point_dict[point_name_map[index]] = (x, y)

    return point_dict


if __name__ == "__main__":
    pd = set_points()
    f = open("../config.txt", 'w')
    with f:
        for x in pd:
            f.write(str(pd[x][0]) + "," + pd[x][1])
            f.write('\n')

    f.close()
