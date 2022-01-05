# -*- coding: utf-8 -*-
# @Time    : 2021/1/27 下午8:48
# @Author  : yinyuanzhang
# @Email   : yinyuanzhang@nudt.edu.cn
# @File    : image_distribution.py
# @Software: PyCharm


def gain_image_distribution():
    f = open("../dataset/methods.txt")

    image_list = []
    for line in f.readlines():
        content = line.strip('\n').split(" ",1)
        image_list.append(content[1])
    f.close()

    image_set = set()
    for i in range(len(image_list)):
        image_set.add(image_list[i])

    print(len(image_set))


    image_dict = {}

    for value in image_list:
        image_dict[value] = image_dict.get(value, 0) + 1

    print(sorted(image_dict.items(), key=lambda x: x[1], reverse=True))
    print(image_dict)
