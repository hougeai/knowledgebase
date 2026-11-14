如何把`小智语音对话机器人`和 `openclaw` 打通？

![](https://i-blog.csdnimg.cn/img_convert/ec6ced5243da49c70983396f146a21a5.png)

`OpenClaw` 是异步处理：收到消息 → 网关处理 → 一段时间后返回回复。

这种模式天然适合文字聊天（如 IM），但不适合语音对话的实时交互需求。

`小智`采用实时语音通信协议，要求低延迟、即时响应。

直接对接 OpenClaw 的异步接口会导致：
- 用户说话后长时间无反馈，体验割裂
- 语音打断、上下文同步困难

因此，需设计中间层，来管理 `OpenClaw` 的异步任务。

前文分享过一种实现思路：

[小智Pro：让小智控制 OpenClaw，一个MCP连接海量Skills，24H在线打工人它来了](https://zhuanlan.zhihu.com/p/2007395274100858961)

但这种设计，要维护两个 `WebSocket` 连接：

- 前端 ↔ 后端，用于接收前端指令、推送 OpenClaw 的流式响应。
- 后端 ↔ `OpenClaw Gateway`，用于和 OpenClaw 服务保持长连接，收发消息。

假设有 N 个活跃用户，就得 2N 条 WebSocket 连接，资源占用高。

怎么搞？

今日分享，聊聊：`小智`控制`OpenClaw`的全新升级版👇：

- 平台侧：和`OpenClaw`的异步通信的基本原理
- 用户侧：接入并管理`OpenClaw`的操作指南


## 1. 基本原理

小智设备与` OpenClaw` 通信，采用 **异步消息转发** 模式，整体流程如下：

```
小智设备 ──(MCP)──> 小智Pro服务端 ──(HTTP)──> OpenClaw Gateway
                                                      │
小智设备 <──(推送)── 小智Pro服务端 <──(Redis 缓存)──────┘
```

![](https://i-blog.csdnimg.cn/img_convert/de69a89afa9dde94e18bac0c49429465.png)
### 1.1 消息发送

1. 用户对小智说出指令（如"让欧克劳帮我发一条飞书消息"）
2. 设备端通过 `self.openclaw.send` 将消息发送到小智Pro服务端
3. 服务端收到后**立即返回确认**，将实际请求放入后台任务异步执行
4. 后台任务调用 `OpenClaw Gateway` 的 API，等待回复

### 1.2 回复投递

OpenClaw 返回结果后，服务端会：

1. **缓存回复**：将回复内容存入 Redis，多条回复自动拼接，5分钟自动过期
2. **感知设备状态**：查询设备当前对话状态
   - 设备**在听**（listening）：发送指令通知设备取消息
   - 设备**空闲**（idle）：先唤醒设备，再通知取消息
   - 设备**在说**（speaking）：自动等待，等待结束后再通知取消息
3. **设备取消息**：设备收到通知后，主动调用 retrieve 接口获取缓存的回复
4. **取完即删**：回复被读取后立即从 Redis 删除，确保消息不重复消费

### 1.3 关键设计

| 特性     | 说明                               |
| -------- | ---------------------------------- |
| 异步响应 | 发送消息后立即返回，不阻塞设备对话 |
| 消息防丢 | 多条回复追加拼接，不会互相覆盖     |
| 可靠投递 | 根据设备状态智能选择推送时机       |
| 原子操作 | 读取回复使用原子操作，避免重复消费  |

## 2. 操作指南

### 2.0 OpenClaw 配置示例

> 确保 `OpenClaw Gateway` 监听在公网可访问的地址和端口，并配置了 Token 认证。


找到 OpenClaw 的配置文件：`~/.openclaw/openclaw.json`

重点关注以下**三个**配置项：

```json
"gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    },
    "tools": {
      "allow": ["sessions_send"]
    },
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "xxx"
    },
    "port": 18789,
    "bind": "loopback",    
  },
  "session": {
    "dmScope": "per-channel-peer",
  },
  "tools": {
    "profile": "full",
    "exec": {
      "security": "full",
      "ask": "off"
    },
    "sessions": {
      "visibility": "all"
    }
  }
```

具体说明：
- gateway.http 配置：允许 API 调用
- gateway.tools.allow：允许 `sessions_send` 工具，以便小智Pro服务端通过该工具将消息发送到指定会话
- tools.profile = "full" — 所有工具都允许
- sessions.visibility = "all" — 支持跨会话查看

### 2.1 小智Pro控制台配置 OpenClaw

前往小智Pro控制台：[https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

左侧菜单 **设备端MCP → OpenClaw**，首次使用需配置连接：

1. 点击 **连接 OpenClaw** 按钮
2. 弹出的对话框中填写：
- **Gateway URL**：OpenClaw Gateway 的地址，如 `http://your-ip:18789`
- **Token**：OpenClaw 的认证 Token
- **Agent**：默认对话的智能体名称，如 `main`，连接成功后支持切换智能体

3. 点击 **保存**，系统会自动检测连接状态

![](https://i-blog.csdnimg.cn/img_convert/bf16f25a6b115e4700cf4d672d4bad09.png)

配置完成后，页面顶部会显示：

- **连接状态标签**（绿色=正常）
- **Gateway URL**
- **Token**（脱敏显示）

你也可以随时点击 **检查连接** 按钮重新检测，或点击`删除`按钮清除配置。

![](https://i-blog.csdnimg.cn/img_convert/c2f001f2f05bfa544a48346e653f9fc7.png)

### 2.2 配置Tab - 切换和小智对话的智能体

**配置Tab**，展示小智和`OpenClaw`的专属会话：

- **智能体**：和小智对话的智能体，支持切换
- **SessionKey**：固定为 `openai-user:xiaozhi-pro:{用户ID}`，即小智设备对话时使用的会话
- **聊天区域**：支持输入消息与 `OpenClaw` 对话
- **刷新按钮**：拉取最近20条对话记录

> 注：这里记录小智设备和`OpenClaw`的专属会话，你可以在前端查看 / 测试对话内容，和`OpenClaw`控制台对话记录同步。

![](https://i-blog.csdnimg.cn/img_convert/576abc0e5e9390be4e844e6ab3cdabd2.webp?x-oss-process=image/format,png)

![](https://i-blog.csdnimg.cn/img_convert/0a5be8f08701502e978485d5483e2fb1.webp?x-oss-process=image/format,png)

### 2.3 聊天Tab - 浏览其他会话

切换到 **聊天Tab**，可以浏览 `OpenClaw` 的所有会话：

1. **选择智能体**：刷新智能体列表，从下拉框中选择一个 Agent
2. **选择会话**：选定智能体后，刷新会话列表并选择一个会话
3. **会话详情**：选中会话后，右侧显示该会话的渠道、模型、Token用量、状态等信息
4. **历史记录**：选择会话后自动加载最近20条消息
5. **发送消息**：在选中会话的输入框中输入消息并发送，和`OpenClaw`控制台对话记录同步。

![](https://i-blog.csdnimg.cn/img_convert/fc5393b808b434f37ee226c733c09526.png)

### 2.4 通过设备语音操控
> 注：设备固件版本需为 `v2.2.5.1` 以上：https://github.com/hougeai/xiaozhiPro/releases

配置好 OpenClaw 连接后，你可以直接对小智说：

```
- '问问欧克劳现在都有哪些定时任务'
- '让欧克劳给我的飞书发一条消息'
- '让欧克劳立刻完成今天的AI资讯整理任务'
```

成功调用后，屏幕或日志中会看到 `self.openclaw.send` 工具调用，欧克劳回复后，服务端会自动推送到设备，设备随即播报回复内容。

## 3. 常见问题

### 连接状态显示异常？

- 检查 Gateway URL 是否正确，确保格式为 `http://ip:port` 或 `https://domain.com`
- 确认 OpenClaw Gateway 服务正常运行
- 确认 Token 有效

### 设备端没有收到欧克劳的回复？

- 确认设备已绑定到小智Pro账号
- 确认设备固件版本为 v2.2.5.1 以上
- 回复会在5分钟后自动过期，如果设备长时间未取消息则无法获取
- 如果设备正在说话，服务端会自动等待（最多25秒），等待结束后再推送

### 发送消息后没有反应？

- OpenClaw 的回复是异步处理的，消息发送后需要等待 Gateway 响应
- 如果 Gateway 响应较慢，请耐心等待或检查 OpenClaw 服务状态

### 发送消息提示异常？

- 参考 2.0 节的配置示例，确保 OpenClaw 的配置项正确设置，特别是工具权限和认证方式

![](https://i-blog.csdnimg.cn/img_convert/a46c5e66c485f951c653dbed3cf4c621.webp?x-oss-process=image/format,png)



## 4. 效果展示

比如，让修一下定时任务失败的问题：

![](https://i-blog.csdnimg.cn/img_convert/c2b8978a31392773937d364485c7e32f.jpeg)

![](https://i-blog.csdnimg.cn/img_convert/76467fb2d520ad07f5befcf41422ac9b.jpeg)

回到 `Openclaw` 控制台，看`小智`和`Openclaw`的对话记录：

![](https://i-blog.csdnimg.cn/img_convert/71aab20bee7bbba256eb99502ff75b08.png)


比如，让打开浏览器查查今日热搜：

![](https://i-blog.csdnimg.cn/img_convert/ce6cc2dbd68e7fa684c295e30fa6f200.png)

![](https://i-blog.csdnimg.cn/img_convert/3e122e5d498a6410bd3fa60b9827ff99.png)

![](https://i-blog.csdnimg.cn/img_convert/267245164050e3d5d9ee0cee051516b8.png)

## 写在最后

本文分享了`小智Pro：让小智控制 OpenClaw`的全新升级方案。

如果对你有帮助，不妨**点赞收藏**备用。

欢迎体验 `小智Pro` 更多功能，请戳👇：

> https://mkwyqeoebedx.sealosbja.site

注：`控制 OpenClaw`能力需设备端固件`v2.2.5.1`版。

固件已全面适配小智官方仓库收录的开发板型号，下载地址：

> https://github.com/hougeai/xiaozhiPro/releases


![](https://i-blog.csdnimg.cn/img_convert/9398f437fc0e163fb43c05af61a77aff.png)

有任何问题，欢迎进群交流。

