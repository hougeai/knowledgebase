上篇文章，带大家动手实现了 MCP Client，将 MCP 协议接入 OpenAI 兼容的 API，给 LLM 接入丰富的外部能力。

[搞不懂 MCP？那就动手搓一个...]()

有朋友问：Client 和 LLM 到底什么关系？

来吧，一图胜千言：

![](https://i-blog.csdnimg.cn/img_convert/59d9a9dfd157987b12bcf35d9e8d819f.jpeg)

不过，上篇实操用 Python 实现，而 MCP sdk 本身是异步的，Python 基于 asyncio 异步编程，在处理事件循环时相对繁琐。

本文继续给出 `node.js` 版实现，并尝试回答：

- 接入 MCP server，对 LLM 回复延时，有多少影响？
- 如何本地部署一个 MCP server 并通过 url 提供服务？

两个版本的代码，放 GitHub了，有需要的朋友自取。
- [https://github.com/hougeai/mcp-client](https://github.com/hougeai/mcp-client)

## 1. 客户端实现

具体流程和上篇一致，4 步搞定。

**step 1**：定义 server 配置文件。

**step 2**：初始化客户端实例：包括 OpenAI 客户端、MCP 客户端列表、可用工具列表和工具映射。

```
class MCPClient {
  constructor(stream = false) {
    this.clients = [];
    this.availableTools = [];
    this.toolClientMap = {};
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
      baseURL: process.env.OPENAI_BASE_URL
    });
    this.model = process.env.MODEL_NAME;
    this.stream = stream;
    this.config = this.parseConfig(
      path.join(__dirname, '../mcp_server_config.json')
    );
  }
```
**step 3**：连接服务器：
- 3.1 连接不同类型的 server：对于含有 url 字段的，优先采用`StreamableHTTPClient`，否则向下兼容`SSEClient`。
- 3.2 获取server提供的工具列表，并将工具转换为 OpenAI tools 参数所需的格式。
- 3.3 将工具名称映射到执行该工具的 Client 实例，方便后续根据工具名称找到正确的 Client 实例进行调用。
```
async connectServer() {
    for (const [serverName, server] of Object.entries(this.config)) {
      const client = new Client({name: serverName, version: "0.1.0"});
      if (server.url) {
        // SSE连接
      } else {
        // Stdio连接
      }
      const response = await client.listTools();
      this.clients.push(client);
      this.availableTools.push(tools);
    }
    // 构建tool到client的映射
    this.clients.forEach((client, idx) => {
      this.availableTools[idx].forEach(tool => {
        this.toolClientMap[tool.function.name] = client;
      });
    });
    console.log("Connected to all servers");
  }
```
**step 4**：工具调用和响应处理

```
async processQuery(query) {
    // 创建消息列表
    const messages = [{role: "user", content: query}];
    while (true) {
      const {tool_functions, response} = await this.getResponse(messages);
      messages.push(...response);
      if (!tool_functions || tool_functions.length === 0) {
        break;
      }
      for (const tool_call of tool_functions) {
        const tool_call_id = tool_call.id;
        const tool_name = tool_call.function.name;
        let tool_args = {};
        
        try {
          tool_args = JSON.parse(tool_call.function.arguments);
        } catch (e) {
          console.error("Failed to parse tool arguments:", e);
        }
        console.log("Tool call:", tool_name, "Tool args:", tool_args);
        const client = this.toolClientMap[tool_name];
        const result = await client.callTool({name: tool_name, arguments: tool_args});
        
        messages.push({
          role: "tool",
          tool_call_id,
          content: JSON.stringify({
            result: result.content.map(c => c.text),
            meta: String(result.meta),
            isError: String(result.isError)
          })
        });
      }
    }
    return messages;
  }
```

问题来了：

接入了 MCP server，对 LLM 答复的延时，有多少影响？

**实测发现，这部分的延时增加非常显著，主要包括两部分**：

- MCP server 处理工具调用本身的延时；
- LLM 需判断是否要工具调用，带来的延时。

## 2. 服务端部署方式对比

### 2.1 MCP server 延时实测

不同类型服务端，延时差异较大，下面我们以地图服务为例：
- 高德地图 MCP server
- 百度地图 MCP server

#### 2.1.1 测试高德地图

**最简单**的方式，直接采用 ModelScope 上部署的服务。

填入你在高德地图申请的 API KEY:

![](https://i-blog.csdnimg.cn/img_convert/1f244bf7fd068632404821739ef84dde.jpeg)

server 就给你准备好了：

![](https://i-blog.csdnimg.cn/img_convert/5a83cdfa4cb765ef019fdff769f7af8c.jpeg)

但是简单的代价，就是延时非常高，**近 4s**：
```
2025-05-27T01:41:22.664Z Calling tool: maps_weather
2025-05-27T01:41:26.305Z Got tool result: {
```

如果对延迟要求不高，那就尽情薅阿里的服务器资源吧。

当然，要想自主可控，还是用高德提供的 npm 包，本地起一个服务：
> [https://www.npmjs.com/package/@amap/amap-maps-mcp-server](https://www.npmjs.com/package/@amap/amap-maps-mcp-server)

![](https://i-blog.csdnimg.cn/img_convert/e719a9b73e37e573555501d27fb3ca11.png)

如果报错提示找不到 npx，是因为 server 子进程找不到 node 安装包，可以参考如下，指定 `command` 和 `PATH`：

```
"amap-maps": {
    "command": "/root/tools/node-v22.14.0-linux-x64/bin/npx",
    "args": [
        "-y",
        "@amap/amap-maps-mcp-server"
    ],
    "env": {
        "AMAP_MAPS_API_KEY": "xxx",
        "PATH": "/root/tools/node-v22.14.0-linux-x64/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    }
}
```

本地服务起来后，你看只需 **0.5s**：

```
2025-05-27T01:40:20.785Z Calling tool: maps_weather
2025-05-27T01:40:21.226Z Got tool result: {
```


#### 2.1.2 测试百度地图
> [https://github.com/baidu-maps/mcp](https://github.com/baidu-maps/mcp)


同样，采用 ModelScope 上部署的服务，需要 **2s**：
```
2025-05-27T01:36:19.070Z Calling tool: map_weather
2025-05-27T01:36:21.201Z Got tool result: {
```

而本地服务，只要 **0.3s**：
```
2025-05-27T01:38:35.188Z Calling tool: map_weather
2025-05-27T01:38:35.455Z Got tool result: {
```

### 2.2 stdio VS SSE

上述对比，你会发现：
- StreamHTTP/SSE 通过 url 连接，更简洁且方便管理
- stdio 服务就在本地，延时更低

如果一个 server 需要服务多个 client，显然第一种方式更合理。


问题来了：如何本地部署一个 MCP server 并通过 url 来提供服务？


### 2.3 使用 MCP 代理
> [https://github.com/sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)

这个项目为 StreamHTTP/SSE 和 stdio 的 MCP 传输之间搭建了一座桥梁。

安装也非常简单，比如采用 uv 管理工具，只需一行命令：

```
uv tool install mcp-proxy
```

然后，把`本地的百度地图Server`切换成`StreamHTTP/SSE`，只需两行命令：

```
export PATH="/root/.local/bin:$PATH"
mcp-proxy --port=9000 -e BAIDU_MAP_API_KEY xxx -- npx -y @baidumap/mcp-server-baidu-map
```

你看启动后的日志，就是用 uvicorn 搭了一座桥：

```
INFO:     Started server process [239341]
INFO:     Waiting for application startup.
[I 2025-05-27 11:09:03,610.610 mcp.server.streamable_http_manager] StreamableHTTP session manager started
[I 2025-05-27 11:09:03,610.610 mcp_proxy.mcp_server] Application started with StreamableHTTP session manager!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9000 (Press CTRL+C to quit)
```

服务启动后，只需修改 server 配置为：

```
"baidu-map": {
        "url": "http://127.0.0.1:9000/sse"
    },
```

实测本地服务 + mcp-proxy，仅 **0.2s**，Nice！
```
2025-05-27T03:10:43.145Z Calling tool: map_weather
2025-05-27T03:10:43.348Z Got tool result: {
```


### 2.4 结果展示

> 注：以下测试 LLM 为阿里云的`qwen-plus`。

```
北京明后两天天气怎么样
```

可以看到模型调用了 `map_weather` 工具，最终回复如下：

```
2025-05-27T03:23:34.074Z Calling tool: map_weather
2025-05-27T03:23:43.485Z llm: 北京明后两天的天气预报如下：
5月28日，星期三，晴朗，最高温度为33度，最低温度为19度，白天和夜晚的风向都是南风和西南风，风力小于3级。
5月29日，星期四，晴朗，最高温度为34度，最低温度为20度，白天和夜晚的风向均为南风，风力小于3级。 
请记得根据天气情况调整穿着和出行计划！
```

继续测试：

```
故宫附近有哪些美食推荐
```


可以看到调用了 `map_search_places` 工具，最终回复如下：
```
2025-05-27T03:24:46.005Z Calling tool: map_search_places
2025-05-27T03:25:09.826Z llm: 在北京故宫附近，我为您找到了一些美食推荐：
1. 老北京炸酱面老店(南长街店)：位于南长街乙30号。
2. 故宫冰窖餐厅：位于北长街故宫博物院慈宁宫南侧。
3. 故宫快餐：位于南长街护照签售处旁。
4. 泽园酒家(南长街店)：位于南长街20号(近中山公园西门)。
5. 崂山渔家(西单店)：位于北新华街29号昌盛大厦1层1010室。
6. 川湘家常菜(西单店)：位于大六部口胡同13号(音乐厅西侧)。
```

连环问：

```
北京今天天气怎么样，故宫附近有哪些美食推荐
```

可以看到模型分别调用了`map_weather` 和 `map_search_places` 工具：

```
2025-05-27T06:03:36.831Z llm: start
2025-05-27T06:03:39.432Z Calling tool: map_weather
2025-05-27T06:03:39.516Z Got tool result
2025-05-27T06:03:42.406Z Calling tool: map_search_places
2025-05-27T06:03:42.641Z Got tool result
```

过程中的所有 message 包括：

```
{ role: 'user', content: '北京今天天气怎么样，故宫附近有哪些美食推荐' },
{ role: 'assistant', content: null, tool_calls: [ [Object] ] },
{ role: 'tool', tool_call_id: 'call_db20e6291ec044daa38876',content: '{"result":["Weather searth failed: 查询的经纬度值范围无效"],"meta":"undefined","isError":"true"}'},
{ role: 'assistant', content: null, tool_calls: [ [Object] ]},
{ role: 'tool', tool_call_id: 'call_c66fde200d8949d1b5d5b5', content: }
```
## 3. LLM 延时实测

看到这里，还会遇到一个问题：MCP server 返回的结果很长，导致用户拿到结果的延时太长！

你看，上面这个案例，从提问到模型回答，足足有**近 30s**：
```
2025-05-27T03:24:40.214Z llm: start
2025-05-27T03:25:09.826Z llm: 在北京故宫附近，我为您找到了一些美食推荐：
```

所以，**流式输出**，对于实时对话应用至关重要。

还是上面那个例子，改为`流式输出`，首句延时**从 30s 降到 5s 左右**：

```
Connected to all servers
2025-05-27T06:43:32.327Z llm: start stream
2025-05-27T06:43:36.027Z Calling tool (stream): map_weather { location: '116.307526,40.056945', districtId: '110108' }
2025-05-27T06:43:36.113Z Got tool result (stream)
2025-05-27T06:43:37.526Z llm: 今天是2025年5月27日星期二，
2025-05-27T06:43:39.443Z llm: 北京海淀的天气情况如下：当前天气：晴当前温度：31度体感温度：32度相对湿度：30%风力等级：2级风向：西南风今天白天天气预计为多云，
2025-05-27T06:43:39.780Z llm: 夜晚也将是多云。
2025-05-27T06:43:40.950Z llm: 风向为西南风，
2025-05-27T06:43:41.512Z llm: 请注意适时增减衣物，
2025-05-27T06:43:41.666Z llm: end
```

如果**不进行任何工具调用**呢？

首句延时需要 **0.9-1.5s**：

```
Connected to all servers
2025-05-27T06:48:22.071Z llm: start stream
2025-05-27T06:48:23.346Z llm: 你好，
```

如果**不加入任何 MCP Server**呢？

首句延时 **0.5s**： 
```
2025-05-27T06:51:33.457Z llm: start stream
2025-05-27T06:51:33.990Z llm: 你好，
```

显然，接入 MCP Server，LLM 需要要判断是否要进行工具调用，大大增加了延时。


## 写在最后

本文分享了 `MCPClient` 的 `nodejs` 实现，并实测对比了不同服务端部署带来的延时。

如果对你有帮助，欢迎**点赞收藏**备用。

完整代码见：[https://github.com/hougeai/mcp-client](https://github.com/hougeai/mcp-client)
