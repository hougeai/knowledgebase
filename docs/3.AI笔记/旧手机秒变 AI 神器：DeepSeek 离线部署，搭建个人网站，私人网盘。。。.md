
最近 DeepSeek 热度不减，很多朋友也想自己本地搞一个玩玩~

无奈没云服务器？

没关系，这两年手机更新换代这么快，一部闲置手机有吧。

而且这些手机配置都不低，内存起码 4G 起，相比各大云厂商提供的轻量级虚拟机，香的很。

这资源闲置着，多浪费~

**今日分享，推荐一款工具 - Termux，让你的手机秒变个人服务器。**


## 1. Termux 简介
> 开源地址：[https://github.com/termux/termux-app/](https://github.com/termux/termux-app/)

简单说：Termux 是一款运行在 Android 系统上的开源终端模拟器。

GitHub 已接近 39K star！

![](https://i-blog.csdnimg.cn/img_convert/fb48701232dbca3311d07df1e75a45d7.png)


它提供了一个类似 Linux 的环境，即使在没有 root 权限的情况下，也能在手机上运行各种命令行工具和程序。

亮点介绍：

- **功能强大**：它提供了完整的 Linux 环境，支持安装多种编程语言和开发工具，如 Python、Node.js、Ruby、Go 等。
- **包管理器**：Termux 自带包管理器（ pkg 和 apt），可以方便地管理软件包。
- **跨平台工具**：支持 SSH、FTP、Web 服务器等工具。

## 2. Termux 安装
Termux 的安装非常简单，只需下载一个安装包到你手机上。

> 下载地址：[https://github.com/termux/termux-app/releases](https://github.com/termux/termux-app/releases)

目前最新稳定版本是 v0.118.1:

![](https://i-blog.csdnimg.cn/img_convert/610fd7bbc9ffd2a81733f8233c046813.png)

*无法访问 GitHub 的伙伴，我把安装包上传到网盘了，文末自取。*

## 3. Termux 基本配置

手机上安装成功后，打开 Termux 就会进入一个终端界面。

### 3.1 安装包更新
Termux 使用 pkg 作为默认的包管理器，apt 也支持。

- **apt**：Debian 及其衍生发行版的包管理工具。
- **pkg**：pkg 是 apt 的封装，使用方法和 apt 完全一致。


在使用 apt 或 pkg 安装软件包时，Termux 的软件源位于国外，这就是下载速度慢的原因。

因此，我们可以考虑换源：

```
termux-change-repo
```

![](https://i-blog.csdnimg.cn/img_convert/a1989824aed633cb5edd02926860803e.png)

![](https://i-blog.csdnimg.cn/img_convert/231ec3bfdb59eccd3de5f7661bf680a5.png)

换源完成后，更新软件包列表：

```
apt update && apt upgrade
```

![](https://i-blog.csdnimg.cn/img_convert/62ccac632ae61adda5b8f8adbd18d91b.png)

最后，输入如下命令，获取手机存储权限：

```
termux-setup-storage #获取存储权限
```


### 3.2 安装 openssh

手机上操作实在不够丝滑~

为此，我们来安装 ssh 服务，然后用 PC 远程登录操作，岂不爽哉！ 

来，一行命令，手机端安装 openssh：

```
apt install openssh
```
![](https://i-blog.csdnimg.cn/img_convert/3682b6612c8a3c8f6d1523bd37d2733a.png)

一键启动 ssh 服务：

```
sshd
```

最后，看下 ssh 服务有没有成功启动：

```
~ $ ps aux | grep sshd
u0_a18   19402  0.0  0.0 2170988 3536 ?        Ss    1970   0:00 sshd
u0_a18   22366  0.0  0.0 2274224 8348 ?        Ss    1970   0:00 /data/data/com.termux/files/usr/libexec/sshd-session -R
u0_a18   22600  0.0  0.0 2274216 4868 ?        S     1970   0:00 /data/data/com.termux/files/usr/libexec/sshd-session -R
u0_a18   26029  1.0  0.0 2218688 3876 pts/1    S+    1970   0:00 grep sshd
```

如果返回结果中包含sshd，则说明SSH服务正在运行。

### 3.3 查看用户名和 IP 地址
要远程登录，总得有个用户名和地址吧。

先看用户名：

```
~ $ whoami
u0_a18
```
Termux 的用户名默认没有密码，为了远程登录，先改下密码：

```
passwd
```


再看 IP 地址：

![](https://i-blog.csdnimg.cn/img_convert/9e239a5e798e87c06ba323986d4de3b1.png)

### 3.4 SSH 远程登录

在电脑上，打开一个终端输入：

```
ssh u0_a18@192.168.10.10 -p 8022
```

**成功搞定！**

![](https://i-blog.csdnimg.cn/img_convert/5d9f87652887c797bc4e8f7c1ed19d10.png)

进来后，可以看到当前目录：

```
~ $ pwd
/data/data/com.termux/files/home
```

看看存储空间吧：

```
df -h
```

![](https://i-blog.csdnimg.cn/img_convert/b4d24b96b386c7b4df08b4d25c2dc89a.png)

你看看，159 G的空间闲置，多浪费啊。



### 3.5 保持 24H 运行

**手机屏幕熄灭后，连接就断？**

问题来了：Termux如何设置一直在后台运行？

在Android设备上，Termux默认情况下在后台运行会被系统限制。为了确保Termux在后台持续运行：

**方法1：**
- 打开手机的设置；
- 应用 -> 应用列表，找到 Termux 应用。
- 在Termux的应用设置中，找到 电池 或者 耗电管理。
- 找到后台运行或省电策略，设置为不限制。

**方法2：**

在Termux中，可以通过以下命令获取唤醒锁，防止设备进入休眠状态：

```
termux-wake-lock
```

此命令会保持设备唤醒状态，避免因屏幕熄灭导致后台进程被终止。

*！注：不管是启用唤醒锁还是关闭电池优化，都会增加电量消耗。*


## 4. 安装 Linux

毕竟 Termux 和常用的 Linux 发行版相比，对于软件的支持有限。

所以，有必要再装一个 Linux 发行版。

## 4.1 安装 proot-distro

proot 是一种容器技术，用于创建独立的运行环境。而 proot-distro 则是基于 proot 的工具，用于在 Termux 中安装和管理 Linux 发行版。

安装 `proot-distro`：
```
apt install proot-distro
```

完成后，看看支持的 Linux 发行版列表：

```
proot-distro list
```

![](https://i-blog.csdnimg.cn/img_convert/918bc4be8ae05a1df11a3ceee0c6747c.png)

笔者用 Debian 比较多，大家根据自己喜好进行选择：

```
proot-distro install debian
```

安装过程比较慢，出现如下列表，代表安装成功：


![](https://i-blog.csdnimg.cn/img_convert/f14fac03ccffe6a0363aab22362bfdef.png)

登录 debian:

```
~ $ proot-distro login debian
root@localhost:~#
```

---
至此，一台 **4c8g** 200G 磁盘空间，**预装 Linux** 的**高配服务器**，就成功搞定了！

而且 **24H 不间断运行**，给它充点电就行，哈哈。

想干点啥不行：搭建个人网站，云端存储盘，部署 AI 应用。。。


下面就来跑个 DeepSeek 试试~

## 5. 部署 DeepSeek
### 5.1 安装 Ollama
部署 DeepSeek 最简单的工具当属 `Ollama` !

但 Termux 中安装的 Debian，本身就是个容器啊，因此无法安装 docker。

为此，可以考虑源码安装 ollama。

```
curl -fsSL https://ollama.com/install.sh | sh
```

安装成功后，会出现如下提示：

```
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
WARNING: No NVIDIA/AMD GPU detected. Ollama will run in CPU-only mode.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
```

启动 Ollama 服务，并放到后台运行：

```
OLLAMA_HOST=0.0.0.0 
nohup ollama serve > log.txt 2>&1 &
```

### 5.2 拉取 DeepSeek 模型

只能 CPU 跑，拉 DeepSeek 最小的蒸馏模型进行测试吧：

```
ollama run deepseek-r1:1.5b
```
搞定！

![](https://i-blog.csdnimg.cn/img_convert/e531e0a6ed5588f37b20e7bb79c9de38.png)

接下来，拿这个模型对应的服务，放到任何你喜欢的 UI 界面中去玩吧~

## 写在最后

本文分享了如何用 Termux 将旧手机打造成一款个人服务器，并尝试了本地部署 DeepSeek。

**当然，服务器在手，想玩出什么花来，还不是你说了算！**

如果对你有帮助，欢迎**点赞收藏**备用。

*无法下载 termux 安装包的朋友，公众号后台回复 **termux** 自取！*

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。



