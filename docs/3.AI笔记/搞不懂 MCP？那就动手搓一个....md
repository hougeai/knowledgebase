MCP 火了有一阵了，市面上相关教程也不少，无奈看完，依旧一头雾水。

原因无他，没动手而已。

这两天实操了一把，发现 MCP 确实以一种更优雅的方式，帮我解决了之前难以搞定的问题。

今天从实战出发，和大家聊聊：**如何把 MCP 接入自己的 LLM**，希望给有需要的朋友，一点点参考。

**本文将首先回答：**
- 万能的 LLM 为啥干啥啥不行？ 
- Function Call 是怎么诞生的？
- MCP 解决了 Function Call 的什么痛点？


**然后，以实操的方式回答：**
- MCP Server 有哪些实现方式？
- MCP Client 和 Server 是如何通信的？
- 如何把 MCP 接入 LLM？


## 1. LLM 的局限性

各大厂商竞相发布 LLM，即便 benchmark 指标刷上天，拉到现实场景中，依然解决不了各种问题。

因为大模型训练完，它的信息量就不再更新。

比如用户要查个天气，就必须借助高德/百度地图等外部 API 来获取最新数据。

笔者在微信 AI 机器人的实现中，就是首先让 LLM 识别用户意图，然后再调用外部 API，获取相关消息后，进行回答：

![](https://i-blog.csdnimg.cn/img_convert/f71369d583ef7286ee0d2b731f09104f.png)

为了实现各种功能，必须在提示词中写明所有意图标签，然后逐一开发对应功能：

![](https://i-blog.csdnimg.cn/img_convert/3815e8a2c2f53d1a6b801efe6e2b3d86.png)

实际你会发现，即便非常明确告诉它这些意图，`意图识别`也不是 100% 正确。

当然，解决上述问题的另外一个思路是：`Function call`，这也是聊 MCP 之前，绕不开的话题。


## 2. Function call 的局限性
`Function call`（下文简称 FC） 早在 2023 年，就由 OpenAI 提出，主要就是为了解决上述 LLM 的局限性。

你在 Coze/Dify 等智能体平台上，看到的各种插件，本质就是基于 FC 实现的。

**但 FC 的缺点也很明显**：必须要 LLM 本身支持，然后在 OpenAI 的接口中传入 `tools` 参数：

![](https://i-blog.csdnimg.cn/img_convert/4a95056642b17c2d40df2d9cda537f86.png)


但是不同 LLM 训练时，因为各种实现方式不一样，导致输入/输出结构、触发结构都不一样。

所以，换个 LLM 就得适配上面的 `tools`，实在是太难受。

只是 Coze/Dify 等平台，做了大量适配工作，才让你感到`用起来很爽`。

但是，即便是生态丰富的 Coze，也不是万能的，总有一些个性化需求，平台是满足不了的。

还是绕不开要定制化开发，然后面临这个头疼的问题：**一顿操作写了个接口，换个 LLM 居然理解不了。**

所以，MCP，它来了！

## 3. MCP 是啥

MCP 全称 Model Context Protocol，模型上下文协议。

就像 Type-C 为设备连接各种外设提供了标准化方式，MCP 为 LLM 连接各种工具提供了统一方式。

### 3.1 整体架构

Anthropic 公司最早提出 MCP 时的一张图，非常形象刻画出了它的整体架构：

![](https://i-blog.csdnimg.cn/img_convert/a9c328d3744d73325a4b51e6667ce982.jpeg)

图中有几个关键概念：
- **MCP hosts**：应用程序，比如各种 AI 工具或 IDE，最新版 Trae 就已接入
- **MCP clients**：客户端组件，和服务端维持连接
- **MCP server**：服务端，通过 MCP 协议提供各种功能
- **Local data**：本地资源，比如本地文件、数据库等
- **Remote services**：远程服务，通过网络访问

抛开这些概念不谈，MCP 和 `Function call` 在应用层面有什么区别？

没区别，还是上面这张图，只是其中的 `tools` 交给 **MCP client** 来托管：

![](https://i-blog.csdnimg.cn/img_convert/4a95056642b17c2d40df2d9cda537f86.png)

下面，我们动手实操一番，相信你就能完全掌握 MCP 了。

### 3.2 MCP 服务端

服务端有两种：
- 一是有很多别人实现好了的 server，完全能够满足你的需求，拿来即用；
- 二是需要自己开发的 server；

**如何接入别人的 server？**

目前各大模型厂商都在拥抱 MCP 生态，比如：
- 阿里云 ModelScope：https://modelscope.cn/mcp：


![](https://i-blog.csdnimg.cn/img_convert/2c8dccc396c9e49bbb292704405291ab.jpeg)

- mcp.so：https://mcp.so/zh，也是一个聚合平台，收集了优秀的 MCP 服务器 和客户端。

![](https://i-blog.csdnimg.cn/img_convert/bf95cc48ff4126db11d2c2ad4e7902e5.png)

以高德地图提供的 MCP 为例：

![](https://i-blog.csdnimg.cn/img_convert/838dcab13d439a3cb8b091459dada4d1.png)

这里就需要有本地安装好 node 环境，本质上就是通过如下命令，启动了 server 服务：


```
npx -y @amap/amap-maps-mcp-server
```

当然，也有通过云端服务提供的 server，比如这个 12306 的 MCP：

![](https://i-blog.csdnimg.cn/img_convert/bde50adbe771fda5f120d72ef12d1a75.jpeg)

**如何自己开发 server？**

基于 FastMCP 框架，和 FastAPI 的用法非常类似。

假设我们要开发一个计算器，只需三步：

首先，创建一个名为 `Calculator` 的服务：

```
mcp = FastMCP("Calculator")
```

然后，添加一个 `tool`，实现具体功能：

```
def calculator(python_expression: str) -> dict:
    """For mathamatical calculation, always use this tool to calculate the result of a python expression. `math` and `random` are available."""
    result = eval(python_expression)
    return {"success": True, "result": result}
```

最后，启动服务：

```
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 3.3 MCP 客户端
> 参考：[https://modelcontextprotocol.io/quickstart/client](https://modelcontextprotocol.io/quickstart/client)

有了 Server，问题来了：**我如何把它们接入自己的 LLM 使用？**

答案是：还需要一个 client，负责以 **MCP 协议**，和所有的 server 进行通信！

**MCP 协议** 又怎么理解？

MCP 包括两种标准传输协议：
- `标准输入/输出（stdio）`：通过标准输入和输出流进行通信。这对于本地集成和命令行工具特别有用。
- `服务器发送事件（SSE）`：通过HTTP POST请求进行客户端到服务器的通信。

为了方便开发，官方开源了不同语言的 sdk：
- [https://github.com/modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk )
- [https://github.com/modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk)

不过从 v1.8.0 版本开始，“Streamable HTTP” 取代了 “SSE” 协议，优势体现在：
- 灵活性和标准化：用标准的 HTTP POST 和 GET 请求进行通信。
- 会话管理：服务端为每个客户端分配一个会话ID，方便处理多个客户端连接。

由于之前的服务都是基于 SSE，所以对 SSE 的支持并没有移除。

下文以 Python 为例展开。

### 3.4 MCPClient开发

之前，我们接入 LLM 采用的都是 OpenAI 的接口：

```
self.openai = OpenAI(api_key=xxx, base_url=xxx)
response = self.openai.chat.completions.create(
            model=self.model,
            messages=messages
        )
```

现在要为它接入各种 MCP Server，为此需要封装一个 `MCPClient`。

具体流程如下：

**step 1**：定义 server 配置文件，格式如下：

```
{
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "/root/projects/"
            ]
        },
        "calculator": {
            "command": "python",
            "args": [
                "calculator.py"
            ]
        },
        "time": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "mcp/time"
            ]
        },
        "amap-maps": {
            "url": "https://mcp.api-inference.modelscope.cn/sse/xxx"
        }
    }
}
```

**step 2**：初始化客户端实例：

```
class MCPClient:
    def __init__(self):
        # 初始化会话和客户端对象
        self.session_list: List[ClientSession] = []
        self.available_tools: List = []
        self.tool_session_map: Dict = {}
        self.exit_stack = AsyncExitStack() # 退出堆栈
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL")) 
        self.model = "qwen-plus"
        self.mcp_server_config = self.parse_mcp_server("./mcp_server_config.json")
```

**step 3**：连接服务器：根据不同协议，分别连接到 stdio 和 sse 服务器：

```
async def connect_server(self):
        for sever_name in self.mcp_server_config:
            server = self.mcp_server_config[sever_name]
            if server.get('url'):
                session, tools = await self.connect_sse_server(sever_name)
            else:
                session, tools = await self.connect_stdio_server(sever_name)
            self.session_list.append(session)
            self.available_tools.append(tools)
        # 构建 tool name 到 session 的映射
        self.tool_session_map = {
            tool['function']['name']: session for session, tools in zip(self.session_list, self.available_tools) for tool in tools
        }
```

**step 4**：获取可用工具列表：以 stdio 服务为例：

```
async def connect_stdio_server(self, server_name: str):
        """连接到 stdio MCP 服务器"""
        server = self.mcp_server_config[server_name]
        # 创建 StdioServerParameters 对象
        server_params = StdioServerParameters(
            command=server['command'],
            args=server['args'],
            env=None
        )
        # 使用 stdio_client 创建与服务器的 stdio 传输
        read, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        # 创建 ClientSession 对象，用于与服务器通信
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        # 初始化会话
        await session.initialize()
        # 列出可用工具
        response = await session.list_tools()
        tools = self.get_tools(response)
        return session, tools
```



**step 5**：工具调用和响应处理

```
async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        while True:
            tool_functions, response = self.get_response(messages)
            messages.extend(response)
            if not tool_functions:
                break
            for tool_functions in tool_functions:
                tool_call_id = tool_functions['id']
                tool_name = tool_functions['function']['name']
                tool_args = json.loads(tool_functions['function']['arguments'])
                session = self.tool_session_map[tool_name]
                result = await session.call_tool(tool_name, tool_args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": json.dumps({
                        "result": [content.text for content in result.content],
                        "meta": str(result.meta),
                        "isError": str(result.isError)
                    })
                })
        return messages
```

**篇幅受限，这里只贴核心步骤的代码，需要完整代码的朋友，文末自取！**

### 3.5 结果展示

问它当前时间：

```
messages = await client.process_query("现在北京时间几点")
```

输出结果如下：

```
{'role': 'user', 'content': '现在北京时间几点'}
{'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'call_ffb7460aa192417cb0218e', 'type': 'function', 'function': {'name': 'get_current_time', 'arguments': '{"timezone": "Asia/Shanghai"}'}}]}
{'role': 'tool', 'tool_call_id': 'call_ffb7460aa192417cb0218e', 'content': '{"result": ["{\\n  \\"timezone\\": \\"Asia/Shanghai\\",\\n  \\"datetime\\": \\"2025-05-25T16:04:43+08:00\\",\\n  \\"is_dst\\": false\\n}"], "meta": "None", "isError": "False"}'}
{'role': 'assistant', 'content': '现在北京时间是2025年5月25日下午15点49分37秒。请注意，这个时间是基于标准时间，不适用夏令时。'}
```

可以看到，成功调用了 `time` 服务中的工具。

再来个双重调用的任务：

```
messages = await client.process_query("现在北京时间几点，天气怎么样")
```

输出结果如下：


```
{'role': 'user', 'content': '现在北京时间几点，天气怎么样'}
{'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'call_18d31b5557e749fbb40b6f', 'type': 'function', 'function': {'name': 'get_current_time', 'arguments': '{"timezone": "Asia/Shanghai"}'}}]}
{'role': 'tool', 'tool_call_id': 'call_18d31b5557e749fbb40b6f', 'content': '{"result": ["{\\n  \\"timezone\\": \\"Asia/Shanghai\\",\\n  \\"datetime\\": \\"2025-05-25T16:06:17+08:00\\",\\n  \\"is_dst\\": false\\n}"], "meta": "None", "isError": "False"}'}
{'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'call_64410ee2fe104b1b943037', 'type': 'function', 'function': {'name': 'maps_weather', 'arguments': '{"city": "北京"}'}}]}
{'role': 'tool', 'tool_call_id': 'call_64410ee2fe104b1b943037', 'content': '{"result": ["{\\n  \\"city\\": \\n}"], "meta": "None", "isError": "False"}'}
{'role': 'assistant', 'content': '现在北京时间是2025年5月25日16点06分17秒。\n\n北京今天的天气情况如下：\n- 白天天气：多云\n- 晚上天气：多云\n- 白天最高温度：28°C\n- 晚上最低温度：15°C\n- 白天风向：东\n- 晚上风向：东\n- 白天风力：1-3级\n- 晚上风力：1-3级\n\n这是未来几天的天气预报：\n- 2025年5月26日：白天和晚上都是多云，温度在17°C到29°C之间。\n- 2025年5月27日：白天和晚上都是阴，温度在20°C到31°C之间。\n- 2025年5月28日：白天多云，晚上阴，温度在20°C到31°C之间。'}
```

可以发现，成功调用了`time`服务和`高德地图`服务。

最后，测试下`本地搭建的数学计算服务`：

```
messages = await client.process_query("半径是8，计算圆的面积")
```

输出结果如下：

```
{'role': 'user', 'content': '半径是8，计算圆的面积'}
{'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'call_c247e31e964344c9922c3d', 'type': 'function', 'function': {'name': 'calculator', 'arguments': '{"python_expression": "math.pi * 8**2"}'}}]}
{'role': 'tool', 'tool_call_id': 'call_c247e31e964344c9922c3d', 'content': '{"result": ["{\\n  \\"success\\": true,\\n  \\"result\\": 201.06192982974676\\n}"], "meta": "None", "isError": "False"}'}
{'role': 'assistant', 'content': '圆的面积为 \\(201.06\\) 平方单位（结果四舍五入到小数点后两位）。'}
```

## 写在最后

本文分享了扩展 LLM 能力边界的框架：`MCP`，并通过实操 MCPClient，了解了其基本原理。

如果对你有帮助，欢迎**点赞收藏**备用。

完整代码，公众号后台回复 `MCP` 自取。


