# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 上午9:17
# @Author  : yinyuanzhang
# @Email   : yinyuanzhang@nudt.edu.cn
# @File    : count_file.py
# @Software: PyCharm

import os
path = '../deduplicated-sources'      # 输入文件夹地址
files = os.listdir(path)   # 读入文件夹
num_png = len(files)       # 统计文件夹中的文件个数
print(num_png)             # 打印文件个数
# 输出所有文件名
