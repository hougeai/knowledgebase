
小智火了！背后的大语言模型 LLM 功不可没。

LLM 虽强，但有一个致命软肋：固定的上下文窗口，无法构建完整的长期记忆！

正因为 LLM 健忘，所以非常影响用户体验。无法记住用户偏好，也就无法真正`懂你`。

问题来了：如何给小智接入长期记忆？

本文分享，**笔者尝试过的两种方案**，并给出优劣分析，欢迎指教。

## 1. 双 LLM 方案

缓存所有对话记录没有必要，这样会导致 LLM 的上下文窗口迅速拉满。

为此考虑，在每次对话结束后，自动对当前对话记录进行总结，并保存到数据库中：

![](https://i-blog.csdnimg.cn/img_convert/e1d62e538e0abe9bf08b69af87469802.png)

下次对话开启后，从数据库中拉取历史记忆，拼接到系统提示词中：

![](https://i-blog.csdnimg.cn/img_convert/1022d0dbf203a4478a742d3456065275.png)


负责对话的 LLM 需要流式输出，而负责总结的 LLM 只需在当前对话结束时，触发即可。

因此，可以把任务解耦，定义两个 LLM Client：

```
# 负责对话的智能体
this.clientChat = await MCPClientOpenAI.create(url, key, model, appid, this.roleDesc, session);
# 负责总结对话记录的智能体
this.clientSum = new ClientOpenAI(url, key, model, appid, config.sys_sum);
```

**优点：**
- 这两个 LLM 是异步的，不会增加`clientChat`的对话延时。
- 实现简单，存储成本低，只需保存文本字符串。

**缺点：**
- 本质上并没有解决`长期记忆`，因为随着时间推理，数据表中的内容逐渐增多，LLM 的上下文窗口，早晚要被突破。
- 每次拼接所有历史记忆，导致大量的 token 资源浪费，实际上并非所有历史记忆都是当前对话必须的。

怎么解决？还是要引入 RAG，而且还要高效且准确的 RAG。

接下来，我们介绍一种企业级 LLM 长期记忆解法方案：`mem0.ai`

## 2. LLM + mem0

### 2.1 什么是 mem0

你看我们的大脑，所谓的记忆，是提取关键经历并不断重塑。

**mem0 所做的**，大白话讲：从海量信息中提取最重要的“精华”，并不断对这些“精华”进行更新。

比如下面这张表记录的：

![](https://i-blog.csdnimg.cn/img_convert/53d675b1c0f3b51533d76218b2f0c9e6.png)

内容是不是精简了很多？

**mem0 怎么做的？**

放一张论文中的架构图：

![](https://i-blog.csdnimg.cn/img_convert/a523b059a6907087e87789c0dff0c1f6.png)

你看，其实我们第一个方案只是做了 mem0 的第一步，也就是用 LLM 提取对话记录中的关键信息。

但是，这个记忆库，只会新增，压根不会更新。

而 mem0 还会从数据库中，检索最相关的记录，进行对比验证，再更新到数据库中。

此外，mem0的增强版，还引入了图谱记忆：

![](https://i-blog.csdnimg.cn/img_convert/f0fe29932c5e3e86caf268ea96b6ce4f.png)



看起来，这个逻辑非常合理，下面来实操一下。


### 2.2 mem0 初体验

mem0 提供了在线服务，非常简单。
> 体验地址：[https://app.mem0.ai/](https://app.mem0.ai/)

官方提供了贴心的 5 步走 checkList，代码都给你备好了:

![](https://i-blog.csdnimg.cn/img_convert/b24d95bcb0567225ed6cff4bdad8f5d0.png)

![](https://i-blog.csdnimg.cn/img_convert/cc4f912056069449a26ecb68869b0351.png)

![](https://i-blog.csdnimg.cn/img_convert/096f6d5f127d95bdc377a29dc0bbbde7.png)

当然，在线服务是有免费额度的：每个月1000次 API 请求。

如果想要二开，官方也提供了开源版本。

### 2.3 mem0 本地部署
> 开源地址：[https://github.com/mem0ai/mem0](https://github.com/mem0ai/mem0)
>
> 开发文档：[https://docs.mem0.ai/](https://docs.mem0.ai/)

官方提供了 Python 和 Nodejs 的 SDK，下面我们以 node.js 为例展开。

**step 1**: 引入依赖
```
import dotenv from 'dotenv';
dotenv.config();
import { Memory } from'mem0ai/oss';
```
**step 2**: 准备 mem0 用到的几个核心部件：
- LLM：提取结构化信息
- Embedding模型：提取特征向量
- 向量数据库：保存、索引、检索相关记录

这些核心部件以配置文件形式，进行初始化。

![](https://i-blog.csdnimg.cn/img_convert/7b5c7b3249e451fe41eac75f7b66986f.png)

**step 2.1**: LLM 配置

由于笔者服务端用的都是 OpenAI 格式的 API， LLM 来自阿里云，因此供应商这里选择 OpenAI ：

```
llm: {
  provider: 'openai',
  config: {
    apiKey: process.env.OPENAI_KEY,
    model: process.env.MODEL_NAME,
    modelProperties: {
      baseURL: process.env.OPENAI_URL
    }
  },
},
```

这里不得不吐槽下：mem0开源的 SDK 坑比较多。

OpenAI 的 baseURL 居然无法入参。

找到库中`dist/oss/index.mjs`文件，加了下面一行才成功搞定：

![](https://i-blog.csdnimg.cn/img_convert/1d78f1d4d817f13f2cc18227ccbc6eb0.png)


**step 2.2**: embedder 配置

`embedder`同样是阿里云的，不过要注意这里的特征维度：

![](https://i-blog.csdnimg.cn/img_convert/6527c9b76210c7f5098de861ce79a4b8.png)
```
embedder: {
    provider: 'openai',
    config: {
      apiKey: process.env.OPENAI_KEY,
      model: 'text-embedding-v3',
      modelProperties: {
        baseURL: process.env.OPENAI_URL
      }
    },
  },
```

同样注意 baseURL 无法入参，找到库中`dist/oss/index.mjs`文件，加入下面一行：

![](https://i-blog.csdnimg.cn/img_convert/11cdec72ee7bc85c64005f3123f7bd3a.png)

**step 2.3**: vectorStore 配置

向量数据库的方案已经很成熟了，不过在 node 版 SDK 中只支持：Qdrant, Redis and in-memory。

看到这里，有两点小疑问：
- 这里的 in-memory 难道是 faiss？

- Redis 是内存数据库，存储容量有限，咋还能用来做向量数据库的？

不管了，先拿 Qdrant 进行演示，最简单的方式就是用 docker 启动一个容器：

```
docker run -d -p 6333:6333 -v ./qdrant/storage:/qdrant/storage --name qdrant --restart=always qdrant/qdrant
```

启动后，配置如下，注意向量维度和之前的 embedder 要对应上：

```
vectorStore: {
    provider: 'qdrant',
    config: {
      collectionName: 'mem0',
      embeddingModelDims: 1024,
      dimension: 1024,
      host: 'localhost',
      port: 6333,
    }
  },
```

**step 3**: 记忆测试

```
const messages = [
  {"role": "user", "content": "我今天买了个熊猫玩具，花了100零花钱，太划算了，你也喜欢吗？"},
  {"role": "assistant", "content": "我也喜欢，不过价格有点贵，不过我也不介意，你喜欢哪种？"},
]
const res = await memory.add(messages, { userId: "john" });
console.log(res)
const allMemories = await memory.getAll({ userId: "john" });
console.log(allMemories)
```



### 2.4 效果展示

所有记忆内容，默认存在本地 sqlite 文件中：

![](https://i-blog.csdnimg.cn/img_convert/53d675b1c0f3b51533d76218b2f0c9e6.png)

内容的确是`精华之精华`，但如果还是一股脑把所有记忆内容加入系统提示词，显然不够优雅。

我们可以在每轮对话，根据用户输入，检索最相关的记忆，加入到上下文中：

```
const result = await memory.search('你知道我喜欢什么吗', { userId: "john" });
console.log(result);
```

然后，再根据 `score` 过滤一下，就可以获取最相关的记忆条目：

![](https://i-blog.csdnimg.cn/img_convert/6575ef552cb156d3cff2085f585844c0.png)

你看，为了支持`记忆功能`，LLM 的 token 消耗岂不是省了好多？

代价是什么？

向量数据库也要存储啊，如果再加上图谱数据库（如 Neo4j），这笔帐也少不了。

## 写在最后

本文分享了 `小智 AI 如何接入长期记忆` 的两种方案，孰优孰劣，欢迎评论区大佬指教。

如果对你有帮助，欢迎**点赞收藏**备用。
