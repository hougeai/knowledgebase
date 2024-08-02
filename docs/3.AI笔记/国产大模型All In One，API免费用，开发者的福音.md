前两天，OpenAI 宣布终止对中国提供 API 服务，国内开发者想访问 GPT 实在是太难了。

前几天，猴哥盘点了**6款可以免费调用的云端API**：

[AI布道师：拒绝Token焦虑，盘点可白嫖的6款LLM大语言模型API~](https://zhuanlan.zhihu.com/p/703523223)

不过不同模型之间切换还是有点麻烦。

有没有可以丝滑切换不同大模型的一站式服务？

这不， SiliconCloud 它来了。

就在最近，AI Infra 领域的专业选手硅基流动（SiliconFlow）上场，推出了一站式大模型 API 平台 SiliconCloud。

更香的是，SiliconFlow 给开发者带来了一份前所未有的豪华大礼：Qwen2 、GLM4 等国内顶尖的 GPT 平替**永久免费**！

>  一键直达：https://cloud.siliconflow.cn/s/free

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-d2335393e3e8efb67c7404202e1c4085_1440w.png)





在这里插入图片描述

## 1. 有哪些亮点

## 1.1 模型多样

为了解决不同大模型无法丝滑切换的痛点问题，硅基流动第一时间将国内主流的开源大模型上架到 SiliconCloud，并且不断更新中。

对于文本生成任务而言，目前官网上已有的模型，包括最强开源代码生成模型 DeepSeek-Coder-V2，超越 Llama3 的大语言模型 Qwen2、GLM-4-9B-Chat、DeepSeek V2 系列模型。

此外，还支持 Stable Diffusion 3 Medium 等文生图和图生图模型（详见后文）。

## 1.2 速度超快

作为世界顶级的 AI Infra 团队，硅基流动致力于将大模型部署成本降低 10000 倍。这一目标的核心挑战是：如何大幅提升大模型推理速度。

猴哥测试了一个文本总结任务：800字的输入，要求用一句话总结。

这里调用的是免费版的 Qwen2-7B-Instruct，下图可以发现，单条输出不超过 1 s。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-b0df38f0430bf89c59166be639d6487e_1440w.png)





添加图片注释，不超过 140 字（可选）

 对于文生图的任务而言，就在最近开源不久的 SD3 Medium ，512x512 单张图像的生图时间，也能够保持在 1s 左右。

知乎上，有网友称赞 SiliconCloud 的输出速度：**“用久了就受不了其他大模型厂商 web 端的响应速度”。** 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-3b9dab441aefa834e7ab8e5f906719bb_1440w.png)





添加图片注释，不超过 140 字（可选）

## 1.3 价格亲民

除了这些大模型的响应速度够快以外，API 价格也更加亲民。即使是 Qwen2-72B 这样的大模型，SiliconCloud 官网显示也只要 4.13 元 / 1M Token，而且新注册用户还可免费畅享 2000 万 Token。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-c5ab9c3b46abf1c30240fa4697178d4b_1440w.png)





添加图片注释，不超过 140 字（可选）

对于中小企业或者个人开发者，还有一众免费的 API 可以调用，唯一的限制是：调用次数。

当前公测版本，每位用户的**RPM限制为100，RPS为3**。  所谓 RPM（Requests Per Minute）和 RPS（Requests Per Second），都是衡量服务器或服务处理能力的性能指标。RPM 指的是每分钟的请求次数。RPS 指的是每秒的请求次数。

## 2. 有哪些 API 服务

官网首页展示了目前支持的两种优质模型服务：

- 文本生成
- 图片生成

## 2.1 文本生成

提供了 Web 端和 API 两种方式，不管哪种方式，是否需要付费取决于你选用的底层模型。

### 2.1.1  Web 端使用

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-8e9f09ab6e054e9dce3c815b11ec4e0c_1440w.png)





在这里插入图片描述

### 2.1.2  API 调用

参考 API 文档：[https://docs.siliconflow.cn/docs/4-api%E8%B0%83%E7%94%A8](https://docs.siliconflow.cn/docs/4-api调用)

使用方式和市面上已有的大模型服务几乎没有差别，首先需要生成自己的 API 密钥，然后通过以下两种接口方式进行调用：

- 使用 REST API 调用服务
- 通过 OpenAI 接口调用

在 [6款可以免费调用的云端API](https://zhuanlan.zhihu.com/p/703523223) 中，猴哥已对这两种方式进行了梳理，有不清楚的小伙伴可以回看。

## 2.2 图片生成

同样提供了 Web 端和 API 两种方式。

### 2.2.1  Web 端使用

图片生成分为两个任务：文生图 和 图生图，右侧可以查看支持的模型，可以发现连最新的 stable-diffusion-3 都上了，感兴趣的小伙伴赶紧去体验。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-3ab5e2fae699aaec6ab0472dd13dc030_1440w.png)





添加图片注释，不超过 140 字（可选）

### 2.2.3  API 调用

参考 API 文档：https://docs.siliconflow.cn/reference/stabilityaistable-diffusion-xl-base-10_text-to-image

通过 REST API 调用服务，文档右侧有支持的模型列表，遗憾的是目前 API 调用 还不支持 stable-diffusion-3 ，可以期待一下~ 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-07068cd52b9a6ef67c6c2753088897d3_1440w.png)





添加图片注释，不超过 140 字（可选）

 下面给出一段 Python 代码调用示例：

```
import requests
url = "https://api.siliconflow.cn/v1/stabilityai/stable-diffusion-xl-base-1.0/text-to-image"
payload = {
    "prompt": "an island near sea, with seagulls, moon shining over the sea, light house, boats int he background, fish flying over the sea",
    "image_size": "1024x1024",
    "batch_size": 1,
    "num_inference_steps": 20,
    "guidance_scale": 7.5
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "Bearer your_api_key"
}
response = requests.post(url, json=payload, headers=headers)
res = response.json()
print(res)
```

我们看一下返回结果的格式：

```
{
    "images": [
        {
            "url": "https://sf-maas-uat-prod.oss-cn-shanghai.aliyuncs.com/output/clxv36914000l6xncevco3u1y_17885302492_5717892_NVPbsSLxjnZCFtUPzqNikjcWGHDkYKfe.webp"
        }
    ],
    "timings": {
        "inference": 2.457
    },
    "seed": 84071684,
    "shared_id": "5717892"
}
```

根据 url 把图片下载保存到本地就 OK 了！

## 写在最后

随着国内大模型厂商的不断迭代，以 Qwen2、GLM4 为代表的开源大模型，其性能表现直逼 GPT4，在某些场景下已足够支持应用。

而 SiliconCloud 的出现，将彻底解决开发者的后顾之忧，不再 Token 焦虑，相信会有更多富有创意的 AI 应用不断出现！

如果本文对你有帮助，欢迎**点赞收藏**备用！

猴哥一直在做 AI 领域的研发和探索，会陆续跟大家分享路上的思考和心得，以及干货教程。

新朋友欢迎关注 **“猴哥的AI知识库”** 公众号，下次更新不迷路。
