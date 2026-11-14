前文分析了`小智如何控制IoT设备`：

[小智AI如何控制IoT设备？LLM vs MCP](https://zhuanlan.zhihu.com/p/1914637833488017038)

并给出了两种方案。

**不过总感觉不是很优雅**，之前的交互逻辑是这样：

![](https://i-blog.csdnimg.cn/img_convert/f2d7ad1750fa2e116df191352a1f6022.png)

你看，客户端需要不时上传`当前状态`给服务端，并放到 LLM 的提示词中。

可是，**大部分时候，服务端压根不需要这些字段啊**。

最近，小智客户端代码更新到 `1.7.x`，而 `IoT 控制` 的交互逻辑，也发生了变化。

核心思想来自 **MCP**：客户端作为 `MCP server`，而服务端的 LLM 作为 `MCP client`，看下图：

![](https://i-blog.csdnimg.cn/img_convert/cb5b5eb28b479c2b834349a2faa439d3.png)

有朋友好奇，咋 `server` 和 `client` 还角色互换了呢？

本文，将尝试拆解这部分，并给出服务端的实现思路。
> 注：本文将基于 MQTT + UDP 协议，websocket 协议实现起来会更容易一些。

> 注：默认读者已了解 MQTT + UDP 协议，以及什么是 MCP 协议。否则建议先翻看之前的文章。

## 1. 客户端

客户端代码中新增了`mcp_server`部分，其中最重要的是通用工具注册部分 `AddCommonTools()`，用于让服务端的 AI 感知和操作硬件设备。

比如：

```
self.get_device_status
用途：获取设备状态信息（如音频、屏幕、电池、网络等）
```
有了这个工具，就不需要每次都无脑给服务端上传`设备状态`了。

再比如：

```
self.audio_speaker.set_volume
用途：设置音频输出音量

self.screen.set_brightness
用途：设置屏幕亮度

self.screen.set_theme
用途：设置 UI 主题（如 light/dark 模式）
```

还有更好玩的：**接入摄像头，提供视觉能力**
```
self.camera.take_photo
用途：拍照并让摄像头解释图像内容（比如用于视觉问答）
返回值：包含照片信息的 JSON 对象。先调用 camera->Capture() 拍照，再通过 camera->Explain(...) 解释内容。
- Explain：将当前摄像头缓冲区中的图像编码为JPEG格式，并通过HTTP POST请求；必须先调用SetExplainUrl()设置服务器URL
- McpServer::ParseCapabilities中定义了SetExplainUrl
```

## 2. 服务端

整个服务端的交互逻辑相对复杂，这里尝试用流程图来说明：

![](https://i-blog.csdnimg.cn/img_convert/25acc5eb3f6000c780d57dab6811a4f1.png)

其中，关于 `MCP 控制 IoT 设备`， 需要重点关注以下几个关键节点：

- 客户端连接 MQTT 服务器
- Hello 消息交互
- 服务端发送 MCP initialize 请求
- 服务端发起工具调用

### 2.1 客户端连接 MQTT 服务器

客户端连接后，通过 MQTT 发送 connected 消息。

正常情况下：客户端连接上 MQTT 服务器，服务端是无感知的啊！

**怎么搞？**

✅ **解决方案**：使用 `EMQX 规则引擎`

创建一条规则，监听 `$events/client_connected` 事件（EMQX 内置事件 topic）。

当有客户端连接时，规则引擎可以自动向指定的 topic 发布一条自定义消息。

具体步骤如图：

![](https://i-blog.csdnimg.cn/img_convert/c4e516e0a180a8cd38640220a1b70173.png)


![](https://i-blog.csdnimg.cn/img_convert/d83c5b569541d26d23db6a2bd1a3f458.png)


此外，EMQX 同样也支持客户端断开 MQTT 连接时，自动发送一条消息。

你可以监听 EMQX 的内置事件主题 `$events/client_disconnected`，用规则引擎自动向指定 topic 发布通知消息。

所以，这里我们建立两条规则，来判断设备是否已经下线：

![](https://i-blog.csdnimg.cn/img_convert/e9c18a1bfd296d89f6a2ce6a8bf1f803.png)

### 2.2 MCP 初始化

服务端收到客户端的连接消息后，立即创建一个 Handler 实例，准备和客户端通信。

然后，开始完成 `MCP 初始化`，主要有两步，下图红框标注：
- 建立连接
- 获取工具列表

![](https://i-blog.csdnimg.cn/img_convert/9eadefef21d5002dce8c5b4fec3c4025.png)

拿到这个工具列表，下一步才可以初始化 LLM 智能体。

### 2.3 Hello 消息交互

当客户端需要进行语音交互时，会发送 hello 类型消息。

服务端会验证设备信息，加载 `2.2 部分的工具列表`，并启动 ASR、TTS、LLM 会话。

最后，服务端向客户端发送 hello 响应，包含 UDP 配置参数。

至此，客户端和服务端，终于成功完成握手。


## 2.4 流程测试

**首先，客户端连接上来：**

![](https://i-blog.csdnimg.cn/img_convert/1fc71dd00e695bc6329ab189b20957ce.png)

**然后，完成 hello 握手：**

- 客户端给服务端请求：

![](https://i-blog.csdnimg.cn/img_convert/21f22887346c6c3f8c04c24a756232e6.png)

- 服务端给客户端响应：

![](https://i-blog.csdnimg.cn/img_convert/5101ed87e88e5bad8d588ae76ab02ae4.png)

**最后，开始工具调用：**

比如问它：设备音量多少？

LLM 会自行判断，并调用`self.get_device_status`方法，请求客户端，客户端返回当前设备状态，再由 LLM 理解后回答：

![](https://i-blog.csdnimg.cn/img_convert/515f0212f59f08a8e5a5c180ef60489c.png)


## 写在最后

本文分享了 `小智 AI 控制 IoT 设备` 的服务端实现方案。

有了这，好玩的事就更多了~

下篇继续聊：

- 小智 AI 如何接入视觉能力？

如果对你有帮助，欢迎**点赞收藏**备用。

---

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

