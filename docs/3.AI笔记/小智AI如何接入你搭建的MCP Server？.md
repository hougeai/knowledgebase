前面，用两篇文章，分享了 MCP 的基本概念，并动手搓了一个 `MCPClient`：
- [搞不懂 MCP？那就动手搓一个...](https://zhuanlan.zhihu.com/p/1912823317011888104)
- [搞不懂 MCP？那就动手搓一个...（续）](https://zhuanlan.zhihu.com/p/1913913519545489400)

基于 `MCP` 的核心优势，我们实现了`小智AI控制IoT设备`的 `LLM+MCP` 方案：

- [小智AI如何控制IoT设备？LLM vs MCP](https://zhuanlan.zhihu.com/p/1914637833488017038)

看到这里，你会发现，MCP 可做的太多了，足以补齐 `LLM` 的短板。

目前，小智后台也支持接入`个人搭建的 MCP Server`，可玩性非常高。

![](https://i-blog.csdnimg.cn/img_convert/279787f3ff6a2f979964d08cec413f15.png)


**有朋友好奇：怎么做到的？**

本文，将拆解`小智 AI 自定义 MCP 接入`背后的原理，并给出一种实现方案。

欢迎评论区大佬指教。

## 1. 技术方案

前两篇，和大家介绍了 MCP 支持的两种协议：stdio 和 sse。其中：
- StreamHTTP/SSE 通过 url 连接，更简洁且方便管理。
- stdio 服务就在本地，延时更低。

如果一个 server 需要服务多个 client，则 SSE 更合理。

为此，可以用 `mcp-proxy` 把本地的 stdio 服务转成成 sse 服务，通过 url 对外提供服务。

问题来了：总不能让用户自建的 `mcp-server`，搞一个公网可访问的 url，供官方服务器访问吧？

怎么解决：**用 websocket 做桥梁**：
- **客户端**：用户把本地的 stdio 服务，通过 websocket 转发，连接到服务端的 ws server 上；
- **服务端**：管理来自用户的 websocket 连接，转发请求，接收客户端的调用结果。

画张图，给出二者之间的关系：

![](https://i-blog.csdnimg.cn/img_convert/0ebd812e425f37fe3b922cf9b919740a.png)

## 2. 客户端实现
> 参考：[https://github.com/78/mcp-calculator](https://github.com/78/mcp-calculator)

小智给出了示例代码🤟，主要包括两部分：
- MCP server 实现：`calculator.py` 定义了一个数学计算工具。当然你完全可以发挥想象力，定义一切你要用到的工具。
- websocket 客户端：`mcp_pipe.py` 连接到服务端，负责将上面定义的工具，和服务端的 LLM 进行通信。

成功连接到服务端后，启动三个任务：

```
# 使用 asyncio.gather 并发运行三个任务
await asyncio.gather(
    pipe_websocket_to_process(websocket, process), # 从 WebSocket 读取消息并写入子进程的标准输入。
    pipe_process_to_websocket(process, websocket), # 从子进程的标准输出读取消息并写入 WebSocket。
    pipe_process_stderr_to_terminal(process) # 从子进程的标准错误输出读取消息并打印到终端。
)
```

这里不再赘述，下面我们来搞定服务端的实现逻辑。


## 3. 服务端实现

### 3.1 接收客户端连接

服务端首先需要识别：接过来的客户端，到底是哪个 `用户or设备` 的，否则全部接受，岂不乱套了。

怎么识别?

藏在服务端提供的 `MCP 接入点`里，小智应该是用的 JWT token，本质还是为了找到对应的`用户or设备`，来判断是否放行。

下面我们以`设备ID`为例，给出示例代码：
- 获取 url 携带的参数，匹配到`设备ID`
- 建立 `McpSession`，和 `设备ID` 一一对应；
- 保存到`sessionManager`中，对`McpSession`统一管理；
```
// 监听客户端连接事件
wss.on('connection', (ws, req) => {
  const requestUrl = new URL(req.url, `ws://${req.headers.host}`); // 解析请求 URL
  const path = requestUrl.pathname;
  if (path === '/mcp') {
    const deviceId = requestUrl.searchParams.get('deviceId'); // 从查询参数获取 deviceId
    const session = new McpSession(ws, deviceId);
    sessionManager.add(session);
  }
```

### 3.2 信息交互逻辑
> 这部分坑有点多，笔者也是查看 MCP SDK 中的 ClientSession，才搞定。

`mcp_pipe.py` 作为 MCP 协议客户端，它要遵循严格的初始化握手流程：

- 它不会主动发消息给 WS 服务端。

- 它需要**两步初始化**，才能完成握手：

  - 收到你的 "method": "initialize" 请求，返回一个结果；

  - 然后还必须发送 "method": "notifications/initialized" 通知

否则它认为初始化未完成，导致你的 "tools/list" 和 "tools/call" 请求全部被拒绝：

```
RuntimeError: Received request before initialization was complete
```

所以，正确的初始化逻辑是：

```
const ini = {
  jsonrpc: "2.0",
  id: 1,
  method: "initialize",
  params: {
    protocolVersion: "0.1.0",
    capabilities: {
      sampling: {},
      roots: { listChanged: true }
    },
    clientInfo: { name: "espbot-server", version: "0.1.0" }
  }
};
ws.send(JSON.stringify(ini));

ws.on('message', (msgBuf) => {
  const msg = JSON.parse(msgBuf.toString());
  // 初始化响应处理
  if (msg.result?.protocolVersion) {
    // 必须发送 initialized 通知
    ws.send(JSON.stringify({
      jsonrpc: "2.0",
      method: "notifications/initialized"
    }));
    // 然后再发送其他请求
  }
});
```

`id` 是干嘛的？必填么？

它是 JSON-RPC 协议里用来匹配请求和响应的字段：

- 当你发一个请求：

```
{ "jsonrpc": "2.0", "id": 42, "method": "tools/list" }
```

- 对方返回响应时：


```
{ "jsonrpc": "2.0", "id": 42, "result": { ... } }
```

客户端日志如下：

![](https://i-blog.csdnimg.cn/img_convert/ac65cfcf676ac0d4cb33548fe737d3c2.png)

服务端接收到的消息如下：

```
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-03-26","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"Calculator","version":"1.9.1"}}}

{"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"calculator","description":"For mathamatical calculation, always use this tool to calculate the result of a python expression. `math` and `random` are available.","inputSchema":{"properties":{"python_expression":{"title":"Python Expression","type":"string"}},"required":["python_expression"],"title":"calculatorArguments","type":"object"}}]}}

{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"{\n  \"success\": true,\n  \"result\": 7\n}"}],"isError":false}}
```

所以，`id` 必填，可以在程序中自增。

### 3.3  LLM 中调用

首先在`connectServer()`时，除了连接`通用的 server`（比如：IoT设备管理），还要接入`自定义的 server`（由上面`sessionManager`管理）：

```
// 新增custom mcp
this.custom_mcp = sessionManager.get(this.deviceId)
if (!(this.custom_mcp.session && this.custom_mcp.alive && this.custom_mcp.isInitialized)) {
  this.custom_mcp = null
}
if (this.custom_mcp) {
  this.clients.push(this.custom_mcp);
  const response = await this.custom_mcp.listTools();
  const tools = response.tools.map(tool => ({
    type: "function",
    function: {
      name: tool.name,
      description: tool.description,
      parameters: tool.inputSchema
    }
  }));
  this.availableTools.push(tools);
  console.log(new Date(), "Connected to custom mcp server");
}
```

接入后，在处理工具调用`handleToolCalls`时，是一样的：

```
const result = await client.callTool({name: tool_name, arguments: tool_args});
```

最后，看下调用日志：


![](https://i-blog.csdnimg.cn/img_convert/9a34886a3834922a001af651163afc50.png)

![](https://i-blog.csdnimg.cn/img_convert/236146fa03390bd7f6f831bf3c3141b4.png)


## 写在最后

本文分享了 `小智 AI 接入自定义的 MCP Server` 的实现方案。

如果对你有帮助，欢迎**点赞收藏**备用。

---

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

