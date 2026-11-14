
前文，分享过如何把`小智语音对话机器人`和 `OpenClaw` 打通：

[小智 × OpenClaw：语音指挥你的 AI 军团，无需公网 IP](https://zhuanlan.zhihu.com/p/2047948271344264122)

同样的思路，`Hermes` 也接入了——

![](https://i-blog.csdnimg.cn/img_convert/48ecb0921c012d1224400b13a76ce864.png)

## 1. Hermes 插件

`Hermes` 是一个开源的 AI Agent 网关，和 OpenClaw 类似，但有两个关键优势：

- **自进化学习**：Hermes 能从经验中自动创建和改进技能（Skill），越用越聪明——这是 OpenClaw 没有的
- **回复更快**：Hermes 的对话循环优化更佳，响应速度比 OpenClaw 更快

不过，`Hermes` 同样是异步的：收到消息 → 处理 → 一段时间后返回回复。

文字聊天无所谓，但 `小智` 是实时语音交互，用户说完话，等几秒，体验就崩了。

所以需要一个中间层，把 `Hermes` 的异步回复桥接到小智的实时语音通道。

为此，和微信、飞书等通道一样，小智Pro 也实现了 Hermes 通道，你只需安装一个插件，即可实现`小智`和 `Hermes` 的实时双向通信。

Github地址：https://github.com/hougeai/xiaozhi-pro-hermes-plugin


## 2. 怎么工作的？

小智设备与 Hermes 通过 **WebSocket 长连接** 通信，由 Hermes 端的插件主动连接到小智Pro服务端：

```
小智设备 ────> 小智Pro服务端 <──(WebSocket)──> Hermes (xiaozhi-pro 插件主动连入)
                        │                      │
小智设备 <──── 小智Pro服务端 <──(WS 实时推送)────┘
```

![](https://i-blog.csdnimg.cn/img_convert/75e2afa78e811efe704afca86910ab46.jpeg)


核心设计：

| 特性 | 说明 |
|------|------|
| 实时通信 | WebSocket 全双工长连接，消息即时推送，无轮询延迟 |
| 无需公网 | Hermes 主动连接服务端，无需暴露端口 |
| 心跳保活 | 30 秒心跳检测，60 秒无响应自动断开 |
| 自动重连 | 指数退避重连（3s → 6s → 12s → ... → 60s 上限） |
| 消息去重 | 重复推送自动跳过，保证幂等 |
| 精确投递 | 支持指定设备投递或广播所有设备 |
| 自动踢旧 | 同一账号新连接自动踢掉旧连接 |


## 3. 怎么用？

### 3.1 太长不看版

让 Hermes 自己搞定插件安装和配置，把下面这段文字发给它：

> 请帮我安装并配置小智Pro Hermes插件，参考这个 GitHub 仓库的 README 操作：https://github.com/hougeai/xiaozhi-pro-hermes-plugin

### 3.2 手动操作版
> 控制台：[https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

**第一步：获取 API 密钥**

前往小智Pro控制台，进入 API 密钥页面，点击创建密钥。

> ⚠️ API 密钥是插件连接小智Pro的唯一凭证，请勿泄露。

**第二步：安装插件**

将插件下载到 Hermes 的平台插件目录（**目录名必须为 `xiaozhi_pro`，下划线，不能用连字符**）：

```bash
git clone https://github.com/hougeai/xiaozhi-pro-hermes-plugin.git ~/.hermes/hermes-agent/plugins/platforms/xiaozhi_pro
```

> ⚠️ 目录名必须是 `xiaozhi_pro`，否则 Hermes 无法加载。

**第三步：配置插件**

编辑 `~/.hermes/config.yaml`，添加：

```yaml
platforms:
  xiaozhi_pro:
    extra:
      token: "你的小智Pro平台API密钥"
```

- 本插件属于 bundled platform 插件，Hermes 会自动加载，**无需**在 `plugins.enabled` 中声明
- 只要配置了 `token`，网关启动时就会自动连接
- 也可以通过环境变量 `XIAOZHI_PRO_TOKEN` 设置 Token
- 要禁用连接，注释掉或删除 `token` 即可（同时确保 `XIAOZHI_PRO_TOKEN` 环境变量未设置）


**第四步：重启**

```bash
hermes gateway restart
```

插件会自动连接小智Pro 服务端，发送认证消息后进入双向通信。

**第五步：验证**

去小智Pro控制台，点击「Hermes插件版」页面的「检查连接」按钮，绿色"已连接"就是成功了。

![](https://i-blog.csdnimg.cn/img_convert/ef60b8765c33905912ad460936008e5e.png)


### 3.3 语音操控示例

配置好后，直接对小智说：

```
- '问问爱马仕现在都有哪些定时任务'
- '让爱马仕给我的飞书发一条消息'
- '让爱马仕立刻完成今天的AI资讯整理任务'
```

爱马仕回复后，服务端会自动推送到设备，设备随即播报回复内容。

![](https://i-blog.csdnimg.cn/img_convert/bfcc7c2e88695baf341cb967044030e3.png)


## 4. 常见问题

**连接状态显示"未连接"？**

- 确认插件已启用：`hermes plugins list` 查看 `platforms/xiaozhi_pro` 是否为 enabled
- 检查 `config.yaml` 中 token 是否配置正确
- 查看 Hermes 日志排查错误：`tail -f ~/.hermes/logs/gateway.log`

**启动报 "No adapter available for xiaozhi_pro"？**

- 确认插件目录名是 `xiaozhi_pro`（下划线，不是连字符）
- 确认 `config.yaml` 中 `plugins.enabled` 包含 `platforms/xiaozhi_pro`
- 确认 `config.yaml` 中 `platforms.xiaozhi_pro.enabled: true`
- 确认已安装 aiohttp 依赖：`pip install aiohttp`

**插件频繁断开？**

- 检查网络稳定性
- 确认服务器时间同步（NTP）
- 插件内置自动重连，短暂断开后会自动恢复

**设备没收到回复？**

- 确认设备已绑定到小智Pro账号
- 确认控制台显示"已连接"
- 如果设备正在说话，服务端会自动等待，消息最多缓存 1 天

## 写在最后

`Hermes` 会学习、会进化——你用得越多，它越懂你。现在，你可以用嘴指挥它。

`小智`给了 `Hermes` 一副耳朵，`Hermes` 还你一个越用越聪明的 AI 管家。

插件已开源，欢迎 Star：

https://github.com/hougeai/xiaozhi-pro-hermes-plugin

欢迎体验 `小智Pro` 更多功能，请戳👇：

> https://mkwyqebedx.sealosbja.site

注：`控制 Hermes`能力需设备端固件`v2.2.6.1`及以上版本。

固件已全面适配小智官方仓库收录的开发板型号，下载地址：

> https://github.com/hougeai/xiaozhiPro/releases

![](https://i-blog.csdnimg.cn/img_convert/86f0640f2f6036ee385f508cd1e7f6d1.png)


有任何问题，欢迎进群交流。
