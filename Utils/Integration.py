import os
import pandas as pd
import glob

csv_list = glob.glob('../records/mani/*.csv') #查看同文件夹下的csv文件数
print(u'共发现%s个CSV文件'% len(csv_list))
print(u'正在处理............')
# for i in csv_list: #循环读取同文件夹下的csv文件
#     fr = open(i,'rb').read()
#     with open('result_of_mani.csv','ab') as f: #将结果保存为result.csv
#         f.write(fr)
#         f.close()
# print(u'合并完毕！')

files = []
for i in csv_list:
    nowf = pd.read_csv(i)
    files.append(nowf)

res = pd.concat(files,ignore_index=True)
res.drop('Unnamed: 0',axis=1,inplace=True)
res.drop_duplicates(inplace=True)
print(res.info())
res.to_csv('../records/integration.csv', index=0)
