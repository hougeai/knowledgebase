从某个版本开始，小智 AI 可以语音控制 IoT 设备了。

有朋友问：怎么做到的？

交互逻辑，是这样的：

![](https://i-blog.csdnimg.cn/img_convert/2b0a24d882deb680fcee8677a2d9ca65.png)


客户端和服务端，会话通道开启后，客户端会主动上报`IoT设备描述`和当前`IoT设备状态`，比如：

```
# Sending IoT descriptors
[{"name":"AudioSpeaker","description":"The audio speaker of the device","properties":{"volume":{"description":"Current audio volume value","type":"number"}},"methods":{"set_volume":{"description":"Set the audio volume","parameters":{"volume":{"description":"An integer between 0 and 100","type":"number"}}}}},{"name":"Lamp","description":"A test lamp","properties":{"power":{"description":"Whether the lamp is on","type":"boolean"}},"methods":{"turn_on":{"description":"Turn on the lamp","parameters":{}},"turn_off":{"description":"Turn off the lamp","parameters":{}}}}]
# Sending IoT states
{"session_id":"14c23594","type":"iot","update":true,"states":[{"name":"AudioSpeaker","state":{"volume":50}}]}
```

当用户要求操控 IoT 设备时，比如：

```
把音量调大一点
把灯打开
```

服务端做出决策，给客户端发送`IoT控制指令`，比如：

```
[{"name":"AudioSpeaker","method":"set_volume","parameters":{"volume":70}}]
[{"name":"Lamp","method":"turn_on","parameters":{}}]
```

**问题来了**：`服务端`是如何处理这些信息，并成功向客户端发送指令的？

本文分享，**笔者尝试过的两种方案**，给出优劣分析，欢迎评论区大佬指教。

## 1. 双 LLM 方案

服务端负责对话的 LLM 需要流式输出，无法承担`输出精准控制指令`的重任。


因此，可以考虑把任务解耦，定义两个 LLM Client，分别负责对话和生成操控 IoT 设备的指令：

```
# 负责对话的智能体
this.clientChat = new ClientOpenAI(url, key, model, this.roleDesc);
# 负责生成操控 IoT 指令的智能体
this.clientIot = new ClientOpenAI(url, key, model, config.sys_iot);
```

在`clientChat`生成对话内容的同时，`clientIot`判断是否需要生成指令，如果需要则生成固定格式的指令，发送给客户端。

**优点：**
- 这两个 LLM 是异步的，并不会增加`clientChat`的对话延时。

**缺点：**
- 每轮对话，都要两个 LLM 处理，**消耗的 token 数倍增**，其实大部分对话，压根不需要`clientIot`。
- 两个 LLM 之间相互无感知，`clientChat`的答复和`clientIot`的指令，存在信息不同步的可能。
- 对 LLM 依赖性较高，如果指令遵循不行，能吐出`可成功解析的 command`，就成了一种奢望。

可以说，这种方案弊大于利。

## 2. LLM + MCP 方案

前段时间，研究了下 MCP：
- [搞不懂 MCP？那就动手搓一个...](https://zhuanlan.zhihu.com/p/1912823317011888104)
- [搞不懂 MCP？那就动手搓一个...（续）](https://zhuanlan.zhihu.com/p/1913913519545489400)

**如果把控制 IoT 设备的任务，交给 MCP server**，岂不是很优雅？

**为什么这么讲？**

将设备操作封装成 LLM 可调用的工具（Tools），比单纯依赖提示词来生成指令，靠谱多了。

确定了思路，该怎么设计 Server 呢？

让每个设备的 method 都对应一个 tool？

对于 IoT 设备固定的场景来说，这样设计没问题。

唯一的缺点是可扩展性差，每次新增设备方法，都要更新 MCP Server。

假设客户端发来的 IoT 设备千千万，Server 将会变得非常复杂，甚至不可用。

为此，可以考虑定义一个通用的 tool：`call_device_method`，它接收的参数包括：

```
const callDeviceMethodSchema = {
  device_name: z.string().describe("The name of the device to interact with (e.g., 'AudioSpeaker', 'Lamp')."),
  method_name: z.string().describe("The name of the method to call on the device (e.g., 'set_volume', 'turn_on')."),
  method_parameters: z.record(z.any()).optional().describe("An object containing the parameters for the method. Refer to the device's method descriptions for required parameters.")
};
```

在 `clientChat` 的提示词中给定`设备描述`和`设备状态`。这样，LLM 在理解用户意图后，只需调用 `call_device_method`，传入三个参数，即可完成工具调用。

我们看下调用效果：

![](https://i-blog.csdnimg.cn/img_convert/323b530eac1f6b3596e6a1480cb41467.png)


**优点：**
- 对话生成和指令生成在同一个 LLM 中搞定，不存在`说的和做的`不一致的情况。
- 一次对话只需一个 LLM，相比双 LLM 的方案，token 整体消耗更少。

**缺点：**
- 加入了 MCP server，`clientChat` 的延时有所增加。

确定好服务端的交互逻辑，只需客户端上报标准化的`IoT设备描述`和`IoT设备状态`，就可以以不变应万变。

接下来，**继续优化 LLM 首句延时**吧。

## 写在最后


本文分享了 `小智 AI 控制 IoT 设备` 的两种方案，并给出优劣分析，欢迎评论区大佬指教。

如果对你有帮助，欢迎**点赞收藏**备用。


