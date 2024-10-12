上篇带大家在 Jetson 开发板上搭建好了环境：

[Jetson 开发系列：Orin Nano 开箱！一款强大的嵌入式&物联网开发板](https://blog.csdn.net/u010522887/article/details/142677847)

如果说板子的算力是大脑，那么我们还需要给它接入： `眼睛`、`耳朵`和`嘴巴`，这样才是一个完整的机器人嘛。

对应到设备上：
- `眼睛` == 摄像头；
- `耳朵` == 麦克风；
- `嘴巴` == 扬声器；

这个好办，市面上随便买一款三合一的摄像头就能搞定。

内置麦克风和扬声器，大概长下面这样：我把商标打码了，以免有打广告的嫌疑。

![](https://img-blog.csdnimg.cn/img_convert/449ce27835908083e5df798d102bbb14.jpeg)

好用不贵，USB免驱，唯一的缺点是单声道输出，对音质有要求的小伙伴慎入哈。

问题来了：在 Linux 系统中，**我怎么管理这些音频设备呢？本文就来系统地盘一盘**。

## 1. 关于 ALSA

ALSA（Advanced Linux Sound Architecture）是 Linux 中广泛使用的开源音频系统。它提供了对音频设备的低级访问，是许多音频应用程序与 Linux 内核之间的桥梁。

ALSA 不仅包括内核驱动，还包括各种工具，如libasound、alsamixer、aplay、arecord等。
- **音频播放和录音**：aplay和arecord，分别用于播放和录制音频文件。
- **混音器控制**：alsamixer，一个基于文本的混音器界面，允许用户调整音频设备的音量和混音设置。
- **广泛硬件支持**：包括但不限于PCI声卡、USB音频设备、HDMI音频等。
- **兼容 PulseAudio**：PulseAudio是一个更高级的音频服务器，提供了更复杂的音频路由、混音等功能，其中 pactl 是 PulseAudio 的命令行工具。

如果你系统上还没安装，可以采用如下命令一键安装：

```
sudo apt-get install alsa-base
sudo apt-get install alsa-utils
```

## 2. 音频设备管理

查看声卡信息：

```
cat /proc/asound/cards
```

前两个是内置声卡，最后是刚插入的自带麦克风扬声器的 USB 摄像头：

![](https://img-blog.csdnimg.cn/img_convert/03070eca0e8d403efbbcc1b880bd577c.png)

接下来，我们需要了解两个专有名词：
- sources：输入设备，比如麦克风，对应 arecord 命令；
- sinks：输出设备，比如扬声器，对应 aplay 命令。

**列出所有输入设备：**

```
arecord -l
# 对应PulseAudio中的命令
pactl list short sources
```

这里可以看到设备号，后面需要用到：

![](https://img-blog.csdnimg.cn/img_convert/6b6d7093ffffe499a3fe447facc6ff40.png)

**列出所有输出设备：**

```
aplay -l
# 对应PulseAudio中的命令
pactl list short sinks
```


## 3. 查看音频设备信息

拿到设备号后，我们就可以调用设备进行`音频播放和录音`了。

不过，还是先来看看设备相关信息吧，其中`2,0`代表设备号：

```
arecord -D hw:2,0 --dump-hw-params | grep '^CHANNELS'
```

关于音频，我们需要了解的主要有两个参数：
- **声道**：Mono 代表单声道，Stereo 代表立体声-两声道，Quad 代表四声道，当然还有 5.1环绕声/7.1环绕声/杜比全景声，一般我们用不到。
- **采样率**：模拟信号转换成数字信号，每秒钟采集样本的次数，通常以赫兹（Hz）为单位，常见的有：
  - 8/16K：常用于电话通信，因为人声的频率通常在 300 到3400 Hz；
  - 22.05K：FM广播的采样率；
  - 44.1 kHz：CD音质的标准采样率，
  - 48 kHz：数字音频和视频制作的标准采样率，常用于电影和专业音频。

![](https://img-blog.csdnimg.cn/img_convert/3c93b385ad94419e97e9ba5a426c4de5.png)


## 4. 音频播放和录音

**如何录音：**

```
arecord -D hw:0,0 -f S16_LE -r 16000 -c 1 -d 5 output.wav
```
参数说明如下：
- -D hw:0,0：指定录音设备。hw:0,0 表示使用第一个声卡的第一个设备。

- -f S16_LE：设置音频文件格式。S16_LE 表示 16 位小端格式（Signed 16-bit Little Endian），一种常用的音频数据格式，“小端”指数据的低位字节存储在内存的低地址端。

- -r 16000：设置采样率。

- -c 1：设置声道数。

- -d 5：设置录音时长/秒。



**如何播放音频：**

```
aplay -D hw:0,0 -f S16_LE -r 16000 -c 1 data/audios/1.wav
```

如果指定采样率和原始音频不匹配，会出现“混叠”，这时你需要用 ffmpeg 转换一下参数：

```
ffmpeg -i data/audios/1.wav -ac 1 -ar 48000 data/audios/2.wav
```


如果你发现：播放音频的指令运行没啥问题，但就是不出声？

接着往下看！

## 4. 音量调节

ALSA 中采用 alsamixer 进行音量调节。使用非常简单，只需终端输入：

```
alsamixer
```

他会给你一个图形界面：

![](https://img-blog.csdnimg.cn/img_convert/262d2d2c9620bc224e0a755d01f3588f.png)

如果你要用摄像头的扬声器，自然要切换声卡，怎么搞？

按下 F6 进行声卡切换：

![](https://img-blog.csdnimg.cn/img_convert/2166fdae02252230b4112a7c716fde13.png)

如果遇到 vscode 快捷键冲突，用 powershell 打开一个终端吧。

按向上键把 PCM 值调高：

![](https://img-blog.csdnimg.cn/img_convert/826b3a12f1d277df72c65b4534f813a6.png)

再来播放音频文件试试吧~

这个坑，折腾了好久，听到出声的那一刻，激动得老泪纵横。。。

## 写在最后

本文带大家实操了ALSA 这位 Linux 的音频管理大师。

终于，给 Jetson 安装上了耳朵和嘴巴，让它能听会说了。

如果对你有帮助，欢迎**点赞收藏**备用。

本系列文章，会陆续更新在 Jetson 上完成 AI 应用开发的相关教程，欢迎感兴趣的朋友关注。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。



