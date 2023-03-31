# -*- coding=utf-8 -*-
# name: nan chen
# date: 2021/4/8 14:28

import csv
import matplotlib.pyplot as plt

# 读取数据文件
with open(r"stock_zh_a_hist_df.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    header_row = next(reader)
    counts = []
    ids = []
    for row in reader:
        ids.append(str(row[0]))
        counts.append(float(row[2]))
plt.plot(ids, counts, color="blue", linewidth=1, linestyle=':', marker=',')

length = len(counts)
singemovings = []
pos = 0
min = 1000000
# 一次移动平均
for n in range(2, 201):
    singemoving = []
    mse_sum = 0
    for i in range(n - 1, length):
        sum = 0
        for j in range(0, n):
            sum = sum + (counts[i - j])
        singemoving.append(int(sum / n))
    singemovings.append(singemoving)
    # 求解MSE
    for x, y in zip(range(len(counts) - 1, n - 1, -1), range(len(singemoving) - 2, -1, -1)):
        mse_sum = mse_sum + ((counts[x] - singemoving[y]) ** 2)
    mse = mse_sum / (len(counts) - n)
    sq_mse = mse ** 0.5
    if mse < min:
        min = mse
        pos = n
    print("n=%s 标准差=%s mse=%s" % (n, sq_mse, mse))
    # 打印结果
    print("n=%s 一次移动平均法的预测值为：%s" % (n, singemoving[len(singemoving) - 1]))
plt.plot(ids[n - 1:], singemoving, color="red", linewidth=1, linestyle=':', marker=',', label='一次移动平均法')
plt.show()

# 二次移动平均
# 选取mse最小的值计算二次移动平均
n = pos
singemoving = singemovings[n - 2]
twicemoving = []
for i in range(n - 1, len(singemoving)):
    sum = 0
    for j in range(0, n):
        sum = sum + singemoving[i - j]
    twicemoving.append(int(sum / n))

# 二次移动平均预测值
a = singemoving[len(singemoving) - 1] * 2 - twicemoving[len(twicemoving) - 1]
b = (2 / (n - 1)) * (singemoving[len(singemoving) - 1] - twicemoving[len(twicemoving) - 1])
x = a + b
print("n=%s 二次移动平均法的预测值为：%s" % (n, x))
