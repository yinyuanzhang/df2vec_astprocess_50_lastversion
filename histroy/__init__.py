# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 下午9:03
# @Author  : yinyuanzhang
# @Email   : yinyuanzhang@nudt.edu.cn
# @File    : __init__.py.py
# @Software: PyCharm
# 统计信息

f = open("../dataset/methods.txt")
kind = set()
for line in f.readlines():
    content = line.strip('\n').split(" ", 1)
    kind.add(content[1])
f.close()
print(len(kind))