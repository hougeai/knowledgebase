
最近，更新了几期`白嫖 Cloudflare 系列`教程：
- [【白嫖 Cloudflare】之 免费图床搭建：PicGo + Cloudflare R2](https://blog.csdn.net/u010522887/article/details/141586984)
- [【白嫖 Cloudflare】之 1 小时快速搭建免费内网穿透](https://blog.csdn.net/u010522887/article/details/141621570)
- [【白嫖 Cloudflare】 之 5 分钟搭建个人静态网站](https://blog.csdn.net/u010522887/article/details/141291673)
- [【白嫖 Cloudflare】之 免费域名解析](https://blog.csdn.net/u010522887/article/details/140786338)

现在做 AI，还有靠谱且免费的 api 接口吗?

今日分享，继续`白嫖 Cloudflare`，给大家系统介绍下 `Cloudflare` 家的免费 AI 服务，不仅包括各种 AI 大模型，还包括翻译、文本生成、文生图、语音识别等各种 AI 服务！ 

## 1. Cloudflare AI 简介

AI 是 Cloudflare 的又一项免费服务，注册登录后，点击左侧边栏的 AI 。

目前包括两个板块：
- Workers AI：包含各种 AI 服务；
- AI Gateway：AI网关管理界面，本质是官方提供的代理，比如你在国内不能直接访问 openai 的 api，可以走这个代理去访问。此外，Gateway 还能方便地监控和管理接口调用情况、tokens 消耗和日志等信息。

![](https://img-blog.csdnimg.cn/img_convert/d77bbdeb7817911e05fdcac6bcfae9c7.png)

本次分享，我们主要介绍 `Workers AI` 如何使用。

## 2. 使用 REST API

### 2.1 支持的服务类型
在[开发者文档](https://developers.cloudflare.com/workers-ai/models/)中可以看到支持的各种服务类型的模型列表：

![](https://img-blog.csdnimg.cn/img_convert/9a463042ad290746a19bd70e5a9ecf99.png)

除了各种大模型，还包括翻译、文本生成、文生图、语音识别等各种 AI 服务，基本覆盖了所有的 AI 应用场景。

### 2.2 LLM 在线体验
如果你只是想用它的 LLM，官方也提供了 [PlayGround](https://playground.ai.cloudflare.com/) 供你在线体验：

![](https://img-blog.csdnimg.cn/img_convert/8c31cf02160fbd049a2e42fb072ff22e.png)

不过，模型参数量都比较小，稍微大一点的（比如14b）都经过了量化，对于简单的对话场景，足够用了。

对于复杂指令，不建议用！



### 2.3 API 调用

API 调用也非常简单，只需获得两个参数即可：
- 账户 ID
- API token

![](https://img-blog.csdnimg.cn/img_convert/5bd9c0add31323240086290f5374adba.png)

有了这两个东西，以 Python 为例，请求代码如下：


```
import requests

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/账户ID/ai/run/"
headers = {"Authorization": "Bearer {API_TOKEN}"}

def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()

inputs = [
    { "role": "system", "content": "You are a friendly assistan that helps write stories" },
    { "role": "user", "content": "Write a short story about a llama that goes on a journey to find an orange cloud "}
];
output = run("@cf/meta/llama-3-8b-instruct", inputs)
print(output)
```

### 2.4 集成到 OneAPI

当然，如果你想要兼容 OpenAI 格式，可以选择接入 OneAPI。

关于如何使用 OneAPI，可以围观教程：[OneAPI-接口管理和分发神器](https://zhuanlan.zhihu.com/p/707769192)。

在 OneAPI 首页，新建一个渠道，其中类型选择 Cloudflare，然后把 密钥 和 Account ID 填入下方文本框，提交即可！

![](https://img-blog.csdnimg.cn/img_convert/c2aa1e5f07ba083859ac194b2228728b.png)

后续，你就可以直接利用 OneAPI 给你提供的令牌，以兼容 OpenAI 的方式，直接调用 Cloudflare 中的所有大模型！

## 3. 应用创建
之前我们介绍过如何使用 Cloudflare Pages 搭建静态网站，Worker 是另一项 serverless 服务，借助 Worker 我们可以搭建 LLM 和 AI 推理模型。

在主页选择 `从 Worker 模板创建`：

![](https://img-blog.csdnimg.cn/img_convert/6cbd44aaebf22391048464d3f1877575.png)

在模板中，筛选出 AI 相关的，我们这里以构建 LLM APP 为例，当然你可以构建任意 AI 应用。

![](https://img-blog.csdnimg.cn/img_convert/7c71a419f3a29929178458e3af9b2a84.png)

进来后，这里你需要修改的地方有两个：
- 名称，分配域名的一部分
- 大模型：选择你想用的大模型（后续也可以改）

下面是模板中的 js 代码！

![](https://img-blog.csdnimg.cn/img_convert/b0193303d08991cb34b8a44608ebe00d.png)

修改好后，点击下方一键部署！

当然，如果你有在 Cloudflare 上解析的域名，也可以绑定自己的域名！

在 Workers 和 Pages 中找到你刚才新建的 worker，在设置中进行添加：

![](https://img-blog.csdnimg.cn/img_convert/22c7f39e6c089e45f2c18e0562633e8c.jpeg)


最后，浏览器中访问，可以看到请求结果：

![](https://img-blog.csdnimg.cn/img_convert/6593d0422746931e5e822cb5a664e7ad.png)

为了让它能接收自定义输入，我们需要简单修改上面的 js 代码。

`编辑代码`区域，在 request 中传入 message 参数：

```
export default {
  async fetch(request, env) {
    // 解析请求体
    const requestBody = await request.json();

    // 提取传入的文本参数
    const userMessage = requestBody.message || 'Tell me a joke about Cloudflare';

    const tasks = [];

    // prompt - simple completion style input
    let simple = {
      prompt: userMessage
    };
    let response = await env.AI.run('@cf/meta/llama-3-8b-instruct', simple);
    tasks.push({ inputs: simple, response });

    return Response.json(tasks);
  }
};
```

修改完成后，可以先在左侧打一个 POST 请求，测试下。成功返回结果后，再点击上方 `部署`重新发布！

![](https://img-blog.csdnimg.cn/img_convert/c86b5ff6805b7b73d1a3c49e08d2792b.png)


发布成功后，我们在本地用 Python 来写一个请求看看：

```
import requests
import json

# 定义请求的 URL
url = 'https://crimson-block-2a4e.xxx.workers.dev/' 

payload = {
    'message': 'What is the weather today?'  # 你想要传递的对话文本
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.json())
```


以上，是对 Worker 构建 LLM 应用的简单示例，希望对大家做出更有创意的应用，有所启发！

## 写在最后

本文是`白嫖 Cloudflare 系列`教程之一，带大家使用 Cloudflare 的免费 AI 服务。

REST API 和 Worker 应用，共享每天 10W 次的免费调用额度，个人使用完全足够了。

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

你学会了吗？有任何问题欢迎通过公众号找到我，一起打怪升级。
