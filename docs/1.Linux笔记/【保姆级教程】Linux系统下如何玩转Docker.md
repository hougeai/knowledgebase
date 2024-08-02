# 0 写在前面
随着云原生、AI等技术的迅猛发展，容器技术逐渐成为每位技术同学的必备技能，上篇教程向大家介绍了什么是虚拟机以及如何在[Windows上安装Linux虚拟机](https://zhuanlan.zhihu.com/p/689560472)。

本篇教程带领大家了解Docker容器技术，从0开始实现将代码打包成Docker镜像，并提交到云仓库，帮助大家熟悉Docker常见的指令，有需要用到Docker技术的同学可以收藏备用！

# 1 什么是Docker
一句话介绍：Docker是一个开源的应用容器引擎，它允许开发者将应用及其依赖打包到一个可移植的容器中，而Docker容器不关心机器的底层环境，可以在任何Linux或Windows操作系统上运行。
## 1.1 Docker和虚拟机的区别
从下图中可以看出，虚拟机是在宿主机上添加了自己的操作系统，是不适合迁移的；
而docker直接寄存在宿主机上，只需要构建好镜像后，当项目需要迁移的时候，直接将镜像拉到需要部署的机器上就OK了，和git的行为类似。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740162.png)

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740163.png)

## 1.2 Docker的三个基本概念
- 镜像image：分层layout，只读的，每层都可以添加删除文件形成新的镜像，所以是树状结构，依赖关系体现在docker镜像制作的dockerfile中的FROM指令。如果要是树的根，那么我们需要"FROM scratch"
- 容器container：在image的最后一层上面再添加一层，这一层比较特殊，可读写。负责运行，启动后就是计算机中的一个进程；也可以通过build命令，把容器打包成我们自己需要的镜像。通常，容器启动过程可以分为如下步骤：
  - 检查镜像是否存在，否则从远程仓库下载，然后利用镜像创建一个容器
  - 启动刚刚创建的容器
  - 分配一个文件系统给容器，并且在镜像层外挂载一个可读可写层
  - 从宿主主机的网桥接口中桥接一个给容器，从网桥中分一个ip地址给容器
  - 执行用户指定的应用程序，执行完毕后容器自动终止
- 仓库repository：远程仓库，存放镜像的地方。默认情况下，是从docker hub中获取镜像（http://registry.hub.docker.com/），当然也可以改变镜像源的位置。

# 2 Docker安装
这里主要介绍Linux系统下的Docker安装，其他操作系统如windows安装由于笔者还没尝试过，待后续探索过再来补充。

Linux系统下的Docker安装主要有两种方式：
## 2.1 脚本安装
下载官方安装脚本自动安装，命令如下：
```
sudo curl -sS https://get.docker.com/ | sh
```
## 2.2 手动安装
这里更推荐手动安装，便于了解安装的具体过程：

```
# 1. 清空旧版本
sudo apt-get remove docker docker-engine docker.io containerd runc

# 2. 更新资源包
sudo apt-get update

# 3. 安装证书
sudo apt-get install ca-certificates curl gnupg lsb-release

# 4. 安装官方GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
## 4.1 如果联网下载失败，浏览器中输入 https://download.docker.com/linux/ubuntu/gpg, 把 gpg 下载下来
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg gpg
## 4.2 如何验证密钥是否导入成功
sudo apt-key list

# 5. 建立 Docker 资源库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

// 6. 再次更新
sudo apt-get update

# 7. 安装 Docker 
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 8. 查看是否成功 如果返回一个 docker 的版本，说明安装成功
sudo docker -v
```
注：如果上述安装报错：`Could not connect to download.docker.com`。参考：https://www.runoob.com/docker/ubuntu-docker-install.html ，切换到 mirrors.ustc.edu.cn。

## 2.3 更新镜像源并启动
更新为国内阿里云的镜像源，加快下载速度。
```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{"registry-mirrors": ["https://yxzrazem.mirror.aliyuncs.com"]}
EOF
```
启动命令如下：
```
sudo systemctl daemon-reload
sudo systemctl restart docker
```
但WSL虚拟机上不支持systemctl命令，为此会出现如下报错：`System has not been booted with systemd as init system (PID 1). Can‘t operate.`
原因是系统没有用systemd启动而是init，如何查看系统启动命令：
```
pstree 或者 ps -p 1 -o comm= # 查看系统启动命令
```
所以需要将启动命令改为：
```
sudo service daemon-reload
sudo service docker restart
```
如果遇到如下报错：`/etc/init.d/docker:62: ulimit: limit setting error (Invalid argument)`，
可以参考[这篇blog](https://forums.docker.com/t/etc-init-d-docker-62-ulimit-error-setting-limit-invalid-argument-problem/139424)的做法，修改`/etc/init.d/docker`这个文件的第62行: `-Hn 改为 -n`。然后再重新启动docker:

```
sudo service docker start # 启动
sudo service docker status # 查看是否成功
sudo service docker stop # 停止
```
## 2.4 添加GPU支持
如果本地电脑含有GPU且安装了显卡驱动，为了使得docker容易能够识别且利用GPU，可以通过如下命令进行设置：

```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) # 代表linux系统的版本
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - 
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list 
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit 
sudo service docker start # 重启
```
如何查看本地电脑是否含有 GPU 且安装了显卡驱动，输入指令`nvidia-smi`，如果出现如下结果则说明 GPU 可以正常使用，其中前者代表驱动版本，后者代表最大支持的 cuda 版本，并不意味着实际环境中使用的 cuda 版本：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740164.png)

# 3 Docker使用
## 3.1 获取和管理Docker image

如果要拉去常见的一些开源镜像，直接运行如下指令：
```
# 获取 hello-world 镜像
sudo docker pull hello-world
# 获取 nginx 镜像
sudo docker pull nginx
```
如果要拉取自己放在远程仓库中的镜像：
```
# 这里需要先登陆（见3.3）
sudo docker pull registry.cn-shanghai.aliyuncs.com/liuwei16/docker-test:0.1
```
有关docker image管理的命令：

```
# 列出当前系统中所有 image 文件
sudo docker image ls
# 查看镜像文件的详情信息
sudo docker image inspect hello-world
# 删除镜像文件
sudo docker image rm hello-world
```


## 3.2 启动和运行Docker container
基础命令：
```
# 运行 hello-world 镜像
sudo docker run hello-world # 执行镜像的默认命令然后退出。
# 返回下面这段文字，说明运行成功
## Hello from Docker!
## This message shows that your installation appears to be working correctly.

# 运行 nginx 镜像, --name指定名称 -p 80:80: 将容器的80端口映射到宿主机的80端口，-d 表示后台启动，一般服务端的应用都会放到后台运行
sudo docker run nginx 
sudo docker run --name testnginx -p 80:80 -d nginx
# 我们通过 inspect 命令返回的相关信息，得到 nginx 的默认端口在80，所以访问: 127.0.0.1 可以得到 nginx 的运行成功页面
```

容器管理常见命令：

```
# ps | 当前正在运行的容器
sudo docker ps
# ps -a | 包括正在运行、没有在运行的
sudo docker ps -a
# 暂停容器
sudo docker stop [container id]
# 启动容器 | run 命令开始一个容器之后，就可以用容器的 ID 进行 stop/start 操作
sudo docker start [container id]

# 删除容器, rm 命令删除之后，就不能用 start/stop 操作容器，需要重新 run
sudo docker rm [container id]
sudo docker rm -f $(sudo docker ps -a) # 删除全部
```



更多命令将结合3.3远程仓库进行介绍。

## 3.3 创建和获取远程仓库
首先我们需要创建远程仓库，这里以申请阿里云容器镜像服务（免费）为例，其他仓库如dockerhub、谷歌、亚马逊、腾讯等详见对应产品说明文档。 

首先打开[阿里云容器镜像服务地址](https://cr.console.aliyun.com) 注册成功并开通后页面如下：（选用个人实例-免费）

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740165.png)
然后先创建一个命名空间，再在命名空间中创建镜像仓库：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740166.png)
仓库创建成功后，需要先在本地登陆:
```
# username password分别是你注册的用户名和密码
sudo docker login --username=xx --password=xx registry.cn-shanghai.aliyuncs.com
```
接下来就可以拉取这个地址下的所有公开镜像了，这里介绍更多容器运行的进阶命令：

```
# 拉取一个初始镜像
sudo docker pull registry.cn-shanghai.aliyuncs.com/tcc-public/python:3
# 注意要加版本号否则默认拉latest
sudo docker run registry.cn-shanghai.aliyuncs.com/tcc-public/python:3 # 默认是启动容器然后退出
# 如果要和这个镜像交互的话 加-it指令，默认使用python指令
sudo docker run -it registry.cn-shanghai.aliyuncs.com/tcc-public/python:3 
# 如果要进入这个容器执行操作 加/bin/bash进入终端
sudo docker run -it registry.cn-shanghai.aliyuncs.com/tcc-public/python:3 /bin/bash
# 如果要将本地文件映射到容器中 加-v
sudo docker run -it -v /tmp:/tcdata registry.cn-shanghai.aliyuncs.com/tcc-public/python:3 /bin/bash
# 如果要使用本地gpu环境 加 --gpus all
sudo docker run --gpus all -it registry.cn-shanghai.aliyuncs.com/tcc-public/python:3 /bin/bash
# 如果进去又退出来了 怎么重新进去
sudo docker start 15bf2d3d14d4 # 先启动这个contanier id 
sudo docker exec -it 15bf2d3d14d4 /bin/bash
```
## 3.4 构建自己的镜像
首先本地新建文件夹，准备文件，比如dockerfile main.py run.sh
```
mkdir dockers/tianchi & cd dockers/tianchi
```
DockerFile 用于构建自己的镜像，FROM 代表基于哪个镜像开始构建；RUN 代表执行终端命令，特别注意要先设置默认工作目录，否则会找不到下面的requirements.txt；CMD 代表容器启动后执行的命令，一个 DockerFile 的示例如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740167.png)
main.py 里面是具体函数处理逻辑，比如这里以[天池赛-Docker练习场](https://tianchi.aliyun.com/competition/entrance/231759)这个任务为例，main.py 的具体逻辑如下：
```
import pandas as pd
import json
# data=np.random.randint(1,100,200)
# data=pd.DataFrame(data)
# data.to_csv("/tcdata/num_list.csv",index=False,header=False)
data = pd.read_csv("/tcdata/num_list.csv",header=None)

result_1 = "Hello world"
result_2 = 0
for i,num in enumerate(data[0]):
    result_2 += num
data.sort_values(by=0,ascending=False,inplace=True)
result_3 = list(data[0][:10])
result={"Q1":result_1,
        "Q2":result_2,
        "Q3":result_3
        }
print(result)
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f)
```
run.sh 是入口文件，所有任务都要放在这里，比如我这里只要执行 main.py 即可：
```
# bin/bash 
# nvidia-smi
python3 main.py
```

上述文件准备好后，就可以构建镜像并推送到远程仓库了：

```
# 构建镜像。注意 . 不可以省略 代表打包当前地址下所有文件 {name_space}替换为你刚刚申请的命名空间
sudo docker build -t registry.cn-shanghai.aliyuncs.com/{name_space}/docker-test:0.1 .
# 打包完成应该就在自己的docker image里了，可以执行一下看看
sudo docker run registry.cn-shanghai.aliyuncs.com/{name_space}/docker-test:0.1 sh run.sh
# 推送到镜像仓库
sudo docker push registry.cn-shanghai.aliyuncs.com/{name_space}/docker-test:0.1
```
如果是进入了容器并安装了新的包，如何打包成新的镜像？

```
# 比如进去容器安装了一些python包，退出后可以给它commit一下
sudo docker commit [ContainerId] registry.cn-shanghai.aliyuncs.com/liuwei16/docker-test:0.4
# 注意这个镜像会继承[ContainerId]的初始命令，比如/bin/bash,所以后续启动这个镜像时还需要加上启动命令
sudo docker run registry.cn-shanghai.aliyuncs.com/liuwei16/docker-test:0.4 sh run.sh
```

# 4 关于Docker Compose
> 需求背景是：我们一个服务需要依赖到多个 Docker 容器，那么使用 Docker Compose 这个工具就能很方便的帮助我们管理。

Docker Compose 主要通过配置文件 .yml 定义所有容器的依赖关系。下面以安装 Wordpress 为例进行说明：
```
# 安装docker-compose
sudo apt install docker-compose
# 新建配置文件
mkdir dockers/wordpress & cd dockers/wordpress
touch docker-compose.yml # 输入对应的依赖文件
# 创建实例
sudo docker-compose up -d
# 删除实例
sudo docker-compose down
# 列出目前正在运行相关容器服务,-a列出所有
sudo docker-compose ps (-a)
# 启动
sudo docker-compose start
# 暂时
sudo docker-compose stop
# 重启
sudo docker-compose restart
```
其中 docker-compose.yml 中的内容如下：

```
version: '3.1'

services:

  wordpress:
    image: wordpress
    restart: always
    ports:
      - 8080:80
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
    volumes:
      - wordpress:/var/www/html

  db:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_DATABASE: exampledb
      MYSQL_USER: exampleuser
      MYSQL_PASSWORD: examplepass
      MYSQL_RANDOM_ROOT_PASSWORD: '1'
    volumes:
      - db:/var/lib/mysql

volumes:
  wordpress:
  db:
```

# 5 总结
本文系统梳理了 Linux 系统下如何使用 Docker 技术进行镜像和容器管理，接下来大家就可以愉快地学习更多云原生开发的相关技术啦~

创作不易，如果对你有帮助，辛苦 **关注 点赞** 支持一下啊~
