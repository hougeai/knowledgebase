# 理清概念
## argparse：
argparse是python中的一个内置模块，argparse== argument(参数)+ parse(解析) 。其**作用类似字典**：给某个程序设置几个参数，并且可以用命令行的形式把值传给它们。举例而言：
 
```bash
python demo.py --data='xxx.txt' --model='xxx.pth'
```
## sys.argv：
sys也是python中的一个内置模块，而argv是sys里的一个用法，代表命令行参数，其**作用类似列表**：同样是给某个程序设置几个参数，命令行中参数以空格为分隔。举例而言：

```bash
python demo.py xxx.txt xxx.pth
```

# 具体用法
## argparse：

```bash
import argparse 
def parse_args():
    parser = argparse.ArgumentParser(description="you can add those parameter")       
    parser.add_argument('--data', default="xxx.txt", help="The path of data")
    parser.add_argument('--model', default='xxx.pth', required=True) # required=True代表必须指定该参数
    args = parser.parse_args() 
    return args

if __name__ == '__main__':
    args = parse_args()
    print(args.model)

python demo.py --data='xxx.txt' --model='xxx.pth' 
```

## sys.argv：
```bash
import sys
a = sys.argv[0]  # 当前py文件路径
print(a) # demo.py
b = sys.argv[1]  # py文件后的第一个参数
print(b) # xxx.txt
c = sys.argv[2] # py文件后的第2个参数
print(c) # xxx.pth

python demo.py xxx.txt xxx.pth
```

# 二者如何一起使用

argparse和sys.argv可以结合在一起使用么，这是很多初学的小伙伴经常会遇到的问题？
答案是可以的！直接上代码：

```bash
import sys

import argparse 
def parse_args():
    parser = argparse.ArgumentParser(description="you can add those parameter")       
    parser.add_argument('--data', default="xxx.txt", help="The path of data")
    parser.add_argument('--model', default='xxx.pth', required=True)
    args = parser.parse_args() 
    return args

a = sys.argv[0]  # 当前py文件路径
print(a) # demo.py
b = sys.argv[1]  # py文件后的第一个参数
print(b) # xxx.txt
c = sys.argv[2] # py文件后的第2个参数
print(c) # xxx.txt
args = parse_args(sys.argv[3:]) # 从py文件后的第2个参数以后的参数开始解析
    print(args.model)

python demo.py xxx.txt xxx.pth --data='xxx.txt' --model='xxx.pth' 
```

