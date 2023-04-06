# -*- coding=utf-8 -*-
# name: nan chen
# date: 2021/4/9 10:56

import csv
# import matplotlib.pyplot as plt


def run(file_name, stock_name):
    # 读取数据文件
    with open(file_name, encoding="utf-8") as f:
        reader = csv.reader(f)
        header_row = next(reader)
        counts = []
        ids = []
        for row in reader:
            ids.append(str(row[0]))
            counts.append(float(row[2]))

    # 一次指数平滑法
    s = []
    list_a = [2 / (len(counts) + 1), 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 0.9]
    # colors = ["brown", "green", "red", "gray", "yellow"]
    # 取初始值为x0
    for a in list_a:
        s1 = [counts[0]]
        for i in range(0, len(counts)):
            tmp = a * counts[i] + (1 - a) * s1[i]
            s1.append(tmp)
        s.append(s1)
    for i in range(0, len(list_a)):
        s_i = s[i]
        # print("%s:a=%s 一次指数平滑法的预测值为：%s,涨跌幅:%s" % (stock_name, list_a[i], s_i[len(s_i) - 1], calaRatio(s_i[len(s_i) - 1], counts[len(counts) - 1])))
        # plt.plot(ids, s_i[1:], label='a = %s' % a, linewidth=1, linestyle=':', marker=',')

    # plt.show()

    # 二次指数平滑法
    twice_s = []
    j = 0
    for a in list_a:
        s2 = [counts[0]]
        single_s = s[j]
        for i in range(1, len(counts)):
            tmp = a * single_s[i] + (1 - a) * s2[i - 1]
            s2.append(tmp)
        twice_s.append(s2)
        j = j + 1

    for i in range(0, len(list_a)):
        single = s[i]
        twice = twice_s[i]
        at = 2 * single[len(single) - 1] - twice[len(twice) - 1]
        bt = (list_a[i] / 1 - list_a[i]) / (single[len(single) - 1] - twice[len(twice) - 1])
        x = at + bt
        # print("%s:a=%s 二次指数平滑法的预测值为%s,涨跌幅:%s" % (stock_name, list_a[i], x, calaRatio(x, counts[len(counts) - 1])))
    return x


def calaRatio(forecast, perValue):
    return (forecast - perValue) * 100 / perValue


if __name__ == "__main__":
    run('stock_zh_a_hist_df.csv', '恺英网络')
