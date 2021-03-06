# %%

# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea
import pandas as pd
import lightgbm as lgb
from matplotlib import pyplot as plt


# gbm = lgb.Booster(model_file='model.txt')

class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [-1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        self.var_set = np.arange(0, 121)  # 设定一个集合，要求决策变量的值取自于该集合
        Dim = 4  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0, 0, 0, 0]  # 决策变量下界
        ub = [100, 100, 75, 120]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):  # 目标函数
        Vars = pop.Phen.astype(np.int32)  # 强制类型转换确保元素是整数
        X = self.var_set[Vars[:, :]]

        J = self.get_value(X)
        # print(J)

        pop.ObjV = J

    def get_value(self, x):
        predictions = np.zeros(len(x))
        # print("lenx = ",len(x))

        for k in range(5):
            clf = lgb.Booster(model_file='model' + str(k) + ".txt")
            predictions += clf.predict(x, num_iteration=clf.best_iteration) / 5.0

        return predictions.reshape(-1, 1)


# 导入自定义问题接口
"""===============================实例化问题对象==========================="""
problem = MyProblem()  # 生成问题对象
"""=================================种群设置=============================="""
Encoding = 'RI'  # 编码方式
NIND = 25  # 种群规模
Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
"""================================算法参数设置============================="""
myAlgorithm = ea.soea_DE_rand_1_bin_templet(problem, population)  # 实例化一个算法模板对象
myAlgorithm.MAXGEN = 200  # 最大进化代数
myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
myAlgorithm.recOper.XOVR = 0.2  # 重组概率
myAlgorithm.trappedValue = 1e-6  # “进化停滞”判断阈值
myAlgorithm.maxTrappedCount = 10  # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
myAlgorithm.logTras = 1  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
myAlgorithm.verbose = True  # 设置是否打印输出日志信息
myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
"""===========================调用算法模板进行种群进化======================="""
[BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
BestIndi.save("BestGen.txt")  # 把最优个体的信息保存到文件中
"""==================================输出结果=============================="""
print('用时：%f 秒' % myAlgorithm.passTime)
print('评价次数：%d 次' % myAlgorithm.evalsNum)
if BestIndi.sizes != 0:
    print('最优的目标函数值为：%s' % BestIndi.ObjV[0][0])
    print('最优的控制变量值为：')
    for i in range(BestIndi.Phen.shape[1]):
        print(problem.var_set[BestIndi.Phen[0, i].astype(int)])
else:
    print('没找到可行解。')
