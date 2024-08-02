# 0 写在前面
很多情况下代码开发需要依赖 Linux 系统，比如安装 Docker 容器来实现代码隔离，然而问题是大部分同学的电脑都是 Windows 系统，这时就会出现大量报错，经历过的同学一定是边踩坑边落泪。

如何**免费**拥有一台 Linux 服务器呢？
- 薅各大云厂商的羊毛，很多厂商对学生都会有优惠，羊毛不薅白不薅，不过问题是不可能让你一直白嫖啊，你总有花钱的时候。
- 在自己的 Windows 电脑上安装一个 Linux 子系统，随时随地都能本地跑代码，装好一次一劳永逸，针对初学 Linux 开发来说足够使用了。

那么，如何在 Windows 电脑上安装 Linux 子系统呢？ 这里也有两种方式：
- 安装虚拟机软件，比如 VMware Workstation Player
- 使用自带的WSL，Windows Subsystem for Linux

对于早期的 Win 操作系统，通常都会采用第一种方式进行安装，而对于 Win10 Win11 系统的小伙伴来说，笔者优先推荐第二种方式，原因下面说，本篇文章我会带大家实践第 2 种方式，分分钟时间搞定一台 Linux 服务器！

# 1 什么是WSL和WSL2
WSL：全称为Windows Subsystem for Linux，这是微软官方开发的[适用于 Linux 的 Windows 子系统](https://learn.microsoft.com/zh-cn/windows/wsl/)，可让开发人员直接在 Windows 上按原样运行 GNU/Linux 环境，且不会产生传统虚拟机或双启动设置开销。

WSL2：具有WSL1的优点，但使用实际的Linux内核，因而性能更好。

下面是官网给出的二者功能比较：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/13f7e1cc32ad8d2978c22ddadf0e9259.png)
WSL有什么优势：
- VMware等虚拟机软件资源消耗大、启动慢、运行效率低。
- 而WSL几乎能运行完整的操作系统，资源消耗小、启动快、切换快

对于没有用过虚拟机软件安装Linux系统的小伙伴而言，直接无脑用WSL2完事！


# 2 如何用WSL2安装Linux
## 2.0 检查是否支持安装
WSL需要电脑支持 Hyper-V 虚拟化，如何查看？
打开一个终端，cmd 或者 PowerShell 都可以，输入如下命令：

```
systeminfo
```
看到如下信息说明电脑就支持：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/2bf77202fa4d74ed90356caeac7cefdb.png)

##  2.1 开启windows的WSL支持
首先在Win11开始菜单搜索“Windows 功能”，打开`启动或关闭 Windows 功能`，勾选Linux子系统以及虚拟机平台2个选项。注意需要按照提示，重启电脑。![](https://i-blog.csdnimg.cn/blog_migrate/1d8c4d82858ba251da3ad933c292bb23.png)

## 2.2 (方式一)安装在系统盘

### 2.2.1 安装
打开终端，输入如下命令即可自动安装到系统盘中：

```
wsl --install # 此时会默认安装最新的Ubuntu发行版。
```
如果希望选择其他版本的 Linux 系统，可以通过如下命令查看：

```
wsl --list --online
```
可以看到wsl支持的 Linux 系统有如下版本：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e05cbcc48e8dc280e03bae258d8c0c8e.png)
如果要安装指定版本，可以采用如下命令：

```
 wsl --install -d <发行版名称>
```
注意，上述步骤中，可能遇到` 0x800701bc`错误，如下：

```
Installing, this may take a few minutes...
WslRegisterDistribution failed with error: 0x800701bc
Error: 0x800701bc WSL 2 ?????????????????? https://aka.ms/wsl2kernel
```
这时需要下载wsl升级包并安装：https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi

双击安装后，再重新执行上述指令就 OK 了。

此外，还可以通过如下指令，查看电脑装了哪些Linux系统，并进行卸载：

```
# 查看本机安装了哪些子系统：
wsl --list --all
# 卸载：
wsl --unregister <System_name>
```
### 2.2.2 转移
因为 wsl 默认将Linux安装在系统盘C盘，后续所有 Linux 系统上安装的软件和数据都会在C盘，你会发现你的C盘很快就爆了！所有非常有必要将它迁移到其他盘上:

```
# 1） 停止正在运行的wsl
wsl --shutdown
# 2）将需要迁移的Linux，进行导出
wsl --export Ubuntu D:/export.tar
# 3）导出完成之后，将原有的Linux卸载
wsl --unregister Ubuntu
# 4） 然后将导出的文件放到需要保存的地方，进行导入
wsl --import Ubuntu D:\export\ D:\export.tar --version 2
```
## 2.3 (方式二)安装在D盘
也许你觉得迁移会比较麻烦，所以初次安装时我们可以直接选择安装在 D 盘。
首先，需要将要安装的系统下载下来，这里以 `Ubuntu20.04` 为例，打开终端，输入如下指令：

```
Invoke-WebRequest -Uri https://wsldownload.azureedge.net/Ubuntu_2004.2020.424.0_x64.appx -OutFile Ubuntu20.04.appx -UseBasicParsing

Rename-Item .\Ubuntu20.04.appx Ubuntu.zip 

Expand-Archive .\Ubuntu.zip -Verbose 

cd .\Ubuntu\ 

.\ubuntu2004.exe
```
根据要求设置用户名和密码即可。

后续如何打开和关闭系统呢：

```
# 打开
cd D:\linux\Ubuntu 
.\ubuntu2004.exe
# 关闭
wsl --shutdown
```

# 3 登陆Linux安装软件
## 3.0 如何查看 IP 地址
- Windows: 终端输入 `ipconfig`
- Linux: 有如下三种方式

```
ifconfig # 需要 sudo apt install net-tools
hostname -I
ip addr show eth0
```
## 3.1 VScode如何访问wsl：
- 打开vscode - 安装wsl插件，然后点击左下角的ssh -> Connect to WSL，可以登陆这台 Linux 服务器了


## 3.2 安装 `ssh`（远程登陆+文件传输）
Linux 中安装 ssh：
```
sudo apt install openssh-server
sudo service ssh start # 启动
sudo service ssh status # 查看启动状态
```
远程登陆：

```
ssh liuwei@172.17.4.63
```

文件传输：

```
scp xxx.file liuwei@172.17.4.63:~/datasets/
```

此时远程登陆和文件传输，都会出现如下报错：
```
liuwei@172.17.4.63: Permission denied (publickey).
```
这是因为 Linux 拒绝访问，有两种方式解决：
- 开启密码验证
- 使用密钥认证

### 3.2.1 开启密码验证
在 Linux 服务器上，vim 打开`/etc/ssh/sshd_config`，然后修改其中的PasswordAuthentication值为 yes ，然后重启 ssh 服务。

```
sudo vim /etc/ssh/sshd_config  PasswordAuthentication改为yes
sudo service ssh restart
```
### 3.2.2 使用密钥认证
如果你觉得每次都要开启密码认证，非常麻烦，可以考虑使用密钥认证。你需要在Windows机器上生成一个SSH密钥对,然后将公钥添加到 Linux 的`~/.ssh/authorized_keys`文件中。
具体而言：

首先需要下载并安装Git for Windows，然后打开Git Bash终端：
```
# windows上生成SSH密钥对
ssh-keygen
```
在.ssh文件夹中生成了密钥文件，其中id_rsa是私钥，id_rsa.pub是公钥。然后将id_rsa.pub中的内容复制到 Linux 的`~/.ssh/authorized_keys`文件中。

## 3.3 安装 Python

```
sudo apt-get update
sudo apt-get install python3
# 默认安装的是python3.8.10
sudo ln -s /usr/bin/python3 /usr/bin/python
sudo apt-get install python3-venv # 安装虚拟环境需要的包
sudo apt-get install python3-dev
```

## 3.4 安装 `conda`
### 3.4.1 什么是 conda
什么是`conda`以及如何在 Windows上安装 `conda`，可以参考笔者之前的一篇文章：[【7天Python入门系列】Day1：环境准备-Conda和VS code安装](https://blog.csdn.net/u010522887/article/details/136969406).
### 3.4.2 如何安装
这里主要介绍如何在 Linux 系统中安装`conda`：

```
# 下载
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
# 安装
sh /Miniconda3-latest-Linux-x86_64.sh
```
注意，安装过程中会询问`Do you wish to update your shell profile to automatically initialize conda?`

其实是问是否希望conda初始化base环境，此处如果选择no，会发现环境变量中并没有conda命令，而真正的命令在/home/liuwei/miniconda3/bin/conda，**所以最好选yes**。

这样的话，每次打开终端都会激活 conda 的 base 环境。如果不想每次启动终端都激活conda环境，可以执行：
```
conda config --set auto_activate_base false # 会生成~/.condarc
```
### 3.4.3 切换镜像源
参考如下方式添加国内的镜像源，这样安装各种包时下载速度会更快。
```
# 添加channels
conda config --set show_channel_urls yes 
vim ~/.condarc
# 然后输入
channels:
  - defaults
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```
## 3.5 安装更多软件...
大家还可以按自己所需，安装指定的软件，比如代码隔离要用到的 Docker ，再比如深度学习需要用到的 CUDA Cudnn 等，由于这两都比较麻烦，笔者打算专门开一篇教程。敬请关注哦！

# 总结
至此，Windows上安装Linux子系统的教程就结束了，接下来大家就可以愉快地学习 Linux 开发的相关技术啦~

创作不易，如果对大家有帮助的话，辛苦 **关注 点赞** 支持一下啊~
