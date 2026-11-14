
随着手头的小智 AI 开发板日益增多，提高固件制作效率，逐渐提上日程。

![](https://i-blog.csdnimg.cn/img_convert/81c0709ddb0d9759cf2d9f38a028476a.jpeg)

目前，市面上的开发板主要围绕 ESP32 展开，因此绕不开配套的软件环境 ESP-IDF。

不过，Windows 环境下，编译一次小智 AI 固件，实在太慢了。

今日分享，`在 windows 主机上提高编译效率`的最佳实践，希望给有类似困惑的伙伴一点点参考。

## 1. Linux 编译环境准备

相同 ESP32 工程，在 Linux 下编译可达 Windows 的 ‌2–3倍‌。

实测发现远不止这个提速。

为啥？

- Linux的EXT4文件系统对大量小文件（如编译中的头文件和源码）的读写效率显著高于Windows的NTFS；
- ESP-IDF 用 GCC 作为编译器，GCC等工具链在Linux下为原生运行，无需兼容层；

因此，**强烈建议切换到 Linux 系统**，安装和配置 ESP-IDF 开发环境。

那么，如何`在 windows 主机上拥有 Linux 系统？`

- 租一台云主机，远程登录 Linx 服务器
- 安装 WSL2

由于之前都是`远程登录 Linux 服务器`进行开发，所以自然尝试了第一种方案：
`windows2linx串口转发`。

不过，先后尝试了`Ser2Net`、`com2com+hub4com`和`socat-windows`，均以失败告终。因为，ESP-IDF 串口通信时，不仅仅是转发数据，还需要完整的硬件串口控制线。

无奈之下，只好重装 windows 下的 Linux 虚拟机 WSL2。
> 关于 WSL2，可参看之前的教程：[Windows上安装Linux子系统，搞台虚拟机玩玩](https://zhuanlan.zhihu.com/p/689560472)

## 2. ESP-IDF 安装

ESP-IDF 的依赖非常复杂，因此推荐在 VsCode 中，通过插件方式进行安装。

![](https://i-blog.csdnimg.cn/img_convert/3fe7e363123ae848e53e1338474f24bb.png)

插件安装完成后，点击左下角`设置`-`command palette`:

![](https://i-blog.csdnimg.cn/img_convert/24e95e157711b2596cf21cb633467ff1.png)

搜索并找到`Configure ESP-IDF Extension`：

![](https://i-blog.csdnimg.cn/img_convert/c222f749a411d320462b88524a7020d0.png)

选择快速安装方式即可：

![](https://i-blog.csdnimg.cn/img_convert/49973b2f6158f7ba95e68e133d2ce0ad.png)

选择官方服务器，指定下载的 ESP-IDF 版本（**最新版小智固件需要v5.4**）:

![](https://i-blog.csdnimg.cn/img_convert/5173d3a1334e7e3690f8aa0de014f8be.png)

等待安装完成：

![](https://i-blog.csdnimg.cn/img_convert/e067260b85da2fad06c37e96228466ab.png)

注：以上安装过程，不论是 windows 还是 Linux 上，都是通用的。

## 3. USB 端口映射

ESP-IDF 安装完成后，在 WSL 上无法识别主机的 USB 端口。

怎么搞？

笔者在之前的 Jetson 刷机教程中，介绍过一款工具 `usbipd-win`：

[Jetson 超频刷机教程！解锁端侧AI推理怪兽的算力极限](https://zhuanlan.zhihu.com/p/28265586559)


打开 PowerShell（以管理员身份），一行命令进行安装：

```
winget install --interactive --exact dorssel.usbipd-win
```

安装完成后，先看看都有本地主机有哪些 usb 端口：

```
usbipd list
```

![](https://i-blog.csdnimg.cn/img_convert/04fa952c2618ca0fda62752374497f0f.png)

图中的 2-2 端口连接的 esp32 官方的开发板，这里的 CH340 是一种串口转 USB 芯片，用于将串口通信转换为 USB 通信。

绑定这里的 2-2 端口到 wsl：

```
usbipd bind --busid 2-1
usbipd attach --wsl --busid 2-1
```

此时，再看端口状态变更为 `Attached`，这时 wsl 中已经可以识别到这个设备：

![](https://i-blog.csdnimg.cn/img_convert/766cd3d196e4b51427f613064d7731c1.png)

来到 wsl 中查看下：

```
# wsl上查看
sudo apt-get install usbutils
lsusb
```

此外，CH340 在 Linux 上需要 ch341 驱动：

```
# 尝试加载 ch341 内核模块
sudo modprobe ch341
# 然后再试试
dmesg | grep ch34
ls /dev/ttyUSB*
~ /dev/ttyUSB0
```

到这里，一个 USB 串口设备就建立好了。

因此，最终串口选择 `/dev/ttyUSB0`：

![](https://i-blog.csdnimg.cn/img_convert/dd6452c0cac28b988fa360b2aeade70e.png)

如果遇到报错：

```
([Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied: '/dev/ttyUSB0')
```

这是因为当前用户没有读写权限：

```
ls -l /dev/ttyUSB0
crw------- 1 root root 188, 0 Jun 22 10:29 /dev/ttyUSB0
```

最简单的方式，就是改为`所有人可读写`：

```
sudo chmod 666 /dev/ttyUSB0
```

不过，因为 `/dev/ttyUSB0` 是由内核动态创建的：当插拔设备，或者 WSL 重启，文件会被删除并重新创建，所以需要再次修改权限。

至此，你就可以愉快地从 Linux 上编译固件，并通过串口转发，把固件刷到本地设备上。


## 写在最后

本文分享了 `如何快速编译和刷写小智AI固件`。

如果对你有帮助，欢迎**点赞收藏**备用。
