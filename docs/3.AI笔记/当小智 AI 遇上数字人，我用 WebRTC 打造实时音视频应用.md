前文，分享了`小智AI服务端`的完整解决方案：

[低至1.5元/天，小智AI服务端，完整解决方案，高可用+可扩展](https://zhuanlan.zhihu.com/p/1937478173907452319)

这套方案，采用微服务、分布式架构，各个服务独立部署，架构如下：

![](https://i-blog.csdnimg.cn/img_convert/7d1dffd04b35b1cb777ed3f646727f76.png)

下游可以对接各种智能终端，进行`音频通信`；

应该说，有了`LLM 大脑 + 音色克隆`的加持，现在的 Bot 越来越接近一个**有灵魂**的人了。

如果再加上`外貌克隆`，那就更完美了。

没错，可以接入 `数字人`。

之前的流程是这样：

![](https://i-blog.csdnimg.cn/img_convert/2f33defe84830844a8572253f748cae6.png)

只需在上述流程的基础上，添加一个`数字人服务`节点：

![](https://i-blog.csdnimg.cn/img_convert/3a3f143a5ab76fc3ea674d92e45b05bc.png)

尽管当前`数字人`技术已经很成熟，但要做到实时渲染，且保持音视频同步，还是有一定挑战。

先看笔者的一个 Demo:

[https://www.bilibili.com/video/BV1BYaGzcERa/](https://www.bilibili.com/video/BV1BYaGzcERa/)

今日分享，聊聊这个 Demo 背后的两个探索：

- 流式数字人渲染
- 低延迟音视频通信

**全文目录**如下，感兴趣的朋友可以按需取用：

![](https://i-blog.csdnimg.cn/img_convert/72197f083d72f12b0c751289252f5cf2.png)


## 1. 流式数字人渲染

该模块的职责：接收 TTS 生成的音频数据，实时合成唇形同步的数字人视频流。

实现思路：通过 WebSocket 协议通信，由 `main-server` 进行中转，大致流程如下：

![](https://i-blog.csdnimg.cn/img_convert/ce30f6266aaa4bba37de0ba0e25a6067.png)


### 1.1 整体架构

为了实现高并发处理能力，方便后续扩展，整体数字人服务采用异步事件驱动架构，建立 WebSocket 服务器，负责处理客户端连接和消息传递。关键功能如下：

- 异步WebSocket连接管理
- 音频流接收与处理
- 视频帧+视频帧流式传输
- 多客户端并发支持

### 1.2 唇形渲染引擎

最关键的就是数字人模型了。

为了快速跑通流程，数字人模型选用了 `Wav2Lip`。原因无它，延迟低啊~

关于模型的技术细节，可以看笔者之前的教程：

[致敬！开源端侧实时数字人项目，附一键整合包](https://zhuanlan.zhihu.com/p/12365528701)

不过，为了实现流式输出，还得费一番周折~

### 1.3 流式处理架构

这里采用`生产者-消费者`模式，通过多个线程实现流式处理。

一个队列负责生产，另一个队列负责消费，各司其职，互不干扰。

![](https://i-blog.csdnimg.cn/img_convert/2aeb9852ee41140c8ec5630c816ee793.png)

流水线如下：
```

音频输入 → MelFrame处理 → Wav2Lip推理 → 视频合成 → 流式输出
    ↓           ↓            ↓          ↓         ↓
audio_queue feat_queue  frame_queue video_track WebSocket
```

- 音频预处理线程：将 40ms 音频帧，转换为 mel 频谱特征
- AI推理线程：使用`Wav2Lip`模型生成唇形动画
- 视频合成线程：将AI生成的唇形与背景头像合成
- 流式传输线程：实时推送音视频到客户端


至此，整个`数字人服务`就搭好了~

当然，最关键，也是最头疼的一步也来了：

怎么把`音视频`发给客户端，才能实现`实时流畅`播放呢？

之前所有服务都基于 `Websocket` 通信，笔者原打算用 `Websocket` 快速跑通流程，后面发现坑实在太多，果断放弃！

最终选择了 `WebRTC`，下面重点聊聊：
- `为什么选择 WebRTC`
- `怎么用 WebRTC 搭建实时音视频通信`

## 2. WebRTC 实时音视频通信

### 2.1 为什么选择 WebRTC

首先，RTC (Real-Time Communication) 是一个广义的概念，泛指所有能够实现实时数据传输的技术，涵盖所有需要实时通信的领域。

`WebRTC` 则是 RTC 的一个具体实现，是 Google 开源的一套**基于浏览器**的实时通信技术。

本质是一套标准化的 JavaScript API。主要包括：

- 标准化 API 实现音视频采集、编码、传输和播放；
- 内置音视频编解码器（如 VP8、VP9、H.264）；
- 使用 ICE 框架实现 NAT 穿透；
- 采用 SRTP 协议实现安全传输；

因此，如果是在网页端实现音视频通信，无脑选择 **WebRTC**！

首先：**超低延迟**！

其次，

- 浏览器原生支持：现代浏览器都内置WebRTC支持，无需安装额外插件。

- 自适应码率：支持根据网络状况动态调整音视频码率，保证在网络波动时提供稳定的服务。

- NAT穿透能力：WebRTC 内置 ICE 框架，能够自动处理防火墙穿透问题；

- 数据安全：WebRTC 强制使用加密传输(DTLS-SRTP)。


如果用 `websocket` 通信，上述所有坑，都得自己再趟一遍~

### 2.2 如何建立 WebRTC 连接

这里我们采用 `WebRTC + Websocket` 双通信协议：

- `WebRTC` 专门负责音视频通信；
- `WebSocket` 负责信令传递，帮助建立 WebRTC 连接

连接建立流程图如下：

![](https://i-blog.csdnimg.cn/img_convert/eafa944d03a723bd0b3bbdf9207fe652.png)

这里有几个关键节点，我们一一来看~


### 2.3 ICE Candidate

WebRTC 采用 P2P 架构，因此，如果在同一局域网，可以通过 IP 点对点通信。

如果不在同一局域网呢？

就得找个中转站了！

这个中转站，在 WebRTC 中，叫做 `信令服务器`，通常也叫`TURN/STUN 服务器`：

- `STUN`：告诉浏览器“在公网的 IP/端口是什么”，能否直连，要看对方的 NAT/防火墙是否允许；
- `TURN`：当 P2P 直连失败时，音视频数据都得通过 TURN 中继转发。

怎么中转？

ICE Candidate 了解下？

所谓 ICE（Interactive Connectivity Establishment），也就是 WebRTC 的 NAT 穿透机制。

当两个端点（客户端 ↔ 服务端）不在同一局域网时，它们需要通过 `STUN/TURN` 服务器，找到可达的公网地址。

`Candidate` 就是`可用的网络地址和UDP端口`。

上面流程图中，WebRTC `offer/answer` 只是协商会话参数，P2P 真正建立还需要交换候选地址。

如何交换?

通过 `WebSocket` 传递~

客户端和服务端，同时连到 `STUN/TURN` 服务器，一旦有`candidate`下发，就发给对方。

举个例子而言，客户端收到后，通过`WebSocket` 发给服务端：

```
pc.onicecandidate = ({ candidate }) => {
  if (candidate) {
    ws.send(JSON.stringify({
      type: "ice-candidate",
      candidate
    }));
  }
});
```

服务端接收到，保存下来：

```
if (data.type === "ice-candidate") {
  pc.addIceCandidate(data.candidate).catch(console.error);
}
```
### 2.4 STUN/TURN 服务部署
WebRTC 的 ICE 流程的优先级如下：局域网直连 → STUN 公网直连 → 最后才是TURN。

如果不在同一局域网，需要自己部署 `STUN/TURN` 服务，这里推荐 `coturn`，支持Docker 一键部署：

```
version: "3"
services:
  coturn:
    image: coturn/coturn:latest
    network_mode: "host"   # coturn 需要真实 UDP 端口，所以用主机网络
    command:
      - --log-file=stdout
      - --lt-cred-mech # 用账号/密码的方式鉴权（你配置了 --user=webrtc:pw ）
      - --no-cli
      - --no-tls
      - --no-dtls
      - --fingerprint # 给每个 STUN/TURN 消息自动加上 fingerprint 属性，很多 WebRTC 实现（包括 Chrome、Firefox）要求 fingerprint 存在，否则可能报错
      - --realm=streamtalk-webrtc # 一台 coturn 服务多个应用，就能用 realm 区分。
      - --server-name=myturn
      - --user=webrtc:pw
      - --listening-port=3478 # 默认同时开启 TCP + UDP
      - --min-port=49152
      - --max-port=65535
      - --external-ip=13.218.106.179
      - --listening-ip=0.0.0.0          # 显式监听所有网卡
      - --relay-ip=0.0.0.0              # 让 relay 使用所有可用 IP
      - --no-tcp-relay                  # 暂时不需要 TCP relay，可以禁用节省资源
```

上述 `49152–65535` 是动态 UDP 端口区间，因为 WebRTC 在走 TURN 时，音视频 RTP/RTCP 传输，需要一堆动态 UDP 端口。

若启用 RTP/RTCP mux（现代浏览器端 WebRTC 默认），每个 TURN 通常只用 1 个 UDP 端口，因此理论上可支持 16k 会话（端口数即上限）。

容器启动后，有两种方式，可以测试服务是否成功：

**方式一**：浏览器打开：

[https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/](https://webrtc.github.io/samples/src/content/peerconnection/trickle-ice/)

输入你的 turn 地址即可~

**方式二**：浏览器控制台输入：

```
const pc = new RTCPeerConnection({
  iceServers: [
    {
      urls: "turn:YOUR_PUBLIC_IP:3478",
      username: "webrtc",
      credential: "pw"
    }
  ]
});

pc.onicecandidate = e => console.log("ICE candidate:", e.candidate);
pc.createDataChannel("test");
pc.createOffer().then(offer => pc.setLocalDescription(offer));
```

### 2.5 前端 WebRTC 实现

无关乎前端框架，主要分为以下几步：

#### 2.5.1 RTCPeerConnection 初始化

通过RTCPeerConnection对象管理WebRTC连接：

```
const initWebRTC = async () => {
  pc.value = new RTCPeerConnection({
    iceServers: [
      { urls: "stun:stun.l.google.com:19302" },
      { urls: "turn:IP:3478", username: "webrtc", credential: "pw" }
    ]
  });
};
```
#### 2.5.2 媒体流处理

1. 获取本地音频：

```
localStream.value = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
localStream.value.getTracks().forEach((track) => pc.value.addTrack(track, localStream.value));
```

2. 监听远端媒体流：

```
pc.value.ontrack = (event) => {
  if (event.track.kind === 'video') {
    remoteStream.value.addTrack(event.track);
    bindAndPlayRemoteVideo(remoteStream.value);
  }
  if (event.track.kind === 'audio') {
    remoteStream.value.addTrack(event.track);
    remoteAudio.value.srcObject = remoteStream.value;
  }
};
```
#### 2.5.3 信令处理

通过WebSocket与服务器交换信令信息：

```
// 发送 WebRTC offer
const offer = await pc.value.createOffer({ offerToReceiveAudio: true, offerToReceiveVideo: true });
await pc.value.setLocalDescription(offer);
ws.value.send(JSON.stringify({ type: "webrtc-offer", sdp: offer.sdp }));

// 处理服务器返回的 answer
const handleSDPAnswer = async (sdp) => {
  if (!pc.value) return;
  await pc.value.setRemoteDescription({ type: "answer", sdp });
};
```


#### 2.5.4 视频渲染

最后，使用Canvas元素渲染视频流，在前端展示：

```
const startVideoRendering = () => {
  const playFrame = () => {
    if (remoteVideoEl.readyState >= 2) {
      const ctx = videoCanvas.value.getContext("2d");
      ctx.drawImage(remoteVideoEl, 0, 0, videoCanvas.value.width, videoCanvas.value.height);
    }
    if (isRenderingActive) {
      animationId = requestAnimationFrame(playFrame);
    }
  };
  playFrame();
};
```


### 2.6 服务端 WebRTC 实现

以 node.js 实现为例，要实现 WebRTC 功能，需要先安装依赖：

```
npm install wrtc
```
#### 2.6.1 RTCPeerConnection 创建

服务端同样使用RTCPeerConnection对象：

```
const pc = new RTCPeerConnection({
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "turn:IP:3478", username: "webrtc", credential: "pw" }
  ]
});
pcs.set(this.ws, pc); // 保存连接引用
```
#### 2.6.2 接收客户端发来的音频流

```
pc.ontrack = async (event) => {
  const [audioTrack] = event.streams[0].getAudioTracks();
  const receiver = pc.getReceivers().find(r => r.track === audioTrack);
  const sink = new nonstandard.RTCAudioSink(audioTrack);
  sink.ondata = (data) => {
    // 处理音频数据：16K/48K int16 PCM
  }
};
```
> 注意：前端 WebRTC 发来的音频帧，分辨率可能不同，比如16K/48K，但一定是 int16 类型，因为 float32 需要 4 字节，浪费带宽啊~

#### 2.6.3 数字人音视频流传输
首先，建立视频/音频 track：

```
pc.videoSource = new nonstandard.RTCVideoSource();
const videoTrack = pc.videoSource.createTrack();
pc.addTrack(videoTrack);
pc.audioSource = new nonstandard.RTCAudioSource();
const audioTrack = pc.audioSource.createTrack();
pc.addTrack(audioTrack);
```


一旦接收到`数字人服务`的音视频帧，通过 WebRTC 发给客户端：
- **视频帧**：WebRTC 默认期望 I420 (YUV420 planar) 格式的数据，因此视频帧要采用 YUV 编码；
- **音频帧**：WebRTC 默认接收 10ms 的音频帧，因此需要切割后发送

```
this.clientDjh.on('frame', (frameBuffer) => {
  try {
    const pc = pcs.get(this.ws);
    // 解析音视频帧
    // 发送视频帧
    const videoSamples = new Uint8Array(videoBuf.length);
    videoBuf.copy(videoSamples, 0, 0, videoBuf.length);
    pc.videoSource.onFrame({width, height, data: videoSamples});
    // 发送音频帧
    const audioSamples = new Int16Array(audioBuf.buffer, audioBuf.byteOffset, audioBuf.byteLength / 2);
    const frameSize = 160;
    for (let i = 0; i < audioSamples.length; i += frameSize) {
      const chunk = new Int16Array(audioSamples.slice(i, i + frameSize));
      pc.audioSource.onData({
        samples: chunk,
        sampleRate: 16000,
        bitsPerSample: 16,
        channelCount: 1,
        numberOfFrames: chunk.length,
      });
    }
  } catch (error) {
    console.error(new Date(), 'Error processing frame:', error);
  }
});
```

## 写在最后

本文分享了`小智 AI 服务端接入 数字人服务` 的具体实现思路，以及用 `WebRTC` 打造低延迟音视频通信的具体流程。

如果对你有帮助，不妨**点赞收藏**备用。
