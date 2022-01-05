import dockerfile
from gensim.models import Word2Vec
import os
from string import digits
import offical_image_dataset


# 遍历文件夹下所有的文件
def gci(filepath):
    global i
    global dockerfile_ast, namelist
    global path_name
    path_name = {}
    namelist = set()
    dockerfile_ast = []

    global fi_d
    i = 0
    files = os.listdir(filepath)
    for fi in files:

        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            gci(fi_d)
        else:      #  直到fi_d 是文件，就可以获取到dockerfile文件
            print(i)
            print(filepath)
            print(fi_d)
            dockerfile_content = get_dockerfile_content(fi_d)
            #print(dockerfile_content)
            try:
                dockerfile_string = dockerfile.parse_string(dockerfile_content)
                #print(dockerfile_string)
                read(dockerfile_string)
                i = i + 1
                print('\n')
            except Exception as ex:
                print('eeeeeeeeeeeeeeeeeeeeeeee')

    writepathfile()
    return dockerfile_ast


# 将.Dockerfile文件转化成String类型
def get_dockerfile_content(fi_d):
    file_inside = open(fi_d, encoding='gb18030', errors='ignore')
    dockerfile_content = ''
    for line in file_inside:
        dockerfile_content += line
    return dockerfile_content



# 解析dockerfile文件 进行数据清洗
def read(dockerfile):
    p = 0
    VALID_DIRECTIVES = [
        'from',
        'run',
        'cmd',
        'label',
        'maintainer',
        'expose',
        'env',
        'add',
        'copy',
        'entrypoint',
        'volume',
        'user',
        'workdir',
        'arg',
        'onbuild',
        'stopsignal',
        'healthcheck',
        'shell'
    ]

    # 指定dockerfile AST 结构   p:doct类型
    this_dockerfile = []
    arg_instruction = {}
    env_instruction = {}
    for instruction in dockerfile:
        if instruction.cmd not in VALID_DIRECTIVES:
            continue
            # Not valid dockerfile
            # raise Exception('found invalid directive {}'.format(directive.cmd))

        # 1.children 节点是list[] 加 dict{}

        if instruction.cmd == 'env':
            env_instruction[instruction.value[0]] = instruction.value[1]


        if instruction.cmd == 'arg':
            name = instruction.value[0].split("=")[0]
            value = instruction.value[0].split("=")[-1]
            arg_instruction[name] = value


        if instruction.cmd == 'from' and p == 0:
            p = p + 1
            from_node = []
            value = instruction.value[0]
            #image_name = value.split('/')[-1] if '/' in value else value
            image_name = value.strip()
            image_name = image_name.split(':')[0].strip() if ':' in image_name else image_name
            repo = 'NULL'
            tag = 'NULL'
            if '/' in value:
                repo = value.split('/')[0].strip()
            if ':' in value:
                tag = value.split(':')[-1].strip() if ':' in value else None
            # from_node.append()
            #print(image_name)
            if str(image_name).startswith("$"):
                print("-------------------------")
                print(instruction)
                print(image_name)
                print(dockerfile)
                for key in env_instruction:
                    if image_name.split("$")[-1] == key:
                        image_name = env_instruction[key]
                        print(image_name)

                for key in arg_instruction:
                    if image_name.split("$")[-1] == "{" + key + "}":
                        image_name = arg_instruction[key]
                        print(image_name)
            image_name = image_name.strip('"')
            if image_name not in offical_image_dataset.gain_officalimages():
                continue
            if '$' not in image_name:
                namelist.add(image_name)
                path_name[fi_d] = image_name

def writepathfile():
    f = open('../dataset/methods.txt', 'w')
    for key, value in path_name.items():
        f.write(key + ' ' + str(value))
        f.write('\n')
    f.close()








