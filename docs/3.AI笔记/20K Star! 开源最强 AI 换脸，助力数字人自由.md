最近 AI 数字人异常火爆，多款开源方案，效果炸裂，直逼付费方案-HeyGen！

我们在各大短视频平台刷到的数字人，背后的制作流程大致包括:
- 底模数字人视频生成
- **AI 换脸**
- 背景去除
- 背景合成

尽管各大厂商开源了不少公版数字人（绿幕背景），但若想商用，就必须要用已授权的肖像或自己的人像素材。

怎么搞？

**AI 换脸**！

作为数字人背后的关键技术，**AI 换脸**很大程度上决定了最终生成视频的真实度。

*今日分享，带大家实操：工业级的**AI 换脸**开源项目-FaceFusion，轻量高效，效果惊艳。*


先看效果：

![](https://i-blog.csdnimg.cn/img_convert/71dff602b3dae9dca8ebd3f3ce29f75e.jpeg)


## 1. FaceFusion简介

> 项目地址：[https://github.com/facefusion/facefusion](https://github.com/facefusion/facefusion)

号称“领先的工业级AI换脸系统”，Facefusion 最近已更新迭代到 3.0 版本，项目集成度非常高，基本覆盖了和人脸相关的各种AI模型，GitHub 斩获近 20K Star!

老规矩，简单介绍下项目亮点：

- **高度真实感的换脸效果**：这是刚需，要不然还玩啥；

- **快速的运行速度**：支持多线程处理，实测 7s 视频，GPU 在不进行 tensorrt 加速的情况下，只需 4s 搞定；

- **实时直播换脸功能**：最新版本3.0引入，增加互动娱乐性；

- **年龄调节处理器等附加功能**：支持通过该模式对面部进行年龄调整；

## 2. 本地部署

### 2.1 Docker 安装

官方提供了不同平台的安装方式，对不熟悉命令行的小伙伴，官方提供了安装包（需付费）：

![](https://i-blog.csdnimg.cn/img_convert/cdadbd8207a680e07b1c39c274febda0.png)

本次实操，我们选择在 Linux 上完成！

为了方便管理，采用 docker 方式部署。
> 参考文档：[https://docs.facefusion.io/usage/run-with-docker](https://docs.facefusion.io/usage/run-with-docker)

首先，下载官方提供的 docker 仓库：

```
git clone https://github.com/facefusion/facefusion-docker.git
```

这里为你提供了不同平台的 Dockerfile 和 docker-compose 配置文件：

![](https://i-blog.csdnimg.cn/img_convert/8fcf465c5a09fb5928c43c517823b469.png)

其中 .cuda.yml 提供了 GPU 支持，我们来看下具体配置内容：

```
services:
 facefusion-cuda:
  build:
   context: .
   dockerfile: Dockerfile.cuda
```
也就是说它将读取本地的`Dockerfile.cuda`来构建镜像。

若要指定显卡设备号，可在.cuda.yml最后添加，如下：

![](https://i-blog.csdnimg.cn/img_convert/f8902da09a5e70cbdb109967b45a9045.png)

### 2.2 修改 Dockerfile

这个 `Dockerfile.cuda`，如果不做修改，你大概率会碰壁，这里给大家分享几个遇到的坑：

**坑1：cuda 版本**
```
FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu24.04
```
这行意味着镜像基于`cuda:12.6`构建，而最新发布的`cuda:12.6`也要求最新的 nvidia 驱动版本，如果觉得更新 nvidia 驱动太麻烦，那就换个镜像：

```
# FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu24.04
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
```
**坑2：python 版本**

换了上面镜像后，你会发现 python3.12 装不了，那就换成 python3.10：

```
# RUN apt-get install python3.12 -y
RUN apt-get install python3.10 -y
```
**坑3：github 仓库拉取失败**

给 github 仓库前面加个镜像地址：

```
# RUN git clone https://github.com/facefusion/facefusion.git --branch ${FACEFUSION_VERSION} --single-branch .
RUN git clone https://mirror.ghproxy.com/https://github.com/facefusion/facefusion.git --branch ${FACEFUSION_VERSION} --single-branch .
```

### 2.3 启动容器
Dockerfile 配置完成后，启动一个容器看看：

```
docker compose -f docker-compose.cuda.yml up 
```
如需放到后台运行，在上述指令之后加上 `-d`。

看到下面日志，说明你的容器已经成功启动：

![](https://i-blog.csdnimg.cn/img_convert/9e32cffef84b4290e4d59264e1567f87.png)


## 3. 效果实测

不同容器的端口号不一样，其中 cuda 版本的容器，默认端口号是 7870。

浏览器打开：`http://localhost:7870/`，打开 webui 界面。

![](https://i-blog.csdnimg.cn/img_convert/070400be94821f789a43490bf1227676.png)

区域说明：
- 设置人脸（**Source**）：上传完整人脸图片（注意图片名字不要用中文）。
- 设置目标（**Target**）：上传待换脸的目标图片或视频。
- 效果预览 （**Preview**）：完成上述两步后，换脸后的图片预览。如果是视频，会截取第一帧作为预览效果。


### 3.1 初体验

采用默认配置，上传一张人脸头像，和待更换人脸的视频，点击下方 `Start`，就可以看到本文开头展示的内容。

**我们来看下日志：**

```
facefusion-cuda-1  | [FACEFUSION.CORE] Processing step 1 of 1
facefusion-cuda-1  | [FACEFUSION.CORE] Extracting frames with a resolution of 854x480 and 25.0 frames per second
facefusion-cuda-1  | [FACEFUSION.FACE_SWAPPER] Processing
Processing: 100%|==========| 169/169 [00:02<00:00, 66.40frame/s, execution_providers=['cuda'], execution_thread_count=4, execution_queue_count=1]
facefusion-cuda-1  | [FACEFUSION.CORE] Merging video with a resolution of 854x480 and 25.0 frames per second
facefusion-cuda-1  | [FACEFUSION.CORE] Processing to video succeed in 4.96 seconds
```

默认配置下，854x480 分辨率的视频，帧率 25 fps，共 7s，处理完成耗时 4.96 s！*（注：这里未采用 tensorrt 加速）*

**显存占用如何？**

不到 4 G 就能跑。

```
0   N/A  N/A    519271      C   python    3824MiB
```

最大支持 1024x1024，因此一张 16G 的消费级显卡妥妥够了。

最后，来看下生成效果：
[演示视频]()

### 3.2 更多配置介绍

**下图中的 Processors 选项干啥的？**

![](https://i-blog.csdnimg.cn/img_convert/070400be94821f789a43490bf1227676.png)

- `face_swapper`: 换脸模型，必选；
- `age_modifier`：年龄修改模型；
- `face_debugger`：从预览图像中显示换脸的依据，比如人脸检测框、关键点等，**正式换脸时需取消该选项**。
- `face_editor`：采用 live_portrait 进行人脸编辑，需等待后台自动下载模型；
- `face_enhancer`: 换脸时提升图像中人脸的质量和清晰度。
- `frame_enhancer`: 提升整个帧的图像质量。


**下图中执行器怎么选？**

![](https://i-blog.csdnimg.cn/img_convert/ff8800da96bd2e73d28930ad290649c8.png)

- `EXECUTION THREAD COUNT`：换脸时的最大线程数，可适当调高该值，加快换脸的运算速度。
- `EXECUTION QUEUE COUNT`：脚本批量换脸时需要，webui界面无需设置。

**下图中的输出视频怎么配置？**

![](https://i-blog.csdnimg.cn/img_convert/087a90e2f790a1e5871d9a07a83a00c3.png)

OUTPUT VIDEO ENCODER选项，是视频编码格式：
- `libx264`: H.264编码，在图像质量和压缩大小之间权衡，默认选项；
- `libx265`: 比H.264更高效的压缩，但耗时更久；
- `h264_nvenc`: 使用NVIDIA的NVENC硬件编码，加速H.264编码，质量不如libx264；
- `hevc_nvenc`: 使用NVIDIA的NVENC硬件编码，加速H.265编码。


OUTPUT VIDEO PRESET 选项，针对视频编码器，影响编码的速度和压缩率。

简单来说，从 ultrafast 到 veryslow，编码越慢，但压缩效果越好，质量越高。


## 写在最后

本文带大家在本地部署了开源的 AI 换脸工具-FaceFusion，并对该工具的进阶使用进行了简单介绍。

如果对你有帮助，欢迎**点赞收藏**备用。

市场上的免费公版数字人有很多，感兴趣的朋友可以实操起来，通过本文的换脸工具，最后到剪映增加背景、字幕，即可投入商用。

无论是打造个人IP，还是帮商家搭建 AI 数字人营销，实现数字人带货，都香的很。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入，公众号后台「联系我」，拉你进群。



