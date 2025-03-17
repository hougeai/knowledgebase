前不久，Nvidia 发布了 JetPack 6.2，帮助 Jetson Orin 系列模组，在不增加硬件成本的前提下，实现性能升级，最多可将 AI 性能提升至 **2 倍**。

以笔者手头的 `Orin Nano` 为例：

![](https://i-blog.csdnimg.cn/img_convert/85d056c75cf8e87cf628c21e24c769a4.png)


![](https://i-blog.csdnimg.cn/img_convert/323253927016fec35ab303f5e8730eef.png)

其本质是，通过在 GPU、DLA 内存和 CPU 时钟上提升模组功耗，从而解锁更高频率。

![](https://i-blog.csdnimg.cn/img_convert/689e028062bc75585c9e2f8128eedcec.png)

这里最值得瞩目的是 `MAXN SUPER` ，它是一种无上限的功率模式，支持的时钟频率最高。

不过你也不必担心安全问题，即便在该模式下，如果总功率超过热设计功率（TDP）上限，系统会自动调低频率，降低性能，将设备温度控制在热上限内。

为了成功给 Jetson 开启 `MAXN SUPER` 模式，笔者也踩了不少坑。

**今日分享，希望能帮有需要的朋友少走点弯路。**

## 1. 刷机前准备

首先，准备一根杜邦线或者跳线帽，把板子的 `FC_rec` 与 `GND` 短接，进入`Recovery mode`。

![](https://i-blog.csdnimg.cn/img_convert/125aa180f8fa5756d3e9e6ddc2c0a547.jpeg)

然后，用一根支持数据传输功能的 USB/Type-C 线，将 `Linux` 主机与 `Jetson` 开发套件连接。

最后给 `Jetson` 上电。

你会发现，要给 `Jetson` 刷机，就得搞来一台 `Linux` 主机，笔者本想偷个懒，直接用 `windows` 上的虚拟机 `wsl` 来搞，浪费了不少时间。

下面，分别分享下`踩坑记录`和`成功实践`。

## 2. WSL 刷机（失败）

`Windows Subsystem for Linux (WSL)` 是微软为 Windows 开发的一个兼容层，允许用户在 `Windows` 中直接运行 `Linux` 发行版。

对于简单的 `Linux` 系统使用，还是很方便的，感兴趣的小伙伴可看教程：[Windows上安装Linux子系统，搞台虚拟机玩玩](https://blog.csdn.net/u010522887/article/details/137632509)。

不过 WSL 1 不支持识别主机的 USB 设备，只有 WSL 2 才行，而且还得一番配置，配置步骤如下：

**step 1: 安装 usbipd-win 工具**
- 在 Windows 上安装 usbipd-win，打开 PowerShell（以管理员身份），运行以下命令进行安装：

```
winget install --interactive --exact dorssel.usbipd-win
```
**step 2: Windows 中配置 USB 设备**
- 打开 PowerShell（以管理员身份），运行以下命令：

```
usbipd list
```

![](https://i-blog.csdnimg.cn/img_convert/d41262f1d78f35a06ebdaa7ef0b123b6.png)

- 绑定设备到 wsl：

```
usbipd bind --busid 2-1
usbipd attach --wsl --busid 2-1
```
![](https://i-blog.csdnimg.cn/img_convert/462805c26f25b87caa5882dd433f456a.png)

![](https://i-blog.csdnimg.cn/img_convert/b041ee8a0b5813694b2c84604710e962.png)

**step 3: WSL 中验证 USB 设备**

```
lsusb
```

![](https://i-blog.csdnimg.cn/img_convert/59412549fe875a58336915417653392d.png)

可以看到  `Jetson` 已出现在列出设备中。

**不过，安装过程中，USB 连接经常断开，非常不稳定，最终放弃！**


## 3. Ubuntu 主机刷机（成功）

看来，还是得搞一台 Linux 主机~

这下好，废弃多年的笔记本终于有了用武之地，4G 内存，跑个 Linux 妥妥没问题~

杀入 Ubuntu 官网，发现 Ubuntu 已更新到 24.04，果断 down 下来，一顿操作，居然识别不了硬盘，折腾了半天没找到问题在哪。

最后换了 22.04，系统成功装上，开始刷机！

**刷机有两种方式，下面任选其一即可。**


### 3.1 SDKManager 刷机

在 Ubuntu 主机中，打开浏览器下载 [SDK Manager](https://developer.nvidia.com/sdk-manager)。
> 下载地址：[https://developer.nvidia.com/sdk-manager](https://developer.nvidia.com/sdk-manager)

![](https://i-blog.csdnimg.cn/img_convert/633b94c829a2e0a285d58c67b8ce6e61.png)


下载完成后，进入下载路径进行安装，终端输入：

```
cd Downloads
sudo dpkg -i sdkmanager_2.2.0-xxx_amd64.deb
```

安装过程中如果出现报错，提示找不到依赖文件，输入修复命令：

```
sudo apt update
sudo apt upgrade
sudo apt --fix-broken install
```

确保没有任何报错，安装成功后，终端输入 `sdkmanager` 打开软件。

首先需要用账号登录 `Nvidia` 并进行验证。

如果板子正确进入到 `Recovery mode`，SDK Manager 就会检测到 Jetson Orin Nano 设备，这里选择 Jetson Orin Nano(8GB deceloper kit version)：

![](https://i-blog.csdnimg.cn/img_convert/fbcb81975924d24fee8c2d9cb6677c82.png)

进来后，选择安装哪些内容，`Host Machine` 无需勾选，这是在你的 Ubuntu 主机上安装 cuda 等内容。

最重要的是这里的 `JetPack 6.2` ，2025年1月发布的最新更新，将电源模式从 6.1 的 7W/15W/MAXN提升到 15W/25W/MAXN SUPER，功率更大，因此性能更强。

![](https://i-blog.csdnimg.cn/img_convert/49de434ac62373cc2b2e48aef3ac1608.png)

确认安装内容后，可以看到刷机内容主要包括**三个部分**：

![](https://i-blog.csdnimg.cn/img_convert/2258224c1bb8ae91486f3b3b94bcc699.png)

接下来进入到漫长的安装过程，大约需要 1-2 小时，安装 `Jetson Linux` 系统后，会跳出界面提示输入用户名和密码：

![](https://i-blog.csdnimg.cn/img_convert/95a5f05ae27f60fbd475be7e01e0dce8.png)

这时给板子接上显示器，即可看到界面，完成配网，系统就算安装成功了：

![](https://i-blog.csdnimg.cn/img_convert/129f4e74fbef1982e355990eb84dae4e.jpeg)

如果选择了 Jetson Runtime Components 和 Jetson SDK Components，那么还会继续下面流程：

![](https://i-blog.csdnimg.cn/img_convert/9dab78ccffc1a71deec9084ce6b6abe8.png)


当然，系统已经 ready 了，这部分也可以登录 `Jetson` 开发板再进行安装。


至此，`SDKManager 刷机`的全部流程就结束了！

如果你觉得麻烦，可以接着往下看，采用`命令行刷机`。

### 3.2 命令行刷机

`命令行刷机`相对更简单。

首先，前往官网下载 `Driver Package (BSP)` 和 `Sample Root Filesystem`。
> 下载地址：[https://developer.nvidia.com/embedded/jetson-linux-r3643](https://developer.nvidia.com/embedded/jetson-linux-r3643)


![](https://i-blog.csdnimg.cn/img_convert/97ce209f46d4729a7a487ec9e68d4a79.png)


然后，解压并构建完整的烧录环境：

```
tar xf Jetson_Linux_R36.4.3_aarch64.tbz2 
sudo tar xpf Tegra_Linux_Sample-Root-Filesystem_R36.4.3_aarch64.tbz2 -C Linux_for_Tegra/rootfs/
cd Linux_for_Tegra/
sudo ./tools/l4t_flash_prerequisites.sh
sudo ./apply_binaries.sh
```

过程中，可能缺失安装包，缺啥装啥。

确保看到如下指令，成功烧录环境：


![](https://i-blog.csdnimg.cn/img_convert/bb3eb9eacfdc7fec396d1027c23ad06c.png)

最后，执行如下命令，开始刷机：

```
sudo ./tools/kernel_flash/l4t_initrd_flash.sh --external-device nvme0n1p1 -c tools/kernel_flash/flash_l4t_t234_nvme.xml -p "-c bootloader/generic/cfg/flash_t234_qspi.xml" --showlogs --network usb0 jetson-orin-nano-devkit-super internal
```

看到如下日志，代表刷机成功：

```
Flash is successful
Reboot device
Cleaning up...
Log is saved to Linux_for_Tegra/initrdlog/flash_1-2_0_20250226-163014.log
```

此时，给 Jetson 开发板接上显示器，右上角可以切换 `Power mode`：


![](https://i-blog.csdnimg.cn/img_convert/14debd2c7c76be3291b5d3063f324731.jpeg)

恭喜您，`Jetson` 已经成功进入 `MAXN SUPER` 模式。



## 4. 刷机后体验

### 4.1 安装 jtop 和 nvidia-jetpack

为了实时查看 CPU、GPU、内存等资源的使用情况，还需要安装一个工具：

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo pip3 install -U jetson-stats
```

安装完成后，终端输入 `jtop` 即可启动工具。

然后，安装 `NVIDIA JetPack` 软件包，这里打包了与设备相关的工具、库和驱动程序，包括：cuda cudnn tensorrt 等。
```
sudo apt update
sudo apt install nvidia-jetpack
```

再次打开 `jtop`，发现依赖全部 ready 了：

![](https://i-blog.csdnimg.cn/img_convert/21e095cf751eb0e7e05eaef4bd701b7c.png)
### 4.2 运行频率对比

**刷机前（Jetpack 5.1）**：

![](https://i-blog.csdnimg.cn/img_convert/353bc7e2817999712f5947b055abe229.png)

**刷机后（Jetpack 6.2）**：

![](https://i-blog.csdnimg.cn/img_convert/45102109d06ce29393a1c1c74e491996.png)

*发现 Super 模式下并没有超频？*

这是因为 `jetson clocks` 处于 `inactive` 状态，`jetson_clocks` 用于管理设备的时钟频率，以实现超频和性能优化。

如果 `jetson_clocks` 已安装但未激活，需手动启用：

```
sudo jetson_clocks
```

终于，成功实现超频！

![](https://i-blog.csdnimg.cn/img_convert/ed9ca438b8c8a15ee7f32b7de4149892.png)

### 4.3 LLM 推理速度对比

以 `Ollama` 跑 `qwen2.5:7b` 为例，非流式输出，直接使用输出文本字数进行平均耗时对比。

测试案例如下：

```
messages = [{ "role": "user", "content": "天空为什么是蓝色的"}]
```


**超频前（Jetpack 5.1）**：


```
qwen2.5-7b time: 45.86s, token/s: 9.31
qwen2.5-7b time: 37.87s, token/s: 9.48
qwen2.5-7b time: 44.05s, token/s: 9.72
qwen2.5-7b time: 30.55s, token/s: 9.23
qwen2.5-7b time: 50.36s, token/s: 9.13
```


**超频后（Jetpack 6.2）**：

GPU 利用率打满, 1GHz 满负荷运行，内存占用 7.1 G/7.4G。

```
qwen2.5:7b time: 24.78s, token/s: 12.19
qwen2.5:7b time: 31.17s, token/s: 12.42
qwen2.5:7b time: 32.50s, token/s: 12.74
qwen2.5:7b time: 41.48s, token/s: 12.32
qwen2.5:7b time: 26.86s, token/s: 13.33
```

可以看到，加速比基本符合预期，对应文首第一张图。

超频模式下，2 分钟内，设备温度会迅速上升，这里可以重点关注一下：

![](https://i-blog.csdnimg.cn/img_convert/5b5b19a0fd65cefc56fece97dbc558ce.png)


## 写在最后

本文分享了 JetPack 6.2 的开发环境搭建，并用 Ollama 大模型推理做了一个简单的测速。

如果对你有帮助，欢迎**点赞收藏**备用。

本系列文章，会陆续更新在 Jetson 上完成 AI 应用开发的相关教程，欢迎感兴趣的朋友关注。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

