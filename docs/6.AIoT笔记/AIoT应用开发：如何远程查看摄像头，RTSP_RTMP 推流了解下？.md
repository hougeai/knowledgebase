最近一直在打造 AI 对话机器人：
![](https://img-blog.csdnimg.cn/img_convert/63257589a055353cc8b13723136264c5.png)

项目基于移动端 arm 开发板，不得不说，这方面的需求还真不少。

前两天把摄像头接入了进来，一位家中有娃的粉丝朋友问：**能否远程查看摄像头的监控画面**，这样就可以随时查看孩子的活动了。

必须能！不仅可以实时查看视频，还可以通过我们之前打造的`微信AI机器人`，将发现的异常情况，实时通报到你的微信端。

*PS：有类似需求的小伙伴，欢迎通过公众号链接我。*

今日分享，就带大家实操：如何实现**远程访问摄像头的监控数据**。

## 1. 流媒体是如何传输的

要实现远程访问，当然离不开网络！

相信大家都听说过 HTTP（超文本传输协议），HTTP 主要用于在Web上传输超文本（如HTML），它是Web的基础协议。

和 HTTP 类似，流媒体传输协议主要有两种：**RTSP**（Real-Time Streaming Protocol）和 **RTMP**（Real-Time Messaging Protocol）

这哥俩有什么区别么？

1. 传输方式
- RTSP：通常通过UDP或TCP传输，适合实时应用，延迟较小。
- RTMP：主要通过TCP传输，确保数据的可靠性，在处理高并发流时表现良好。最初由Adobe开发，用于Flash播放器。

2. 应用场景
- RTSP：常用于监控摄像头、视频点播等场景。
- RTMP：广泛用于直播流媒体（如 YouTube 等）。

如何利用这两种协议成功实现推流呢？

下面我们介绍**两种方法**：
- Nginx 实现 RTMP 推流
- MediaMTX 实现 RTSP/RTMP 推流

## 2. Nginx 实现 RTMP 推流
Nginx 不支持 RTSP 推流，只有在安装 RTMP 支持后，才可以转发 RTMP 的数据。

### 2.1 安装 Nginx 和 RTMP 支持

Nginx 是啥？如何安装？不了解的小伙伴，可参考猴哥这篇教程：[免费域名注册 & Cloudflare 域名解析 & Ngnix端口转发](https://blog.csdn.net/u010522887/article/details/140786338)

如果你已装了 Nginx，还要查看 Nginx 是否安装了 RTMP 支持，输入`nginx -V`，如果没有`nginx-rtmp-module`等内容，则需要重新编译安装 Nginx。

编译安装 Nginx 并不复杂，参考如下步骤即可：

```
cd ~/tools
mkdir nginx 
cd nginx
wget https://nginx.org/download/nginx-1.26.1.tar.gz
wget https://github.com/arut/nginx-rtmp-module/archive/refs/heads/master.zip
tar -xf nginx-1.26.1.tar.gz
unzip master.zip
cd nginx-1.26.1/
# 安装 PCRE 库来启用 HTTP 重写模块
sudo apt-get install libpcre3 libpcre3-dev
# 编译
./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-master
make
sudo make install
# 默认安装在：/usr/local/nginx/sbin/nginx
```
### 2.2 启动 RTMP 服务器

假设已安装好 Nginx，首先查看配置文件在哪：

```
sudo /usr/local/nginx/sbin/nginx -t
# 输出
nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
```

打开配置文件，添加以下配置：

```
rtmp {
    server {
        listen 10035;
        chunk_size 4096;

        application live {
            live on;
            record off;
        }
    }
}
```

修改配置文件后，记得一定要重启 Nginx，否则配置无法生效。

```
sudo /usr/local/nginx/sbin/nginx
```

至此，RTMP 服务器已成功启动，正在监听 localhost:10035，地址是`rtmp://<your_ip>:10035/`

接下来，我们还需要用另外一个工具把视频流，推送到上面这个地址上。


### 2.3 FFmpeg 推 RTMP 流

```
sudo apt install ffmpeg
ffmpeg -version
```

确保已经成功安装 FFmpeg，然后使用以下命令开始推流：

```
ffmpeg -f v4l2 -i /dev/video2 -c:v libx264 -f flv rtmp://localhost:10035/live/stream
```

参数说明：
- **-f v4l2**：指定视频输入格式为 V4L2（Video for Linux 2）。
- **-i /dev/video2**：指定摄像头设备。
- **-c:v libx264**：使用 H.264 编解码器。
- **-f flv**：输出格式为 FLV。
- **rtmp://localhost:10035/live/stream**：指定 RTMP 服务器地址。

看到如下信息，代表推流成功：

```
frame= 1188 fps= 30 q=29.0 size=     664kB time=00:00:37.93 bitrate= 143.5kbits/s speed=0.951x
```
## 3. MediaMTX 实现 RTSP/RTMP 推流

MediaMTX 是一个更高效、更简洁的多协议流媒体服务器，支持包括 RTSP、RTMP、HLS、WebRTC 等多种协议。
### 3.1 启动 MediaMTX

前往：[https://github.com/bluenviron/mediamtx/releases](https://github.com/bluenviron/mediamtx/releases)
找到对应操作系统和 CPU 架构的安装包，比如我的是 Linux + ARM 架构：
```
wget https://github.com/bluenviron/mediamtx/releases/download/v1.9.1/mediamtx_v1.9.1_linux_arm64v8.tar.gz
cd mediamtx
```
配置文件`mediamtx.yml`在当前目录下，可根据需要进行修改：

```
rtmp: yes
rtmpAddress: :8554
rtmp: no
rtmpAddress: :1935
```

执行如下命令，默认情况下，MediaMTX 会启动一个支持多协议的服务器，监听配置文件中的端口。

```
./mediamtx
```
看到如下日志，说明 RTSP 服务已启动：

```
2024/09/21 16:18:27 INF MediaMTX v1.9.1
2024/09/21 16:18:27 INF configuration loaded from /home/aidlux/tools/mediamtx/mediamtx.yml
2024/09/21 16:18:27 INF [RTSP] listener opened on :8554 (TCP), :8000 (UDP/RTP), :8001 (UDP/RTCP)
```

接下来开始推流！

### 3.2 FFmpeg 推 RTSP 流

```
ffmpeg -f v4l2 -i /dev/video2 -c:v libx264 -f rtsp rtsp://localhost:8554/live/stream
```
参数说明：
- **-f rtsp**：注意 RTSP 不支持 flv 容器格式，这里应该是 rtsp。


## 4. 如何获取视频流数据

推流成功后，就可以在远程客户端查看视频数据了，如何实现？

下面先介绍最常见的两种方式。

### 4.1 FFmpeg 获取视频流

示例代码如下：
```
# 安装`ffmpeg-python`包
pip install ffmpeg-python
# 代码中添加
import ffmpeg
rtmp_url = "rtmp://192.168.10.2:10035/live/stream"
ffmpeg.input(rtmp_url).output("1.jpg", vframes=1)global_args('-loglevel', 'error').run()
```

### 4.2 OpenCV 获取视频流

示例代码如下：
```
import cv2
rtmp_url = "rtsp://192.168.10.2:8554/live/stream"
cap = cv2.VideoCapture(rtmp_url)
while True:
    ret, frame = cap.read()
    cv2.imshow("frame", frame)
```

在 xfce 桌面成功显示：

![](https://img-blog.csdnimg.cn/img_convert/0cfeb71962b188ab472c9a40dbc69f06.jpeg)


在[如何在手机端部署大模型？](https://blog.csdn.net/u010522887/article/details/142296552)中，已经向大家介绍过 AidLux。如果你已有 AidLux 环境，也推荐了解下获取视频流的第三种方式。

### 4.3 AidStream 获取视频流

AidStream 是 AidLux 推出的用来构建流媒体应用的框架。

AidStream 核心是 pipeline，你只需为每条 pipeline 配置`输入流`与`输出流`即可。注意：`输入流`只支持 rtsp 流。

> 参考文档：[https://v2.docs.aidlux.com/sdk-api/aid-stream/aidstream_for_python](https://v2.docs.aidlux.com/sdk-api/aid-stream/aidstream_for_python)

比如要把 rtsp 输出到屏幕：

```
import aidstream
inrtsp = "rtsp://192.168.10.2:8554/live/stream"
pipelines = aidstream.ast()
pipelines.add(input=inrtsp)
pipelines.build()
while True:
    frame = pipelines.read()
    pipelines.show(frame)
```
上述代码暂未成功，难道要屏幕分辨率和摄像头分辨率一致？懂的小伙伴评论区交流下。


> 注：如需外网访问， `192.168.10.2` 要更换为设备的公网 IP 地址，有小伙伴问，我没有公网 IP 咋办？内网穿透了解下：👉[【白嫖 Cloudflare】之 免费内网穿透，让本地AI服务，触达全球](https://blog.csdn.net/u010522887/article/details/141621570)

## 写在最后
本文带大家了解了RTSP和RTMP两大流媒体传输协议，并实操了如何实现远程监控。

基于此，可以对获取的视频流进行 AI 处理，实现更多好玩且实用的创意，敬请期待！

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。

--- 

猴哥的文章一直秉承`分享干货 真诚利他`的原则，最近陆续有几篇`分享免费资源`的文章被CSDN下架，申诉无效，也懒得费口舌了，欢迎大家关注下方公众号，同步更新中。
