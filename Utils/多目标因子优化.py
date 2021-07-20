import numpy as np
import geatpy as ea
import pandas as pd
import lightgbm as lgb
import joblib
from matplotlib import pyplot as plt

class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, M=2):
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        maxormins = [-1, 1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
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
        Vars = pop.Phen.astype(np.int32) # 得到决策变量矩阵
        X = self.var_set[Vars[:, :]]
        J = self.get_value(X)
        S = self.get_std(X)
        here = np.hstack([J, S])
        # print("here:\n",here)
        pop.ObjV = here # 把求得的目标函数值赋值给种群pop的ObjV

    def get_value(self, x):
        predictions = np.zeros(len(x))
        # print("lenx = ",len(x))

        for k in range(5):
            clf = lgb.Booster(model_file='model' + str(k) + ".txt")
            predictions += clf.predict(x, num_iteration=clf.best_iteration) / 5.0

        return predictions.reshape(-1, 1)

    def get_std(self, x):
        pipe = joblib.load("./pipe.pkl")
        pred, sigma = pipe.predict(x, return_cov=True)
        lst = []
        for ind in range(len(pred)):
            lst.append(sigma[ind, ind] ** 0.5)
        lst = np.array(lst).reshape(-1, 1)
        # print("lst", lst)
        return lst


if __name__ == '__main__':
    """===============================实例化问题对象============================"""
    problem = MyProblem()  # 生成问题对象
    """==================================种群设置==============================="""
    Encoding = 'BG'  # 编码方式
    NIND = 50  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders,
                      [10] * len(problem.varTypes))  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """================================算法参数设置============================="""
    myAlgorithm = ea.moea_NSGA2_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.mutOper.Pm = 0.3  # 修改变异算子的变异概率
    myAlgorithm.recOper.XOVR = 0.9  # 修改交叉算子的交叉概率
    myAlgorithm.MAXGEN = 200  # 最大进化代数
    myAlgorithm.logTras = 2  # 设置每多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）

    [NDSet, population] = myAlgorithm.run()  # 执行算法模板，得到非支配种群以及最后一代种群
    NDSet.save()  # 把非支配种群的信息保存到文件中
    """==================================输出结果=============================="""
    print('用时：%s 秒' % myAlgorithm.passTime)
    print('非支配个体数：%d 个' % NDSet.sizes) if NDSet.sizes != 0 else print('没有找到可行解！')
    if myAlgorithm.log is not None and NDSet.sizes != 0:
        print('HV', myAlgorithm.log['hv'][-1])
        print('Spacing', myAlgorithm.log['spacing'][-1])
        """=========================进化过程指标追踪分析========================="""
        metricName = [['igd'], ['hv']]
        Metrics = np.array([myAlgorithm.log[metricName[i][0]] for i in range(len(metricName))]).T
        # 绘制指标追踪分析图
        ea.trcplot(Metrics, labels=metricName, titles=metricName)