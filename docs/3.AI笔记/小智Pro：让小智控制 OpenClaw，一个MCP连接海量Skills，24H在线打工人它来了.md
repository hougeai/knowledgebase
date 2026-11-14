前文，分享了 `openclaw` 免费部署教程：

[永久免费 OpenClaw 部署和实战，7x24在线，手把手教程](https://zhuanlan.zhihu.com/p/2006309221654889869)

上面带大家跑通了接入飞书的流程。

不管是飞书，还是QQ、微信等IM工具，最常用的交互方式是文字。

语音，才是最天然的聊天交互。

**如何把`小智语音对话机器人`和 `openclaw` 打通？**

其基本流程是：

![](https://i-blog.csdnimg.cn/img_convert/515a3c8e45808e9974e70719dea691c9.png)

进一步，小智的能力就不再局限于**接入的MCP工具**，而是 `openclaw` 背后的**海量Skills**。

今日分享，聊聊：`小智Pro`的具体做法👇：

- 平台侧：建立和`openclaw`的通信
- 用户侧：接入自己的`openclaw`，并通过设备端MCP指挥`openclaw`

![](https://i-blog.csdnimg.cn/img_convert/7fbfadf08b2e1513ca5fd4e42a97b385.png)

![](https://i-blog.csdnimg.cn/img_convert/82b86582be8338833fa1e9ed6c5b4693.png)

## 1. 建立和`openclaw`的通信

### 1.1 通信协议

要实现和 `openclaw` 通信，传输层本质上是 `WebSocket`。

飞书、微信都是一种终端。

如何进行区分不同终端和不同会话？

答：`client.id` 和 `session_key`

![](https://i-blog.csdnimg.cn/img_convert/2762a26e58b93031d6303153ce26de40.png)

因此，多个 client，可以共用一个 session 的记忆和对话历史：

![](https://i-blog.csdnimg.cn/img_convert/65c551844702664bae09271205d22eca.png)

我们可以在`openclaw`控制台，选择查看指定`session`的对话：

![](https://i-blog.csdnimg.cn/img_convert/c9bbc3281fbc9ee86a06b5fdb90729a5.png)

### 1.2 核心接口

基于`openclaw`的通信协议，关键请求方法整理如下：

![](https://i-blog.csdnimg.cn/img_convert/3c9a15975d380efe2a7807040b3d2cfe.png)

我们把所有方法通过 `self.request` 接口封装，底层协议采用 WebSocket 传输，示例代码如下：

```
async def chat_send(self, message: str) -> Any:
    """发送聊天消息到指定session"""
    return await self.request('chat.send', {
        'sessionKey': self.session_key,
        'message': message,
        'idempotencyKey': f'{int(time.time() * 1000)}-{hash(message)}',
    })

async def get_history(self, limit: int = 50) -> Any:
    """获取聊天历史"""
    return await self.request('chat.history', {
        'sessionKey': self.session_key,
        'limit': limit
    })

async def list_sessions(self) -> Any:
    """列出所有session"""
    return await self.request('sessions.list')

async def list_agents(self) -> Any:
    """列出agents"""
    return await self.request('agents.list')

async def get_config(self) -> Any:
    """获取配置"""
    return await self.request('config.get')
```


### 1.3 响应解析

响应结果中，重点关注`agent`和`chat`事件，从日志中查看几个关键节点的数据结构：
```
2026-02-15 17:38:44 - openclaw - INFO - 尝试连接: ws://14.xx.xx.82:18789
2026-02-15 17:38:44 - openclaw - INFO - WS已连接，等待 challenge...
2026-02-15 17:38:44 - openclaw - INFO - 收到 challenge: {'type': 'event', 'event': 'connect.challenge', 'payload': {'nonce': 'ae76555e-1d6e-4dc1-acea-294e67e0dcce', 'ts': 1771148324902}}
2026-02-15 17:38:44 - openclaw - INFO - ✅ 连接成功！
2026-02-15 17:38:44 - openclaw - INFO - 🚀 消息已发送，runId: 1771148324960--1126353816726381137，等待 AI 回复...
2026-02-15 17:38:45 - openclaw - INFO - 🤖 Agent事件: runId=1771148324960--1126353816726381137, stream=lifecycle, data={'phase': 'start', 'startedAt': 1771148325217}
2026-02-15 17:38:50 - openclaw - INFO - 🤖 Agent事件: runId=1771148324960--1126353816726381137, stream=assistant, data={'text': '收到', 'delta': '收到'}
2026-02-15 17:38:50 - openclaw - INFO - 💬 Chat事件: runId=1771148324960--1126353816726381137, state=delta, message={'role': 'assistant', 'content': [{'type': 'text', 'text': '收到'}], 'timestamp': 1771148330101}
2026-02-15 17:38:50 - openclaw - INFO - 🤖 Agent事件: runId=1771148324960--1126353816726381137, stream=assistant, data={'text': '收到，我去', 'delta': '，我去'}
2026-02-15 17:38:50 - openclaw - INFO - 💬 Chat事件: runId=1771148324960--1126353816726381137, state=delta, message={'role': 'assistant', 'content': [{'type': 'text', 'text': '收到，我去检查下人设文件'}], 'timestamp': 1771148330294}
2026-02-15 17:38:50 - openclaw - INFO - 🤖 Agent事件: runId=1771148324960--1126353816726381137, stream=assistant, data={'text': '收到，我去检查下人设文件。', 'delta': '。'}
2026-02-15 17:39:11 - openclaw - INFO - 🤖 Agent事件: runId=1771148324960--1126353816726381137, stream=lifecycle, data={'phase': 'end', 'endedAt': 1771148351507}
2026-02-15 17:39:11 - openclaw - INFO - 💬 Chat事件: runId=1771148324960--1126353816726381137, state=final, message={'role': 'assistant', 'content': [{'type': 'text', 'text': '你说得对，我漏了。SOUL.md 里写得清清楚楚：\n\n> 收到任何消息或者任务，先立即回复我\'收到\'，然后再去具体执行\n\n以后我会先回"收到"，再干活。记住了。'}], 'timestamp': 1771148351507}
```

### 1.4 架构设计

基于以上分析，`小智Pro` 采用双` WebSocket` 桥接架构：

- 后端服务作为中间代理（Proxy）
- 一端连接 前端客户端/Esp32设备端
- 一端连接用户的 `OpenClaw Gateway`

![](https://i-blog.csdnimg.cn/img_convert/c783b19971b108407dd181054b9cdd3a.png)


前端连接成功后，可以尝试给`openclaw`发一条消息：

![](https://i-blog.csdnimg.cn/img_convert/551a81f6ca3cd8534a78f70f9f9c5551.png)


## 2. 设备端 MCP 调用

以上，`小智Pro` 已打通和`openclaw`的通信。

设备端如何调用呢？

本质上还是通过MCP，再看文章开头的流程图：

![](https://i-blog.csdnimg.cn/img_convert/515a3c8e45808e9974e70719dea691c9.png)

因此，我们只需在设备端新增一个 Tool：`self.openclaw.send`。

但是，小智的语音识别很难精准命中`openclaw`，所以最好给`openclaw`一个中文名字：

![](https://i-blog.csdnimg.cn/img_convert/b8c47022287ef0d0be80e5bc3356f170.png)

`欧克劳`，就他了。

测试发送成功，并收到了 `openclaw` 的回应：

![](https://i-blog.csdnimg.cn/img_convert/5cd0283e6bc3ab0abf2b466a42be41eb.png)


## 3. 用户接入`openclaw`流程

### 3.1 修改人设设定

因为 `openclaw` 接入的是推理模型，`thinking`阶段耗时较长。

为了减少等待时长，需要修改下`openclaw`的人设：

![](https://i-blog.csdnimg.cn/img_convert/86621d77387720a263f4d1f4d010032f.png)

### 3.2 前端建立连接

首先，在 `openclaw` 控制台获取你**公网可访问**的 `Gateway URL` 和用于鉴权的 `Token`。

![](https://i-blog.csdnimg.cn/img_convert/dac988b2819369f2c905fe58d8cb95e7.png)

然后，前往`小智Pro`控制台，填入对应字段：

![](https://i-blog.csdnimg.cn/img_convert/aa71a77f550b3b5c159440a3e145440d.png)

注：`session_key` 需遵循以下命名规范：

```
agent:<agent_id>:<label>
```

如果不需要区分会话，可用 `openclaw` 控制台的 `Default Session Key`。

连接成功后，可在`小智Pro`控制台进行对话和查看历史对话记录：

![](https://i-blog.csdnimg.cn/img_convert/835432c9408aba34f6b1fa2879e6da4a.png)


人设修改后，在前端看下延时：

![](https://i-blog.csdnimg.cn/img_convert/364dda48de387278b92c2db7be312955.png)

![](https://i-blog.csdnimg.cn/img_convert/5182de32ed1ecd59c41cd0f207f0ba5c.png)

![](https://i-blog.csdnimg.cn/img_convert/4eb57340d4998f5875cd77a89704c532.png)


简单指令，基本秒回~

再让小智给 `openclaw` 发送一个任务指令：

![](https://i-blog.csdnimg.cn/img_convert/d67016ed196dcf9d737dd653e4cb6081.png)

![](https://i-blog.csdnimg.cn/img_convert/4594dd6c84abd04b1fbd5f7284b788a8.png)


回到 `openclaw` 控制台验收下：

![](https://i-blog.csdnimg.cn/img_convert/75e992b02af7f4cb6a42267a4d9e7fdd.png)

成功搞定！

## 写在最后

本文分享了`小智Pro：让小智接管 OpenClaw`的实现方案。



如果对你有帮助，不妨**点赞收藏**备用。

欢迎体验 `小智Pro` 更多功能，请戳👇：

> https://mkwyqeoebedx.sealosbja.site

注：`接管 OpenClaw`能力需设备端固件`v2.2.2.2`版支持。

目前已全面适配小智官方仓库收录的开发板型号，下载地址：

> https://github.com/hougeai/xiaozhiPro/releases

![](https://i-blog.csdnimg.cn/img_convert/38349590548cb9ebbfbe275229825374.png)

有任何问题，欢迎进群交流。


