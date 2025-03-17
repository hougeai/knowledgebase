
前段时间爆火的图片数字人：LivePortrait、AniPortrait、MuseTalk、EchoMimic等，核心原理都是通过 **姿态/音频等** 驱动**单张图片**，生成对应的视频。

我们将上述图片数字人，称为 **2D 真人**，这些数字人偏娱乐属性，无法做到代替真人。

而要想代替真人出镜，实现数字人口播，就必须上**2.5D真人**。

上篇和大家分享了：实时视频数字人方案 Ultralight Digital Human：
- [致敬！开源端侧实时数字人，附一键整合包](https://zhuanlan.zhihu.com/p/12365528701)

类似的**2.5D真人**开源项目还有 dh_live，实现流程基本一致，区别在底层模型不同，比如 dh_live 中，音频编码用的 LSTM 模型，生成模型用的DINet。

但，上述**2.5D真人**方案的缺陷是：只能实现`对口型`，**无法生成和音频协调的肢体动作**！

全身动作生成，一直都是急需攻克的难题。

即便是付费方案 Heygen，也只能实现面部表情和上半身动作生成。

直到看到一个开源项目 - **TANGO**，瞄准了全身动作生成这一更具挑战性的目标。

**今日分享，带大家一探 TANGO 的究竟，并本地实操起来，看看效果如何**。

## 1. TANGO 简介

TANGO 由东京大学和 CyberAgent AI Lab 联合开发，技术路径非常独特。

老规矩，简单介绍下项目的亮点：

![](https://i-blog.csdnimg.cn/img_convert/fd7f036f4484d8c2623e980c81565ce2.png)

对照论文中的流程图，TANGO 的核心技术主要有：
- **图结构表示**：节点代表视频帧；边表示帧之间的转换。子图检索: 可根据目标音频的时序特征，检索最佳的视频播放路径子集。
- **AuMoCLIP**：分层音频运动嵌入，通过对比学习创建一个隐式的层次化音频-动作联合嵌入空间，能够捕捉更细微的音频-动作关系，从而生成更自然、更流畅的动作序列；
- **ACInterp**：扩散插值网络，在现有扩散模型之上，参考运动模块确保生成的动作与参考视频保持一致。

如果只是想尝个鲜，可前往官方体验地址：[https://huggingface.co/spaces/H-Liu1997/TANGO](https://huggingface.co/spaces/H-Liu1997/TANGO)

![](https://i-blog.csdnimg.cn/img_convert/53fe4cf07b9b5ff803b031966230e6fd.jpeg)


## 2. TANGO 本地部署
>本地部署，有两点需要注意：
>- **至少确保 35G 磁盘空间**，用于存放模型；
>- **至少确保 6G 显存**，用于模型推理。

> 项目地址：[https://github.com/CyberAgentAILab/TANGO](https://github.com/CyberAgentAILab/TANGO)

首先，下载项目仓库：因项目依赖 wav2lip 和 FILM，因此在 TANGO 目录下把这两个项目也要拉取下来。

```
git clone https://github.com/CyberAgentAILab/TANGO
cd TANGO
git clone https://github.com/justinjohn0306/Wav2Lip.git
git clone https://github.com/dajes/frame-interpolation-pytorch.git
```

然后，参考项目主页，安装好依赖后，即可一键启动 WebUI:

```
python app.py
```

其中，项目默认会生成带有 TANGO 水印的视频，类似下面这样：

![](https://i-blog.csdnimg.cn/img_convert/9f88fec62de749249d9afd357afe87bd.png)

本质上是调用本地的 ffmpeg 将原视频和水印图片合成了新视频。

如果不想要水印，可修改`app.py`中：

```
gr.Video(value="./datasets/cached_audio/demo1.mp4", label="Demo 0", , watermark="./datasets/watermark.png")
# 修改为
gr.Video(value="./datasets/cached_audio/demo1.mp4", label="Demo 0")
```

非本地主机可访问，需修改：

```
demo.launch(server_name="0.0.0.0", server_port=7860)
```

再次打开，可以发现加载的视频中无水印：

![](https://i-blog.csdnimg.cn/img_convert/77a9998cdbe2da61b9bd4681d98ddb43.jpeg)

视频能否加载成功，取决于你本地的网速。

接下来，只需上传一段音频和参考视频，点击生成即可。

![](https://i-blog.csdnimg.cn/img_convert/2c7fba345312345ddde71b7b8f7b1e6b.jpeg)


最终生成的视频没有音频，需要手动把音频合成进去：

```
/usr/bin/ffmpeg -i outputs/gradio/test_0/xxx.mp4 -i gen_audio.wav -c:v libx264 -c:a aac result_wav.mp4
```

一起来看下效果吧：


[video(video-erzNbNIi-1734395231006)(type-csdn)(url-https://live.csdn.net/v/embed/438952)(image-https://v-blog.csdnimg.cn/asset/19382837bfd888c02b472ec2b94fa9c0/cover/Cover0.jpg)(title-数字人)]


可以发现：肢体动作没什么问题，口型完全对不上。

这不，上篇分享的 Ultralight Digital Human就派上用场了？

所以，

`Ultralight Digital Human` 对口型，`TANGO` 生成肢体动作，`FaceFusion` 换脸，完美！

> 值得注意的是：当前开源的 TANGO 只支持最长 8s 音频，使用前，需对音频文件做分段处理！

## 写在最后

本文带大家在本地实操了支持**全身动作生成**的数字人项目 TANGO。

不知大家使用体验如何，欢迎评论区聊！

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。
