import dockerfile
from gensim.models import Word2Vec
import os
from string import digits

# 遍历文件夹下所有的文件
def gci(filepath):
    global dockerfile_ast
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
    for instruction in dockerfile:
        if instruction.cmd not in VALID_DIRECTIVES:
            continue
            # Not valid dockerfile
            # raise Exception('found invalid directive {}'.format(directive.cmd))

        if instruction.cmd == 'run':
            whole_run_instruction = instruction.value[0]
            print(whole_run_instruction)
            if(whole_run_instruction.startswith('apt-get update && apt-get install -y')):
                value = whole_run_instruction.split('apt-get update && apt-get install -y')[-1].split('&&')[0]
                print(value)
                installs = value.strip().split(' ')
                installs = [x for x in installs if x != '']
                print(installs)
                for install in installs:
                    DRUNINSTALL = 'DOCKER-RUN-install-' + install.lstrip().translate(str.maketrans('', '', digits))
                    print(DRUNINSTALL)
                    this_dockerfile.append(DRUNINSTALL)

            elif(whole_run_instruction.startswith('apt-get update && apt-get install')):
                value = whole_run_instruction.split('apt-get update && apt-get install')[-1].split('&&')[0]
                print(value)
                installs = value.strip().split(' ')
                installs = [x for x in installs if x != '']
                print(installs)
                for install in installs:
                    DRUNINSTALL = 'DOCKER-RUN-install-' + install.lstrip().translate(str.maketrans('', '', digits))
                    print(DRUNINSTALL)
                    this_dockerfile.append(DRUNINSTALL)

            elif(whole_run_instruction.startswith('apt-get install')):
                value = whole_run_instruction.split('apt-get install')[-1].split('&&')[0]
                print(value)
                installs = value.strip().split(' ')
                installs = [x for x in installs if x != '']
                print(installs)
                for install in installs:
                    DRUNINSTALL = 'DOCKER-RUN-install-' + install.lstrip().translate(str.maketrans('', '', digits))
                    print(DRUNINSTALL)
                    this_dockerfile.append(DRUNINSTALL)

        # 1.children 节点是list[] 加 dict{}

        elif instruction.cmd == 'from':
            from_node = []
            value = instruction.value[0]
            image_name = value.split('/')[-1] if '/' in value else value
            image_name = image_name.split(':')[0].strip() if ':' in image_name else image_name
            repo = 'NULL'
            tag = 'NULL'
            if '/' in value:
                repo = value.split('/')[0].strip()
            if ':' in value:
                tag = value.split(':')[-1].strip() if ':' in value else None
            # from_node.append()

            DFROM = 'DOCKER-FROM-' + image_name
            print(DFROM)
            this_dockerfile.append(DFROM)
        # 2.FROM 指令涉及镜像名、仓库名、版本tag

    if(this_dockerfile != []):
            dockerfile_ast.append(this_dockerfile)








global i
global dockerfile_ast
dockerfile_ast = []
dockerfile_ast = gci('../deduplicated-sources')
print(dockerfile_ast)

#print(model.wv.index2word)