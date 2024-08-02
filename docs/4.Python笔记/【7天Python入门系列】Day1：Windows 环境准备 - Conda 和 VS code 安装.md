> **写在前面**：本系列文章的起源是最近参加DataWhale组织的一场《聪明办法学Python》活动，不得不说这是一门对小白非常友好的Python入门课。Python作为一门开发语言，涉及的内容非常多，不过走完该系列课程，完全可以达到‘师傅领进门，修行在个人’的目的了。本系列文章将对课程的内容做一个系统梳理和必要补充，便于后续有疑问时随时翻阅。
# 灵魂三问
Q: 什么是 Python
- 一门最适合入门人工智能的编程语言

Q: 为什么学 Python

- ![](https://i-blog.csdnimg.cn/blog_migrate/6c1cdf8bee4f69fe72d0a7520e463568.png)

- ![](https://i-blog.csdnimg.cn/blog_migrate/6a8540da498338d08b87296d17ffc657.png)

Q: 怎么学 Python
- 多动手

# 环境准备
## 安装清单
- Miniconda: 一款开源软件包管理系统，用于管理python环境
- Visual Studio Code: 一款集成开发环境（IDE），用于编写python代码

为什么选用Miniconda？
- Conda：一个可以在不同操作系统（Windows、macOS、Linux）上运行的环境管理系统，可以快速安装、运行和更新软件包及其依赖项，尽管它可以为任何语言打包和分发软件，但用的最多的还是Python。其解决的核心痛点问题是：各种库/包(libraries/package)之间的依赖冲突，通过环境隔离的方式加以解决。
- Miniconda：anaconda的轻量级版本, 只包含conda的基础功能，不过这些基础功能完全够用，其他需要的包可以自由搭配。相比其他环境管理工具，miniconda自带不同版本的python，面向小白更加友好。

为什么选用VS code？
- 一款非常轻量级的IDE，而且各种操作也非常对小白友好，学习成本低，在使用过程中再按需安装各种插件。

## Miniconda
> 这里主要介绍Windows下的Miniconda下载和安装，以及过程可能遇到的坑。Linux系统下安装相对简单一些。
### 下载
首先通过如下链接下载安装包：[最新版 Miniconda For Windows 下载链接](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)
### 安装
双击打开下载好的exe文件，比较推荐的安装配置选项如下：
<p> 
  <img src="https://i-blog.csdnimg.cn/blog_migrate/dd42ccd2ac02ac61ee5270f82df43ed6.png" width="50%" align="left" />
  <img src="https://i-blog.csdnimg.cn/blog_migrate/867e45936ee8cad6154755343b29ac40.png" width="50%" align="right" />
</p>

此外，miniconda默认是安装在C盘，如果你的C盘空间比较紧张，可以选择自定义安装位置，比如通常我习惯将软件安装在D盘，注意路径不能有空格，所以不能放在D:\Program Files之类的文件夹下，最终我选择安装在了D盘目录下的D:\miniconda3。
### Conda初始化
为什么要初始化？
- 在Windows下，PowerShell是比cmd更友好的终端，而且vs code默认使用的也是PowerShell。如果我们将conda初始化到PowerShell环境中，那么我们只要一打开PowerShell，conda的base环境就自动加载了，类似下图所示：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/72c7642adaed6e8f63a2d41320ef9edf.png)

具体怎么实现？
- Step 1: 到安装miniconda的路径下，比如我的就是D:\miniconda3，打开其下的condabin文件夹
- Step 2：在空白处按住Shift键，然后鼠标右键点击，找到”打开PowerShell窗口“。注意：要按住Shift键
- Step 3：在PowerShell窗口中输入 ./conda init --all

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/46f79141ed77511e3633281168d8cd98.png)
如果没什么问题，conda会自动注册到PowerShell上, 下次启动PowerShell就会自动加载base环境了。

如果遇到报错提示”权限问题“，此时说明需要用管理员权限打开PowerShell窗口，如下图所示:
- 找到键盘上的Windows键（通常位于左下角的Ctrl键和Alt键之间）
- 搜索框输入powershell，并点击”以管理员身份运行“，
- 打开PowerShell窗口后，需要首先cd到condabin目录下，比如我的就是cd D:\miniconda3\condabin
- 最后再输入 ./conda init --all

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/cdddfd3ba61ec32e4cff68ec355feb01.png)
如果重新打开 PowerShell 遇到如下报错：

```
. : 无法加载文件 C:\Users\12243\Documents\WindowsPowerShell\profile.ps1，因为在此系统上禁止运行脚本。有关详细信息，请参
阅 https:/go.microsoft.com/fwlink/?LinkID=135170 中的 about_Execution_Policies。
所在位置 行:1 字符: 3
+ . 'C:\Users\12243\Documents\WindowsPowerShell\profile.ps1'
+   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) []，PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

原因是：脚本执行策略受限。怎么解决?

更换脚本执行策略：以管理员身份运行 PowerShell ，然后输入 set-ExecutionPolicy RemoteSigned，然后输入 Y。

```
PS C:\Windows\system32> set-ExecutionPolicy RemoteSigned

执行策略更改
执行策略可帮助你防止执行不信任的脚本。更改执行策略可能会产生安全风险，如 https:/go.microsoft.com/fwlink/?LinkID=135170
中的 about_Execution_Policies 帮助主题所述。是否要更改执行策略?
[Y] 是(Y)  [A] 全是(A)  [N] 否(N)  [L] 全否(L)  [S] 暂停(S)  [?] 帮助 (默认值为“N”): Y
```
更换完成后，使用命令 get-ExecutionPolicy 查看脚本执行策略。

```
PS C:\Windows\system32> get-ExecutionPolicy
RemoteSigned
```

这时再打开 PowerShell 就不报错了，完美解决~
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/03306ca85dd488318066e885edbc3db9.png)



### Conda配置
安装完成后，首先我们需要先进行一番配置，以便后续获得最佳的开发体验。conda配置无外乎需要做如下几件事情：
#### 更换镜像源
当我们安装各种包的时候，如果直接使用pip install或者conda install会很慢，因为默认是从国外的镜像源去下载的，而目前我国访问海外网络的带宽很低，为此，我们需要修改一下pip和conda的默认镜像源
- pip换镜像源(两种方式)：
  - 新建 C:\Users\%你的用户名%\pip\pip.ini文件，打开后添加如下内容，这样默认从国内的阿里云镜像站下载各种安装包

  ```
  [global]
  index-url=http://mirrors.aliyun.com/pypi/simple/
  [install]
  trusted-host=mirrors.aliyun.com
  ```
  -   在PowerShell窗口中输入:`pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/`

- conda换镜像源：
  - 在PowerShell窗口中输入如下指令，然后会在`C:\Users\%你的用户名%\`文件下生成`.condarc`这个文件

  ```
  conda config --set show_channel_urls yes
  ```

  - 可以用记事本打开`.condarc`，然后填入如下指令，就可以使用清华源了
  ```
  channels:
    - defaults
  show_channel_urls: true
  default_channels:
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
    - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
  custom_channels:
    conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
    pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  ```

当然国内还有很多不错的镜像源，例如：
- 更多pip镜像源：
  - 阿里云 http://mirrors.aliyun.com/pypi/simple/ 
  - 中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/ 
  - 豆瓣(douban) http://pypi.douban.com/simple/ 
  - 清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/ 
  - 中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/ 
  - 校园网联合镜像 https://help.mirrors.cernet.edu.cn/pypi/
- 更多conda镜像源：
  - 清华大学 https://help.mirrors.cernet.edu.cn/anaconda/
  - 南方科技大学 https://help.mirrors.cernet.edu.cn/anaconda-extra/

#### 设置环境默认安装位置
conda有一个基础环境base环境,  这个也是系统环境。如果你要新建环境, 会默认新建到C盘，而 conda新建的环境随着安装包增多，其占用的空间会大的离谱，**所以如果你不想让你的C盘很快爆满的话，最好重新设置下conda的默认安装环境**。同样还是在`.condarc`中添加：
```
envs_dirs:
  - D:\miniconda3\envs
```
#### conda基础命令
创建新环境：

```
conda create --name=labelme python=3.8
conda create -p D:\miniconda3\envs\labelme python=3.8
# --name 指定环境名称，-p指定安装位置
# 如果不指定python版本，会默认使用系统python版本，后面安装的所有包都会安装到系统python环境中
# 如果显示没有权限：右键点击目标文件夹，选择"属性"，然后进入"安全"选项卡，确保你的用户账户具有对该文件夹的完全控制权限。
```
启动/退出新环境：

```
source activate labelme
# 或者
conda activate labelme
conda deactivate
```
删除环境：
```
conda remove --name py39 --all
```

列出所有环境：
```
conda env list
conda info -e
```
## VS code
首先通过如下链接下载安装包：https://code.visualstudio.com/，双击安装即可
这里重点介绍下如何安装插件：左侧找到Extension组件，搜索框中输入需要安装的插件，点击右侧Install

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f52780c6faecfc72d3e358c85240e3f6.png)

VSCode 推荐安装的插件清单如下：
- Python
- Jupyter
- Office Viewer(Markdown Editor)
- Chinese (Simplified) (简体中文) Language Pack for Visual Studio Code
# 总结：
本篇主要介绍了学习Python之前的准备工作，主要介绍了Python环境管理工具Miniconda和开发者工具VS code的安装，下篇文章我们将从0到1开始学习Python编程语言的一些基础概念。
