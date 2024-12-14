
最近各大厂商都在搞`智能体平台`，前有字节的 Coze，后有腾讯的元器、支付宝的百宝箱。

之前免费出圈的 Coze 从 8 月开始收费之后，很多小伙伴们在问**有没有好用的开源平替？**

就笔者目前的体验而言：Dify / FastGPT / MaxKB 三者，从部署和使用角度来看，对小白还算友好。

若问三者怎么选？

- FastGPT：在知识库召回上更优；
- Dify：插件生态更完善。
- MaxKB：界面最简洁，内存占用高。

**如果都没用过，那么首推 Dify。**

前段时间，和大家分享了一个开源 AI 搜索引擎的实现方案 - MindSearch：

[4.9K Star！开源 AI 搜索引擎本地搭建，全程免费，邀你围观体验](https://zhuanlan.zhihu.com/p/2621376476)

MindSearch 默认采用 DuckDuckGo 搜索引擎，导致后端服务经常出问题，用户体验非常不好。

最近在琢磨有没有更好的平替方案：何不用 Dify 自己搭一个？

今日分享，带大家实操：**如何用 Dify 搭建一个 AI 搜索引擎。**


## 1. 为什么是 Dify
> 在线体验：[https://dify.ai/](https://dify.ai/)
> 
> 开源地址：[https://github.com/langgenius/dify](https://github.com/langgenius/dify)
>
> 官方文档：[https://docs.dify.ai/v/zh-hans](https://docs.dify.ai/v/zh-hans)

Dify 应该算是`智能体平台`的鼻祖，在 ChatGPT 推出后不久就已问世。

只不过 Coze 后来居上，在用户体验上，对小白更加友好。

但从关键技术栈上来看，二者非常类似。

如果你用过 Coze 搭建智能体，那么迁移到 Dify 会非常丝滑。

如果不想本地部署，上面的体验地址也提供了一定的免费额度，知识库支持上传 50 个文档，RAG 向量空间只有 5 MB。

## 2. Dify 本地部署

如果不想付费，且对数据安全有要求，那么强烈建议你本地部署，参考下方教程，相信你也能搞定：

[本地部署 AI 智能体，Dify 搭建保姆级教程（上）](https://blog.csdn.net/u010522887/article/details/141407784)

推荐采用 Docker compose 傻瓜式安装。

不过，有一点需要注意，所有环境变量都在 `.env` 中配置，Dify 采用 Nginx 把 web 界面映射到了 80 端口，如果 80 端口已被占用，需修改`EXPOSE_NGINX_PORT`变量，比如：

```
EXPOSE_NGINX_PORT=3006
```

启动成功后，你应该看到有 9 个容器：

```
 ✔ Network docker_ssrf_proxy_network  Created
 ✔ Network docker_default             Created
 ✔ Container docker-weaviate-1        Started
 ✔ Container docker-web-1             Started
 ✔ Container docker-sandbox-1         Started
 ✔ Container docker-redis-1           Started
 ✔ Container docker-ssrf_proxy-1      Started
 ✔ Container docker-db-1              Started
 ✔ Container docker-worker-1          Started
 ✔ Container docker-api-1             Started
 ✔ Container docker-nginx-1           Started
```


接下来，我们一起搞定`AI 搜索引擎`的智能体搭建！

> 注：无论在线体验，还是本地部署，下面的实操没任何区别。

## 3. AI 搜索引擎搭建

### 3.1 接入大模型
参考[本地部署 AI 智能体，Dify 搭建保姆级教程（上）](https://blog.csdn.net/u010522887/article/details/141407784)，接入你能用上的各种大模型。

比如，我常用的有：

![](https://img-blog.csdnimg.cn/img_convert/0f62a4e4c3b3b27cbf3e4d0c96f79b4c.png)

其中：Ollama 用来接入本地部署的大模型；OpenAI-API-compatible 则用来接入 OneAPI 代理的各种大模型。

大模型接入后，就可以着手智能体搭建了。

### 3.2 创建应用
参考下图，注意选择`工作流编排`：

![](https://img-blog.csdnimg.cn/img_convert/0db9004a6e3fd7cf9195f72c2a4ba2d8.png)

**二者有什么区别？**

- 基础编排：只支持知识库接入，和角色提示词的设定，适合简单应用搭建；
- 工作流编排：支持各种外部插件的接入，可定制化程度非常高。

### 3.3 编辑应用
进来后，默认的初始化页面如下图，一个非常干净的聊天助手，啥附加功能也没有，本文就以加入`搜索功能`为例，带大家体验下，给`智能体`装上三头六臂的效果。

![](https://img-blog.csdnimg.cn/img_convert/1410ff984321719aa1bceaff95172a9b.png)

最终实现如下：

![](https://img-blog.csdnimg.cn/img_convert/672e615b34a25fb9274c7e7c88ea93ea.png)

你会发现，其实就比上图多了一个模块：`TavilySearch`。

`TavilySearch` 就是 Dify 内置的一个搜索插件。

当然，Dify 内置的搜索插件还有很多，考虑到很多朋友在国内无法访问，`TavilySearch`是笔者亲测对小白比较友好的一个。

**怎么添加？**

看下图：

![](https://img-blog.csdnimg.cn/img_convert/eef1dbb6db260af27aa871158e5f17c7.png)

当然你也可以选择其他搜索插件，基本都有免费额度，去点点看！

添加之后，`TavilySearch` 的输入是啥呢？

点击 `TavilySearch` 模块，在这里：

![](https://img-blog.csdnimg.cn/img_convert/af2bb5884738e40d2174a4ea2379028f.png)


它代表`开始`模块的`sys.query`参数，其他模块也大同小异，聪明如你，多点点就熟悉了！


最后，来看下 LLM 模块，`System` 中填入角色提示词：`根据搜索引擎检索到的内容：{{text}}，回答用户的提问。`

![](https://img-blog.csdnimg.cn/img_convert/5f304023f2e59f217a192a6f056eb55e.png)

Dify 默认支持 10 轮对话的记忆，在下方可以手动设置。

### 3.4 测试应用

把所有模块连接好后，点击右上角`预览`，测试一下：

![](https://img-blog.csdnimg.cn/img_convert/c2f99e389b651164f7914b84f81ac5a4.png)

如果没什么问题，点击右侧`发布`。

至此，一个简单的 `AI 搜索引擎` 宣告搭建完毕！


## 4. API 接入小爱

如果希望将 `AI 搜索引擎` 内嵌到应用中，自然还少不了后端的 API。

左侧菜单栏，找到`访问 API`，点击获取 API 密钥：

![](https://img-blog.csdnimg.cn/img_convert/a5363184911922b75cf888d5a66c5932.png)


> 注意：API 基础 URL 是不变的，Dify 用来区分不同智能体的是`API 密钥`


来写个请求看看：

```
import requests

url = 'http://10.18.xxx.xxx:3006/v1/chat-messages'
api_key = 'app-xxx'  

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

data = {
    "inputs": {},
    "query": "今日AI热点",
    "response_mode": "blocking",
    "conversation_id": "",
    "user": "xiaoai",
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```
几个关键参数说明：
- `user`: 用于定义终端用户的身份，方便检索、统计，必填;
- `conversation_id`：如果需要基于之前的聊天记录继续对话，必须传入；
- `response_mode`：为 blocking 时，全部生成后再返回，为streaming时，流式输出。


输出结果如下：

```
{'event': 'message', 'task_id': '98524256-40ad-471b-9481-57b2ba8f564d', 'id': '45811855-6ce8-4788-8e3d-ff307f5663a6', 'message_id': '45811855-6ce8-4788-8e3d-ff307f5663a6', 'conversation_id': 'da72fe30-795b-4259-a114-193b6ed0828d', 'mode': 'advanced-chat', 'answer': '以下是今日一些值得关注的AI热点新闻：\n\n1. **Microsoft退出OpenAI董事会**：迫于监管压力，微软和苹果放弃了在OpenAI董事会中担任职务的计划。此举引发了广泛关注，凸显出大型科技公司对人工智能的影响力正日益成为监管机构的焦点。\n\n2. **稳定音频重磅更新**：Stability AI为用户友好的AI创作工具Stable Assistant推出了重磅更新，包括备受期待的Stable Audio音乐生成功能和“搜索和替换”图像编辑功能，为用户带来更强大的图像和音频生成体验。', 'metadata': {'usage': {'prompt_tokens': 18657, 'prompt_unit_price': '0', 'prompt_price_unit': '0.000001', 'prompt_price': '0E-7', 'completion_tokens': 1385, 'completion_unit_price': '0', 'completion_price_unit': '0.000001', 'completion_price': '0E-7', 'total_tokens': 20042, 'total_price': '0E-7', 'currency': 'RMB', 'latency': 7.6047362219542265}}, 'created_at': 1730093219}
```

请求成功后，在客户端可以查看日志：

![](https://img-blog.csdnimg.cn/img_convert/7331901692461fdd8b7896ca98edaf36.png)

最后，我们只需把微信 AI 机器人的后端接口，改为 Dify 的接口，就 OK 了。

实测效果如下：

![](https://img-blog.csdnimg.cn/img_convert/359177a5a6b18d95e7878d7fec417b19.png)

## 写在最后
本文通过一个简单案例，带大家实操了**Dify 搭建 AI 搜索引擎**，整体流程比较简单，相信看到这里的你，一定还有很多想法要实现，快去试试吧~

如果对你有帮助，欢迎**点赞收藏**备用。

之前微信机器人`小爱(AI)`所有的后端逻辑，都是一行行代码堆出来的，现在发现，完全可以在 Dify 的工作流中，通过鼠标`点点点`来完成，后面抽空改造后，再和大家分享！

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。


