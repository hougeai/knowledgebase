
现在做大模型，还有靠谱且免费的 API 接口吗?

靠谱的不免费，免费的不靠谱，鱼和熊掌不可兼得？

非也！

对于简单的指令而言，绝大部分免费的 LLM API 还是能打的，本文就给大家介绍几款，猴哥亲测好用的免费的 API 接口！

## 1. 免费 LLM API 汇总（持续更新中）

|大模型|免费版本|免费限制|备注|API|
|:------:|:------:|:------:|:------:|:------:|
| 讯飞星火大模型 | spark-lite | Tokens：总量不限；QPS：2| |[链接](https://www.xfyun.cn/doc/spark/Web.html)|
| 百度千帆大模型 | ERNIE-Speed-128K             | RPM=60，TPM=300000 ||[链接](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/6ltgkzya5) |
|            | ERNIE-Speed-8K/ERNIE-Lite-8K/ERNIE-Tiny-8K| RPM=300，TPM=300000 | | |
| 腾讯混元大模型 | hunyuan-lite                | 限制并发数 5 | | [链接](https://cloud.tencent.com/document/api/1729/105701)|
| 智谱 AI 大模型 | glm-4-flash               | 限制并发数 5 |自带联网搜索，支持微调 | [链接](https://open.bigmodel.cn/dev/api#glm-4)|
| 书生浦语大模型 | internlm2.5-latest      | RPM=10, TPM=5000 |需申请使用| [链接](https://internlm.intern-ai.org.cn/api/document)|
| Llama Family  | Llama3-Chinese-8B-Instruct/Atom-13B-Chat | 8-22 点：RPM=20；22-次日 8 点：RPM=50 | | [链接](https://llama.family/docs/chat-completion-v1)|
| Groq  | gemma-7b-it/llama-3.1-70b等 | RPM=30, RPD=14400 | |[链接](https://console.groq.com/docs/openai) |
| Google Gemini | gemini-1.5-flash/gemini-1.0-pro | RPM=15, TPM=100万, RPD=1500|   | [链接](https://ai.google.dev/gemini-api/docs/models/gemini)|
|  | gemini-1.5-pro   | RPM=2, TPM=3.2万, RPD=50|   | |
|  | text-embedding-004   | RPM=1500|   | |
| 硅基流动  | Qwen2-7B-Instruct等  | RPM=100，QPS=3| | [链接](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y)|
>- RPM：每分钟处理的请求数量；
>- TPM：每分钟处理的Token数量；
>- RPD：每天处理的请求数量；
>- QPS：每秒内处理的请求数量；
>- 并发数：系统同时处理的请求数量。


接下来，我们一起梳理下各家的 API 调用示例代码，以及如何把它们接入 OneAPI，方便集成到兼容 OpenAI 格式的应用中!

关于如何使用 OneAPI，可以围观教程：[OneAPI-接口管理和分发神器](https://zhuanlan.zhihu.com/p/707769192)。


## 2. 讯飞星火大模型
掉用示例代码见：[拒绝Token焦虑，盘点可白嫖的6款LLM大语言模型API](https://zhuanlan.zhihu.com/p/703523223)

当然，更简洁的方式是：接入 OneAPI!

添加一个新的渠道，类型选择`讯飞星火认知`，模型处手动填入`spark-lite`。

![](https://img-blog.csdnimg.cn/img_convert/33308d9576effe2b699c602b4b72a3f7.png)


## 3. 百度千帆大模型

首先，到千帆平台上开通免费的模型：[https://console.bce.baidu.com/qianfan/ais/console/onlineService](https://console.bce.baidu.com/qianfan/ais/console/onlineService)

![](https://img-blog.csdnimg.cn/img_convert/4ec7fffe256cbd0df9bf09068b98ea88.png)

然后，到应用接入中创建应用，获取API Key、Secret Key

![](https://img-blog.csdnimg.cn/img_convert/9cebddae3a0bb0990abf62b1b9d7c5b3.png)

最后，调用示例代码：

```
import requests
import json

API_KEY = "xxx"
SECRET_KEY = "xxx"

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
     
url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token=" + get_access_token()

payload = json.dumps({
    "messages": [
        {
            "role": "user",
            "content": "你好"
        },
    ]
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
```

当然，更简洁的方式是：接入 OneAPI!

添加一个新的渠道，类型选择`百度文心千帆`，模型处只保留你开通的免费模型。

![](https://img-blog.csdnimg.cn/img_convert/8dc24fcec29bd1eb7df591917f69cb27.png)


## 4. 腾讯混元大模型

腾讯云的产品，接入地址：[https://console.cloud.tencent.com/hunyuan/start](https://console.cloud.tencent.com/hunyuan/start)

新用户首先要开通，然后点击创建密钥，到新页面，新建密钥。

首次记得保存！后续不支持查询！

![](https://img-blog.csdnimg.cn/img_convert/97c3dd64c73014a2e52686ce7d79c068.png)

混元大模型的调用接口，鉴权非常麻烦，最好安装它的 SDK 进行使用。

当然，更简洁的方式是：接入 OneAPI!

添加一个新的渠道，类型选择`腾讯混元`，模型处需要手动填入`hunyuan-lite`。

![](https://img-blog.csdnimg.cn/img_convert/6ed0a66fc4f0e682b50b00ecfdfc623b.png)

在下面的`密钥`处填入你的：APPID|SecretId|SecretKey。


## 5. Google Gemini

Google Gemini 集成在 Google AI Studio中。

首先需要创建一个项目，然后获取 `API 密钥`。

`API 密钥`获取地址：[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

![](https://img-blog.csdnimg.cn/img_convert/9ffb4e56977ce534f197ac32818cd5d8.png)


在 API 价格文档中，可以看到各个模型的限速详情：[https://ai.google.dev/pricing](https://ai.google.dev/pricing)


![](https://img-blog.csdnimg.cn/img_convert/176cf6ab05465e6f4ff562785226f2e2.png)

调用示例代码：
```
import requests
import json

# 设置请求的URL和API密钥
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
api_key = "xxx"  # 替换为你的API密钥

headers = {
    "Content-Type": "application/json"
}

data = {"contents": [{"parts": [{"text": "Explain how AI works"}]}]}

response = requests.post(f"{url}?key={api_key}", headers=headers, data=json.dumps(data))
print(response.json())
```

如果是国内 IP，是调不通的，会报下面的错误：
```
{'error': {'code': 400, 'message': 'User location is not supported for the API use.', 'status': 'FAILED_PRECONDITION'}}
```

因此，请自行备好梯子，或在代码中加上海外 IP 的代理！

当然，更简洁的方式是：接入 OneAPI!

添加一个新的渠道，类型选择`Google Gemini`，模型处只保留你开通的免费模型。

![](https://img-blog.csdnimg.cn/img_convert/7579095edb4b171f8d809d672e9f39db.png)

## 6. All in One
如果你还在因适配各种 LLM 接口而苦恼，强烈推荐使用 OneAPI 管理自己的各种 LLM API！

![](https://img-blog.csdnimg.cn/img_convert/9f078c9c10f05e757811a16b1cb78c6b.png)

关于如何使用 OneAPI，可以围观之前的教程：[OneAPI-接口管理和分发神器](https://zhuanlan.zhihu.com/p/707769192)

## 写在最后

本文盘点了几款免费又好用的 LLM API，并接入了 OneAPI 统一管理！

你要问目前这些免费的 API 中，哪个更能打？

我要说：Google 家的 `gemini-pro-1.5` 指令遵循最佳，没有之一！

不知你的体验如何？欢迎评论区交流！

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

有任何问题欢迎通过公众号找到我，一起打怪升级。


