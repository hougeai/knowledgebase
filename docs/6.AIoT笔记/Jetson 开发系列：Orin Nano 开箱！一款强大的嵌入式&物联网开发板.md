
边缘计算作为 AI 的一个重要应用场景，面临着前所未有的机遇与挑战。

谈及 AI，自然绕不开 NVIDIA 的产品：

![](https://img-blog.csdnimg.cn/img_convert/6546c5c879bdba1ed7d25e3709851857.png)

其中，**Jetson 系列**均为 AIoT 设备打造，功耗低是其最大的特点。以我手头的 Jetson Ori Nano 为例，**满载功耗不过 15W**。

@[TOC]
## 1. 关于 Jetson 你最关心的

从2015年推出第一代 Jetson TK1 开始，NVIDIA 不断推出性能更强的 Jetson 产品，下面是不同主板的算力图。

![](https://img-blog.csdnimg.cn/img_convert/192fb09300df554000eb259b7916c35a.jpeg)

那是不是意味着算力越高，越值得拥有呢？

也未必，还得看一个参数：GPU Compute Capability（GPU计算能力）。

这玩意是 NVIDIA 定义的一个术语，用于描述 GPU 执行并行计算任务的能力。不同的 Compute Capability 版本意味着支持不同的 CUDA 特性，以及不同的计算性能和内存带宽。

不同 Jetson 主板的 Compute Capability 怎么样？

![](https://img-blog.csdnimg.cn/img_convert/041cc46a163440670be5a82efcb07c39.png)

在预算充足的情况下，建议入手 Compute Capability 高的板子，会省掉后续很多麻烦。

## 2. 性价比之王- Jetson Ori Nano

为何选择 Jetson Ori Nano？

Jetson Orin Nano 是 Jetson Nano 的升级版，算力提升了80倍，高达 40 TOPS（每秒万亿次）的计算性能，为曾经难以企及的复杂 AI 模型铺平了道路。

放一张图给大家感受下：

![](https://img-blog.csdnimg.cn/img_convert/a3c7c52e93c6c79f50a8e0ec56063fae.png)

核心参数，单独摘出来：

**模组：**
- GPU：不同于 Jetson NANO 的 Maxwell 架构，Orin NANO 是基于 Ampere 架构，具有 1024 个 CUDA 核心和 32 个 Tensor 核心；
- CPU：6 核 Arm Cortex-A78AE 64位CPU；
- 内存：4/8GB 128-bit LPDDR5，68GB/s 的带宽。注：**系统内存和 GPU 显存共享**，内存分配根据 CPU 和 GPU 的需求动态调整。

**载板正面接口：**
- 一个 DP 接口接显示屏；
- 四个 USB 3.1 Type A 接口；
- 一个千兆以太网端口；
- 一个 USB-C 接口（用来传输数据，而非供电）

**载板底部接口：**
- 一个 M.2 Key E 接口，出厂已接了无线网卡，所以可以连 Wifi 和 蓝牙；
- 两个 M.2 Key M 接口，可以扩展 SSD 存储。

板子正面图，小巧且强悍：

![](https://img-blog.csdnimg.cn/img_convert/1829082c5790dd6ee4bb1f9dd92fdda0.jpeg)


##  3. 开箱测评

如果你在国内厂商那购买，一般都烧录好了镜像，因此你拿到手的是：
- 硬件：Jetson 模组；
- 软件：Ubuntu 20.04 操作系统 + JetPack™ SDK。

记得保留所有配件和外包装盒，因为 NVIDIA 提供为期一年的质保。

**接下来，带大家开机实操感受一下。**

### 3.1 开机启动

首先，把烧录好镜像的固态硬盘，插进载板底部的卡槽中：

![](https://img-blog.csdnimg.cn/img_convert/aa5011df49d91b7d6baf54e2b42c6b51.jpeg)

记得一定把天线接到载板底部的网卡处，否则 WIFI 信号会很弱的。

联网成功后，需要更新一下源，否则后面安装一些库会很痛苦：

```
 sudo apt-get update
 sudo apt-get full-upgrade
```

![](https://img-blog.csdnimg.cn/img_convert/57bc790c6ddba2e7a4d48885046751a5.jpeg)

最后，用 HDMI 线连到一台显示器，插电自动开机，风扇转起来。


### 3.2 桌面环境
Jetson 官方系统是ubuntu20.04，因此自带桌面环境，右上角先把 WIFI 连上吧。

此外，我还尝试了连接蓝牙音箱，**蓝牙可以配对成功，但是音频设备识别不了，一直没找到解决方案**，懂的小伙伴评论区交流下啊。

![](https://img-blog.csdnimg.cn/img_convert/b91f552b82b721e4a30efc7ed457e5d8.png)


### 3.3 VNC 远程桌面

有同学说，我没有那么多显示屏怎么办？

远程桌面了解下？

不了解的小伙伴可回看：[【保姆级教程】Windows 远程登录 Ubuntu桌面环境](https://blog.csdn.net/u010522887/article/details/138137107)

Ubuntu 中远程桌面主要有两种方式：上篇教程中我们主要讲的是 xrdp，本篇我们来聊聊 如何使用 VNC。

简单来说，VNC 配置分两步：服务端和客户端。

**服务端：**

安装 vino:

```
sudo apt update
sudo apt install vino
```
设置 vino 登录选项：

```
gsettings set org.gnome.Vino prompt-enabled false
gsettings set org.gnome.Vino require-encryption false
gsettings set org.gnome.Vino authentication-methods "['vnc']"
# 设置自己的登录密码
gsettings set org.gnome.Vino vnc-password $(echo -n 'yourpassword' |base64)
```

启动服务：

```
/usr/lib/vino/vino-server
```

设置开机自启动：

```
gsettings set org.gnome.Vino enabled true
mkdir -p ~/.config/autostart
vim ~/.config/autostart/vino-server.desktop
# 填入如下内容
[Desktop Entry]
Type=Application
Name=Vino VNC server
Exec=/usr/lib/vino/vino-server
NoDisplay=true

```

**客户端：**

服务端启动成功后，需要下载 VNC viewer 软件，以 RealVNC 为例，新建一个连接，这里填入 IP 地址即可，VNC server 默认端口号是 5900。

![](https://img-blog.csdnimg.cn/img_convert/a207b1801effefc33e42db8ac518a95f.png)

注意：使用 VNC 桌面，需要接好 DP 线，否则无法进入桌面。

### 3.4 SSH 远程登录
当然，相信拿到这块板子的你，一定是不会需要桌面环境的，因为它太占内存拉。**实测关闭桌面环境，可省出 800M+ 的内存空间。**

如何关闭桌面环境？

如果是临时关闭：

```
sudo init 3     # stop the desktop
sudo init 5     # restart the desktop
```

如果要永久关闭：

```
# 关闭桌面环境
sudo systemctl set-default multi-user.target
# 开启桌面模式
sudo systemctl set-default graphical.target
# 立即打开桌面
sudo systemctl isolate graphical.target
```

接下来，你只需要远程登录它进行开发就 OK 了。

如何远程登录，看这篇就够了👉：[【保姆级教程】Windows 远程登陆 Linux 服务器的两种方式：SSH + VS Code，开发必备](https://blog.csdn.net/u010522887/article/details/138187926)

### 3.4 熟悉 jtop
最后，你还需要了解下 jtop。

也许你已经习惯了用 `nvidia-smi` 来查看显卡运行状态。

不好意思，在 Jetson 系列板卡中，你用不了 `nvidia-smi`。

因为 Jetson 板卡使用的是专门为嵌入式系统优化的驱动和API，如 CUDA for Tegra。

不过，JetPack™ SDK 提供了 jtop 命令。

类似于 Linux 系统中的 top 命令，jtop 用于监控 Jetson 设备的性能和资源使用情况：

- GPU/CPU 使用率
- 内存使用
- 存储使用
- 网络状态
- 进程信息
- 温度：对监控设备是否过热非常重要。

贴张图给大家感受下，关闭桌面环境 + 三个docker容器，共占用 1.1G 内存空间。

![](https://img-blog.csdnimg.cn/img_convert/d602dece89c979f43089e0f13b4063a7.png)

按下 7，可以查看系统信息，和内置软件包的版本，后面开发过程中你一定会用到的。

![](https://img-blog.csdnimg.cn/img_convert/a0a29eb74c4d4988006c1b0840ef4d7c.png)

## 写在最后
至此，你的 Jetson 开发环境就基本搭建好了。

如果对你有帮助，欢迎**点赞收藏**备用。

本系列文章，会陆续更新在 Jetson 上完成 AI 应用开发的相关教程，欢迎感兴趣的朋友关注。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。
