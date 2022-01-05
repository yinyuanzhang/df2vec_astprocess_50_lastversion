# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 下午9:07
# @Author  : yinyuanzhang
# @Email   : yinyuanzhang@nudt.edu.cn
# @File    : data.py
# @Software: PyCharm

import dockerfile
import os
import offical_image_dataset
import gain_imagename
import offical_dockerfile_parse
import image_distribution

if __name__ == '__main__':
    # gain_imagename.gci('../deduplicated-sources')
    # offical_dockerfile_parse.start(1)
    # offical_dockerfile_parse.start(2)
    image_distribution.gain_image_distribution()






