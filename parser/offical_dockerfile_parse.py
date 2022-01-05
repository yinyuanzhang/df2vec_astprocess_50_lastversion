# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 下午7:45
# @Author  : yinyuanzhang
# @Email   : yinyuanzhang@nudt.edu.cn
# @File    : offical_dockerfile_parse.py
# @Software: PyCharm

import random

import dockerfile
import subprocess
import json
import os
import gain_filepath
import offical_image_dataset

def gci(filepath,time):
    global time_
    global i
    print(i)
    i = i + 1
    time_ = time
    global small_paths,env_instruction, arg_instruction

    dockerfile_content = gain_filepath.get_dockerfile_content(fi_d)
    #print(dockerfile_content)

    try:
        small_paths = []
        dockerfile_string = dockerfile.parse_string(dockerfile_content)
        #print(dockerfile_string)
        env_instruction, arg_instruction = gain_arg_cmd_structions(dockerfile_string)
        # 对 dockerfile 做第一层解析：
        dockerfile_phase1 = gain_filepath.process(dockerfile_string)
        #print("dockerfile_phase1", dockerfile_phase1)

        # 对 dockerfile 做第二层解析:
        dockerfile_phase2 = gain_filepath.parse_embedded_bash(dockerfile_phase1)
        #print("dockerfile_phase2:", dockerfile_phase2)

        if(time_ == 2):
            f = open('../dataset/corpus.txt', 'a')
            if(i != 1):
                f.write('\n')
            f.write("#" + str(i - 1))
            f.write('\n')
            f.write("label:" + gain_label(fi_d))
            f.write('\n')
            f.write("class:" + fi_d)
            f.write('\n')
            f.write("paths:")
            f.write('\n')
            f.close()
        search(dockerfile_phase2)

        print('\n')

    except Exception as ex:
        print("--------------------------------------------------------------------------------------------------------------------")



#return dockerfile_ast


def gain_label(fi_d):
    return path_label_index[fi_d]

def search(ast_dockerfile):
    dic_instructions = ast_dockerfile['children']
    global path,token_set
    token_set = set()

    for instruction in dic_instructions:
        path = []
        # print(type(instruction))
        #parse(instruction)
        # print(path)
        # if path not in paths:
        #     paths.append(path)
        path_all(instruction)
    combine_path1(small_paths)


# 迭代式的写法
# def parse(nodes):
#     if(nodes['children'] == []):
#         path.append(nodes['type'])
#         if 'value' in nodes:
#             path.append(nodes['value'])
#         token_set.add(nodes['type'])
#         # print(nodes['type'])
#     else:
#         path.append(nodes['type'])
#         for node in nodes['children']:
#             # print(type(node['children']))
#             parse(node)


def path_all(nodes):
    global small_path
    for node in nodes['children']:
        nodes['type'].strip()
        if (nodes['type'] == 'DOCKER-ADD' or nodes['type'] == 'DOCKER-COPY'):
            for c_node in node['children']:
                small_path = {}
                small_path["0"] = nodes['type'].strip().replace('\n', '').replace('\r', '')
                small_path["1"] = node['type'].strip().replace('\n', '').replace('\r', '')
                small_path["2"] = c_node['type'].strip().replace('\n', '').replace('\r', '')
                value_replaced = arg_env_replace(c_node['value'])
                small_path["3"] = value_replaced.strip().replace('\n', '').replace('\r', '')
                # print(small_path)
                small_paths.append(small_path)

        elif (nodes['type'] == 'DOCKER-RUN'):
            if (node['type'] == 'UNKNOWN'):
                small_path = {}
                small_path["0"] = nodes['type'].strip().replace('\n', '').replace('\r', '')
                small_path["1"] = node['type'].strip().replace('\n', '').replace('\r', '')
                small_path["2"] = node['value'].strip().replace('\n', '').replace('\r', '')
                # print(small_path)
                small_paths.append(small_path)
            else:
                for c_node in node['children']:
                    small_path = {}
                    small_path["0"] = nodes['type'].strip().replace('\n', '').replace('\r', '')
                    small_path["1"] = node['type'].strip().replace('\n', '').replace('\r', '')
                    small_path["2"] = c_node['type'].strip().replace('\n', '').replace('\r', '')
                    value_replaced = arg_env_replace(c_node['value'])
                    small_path["3"] = value_replaced.strip().replace('\n', '').replace('\r', '')
                    # print(small_path)
                    small_paths.append(small_path)

        else:
            small_path = {}
            small_path["0"] = nodes['type'].strip().replace('\n', '').replace('\r', '')
            small_path["1"] = node['type'].strip().replace('\n', '').replace('\r', '')
            value_replaced = arg_env_replace(node['value'])
            small_path["2"] = value_replaced.strip().replace('\n', '').replace('\r', '')
            # print(small_path)
            small_paths.append(small_path)





def combine_path1(paths):
    if len(paths) > 500:
        paths = random.sample(paths, 300)
    for i in range(len(paths)-1):
        for j in range(i+1,len(paths)):
            combine_path2(i,j)

def combine_path2(i,j):
    len_i = len(small_paths[i])
    len_j = len(small_paths[j])
    start_token = small_paths[i]['' + str(len_i - 1)]
    end_token = small_paths[j]['' + str(len_j - 1)]

    if(len_i == 4):
        up_path = small_paths[i]['2'] + '88' + small_paths[i]['1'] + '88' + small_paths[i]['0'] + '88' + 'DOCKER-FILE'
    if(len_i == 3):
        up_path = small_paths[i]['1'] + '88' + small_paths[i]['0'] + '88' + 'DOCKER-FILE'
    if(len_i == 2):
        up_path = small_paths[i]['0'] + '88' + 'DOCKER-FILE'

    if(len_j == 4):
        down_path = '66' + small_paths[j]['0'] + '66' + small_paths[j]['1'] + '66' + small_paths[j]['2']
    if(len_j == 3):
        down_path = '66' + small_paths[j]['0'] + '66' + small_paths[j]['1']
    if(len_j == 2):
        down_path = '66' + small_paths[j]['0']
    path_token = up_path + down_path
    #print(path_token)
    combine_path3(start_token,end_token,path_token)

    if(time_ == 2):
        start_token_number = gain_terminal_token_number(start_token)
        end_token_number = gain_terminal_token_number(end_token)
        path_token_number = gain_path_token_number(path_token)

        f = open('../dataset/corpus.txt', 'a')
        f.write(start_token_number + '  ' + path_token_number + '  ' + end_token_number)
        f.write('\n')
        f.close()


def gain_terminal_token_number(token):
    return new_terminal_token_index[token]

def gain_path_token_number(token):
    return new_path_token_index[token]

def combine_path3(start_token,end_token,path_token):
    start_token_set.add(start_token)
    end_token_set.add(end_token)
    path_token_set.add(path_token)
    terminal_token_set.add(start_token)
    terminal_token_set.add(end_token)


def terminal_token_index():
    m = 0
    global terminal_token_index
    terminal_token_index = {}
    for every in iter(terminal_token_set):
        terminal_token_index[m] = every
        m = m + 1

    f = open('../dataset/terminal_idxs.txt', 'w')
    for key, value in terminal_token_index.items():
        f.write(str(key) + ' ' + str(value))
        f.write('\n')
    f.close()

def path_token_index():
    n = 0
    global path_token_index
    path_token_index = {}
    for every in iter(path_token_set):
        path_token_index[n] = every
        n = n + 1

    f = open('../dataset/path_idxs.txt', 'w')
    for key, value in path_token_index.items():
        f.write(str(key) + ' ' + str(value))
        f.write('\n')
    f.close()


def gain_new_terminal_token_index():
    global new_terminal_token_index
    new_terminal_token_index = {}

    f = open("../dataset/terminal_idxs.txt")
    t = 0
    for line in f.readlines():
        content = line.strip('\n').split(" ",1)
        new_terminal_token_index[content[1]] = content[0]
        print(t)
        t =t + 1
    f.close()


def gain_new_path_token_index():
    global new_path_token_index
    new_path_token_index = {}

    f = open("../dataset/path_idxs.txt")
    for line in f.readlines():
        content = line.strip('\n').split(" ",1)
        new_path_token_index[content[1]] = content[0]
    f.close()


def gain_path_label_index():
    global path_label_index
    path_label_index = {}

    f = open("../dataset/methods.txt")
    for line in f.readlines():
        content = line.strip('\n').split(" ",1)
        path_label_index[content[0]] = content[1]
    f.close()



def start(time_):
    if(time_ == 2):
        gain_new_terminal_token_index()
        gain_new_path_token_index()
        gain_path_label_index()


    f = open("../dataset/methods.txt")
    global dockerfile_ast,fi_d
    global paths,i
    paths = []

    global start_token_set,end_token_set,path_token_set,terminal_token_set
    start_token_set = set()
    end_token_set = set()
    path_token_set = set()
    terminal_token_set = set()

    i = 0
    for line in f.readlines():
        content = line.strip('\n').split(" ",1)
        fi_d = content[0]
        gci(fi_d,time_)
    f.close()

    # print(small_paths)
    print(len(small_paths))

    if (time_ == 1):
        terminal_token_index()
        path_token_index()


def arg_env_replace(var_name):

    for key in env_instruction:
        if var_name.split("$")[-1] == key:
            var_name = env_instruction[key]
            print(var_name)

    for key in arg_instruction:
        if var_name.split("$")[-1] == "{" + key + "}":
            var_name = arg_instruction[key]
            print(var_name)
    return var_name



def my_filter(var_name):
    pass


def gain_arg_cmd_structions(dockerfile):
    arg_instruction = {}
    env_instruction = {}
    for instruction in dockerfile:

        if instruction.cmd == 'env':
            env_instruction[instruction.value[0]] = instruction.value[1]


        if instruction.cmd == 'arg':
            name = instruction.value[0].split("=")[0]
            value = instruction.value[0].split("=")[-1]
            arg_instruction[name] = value

        return env_instruction,arg_instruction