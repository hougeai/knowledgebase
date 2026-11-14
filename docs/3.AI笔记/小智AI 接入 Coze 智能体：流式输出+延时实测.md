>写在前面：
>
> 大家好，我是猴哥，我会在这里围绕 `AI`，分享工具、技术、思路、感悟。。。
>
> 所有文章纯手打，无 AI 添加剂，更多是个人思考和实操总结，欢迎交流。
>
> 若对您有帮助，不妨一键三连，帮我增加曝光，触达更多志趣相投的朋友，谢谢支持~

前面分享了，小智 AI 如何接入 LLM：

[低延迟小智AI服务端搭建-LLM篇](https://zhuanlan.zhihu.com/p/1897978035438874729)

服务端统一采用 OpenAI 格式调用，虽然这是目前的最优解，能够兼容不同厂商的大模型，并通过 MCP 接入各种外部工具。

不过，缺陷也很明显：如果 LLM 的指令遵循不 OK，就会经常一本正经地胡说八道。

![](https://i-blog.csdnimg.cn/img_convert/8989649237867e3d3222d6de81c11983.png)

实测了以上 LLM，只有 `deepseek-v3` 和 `glm-4-flash` 能够 90% 以上成功调用 MCP，无论怎么刁难它。

没错，就这个免费的 `glm-4-flash`，在工具调用方面，相当出色！且延时低，非常适合拿来测试。

以上，所有 LLM，陪聊还行。

但凡要发挥点生产力，最好是接入 `Agent` (智能体)！

而提到 `Agent`，自然绕不开`Coze/扣子`。

因此，本文，来聊：

**如何将`Coze/扣子`通过 API 形式，接入小智 AI。**

## 1. Coze/扣子体验
> [https://www.coze.cn/](https://www.coze.cn/)

`Coze/扣子` 是字节出品的智能体搭建工具，相信关注笔者的朋友都不陌生。

![](https://i-blog.csdnimg.cn/img_convert/166e9c4924b71f3c3cdb0d41ff59687e.jpeg)

`Coze/扣子` 极大降低了普通人`使用AI`的门槛。

如下，搭建一个`陪伴型女友`智能体，只需简单几步操作即可：

![](https://i-blog.csdnimg.cn/img_convert/91567f057687c11b76f222780983c1f3.png)

测试没问题后，点击右上角`发布`，注意勾选下方 `API`：

![](https://i-blog.csdnimg.cn/img_convert/33b8f7fc2e1c2d64dfe2d4506af8bc1a.png)

下面，我们重点聊聊如何调用 `Coze` 的 API。

## 2. Coze/扣子 API 调用
> API 文档：[https://www.coze.cn/open/docs/developer_guides](https://www.coze.cn/open/docs/developer_guides)

![](https://i-blog.csdnimg.cn/img_convert/cee9f06c3a0b8c8fba644b66042f1050.png)

个人免费版只有 100 次免费额度，勉强够测试用，因此要想使用 `Coze` 的 API，需付费到个人进阶版。

`Coze` 为了配合前端降低大家`使用AI`的门槛，后端做了大量工作，为此专门设计了一套独立的 API。

这套 API 不兼容 OpenAI 格式，因此要接入小智 AI 的服务端，需进行一番适配。

### 2.1 准备工作

**step 1**: 申请访问令牌

前往：[https://www.coze.cn/open/oauth/pats](https://www.coze.cn/open/oauth/pats)

添加新令牌，注意有效期，现在最多只有一个月了:

![](https://i-blog.csdnimg.cn/img_convert/da1a7f3351512bddb70e3b5750d8f111.png)

**step 2**: 获取 `bot_id`

智能体的搭建页面，URL 中 bot 参数后的数字就是`bot_id`。

例如 https://www.coze.cn/space/123/bot/73428668，`bot_id` 为73428668。

### 2.2 创建会话

会话（Conversation）是 `Coze` 中一个特有的概念：

![](https://i-blog.csdnimg.cn/img_convert/83e553edef1b7acf697f883785018bbf.png)

所有的聊天必须在会话中进行，所以须先创建会话。

`python` 示例代码如下：

```
headers = {
    'Authorization': 'Bearer pat_xxx',
}
def create_conversation():
    url = 'https://api.coze.cn/v1/conversation/create'    
    data = {
        'bot_id': '752'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(response.json())
        conversation_id = response.json()['data']['id']
        print(f'Conversation created with id: {conversation_id}')
```

### 2.3 对话-非流式调用

非流式接口（stream: false），是异步的，它不会立即返回 LLM 的回复，而是：

先返回一个状态，再查询是否完成，最后获取结果。

因此，一次对话，需要**三次请求**：

**step 1**: 发起会话请求：只会返回一个 `chatId`

```
def send_nonstream():
    # 不包含模型处理结果，只返回状态
    url = 'https://api.coze.cn/v3/chat'
    params = {'conversation_id': '7521349315088973833'}
    data = {
        'bot_id': '752',
        'user_id': '123',
        'stream': False,
        'additional_messages': [{'role': 'user', 'content': '你好', 'content_type': 'text'}],
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        print(response.json())
        data = response.json()['data']
        chat_id = data['id']
        print(f'Message sent with id: {chat_id}')
```

**step 2**: 查询是否完成：等待 status === 'completed'

```
def chat_retrieve():
    # 查看对话详情
    url = 'https://api.coze.cn/v3/chat/retrieve'
    params = {'conversation_id': '7521349315088973833', 'chat_id': '7521354516424458286'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(response.json())
        data = response.json()['data']
        status = data['status'] # in_progress, completed, cancelled, failed
        tokenCounts = data['usage']
        print(f'Chat status: {status}, tokenCounts: {tokenCounts}')
```

**step 3**: 获取结果：

```
def chat_message():
    # 查看对话消息详情
    url = 'https://api.coze.cn/v3/chat/message/list'
    params = {'conversation_id': '7521349315088973833', 'chat_id': '7521354516424458286'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()['data']
        for message in data:
            msgType = message['type'] # verbose answer follow_up
            content = message['content']
            print(f'Message type: {msgType}, content: {content}')
```

**注**：实际业务场景中，可设置`定时轮询`，需要异步 I/O 和事件循环。

如下：

```
2025-06-30T03:06:04.472Z Message sent with id: 7521573344756662322
2025-06-30T03:06:14.669Z Chat completed with status: completed
2025-06-30T03:06:14.894Z llm: 亲爱的，我查到啦，北京海淀现在是阴天，温度27度，体感温度29度，湿度76%，西北风1级呢。不过比起这天气，我更在意你有没有好好照顾自己呀。你今天有没有遇到什么开心的事儿呢？ 
```

### 2.4 对话-流式调用

流式接口返回的是 `Server-Sent Events (SSE)` 格式。

流式响应的事件类型有：

- chat：对话状态事件（如 created, in_progress, completed, ...）
- message：消息内容事件（包含模型回复）
- audio：音频事件（如果有）
- 还有可能有 error、end 等

每个事件的格式大致如下：

```
event: message
data: {...}
# or
event: chat
data: {...}
```
你需要逐行解析，并判断 event: 和 data:.

示例代码如下：

```
def send_stream():
    url = 'https://api.coze.cn/v3/chat'
    params = {'conversation_id': '7521349315088973833'}
    data = {
        'bot_id': '752',
        'user_id': '123',
        'stream': True,
        'additional_messages': [{'role': 'user', 'content': '你好', 'content_type': 'text'}],
    }
    response = requests.post(url, headers=headers, params=params, json=data, stream=True)
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    try:
                        json_data = json.loads(decoded_line[5:].strip())
                        msgType = json_data.get('type', '') # verbose answer follow_up
                        status = json_data.get('status', '') # created in_progress, completed, cancelled, failed
                        if status:
                            tokenCounts = json_data['usage']
                            print(f'Chat status: {status}, tokenCounts: {tokenCounts}')
                        if msgType:
                            created_at = json_data.get('created_at', '')
                            content = json_data['content']
                            print(f'Message type: {msgType}, content: {content} at {created_at}')
                    except Exception as e:
                        print(f'Invalid JSON data: {decoded_line}')
```

## 3. 延时实测

由于我们的服务端是 node.js，所以我把上述 API 用 node.js 重写了一遍。

以下是实测数据：

### 3.1 无工具调用

比如我问：
```
'北京海淀今天天气'
```

首句延时需要 `2 s`：

![](https://i-blog.csdnimg.cn/img_convert/51664364087ade4ef7badf69d9d48ef6.png)

因为没有接入外部工具插件，智能体拒绝回答了~

### 3.2 有工具调用

我们以`接入天气插件`为例：

![](https://i-blog.csdnimg.cn/img_convert/78c0cddba93cb32939b206219145e8f0.png)

得找一个**延时最低**的插件，你看`百度天气`平均耗时只有`61ms`:

![](https://i-blog.csdnimg.cn/img_convert/c514237c75db8164124ba220d2b8891f.png)

此外，还需在插件中填入百度天气申请的key，并关闭`对大模型可见`：

![](https://i-blog.csdnimg.cn/img_convert/fffac6f0f5161d2a2485d85ab54b205b.png)

![](https://i-blog.csdnimg.cn/img_convert/80f631d006a3014f0e619735a46ac209.png)

测试成功后，别忘了发布！

还是同样的问题：
```
'北京海淀今天天气'
```

你看，

![](https://i-blog.csdnimg.cn/img_convert/5ed65f0923c27e904ae45bea2a7c80ff.png)

成功查询到天气，不过`首句延时`飙升到 `4 s`，且 Token 消耗也接近翻倍。


### 3.3 接入小智 AI

这里主要看 `Coze` API 的 `延时情况`。

我测试了连续多轮对话：

如果没有工具调用，平均延时 `2s 以内`：

![](https://i-blog.csdnimg.cn/img_convert/4b5cbe9a45131fa7e940e2b42c03ce01.png)

![](https://i-blog.csdnimg.cn/img_convert/e8d76b2e3e8ec80304d7ede2f8d38a6b.png)

![](https://i-blog.csdnimg.cn/img_convert/7fff6495f8ce5c9a5d6f1950278f6086.png)

![](https://i-blog.csdnimg.cn/img_convert/194f75bc65bfdc6f5cb819b5a4df68d5.png)

![](https://i-blog.csdnimg.cn/img_convert/cb586e38fce9d7eba4199b3b9aab8817.png)

![](https://i-blog.csdnimg.cn/img_convert/810a9b102cc3825478ee74dd4781b6f8.png)

如果调用工具，延时来到`4s`:

![](https://i-blog.csdnimg.cn/img_convert/db231b8fa12ad43f68a29e997e211fce.png)

此外，`Coze` 还内置了长期记忆：

![](https://i-blog.csdnimg.cn/img_convert/6be7a958dae8a6b32fd23f47c4ef23a3.png)

## 写在最后

本文分享了`小智AI服务端接入 Coze 智能体`的实现，并对`流式推理的延时`进行了实测。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

