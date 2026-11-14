前面，分享了`低延迟小智AI服务端搭建`系列：
- [低延迟小智AI服务端搭建-ASR篇](https://zhuanlan.zhihu.com/p/1895438759719306293)
- [低延迟小智AI服务端搭建-ASR篇（续）](https://zhuanlan.zhihu.com/p/1896830194364445963)
- [低延迟小智AI服务端搭建-LLM篇](https://zhuanlan.zhihu.com/p/1897978035438874729)
- [低延迟小智AI服务端搭建-TTS篇](https://zhuanlan.zhihu.com/p/1900125186654700030)
- [低延迟小智AI服务端搭建-本地TTS篇](https://zhuanlan.zhihu.com/p/1908795805793486607)
- [小智AI如何控制IoT设备？LLM vs MCP](https://zhuanlan.zhihu.com/p/1914637833488017038)
- [小智AI如何接入你搭建的MCP Server？](https://zhuanlan.zhihu.com/p/1916061081077539780)

问题来了：**客户端和服务端是如何通信的？**

小智客户端，目前支持 `websocket` 和 `MQTT+UDP` 两种通信协议。

本篇，将首先尝试回答：

- 这两种协议有什么区别，适用场景是什么？
- 小智 AI 为什么要 `MQTT+UDP`？
- `MQTT`是什么？
- 如何使用`MQTT`？ 


## 1. `websocket` 和 `MQTT+UDP` 选型

之前我们的协议都是基于 `websocket`，因为实现起来非常简单，便于快速测试通信过程。

但小智官方固件，默认采用 `MQTT+UDP` 通信，为啥呢？

回答这个问题之前，先看下两种协议的优劣势：

**`MQTT+UDP` 优势：**
- **轻量级、低带宽**：MQTT 设计用于低带宽、不稳定网络，非常适合物联网设备。
- **消息推送/订阅机制**：天然支持发布/订阅（Pub/Sub），适合**多设备**消息分发。
- **断线重连与消息保留**：支持 QoS、遗嘱消息等机制，断线后可自动恢复。
- **UDP 音频通道**：音频数据通过 UDP 发送，延迟低。

**`MQTT+UDP` 劣势：**
- **配置门槛高**：必须有稳定的 MQTT 服务器（Broker），配置和维护有一定门槛。
- **协议复杂度高**：比 WebSocket 多了一层 UDP 协议栈，实现上更为复杂。

**`websocket` 优势：**
- **简单直连**：直接基于 TCP，和 HTTP 兼容性好。
- **服务端实现广泛**：很多云服务、后端框架原生支持 WebSocket。

**`websocket` 劣势：**
- **实时性逊于 UDP**：音频数据走 TCP，丢包会自动重传，所以实时性不如 UDP。
- **带宽利用率低**：长连接，且 TCP 有一定的头部开销。

了解完二者各自的优势，再看它们的适用场景就一目了然了：
- **`MQTT+UDP` 适用场景**：设备数量多，网络环境不稳定，带宽有限；
- **`websocket` 适用场景**：设备数量不多，主要是一对一通信；需要快速开发、调试和上线。

所以，**小智 AI 为什么要用 `MQTT+UDP`？**

- 据公开报道，小智日活已过万，一旦并发量上来，服务端要`以一敌百`，`websocket` 将很快把带宽吃完，这种场景下，`MQTT+UDP` 势在必行！

- 如果是个人用户，服务端只为自己服务，显然还是`websocket`更香啊！


## 2. `MQTT`是什么

MQTT（Message Queuing Telemetry Transport），一种发布/订阅消息传输协议，因为轻量，所以广泛用于物联网。

我们通过下图简单理解：生产者和消费者完全解耦，都和中介（MQTT Broker）进行通信，生产者发布（Publish）消息，消费者订阅（Subscribe）消息。

![](https://i-blog.csdnimg.cn/img_convert/05f5ca2a9eeb845a2edd37edde86a16b.png)

所以，在小智 AI 中：
- 当客户端要给服务端发送消息时，**客户端发布**，服务端订阅
- 当服务端要给服务端发送消息时，**服务端发布**，客户端订阅

这里的中介（MQTT Broker），作为中转站，就扮演了至关重要的作用。

开源的 MQTT Broker 实现主要有：
- **Eclipse Mosquitto**：适用小型物联网项目，可轻松部署在树莓派等设备；
- **EMQX**：支持海量设备连接，适用于大规模物联网应用；
- **HiveMQ**：同样支持海量设备连接和高并发，但不支持规则引擎。

下面，我们采用**EMQX**来搭建一个 MQTT Broker。

## 3. `EMQX` 搭建 MQTT Broker

### 3.1 `EMQX` 部署
> 开源地址：[https://github.com/emqx/emqx](https://github.com/emqx/emqx)
>
> 官方文档：[https://docs.emqx.com/zh/emqx/latest/](https://docs.emqx.com/zh/emqx/latest/)

注：开源版本只支持单节点部署，如果需要集群支持，需向官方购买 Lincese。

**`EMQX` 单节点能支持多少并发？**
- 看硬件配置，16c32g 稳定支持10万并发连接，完全没问题。


**`EMQX` 怎么快速上手？**

最简单的自然是 docker 部署。

首先拉取镜像：

```
# 下面这两个镜像应该是一样的，从5.9版本开始，不再区分社区版和企业版了
docker pull emqx/emqx:latest
docker pull emqx/emqx-enterprise:latest
```

容器启动命令：

```
docker run -d --name emqx -p 1883:1883 -p 18083:18083 -v ./emqx/data:/opt/emqx/data -v ./emqx/log:/opt/emqx/log emqx/emqx:latest
```

注：我们这里映射了两个目录到本地，确保数据和日志持久化，为此要为本地文件夹添加权限：

```
sudo chmod -R 777 ./emqx/data
sudo chmod -R 777 ./emqx/log
```

再看下各个端口号有什么作用：

```
默认情况下，EMQX 启动时会占用 7 个端口，它们分别是：
1883，用于 MQTT over TCP 监听器，可通过配置修改。
8883，用于 MQTT over SSL/TLS 监听器，可通过配置修改。
8083，用于 MQTT over WebSocket 监听器，可通过配置修改。
8084，用于 MQTT over WSS (WebSocket over SSL) 监听器，可通过配置修改。
18083，HTTP API 服务的默认监听端口，Dashboard 功能也依赖于这个端口，可通过配置修改。
```
成功启动后，打开`http://localhost:18083`即可访问控制台：
> 默认用户名：admin，密码：public，初次登录后修改。

![](https://i-blog.csdnimg.cn/img_convert/8e1efc00a1eea5a9a12cb2a4fafd53c8.png)

### 3.2 客户端怎么收消息：自动订阅主题

从小智官方下发的`mqtt`字段来看，每个客户端**只有发布主题**，并**没有订阅主题**啊：

```
'mqtt': {
'endpoint': 'mqtt.xiaozhi.me', 
'client_id': 'GID_test@@@98_3d_ae_e6_83_d0@@@', 
'publish_topic': 'device-server', 
'subscribe_topic': 'null'
}
```

问题来了：**客户端怎么接收服务端下发的消息呢？**

✅ 答案是：**自动订阅主题**。

![](https://i-blog.csdnimg.cn/img_convert/33fc21ac1e63d632392f099f27777d45.png)

✅ 解决方案：添加一个占位符构建的主题，只要客户端连接上来，将自动创建一个订阅主题：

![](https://i-blog.csdnimg.cn/img_convert/d468457d6dc088ba850d88d3d57f797f.png)

客户端下线后，会自动清理主题。

### 3.3 服务端怎么收消息：规则引擎

从小智客户端代码看，客户端发的消息中，压根没有`clientId`字段：

问题来了：**服务端怎么知道是哪个客户端发来的消息呢？**

![](https://i-blog.csdnimg.cn/img_convert/74dd4362012d1d79436e4c1d0db5c3e8.png)


✅ 解决方案：使用 `EMQX 规则引擎`，给消息添加 clientId

![](https://i-blog.csdnimg.cn/img_convert/bb5d2dccfe3b9a4ce893ace9937d3c20.png)

✅ 具体步骤：

**1.创建规则：** 每当有客户端往 `device-server` 发消息，就触发这条规则，提取 clientid、payload。

```
SELECT
  clientid,
  payload
FROM
  "device-server"
```

![](https://i-blog.csdnimg.cn/img_convert/e6064f4504456333c6aa655468ec3179.png)

**2. 添加动作：**

![](https://i-blog.csdnimg.cn/img_convert/fdf77cd8ac9173c2d7d6854130fa9147.png)

动作类型选择`消息重发布`，Payload 模板：

```
{
  "clientId": "${clientid}",
  "data": ${payload}
}
```
这表示：构建一个新 JSON，把客户端的 clientid 和原始 payload 都打包进去。

> 注意：payload 本身如果是字符串 JSON，需要在规则引擎中用 ${payload} 直接插入（不能加引号），否则会变成字符串嵌套字符串。

![](https://i-blog.csdnimg.cn/img_convert/69f66f6b0c7cd47cafdcf4b353f9a989.png)

此外，主题最好换一个，比如`device-server-enhanced`，否则会收到两条消息，因为原消息也会被订阅。

**3. 测试一下**

![](https://i-blog.csdnimg.cn/img_convert/75145907aa696f27ccfb245fe4609f60.png)


服务端打印结果如下：

```
device-server-enhanced {
  clientId: '98_3d_ae_e6_83_d0',
  data: {
    type: 'hello',
    version: 3,
    transport: 'udp',
    audio_params: {
      format: 'opus',
      sample_rate: 16000,
      channels: 1,
      frame_duration: 60
    }
  }
}
```
成功获取到 `clientId`，据此就可以区分`哪个客户端`发来的消息了。

### 3.3 启用认证模块
EMQX 会默认允许所有客户端连接（匿名登录），可以设置用户名密码认证。

![](https://i-blog.csdnimg.cn/img_convert/90db0eb1f3c324f0c6da9d70192911fc.png)

![](https://i-blog.csdnimg.cn/img_convert/4d19898f926590f972d800619b5eae0f.png)

设置后，客户端连接时传递用户名密码：

```
const client = mqtt.connect('mqtt://your-host:1883', {
  clientId: 'server',
  username: 'server',
  password: 'yourpassword'
});

```


### 3.4 测试 MQTT 延时

有了 MQTT Broker 这座桥梁后，我们拉到真实对话场景中，看下客户端和服务端的通信延时：

```
# 客户端-接收
2025-06-09T11:52:20.149Z MQTT publish: {"session_id":"93:3d:re:e6:83:d0","type":"listen","state":"detect"}
# 服务端-发送
2025-06-09T11:52:20.151Z recv mqtt msg: {"session_id":"93:3d:re:e6:83:d0","type":"listen","state":"detect"}

# 服务端-发送
2025-06-09T11:52:20.280Z MQTT publish: devices/p2p/93:3d:re:e6:83:d0 {"type":"stt","text":"你好"}
# 客户端-接收
2025-06-09T11:52:20.285Z MQTT recv: devices/p2p/93:3d:re:e6:83:d0 {"type":"stt","text":"你好"}
```

可以发现，基本保持 5ms 以内，真正做到了**毫秒级消息交付时延**！

## 写在最后

本文分享了 `小智 AI 通信协议之 MQTT+UDP`，并给出了 `EMQX` 搭建 `MQTT Broker` 的方案。

如果对你有帮助，欢迎**点赞收藏**备用。

篇幅有限，本篇主要涉及 `MQTT` 部分的通信流程，那么：
- `UDP` 呢？为啥还要加个 `UDP`？
- 音频信号是如何通过 `UDP` 进行传输的？ 

我们下篇见！
