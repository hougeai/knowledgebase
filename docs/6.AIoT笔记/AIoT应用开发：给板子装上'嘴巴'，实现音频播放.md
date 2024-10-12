最近新入手了一台 arm 开发板，希望打造一款有温度、有情怀的陪伴式 AI 对话机器人。

大体实现思路如下：

![](https://img-blog.csdnimg.cn/img_convert/75e308667bda7c30d80ced5c8cf0942a.png)

前几篇，在板子上把`LLM 大脑`和`耳朵`装上了：

- [如何在手机端部署大模型？](https://blog.csdn.net/u010522887/article/details/142296552)
- [手机端跑大模型：Ollma/llama.cpp/vLLM 实测对比](https://blog.csdn.net/u010522887/article/details/142310279)
- [AIoT应用开发：给板子装上'耳朵'，实现实时音频录制](https://blog.csdn.net/u010522887/article/details/142325531)

对应到设备上：
- `耳朵` == 麦克风（上篇搞定）；
- `嘴巴` == 扬声器（本篇开搞）；

今日分享，带大家实操：**如何在开发板上接入扬声器，实现音频播放。**

>有小伙伴问：没有 arm 开发板怎么办？准备一台 Android 手机就行。
>
>友情提醒：本文实操，请确保已在手机端准备好 Linux 环境，具体参考教程：[如何在手机端部署大模型？](https://blog.csdn.net/u010522887/article/details/142296552)


## 1. 两种思路

开发板上预装了 Android 13系统和 AidLux 开发工具，拥有丝滑的 Linux 环境。

如何接入扬声器，实现音频输出呢？

我尝试了两种方案：

1. 耳机：找了一个 3.5mm 接头的耳机，插入音频输出接口，不过，在终端中执行 `aplay -l`，无法识别到音频设备。折腾了半天最终放弃!

![](https://img-blog.csdnimg.cn/img_convert/1ce5762a8852dcf67eac393f26dbdd94.png)


2. 蓝牙音箱：成功接入！下文我们一起来聊聊：我是如何接入蓝牙音箱，并实现音频播放的。

## 2. 接入蓝牙音箱

首先是在 Linux 环境中配置蓝牙：`bluetoothctl` 打开蓝牙，显示 `No default controller available`，表明系统没有检测到任何蓝牙适配器。

无奈之下，把开发板接入显示器，进入 Android 界面看看吧。人肉打开蓝牙，依然无法搜索到周围蓝牙设备。。。

蓝牙信号接收不了？

后来经一大佬提示：外界蓝牙和 WIFI 信号都走同一个天线。

那就把天线接上试试吧！

果然，WIFI 信号直接拉满，蓝牙设备也接进来了~

![](https://img-blog.csdnimg.cn/img_convert/8d60958bc7e593df32a559c6d0e371d5.jpeg)

## 3. 实现音频播放

### 3.1 尝试1：Linux 端
蓝牙音箱是接入进来了，不过终端还是发现不了。

```
aidlux@aidlux:~$ aplay -l
aplay: device_list:276: no soundcards found...
```

运行以下命令检查音频设备的权限：

```
aidlux@aidlux:~/projects/aibot$ ls -l /dev/snd
total 0
drwxr-xr-x. 2 root   root       60 Sep 17 16:27 by-id
drwxr-xr-x. 2 root   root       60 Sep 17 16:27 by-path
crw-rw----. 1 system  1005 116, 61 Jan  1  1970 comprC1D11
crw-rw----. 1 system  1005 116, 62 Jan  1  1970 comprC1D24
```

发现音频设备的权限又被默认设置为了 1005 用户组，再改一次吧：

```
sudo chgrp audio /dev/snd/*
```

再次执行 `aplay -l`，还是没发现新设备：
```
aidlux@aidlux:~/projects/aibot$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 1: lahainayupikidp [lahaina-yupikidp-snd-card], device 0: MultiMedia1 (*) []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

看来，这条路是走不通了，赶紧换！

### 3.2 尝试2：Android 端
> 参考文档：[https://docs.aidlux.com/api/#/?id=%E7%A1%AC%E4%BB%B6](https://docs.aidlux.com/api/#/?id=%E7%A1%AC%E4%BB%B6)

原来 AidLux 中提供了对 Android 端的系统访问，其中有一项`媒体播放`。

目测应该是下面这两个包提供的支持。
```
pip list | grep aid   
aidlux-aistack-base     1.1.0
pyaidlite               2.0.9
```
根据文档，`媒体播放`模块可实现如下几个功能：

- 音频播放：入参分别是文件URL，tag，是否立即播放。

```
res = droid.mediaPlay('/sdcard/audios/20240914_204515.wav', 'default', True)
print(res)
# 输出结果
Result(id=0, result=True, error=None)
```
注意：音频文件需放在 Android 目录 `/sdcard` 下，否则播放不了哦。

- 检查是否正常播放：
    
```
res = droid.mediaIsPlaying('default')
print(res)
# 输出结果
Result(id=0, result=True, error=None)
```

- 查看播放列表：

```
res = droid.mediaPlayList()
print(res)
# 输出结果
Result(id=0, result=['default'], error=None)
```

- 查看播放信息：

```
res = droid.mediaPlayInfo('default')
print(res)
# 输出结果
Result(id=0, result={'loaded': True, 'duration': 2880, 'looping': False, 'isplaying': False, 'tag': '20240914_204515', 'position': 2880, 'url': '/sdcard/audios/20240914_204515.wav'}, error=None)
```

- 停止播放：从缓存中清除

```
res = droid.mediaPlayClose('default')
print(res)
# 输出结果
Result(id=0, result=True, error=None)
```

基于以上接口，音频播放终于成功搞定!

大家有更好的想法，欢迎交流。

## 写在最后

至此，我们已经给开发板装上了：`大脑` + `耳朵` + `嘴巴`，下篇我们将这三者串联起来，实现 AI 机器人的雏形，敬请期待！

如果对你有帮助，欢迎**点赞**和**收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。




