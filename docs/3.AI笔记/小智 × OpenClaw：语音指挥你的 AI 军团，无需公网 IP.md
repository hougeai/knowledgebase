如何把`小智语音对话机器人`和 `openclaw` 打通？

![](https://i-blog.csdnimg.cn/img_convert/f18e4f0e1cb16230547335134da76e1e.png)

`OpenClaw` 天然是异步的：收到消息 → 处理 → 一段时间后返回回复。

文字聊天无所谓，但 `小智` 是实时语音交互，用户说完话，等几秒，体验就崩了。

所以需要一个中间层，把 `OpenClaw` 的异步回复桥接到小智的实时语音通道。

前文分享过两种实现思路：

[小智Pro：让小智控制 OpenClaw，一个MCP连接海量Skills，24H在线打工人它来了](https://zhuanlan.zhihu.com/p/2007395274100858961)

[小智指挥 OpenClaw：异步响应、超低延迟](https://zhuanlan.zhihu.com/p/2029523042582163582)

**但都需要公网 IP、手动配置 Gateway 地址和 Token，门槛太高了。**

现在，**插件版来了**——

一条命令装完，自动连接，无需公网 IP，消息实时双向推送。


## 1. 插件版 vs 之前的方案

| 对比项 | 插件版（新） | API 版（旧） |
|--------|------------|-------------|
| 网络要求 | OpenClaw **无需公网 IP** | OpenClaw 需要公网可访问 |
| 连接方式 | 插件主动 WS 连接服务端 | 服务端调用 OpenClaw HTTP API |
| 消息延迟 | 实时推送，**毫秒级** | 异步轮询，有延迟 |
| 配置方式 | 安装插件 + API 密钥 | 控制台配置 Gateway URL + Token |
| 主动推送 | 即时，零延迟 | 受轮询间隔制约 |

一句话：**装个插件就行，不用折腾网络和配置。**


## 2. 怎么工作的？

小智设备与 OpenClaw 通过 **WebSocket 长连接** 通信，由 OpenClaw 端的插件主动连接到小智Pro服务端：

```
小智设备 ────> 小智Pro服务端 <──(WebSocket)──> OpenClaw (xiaozhi-pro 插件主动连入)
                        │                      │
小智设备 <──── 小智Pro服务端 <──(WS 实时推送)────┘
```

![](https://i-blog.csdnimg.cn/img_convert/f31927c620402bebee86c0302e33d1e0.jpeg)


核心设计：

| 特性 | 说明 |
|------|------|
| 实时通信 | WebSocket 全双工长连接，消息即时推送，无轮询延迟 |
| 无需公网 | OpenClaw 主动连接服务端，无需暴露端口 |
| 心跳保活 | 30 秒心跳检测，60 秒无响应自动断开 |
| 自动重连 | 指数退避重连（1s → 2s → 4s → ... → 30s 上限） |
| 消息去重 | 重复推送自动跳过，保证幂等 |
| 精确投递 | 支持指定设备投递或广播所有设备 |
| 自动踢旧 | 同一账号新连接自动踢掉旧连接 |


## 3. 怎么用？

### 3.1 太长不看版

把下面这段文字直接发给你的 OpenClaw，让它帮你搞定：

> 请帮我安装并配置小智Pro OpenClaw插件：
> 
> 1. 安装插件：`openclaw plugins install @xiaozhi-pro/openclaw-plugin`
> 2. 如已安装，更新：`openclaw plugins install @xiaozhi-pro/openclaw-plugin --force`
> 3. 在 `openclaw.json` 的 `channels` 中添加配置：
> 
> ```json
> "xiaozhi-pro": {
>   "token": "<我的API密钥>",
>   "agentId": "main"
> }
> ```
> 
> - `token`（必填）：小智Pro API密钥
> - `agentId`（可选）：智能体ID，不填默认 `main`


### 3.2 手动操作版

**第一步：获取 API 密钥**
> 
> 控制台：[https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

前往小智Pro控制台，进入 API 密钥页面，点击创建密钥。

> ⚠️ API 密钥是插件连接小智Pro的唯一凭证，请勿泄露。

**第二步：安装插件**

在 OpenClaw 所在服务器上执行：

```bash
openclaw plugins install @xiaozhi-pro/openclaw-plugin
```

已安装过旧版？更新即可：

```bash
openclaw plugins install @xiaozhi-pro/openclaw-plugin --force
```

**第三步：配置插件**

编辑 `openclaw.json`，添加：

```json
{
  "channels": {
    "xiaozhi-pro": {
      "token": "你的小智Pro平台API密钥",
      "agentId": "main"
    }
  }
}
```

- `token`（必填）：小智Pro API密钥，也可通过环境变量 `XIAOZHI_PRO_TOKEN` 设置
- `agentId`（可选）：指定智能体ID，不填默认 `main`

**第四步：重启**

安装插件和更新配置后，`OpenClaw` 通常会自动重启 Gateway。

如果没有重启，可以手动执行：

```bash
systemctl --user restart openclaw-gateway.service
# or
openclaw gateway restart
```

插件会自动连接小智Pro 服务端，发送 `{"type":"auth","token":"..."}` 完成认证后进入双向通信。

查看 OpenClaw 日志确认连接状态：

```bash
journalctl --user -u openclaw-gateway.service -f
```

**第五步：验证**

1. 进入小智Pro控制台，点击左侧菜单 **设备端MCP → 龙虾插件版**
2. 点击 **检查连接** 按钮
3. 如果显示绿色"已连接"标签，说明插件已成功连接

![](https://i-blog.csdnimg.cn/img_convert/fd1315f2f7200e7d20a6661786e9b8d4.png)


### 3.3 语音操控示例

配置好后，直接对小智说：

```
'问问欧克劳现在都有哪些定时任务'
'让欧克劳给我的飞书发一条消息'
'让欧克劳立刻完成今天的AI资讯整理任务'
```

成功调用后，屏幕或日志中会看到 `self.openclaw.send` 工具调用，`OpenClaw`回复后，服务端会自动推送到设备，设备随即播报回复内容。

## 4. 常见问题

**连接状态显示"未连接"？**

- 确认插件已安装：`openclaw plugins list`
- 检查 `openclaw.json` 中 token 是否配置正确
- 查看 OpenClaw 日志排查错误

**插件频繁断开？**

- 检查网络稳定性
- 确认服务器时间同步（NTP）
- 插件内置自动重连，短暂断开后会自动恢复

**设备没收到回复？**

- 确认设备已绑定到小智Pro账号
- 确认固件版本 v2.2.5.1 以上
- 确认控制台显示"已连接"

**如何同时使用插件版和 API 版？**

- 插件版和 API 版共享同一套设备端 MCP 工具
- 服务端优先走 WebSocket 通道（插件版），插件未连接时自动回退到 HTTP API（API 版）。

## 写在最后

**装个插件，语音指挥你的 AI 军团，就这么简单。**

同样的思路，下一步我们接入**Hermes**，敬请期待。

如果对你有帮助，不妨**点赞收藏**备用。



欢迎体验 `小智Pro` 更多功能，请戳👇：

> https://mkwyqeoebedx.sealosbja.site

注：`控制 OpenClaw`能力需设备端固件`v2.2.5.1`版。

固件已全面适配小智官方仓库收录的开发板型号，下载地址：

> https://github.com/hougeai/xiaozhiPro/releases

![](https://i-blog.csdnimg.cn/img_convert/058e9c6b750f80d162c5c98a41049f6b.png)

有任何问题，欢迎进群交流。


