
之前免费出圈 Coze 开始收费了，总结来看：

- API 只有 100 次免费额度；
- 除了在 coze 主页使用，其他外部平台如：微信公众号/抖音，只有 100 次免费额度
- 不能使用火山引擎的方舟大模型中的免费额度；

![](https://img-blog.csdnimg.cn/img_convert/093c3c6363cca74f60364275208d9119.png)

有没有类似 Coze 的开源项目？

目前有两个 Coze 的开源平替，同样支持智能体搭建：FastGPT 和 Dify。

就目前的体验来看，二者各有优劣：
- FastGPT：在知识库召回上更优；
- Dify：支持的AI大模型更为丰富，插件生态更完善。

关于 FastGPT，可以看之前的教程：[FastGPT：给 GPT 插上知识库的翅膀！0基础搭建本地私有知识库，有手就行](https://zhuanlan.zhihu.com/p/708174104)。

今日分享，将手把手带大家私有化部署体验 Dify，并把它接入个人微信。

## 1. Dify 简介

> 在线体验：[https://dify.ai/](https://dify.ai/)
>
> 开源地址：[https://github.com/langgenius/dify](https://github.com/langgenius/dify)
>
> 官方文档：[https://docs.dify.ai/v/zh-hans](https://docs.dify.ai/v/zh-hans)

Dify 是 Do it for you （为你而做）的简称。

和 Coze 非常类似，Dify 也内置了构建 LLM 应用所需的关键技术栈，包括对数百个模型的支持、直观的 Prompt 编排界面、高质量的 RAG 引擎、稳健的 Agent 框架、灵活的流程编排，以及一套易用的界面和 API。

如果你用过 Coze 搭建智能体，那么迁移到 Dify 会非常丝滑。

如果你没用过 Coze，那么可以前往上面的在线体验地址，先去点点看~

如果不想自己部署，官方地址也提供了一定的免费额度，不过只支持上传 50 个文档，且支持 RAG 的向量空间也只有 5 MB。

如果不想付费，且对自己的私有数据安全有更高要求，那么强烈建议你本地私有化部署，参考下面步骤，相信你也能搞定！

## 2. Dify 私有化部署
> 参考文档：[https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/docker-compose](https://docs.dify.ai/v/zh-hans/getting-started/install-self-hosted/docker-compose)


首先，克隆 Dify 源代码至本地，然后进入 docker 目录，复制一份环境变量，采用默认端口，一键启动：

```
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
docker compose up -d
```


启动成功后，你会发现共有 9 个容器：包括 3 个业务服务 api / worker / web，以及 6 个基础组件 weaviate / db / redis / nginx / ssrf_proxy / sandbox。

![](https://img-blog.csdnimg.cn/img_convert/1bce829e93432399c5e5f718e0b6dcf8.png)

内存占用共计 1690 M，所以至少确保有一台 2G 内存的机器。

![](https://img-blog.csdnimg.cn/img_convert/2790f743177eafe49a87a2305cb859f2.png)

因为项目中启动了一个容器 nginx 将 web 服务转发到 80 端口，所以在浏览器中，直接输入公网 IP 即可，设置一下管理员的账号密码，进入应用主界面。

![](https://img-blog.csdnimg.cn/img_convert/fbef7d6afd5964dd677114200cfdd8ce.png)


## 3. 接入大模型

整个界面非常简单，先不管能干啥，我们先把大模型接入进来。

怎么接入？

不得不说，Dify 把这么重要的需求设置的实在太隐秘了，着实折腾了一段时间才找到👇

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F466dc304-25bc-4a5b-8d5c-64872282d20c.png&pos_id=img-Hu5hcuzk-1724285222897)

在`设置`里找到 `模型供应商`，这里已经支持了上百款模型，我这里主要先接入了三款有免费额度的。

![](https://img-blog.csdnimg.cn/img_convert/50fd5d9effb71693d6df4d472cd54a41.png)

其中：

- SiliconFlow 提供了大量免费的 LLM API，即便是需要付费的模型，新注册用户也有 2000W Token 的体验额度。可前往[**注册&体验地址**](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y) 领取。
- 火山引擎的方舟大模型也提供了一定的免费额度，怎么接入？

在[火山方舟控制台](https://console.volcengine.com/ark/)找到：在线推理-创建推理接入点，就可以拿到接入点名称。

![](https://img-blog.csdnimg.cn/img_convert/4fe2e93be65804a93cd8786da4033f1f.png)

如果你打算采用本地部署的大模型，Dify 也提供了对 Ollama 的支持：


![](https://img-blog.csdnimg.cn/img_convert/7dd82ee01c78591c506a7ef52c70a48f.png)

不了解 Ollama 的小伙伴，可以回看教程：[本地部署大模型？Ollama 部署和实战，看这篇就够了](https://zhuanlan.zhihu.com/p/710560829)

如果你有用过 OneAPI 管理过各种大模型，Dify 也提供了对 OpenAI-API-compatible 的支持：

![](https://img-blog.csdnimg.cn/img_convert/e290009a3d85600077aaf2e6890454f1.png)

不了解 OneAPI 的小伙伴，可以回看教程：[OneAPI-接口管理和分发神器：所有大模型一键封装成OpenAI协议](https://zhuanlan.zhihu.com/p/707769192)

## 4. 创建工作流

回到主页，点击`创建空白应用`，这里的聊天助手和文本生成应用，是功能最为单一的 LLM 应用，都不支持工具和知识库的接入。

Agent 和 工作流有什么区别？
- Agent：智能体，基于大语言模型的推理能力，可以自主选择工具来完成任务，相对简单。
- 工作流：以工作流的形式编排 LLM 应用，提供更多的定制化能力，适合有经验的用户。

![](https://img-blog.csdnimg.cn/img_convert/13341d4c8975f5e2bdf123e5bea2ad37.png)

通常，我们需要 Agent 和 工作流配合使用，Agent 负责对话理解，Workflow 处理具体的定制功能。


今天，我们就把[上一篇](https://zhuanlan.zhihu.com/p/715637724)在 coze 做的微信消息转发插件迁移过来，给大家展示一下工作流的搭建方式。看看 Dify 能否完成同样的功能。

先创建一个工作流，进来后，在`开始`中添加后面添加添加两个参数：好友昵称 和 消息内容：

![](https://img-blog.csdnimg.cn/img_convert/08a99e7c5d2b1dbf417fd013a9667fbc.png)

然后在 `开始` 后面添加一个 Http 请求：

![](https://img-blog.csdnimg.cn/img_convert/dedc23a4417585a4c8a91e5a0b1cb349.png)

在 Http 请求中填入相关信息：url 就是上篇中搭建的机器人的`发送消息的API`，body 内容参考请求体参数填写，如下图所示。

![](https://img-blog.csdnimg.cn/img_convert/66efb1360135659b494c8e2629d9d267.png)

注意，上述填写 json 结构体时，一定要将变量加双引号，否则后面测试不通。

最后，创建一个结束流程，把 http 请求接口的结果进行返回。

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F649806c8-5e1d-425a-a2e4-78f157b3847c.png&pos_id=img-XH06T9KD-1724285222898)

创建成功后，点击`运行`测试一下：

![](https://img-blog.csdnimg.cn/img_convert/53847bd5a2a108fb3cda4cfbd7f95e5a.png)

`运行`测试没问题后，你需要将它发布为一个工具（类似 coze 中的插件），才能供后面的 Agent 调用。

![](https://img-blog.csdnimg.cn/img_convert/6b6dab8dc75429f9d511fd6186a6ce67.png)

注意：这里的工具调用名称，是后续给大模型调用的，工具描述需要写清楚。

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F7ec73627-fb8b-4d2f-920d-66efa86cc1c1.png&pos_id=img-muVRGVSG-1724285222899)

## 5. 创建 Agent 应用

工具发布以后，回到首页，在工具 tab 页的工作流中可以看到：

![](https://img-blog.csdnimg.cn/img_convert/72938c13993fc2320e9c7c51b332e126.png)


接下来，我们来创建一个 Agent 应用，来调用该工具：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2Ff52bc8e2-b6df-48ba-bfdd-a0379b456f8c.png&pos_id=img-tfJ6o4Bk-1724285222900)

可以先设置一下角色提示词：

```
你作为一个聊天机器人，能够深刻理解对话内容背后的意图。可以使用wechat_msg工具，给对方的微信号发送答复。
```
然后，在下方的工具处，把我们刚发布的工具添加进来：

![](https://img-blog.csdnimg.cn/img_convert/056723db54bf21971507a2c73c03de52.png)

最后，如果指令任务执行的不够好，右上角选择切换一个大模型：

![](https://img-blog.csdnimg.cn/img_convert/1a510e08c2ce0b6bf1c9fed0f7d5cb3f.png)

在右侧的`预览与调试`区域，测试一下吧~

**测试案例一**：

让它给我的`大号`微信讲一句土味情话，可以看到成功调用了刚刚添加的工具！

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F6f1ab156-9a18-4cbb-b973-896a2261bdbc.png&pos_id=img-iumPAiZ0-1724285222900)

还能干点啥？

**测试案例二**：

比如查询天气，那就添加天气相关的工具，Dify 中内置了两款插件。

`OpenWeather` 这个工具申请 API Key 后需要等大约 1h 后才能生效。这里选择高德的天气插件，给大家演示。

![](https://img-blog.csdnimg.cn/img_convert/73732efa5eee9ebf72e19f3412842672.png)

首先采用的是豆包大模型，需要调用两个工具的任务，居然就掉链子了，得再次强调一次任务才能发送成功！

![](https://img-blog.csdnimg.cn/img_convert/ae025ae4d0607833bb7e56f0094a4926.png)

所以，指令遵循是否完美，和选用的大模型有很大关系，`Doubao-pro-128k`就需要发两次消息，换用 `gpt-4` 后就一次搞定了!

![](https://img-blog.csdnimg.cn/img_convert/bf747b004527c6b2ea47986e5d6e3c23.png)


来微信看看，成功发送！👇

![](https://img-blog.csdnimg.cn/img_convert/21845e5182e06a139c02fd8453636dc2.png)

完美实现类似昨天 coze 的功能!

## 写在最后

作为 Coze 的开源平替，Dify 也是一个非常强大的智能体开发和搭建平台，

今天通过搭建一个简单的工作流和 Agent 的具体实操，带着大家熟悉了 Dify 的本地部署体验，成功实现了微信 AI 消息转发。

关于 Dify，还有诸如`知识库`、`API 调用`等更丰富的功能，后续再跟大家分享~

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

