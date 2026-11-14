
话接上篇，继续回答：**小智 AI 的客户端和服务端是如何通信的？**

[小智AI为何要用MQTT+UDP？怎么接入MQTT？](https://zhuanlan.zhihu.com/p/1916821312619389751)

上篇，主要聊了 `MQTT` 部分的搭建，那么：

- 为啥还要加个 `UDP`？
- 音频是如何通过 `UDP` 进行传输的？ 
- 客户端和服务端的整体交互逻辑是怎样的？

本篇，主要回答以上三个问题。

## 1. 为啥要加 `UDP`

从小智客户端我们可以看到：在 MQTT 协议下，加了 UDP 通道来实现音频通信。

问题来了：**也用 MQTT 来发音频不行么**？ 

答案是不行，有这么几个考量：

**1. MQTT 的特点**
- MQTT 是基于 TCP 的消息队列协议，适合小体积、低频率、可靠性要求高的消息（如控制指令、状态同步、文本等）。

**2. 音频流的需求**
- 实时语音对讲、TTS 播放等场景下，音频数据量大、对实时性和延迟要求高。
- 音频流通常是连续、带宽占用高的数据，要求尽快送达，偶尔丢包也能容忍。

**3. UDP的优势**
- UDP 是无连接、无确认的协议，延迟极低，适合实时音频/视频流。
- 即使有少量丢包，音频播放也不会卡顿（可容忍）。
- 发送端可以持续推送音频包，接收端实时解码播放。

**4. MQTT + UDP 的优势**
- **MQTT 用于**：设备注册、会话管理、控制指令、状态同步、文本消息（如ASR/LLM/TTS文本）。
- **UDP 用于**：高频、低延迟的音频数据传输（ASR语音流、TTS音频流）。


**总结来说**：MQTT 负责可靠的文本消息，UDP 负责高效的音频传输。既保证了可靠性，又兼顾了实时性和带宽效率。

接下来，我们来看下客户端和服务端的整体交互逻辑。

## 2. 客户端整体流程梳理

### 2.1 连接 MQTT 服务器
设备上电后，会请求`ota`地址，拿到 MQTT 服务器的相关信息。

设备和  MQTT 服务器 建联：
```
mqtt_->Connect(broker_address, broker_port, client_id_, username_, password_)
```

随后，设备给 MQTT 发送 hello 消息，服务端下发 UDP 通道参数（ip/port/key/nonce）。

```
# 客户端发送
{
  "type": "hello",
  "version": 3,
  "transport": "udp",
  "audio_params": {
    "format": "opus",
    "sample_rate": 16000,
    "channels": 1,
    "frame_duration": 60
  }
}
# 服务端返回
{
  "type": "hello",
  "session_id": "xxxx",
  "audio_params": {"sample_rate": 24000,"frame_duration": 60},
  "udp": {"server": "106.xx.xxx.xxx","port": 8843,"key": "xxxx","nonce": "xxxx"}
}
```

### 2.2 开启 UDP 通道

**step 1**：拿到 UDP 地址后，设备和服务端直接建联：

```
udp_->Connect(udp_server_, udp_port_);
```

注意：这一步只是设置目标 IP 和端口，准备好后续的发送，不会自动发包。


而正式发包之前，还有对音频进行加密，怎么加密的？
> 还记得刚才 MQTT 下发的`key/nonce`字段么，就是用来加密的。

![](https://i-blog.csdnimg.cn/img_convert/1b7fc86c8605d3ecde11c64f5dd5b093.png)


**step 2**：开始给服务端发包：

```
udp_->Send(encrypted);
```

服务端只有在收到客户端的第一个 UDP 包后，才能知道客户端的 IP 和端口。

**至此，客户端和服务端的 UDP 通道，才算真正建立！**

### 2.3 音频内容走 UDP 通道

你看，客户端直接扔了一个`加密包`过来，压根没有身份信息啊！

问题来了：**服务端是怎么识别发件人呢？**

总不能暴露客户端身份信息吧！

所以，需要服务端进行特殊处理，可以采用`首包即认证`的做法：

```
客户端通过 MQTT 握手，服务端记录了每个 clientId 关联的 key/nonce
1. 客户端发 UDP 包时，使用该 key 加密了数据
2. 服务端收到 UDP 包：
  - 遍历所有未绑定 IP:Port 的 session，尝试解密
  - 解密成功说明找到了客户端
  - 将该 IP:Port 绑定到对应 session，后续直接识别
```

看下图：绑定后，下次即可根据`IP:Port`确认客户端身份，从而实现`一次绑定，终身受用`。

![](https://i-blog.csdnimg.cn/img_convert/ef1b9a5ff3ea74ec8523f9ef26f577aa.png)

这样做，虽然慢一点（需要解一次密），但不需要客户端暴露任何身份。

后续，设备和服务端，就可以通过 UDP 通道，基于约定的 `key`，收发加密的音频包。

### 2.4 文本消息走 MQTT 通道

控制消息、状态同步、文本内容等依然走 MQTT。

![](https://i-blog.csdnimg.cn/img_convert/fa83154c69c7fc736b66083a78fdb9a3.png)

## 3. 服务端整体流程梳理

理清了上述交互逻辑，我们来简单梳理一下，服务端处理的几个关键点：

**MQTT hello 消息到达**：
- 随机生成 key/nonce，创建 Handler，保存到 sessionMap（key: clientId）。
- 发送 hello 响应（带 key/nonce/UDP参数），经过 MQTT 通道，到客户端。
- 等待客户端 UDP 首包。

**UDP 首包到达**：
- 构建双索引结构：sessionMap（clientId）、ipPortMap（ip:port）。
- 遍历所有未绑定 UDP 地址的 session，尝试用 key/nonce 解密。
- 解密成功则绑定 clientAddr/clientPort，并建立 ipPortMap 快速索引。
- 后续所有 UDP 包直接用 ipPortMap 查找 handler。

**MQTT 业务消息到来时**：
- 用 clientId 查找 handler，分发到对应 handler 处理。

**音频包下发**：
- handler 负责组装、加密音频包，通过 UDP 发送给客户端。

**会话关闭**：
- handler 负责资源清理、MQTT goodbye 消息、统计上报token消耗等。

**超时管理**：
- 服务端定期检查活跃的客户端，长时间无交互则清理。

值得注意的是：在 node.js 中，**UDP/MQTT 都是异步的**，而：
- UDP：无连接、无确认、无排队，直接发，延迟极低。
- MQTT：基于 TCP，有队列、确认、QoS，消息到达服务端有一定延迟。

所以，需要确保发布顺序，比如：要等待 UDP 所有音频发送完成，才能用 MQTT 下发 stop 状态。


## 写在最后

本文分享了 `小智 AI 通信协议之 MQTT+UDP`，并给出了客户端和服务端的整体交互逻辑。

如果对你有帮助，欢迎**点赞收藏**备用。

