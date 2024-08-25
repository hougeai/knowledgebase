前两天和大家分享了最近 AI 绘画界的新星：
[FLUX.1 实测，堪比 Midjourney 的开源 AI 绘画模型，无需本地显卡，带你免费实战](https://blog.csdn.net/u010522887/article/details/140977067)


如果你还只用过 MJ（Midjourney）和 SD（Stable Diffusion），那么强烈建议你去 试试 FLUX，它的表现绝对会让你眼前一亮~

官方的体验链接只能让你在线体验，对于开发者而言，自然需要把模型部署成服务，方便任性调用！

不过 FLUX 的模型参数量实在太大了，开源的两个版本足足有 23.8G，就这一点，就拦住了不少玩家。

现在，AI Infra 领域的专业选手硅基流动，把 FLUX 的两个开源版本上线了，不仅可以在线体验，也有免费 API 可调。

> 此外，硅基流动还提供了大量免费的 LLM API，即便是需要付费的模型，新注册用户也有 2000W Token 的体验额度。 可前往 [**注册&体验地址**](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y)，速速领取。

## 1. 在线体验

注册成功后，左侧选择“文生图”，右侧 Model 选择这里：
- Schnell：生成速度最快；
- Dev：生成质量更佳。

最下方的 prompt 这里最好用英文，实测中文表现不太好。

![](https://img-blog.csdnimg.cn/img_convert/950ef6d3297cb181abf2e4a6bbe92ee7.png)

接下来，我们用一些案例实测一番~

**人物肖像**：

提示词：一个年轻艺术家坐在画布前，专注地画画，周围是五颜六色的颜料和画具，阳光透过窗户洒在他身上。

```
Prompt：
a young artist sitting in front of a canvas, focused on painting, surrounded by colorful paints and brushes, sunlight streaming through the window onto him.
```
![](https://img-blog.csdnimg.cn/img_convert/34ab356d866fbdb8d273821c6c787643.png)

**手部特写**

提示词：一只手握着一杯热咖啡，背景是模糊的咖啡馆内景，温暖的氛围。

```
Prompt：
close-up of a hand holding a cup of hot coffee, with a blurred café interior in the background, warm ambiance.
```

![](https://img-blog.csdnimg.cn/img_convert/446195c470e05458914663f860a1e4e6.png)


**文字理解**

提示词：
有一张木桌，上面放着一本翻开的书，封面上标题写着‘Houge AI 笔记’。

```
Prompt：
a wooden table with an book written "Houge AI".
```

![](https://img-blog.csdnimg.cn/img_convert/cce77b869e9a430169a2fe8098993612.png)


**写实摄影**

提示词：一只小猫在夜空下的星星中玩耍，旁边是一颗明亮的星星在微笑。

```
Prompt：
a tiny kitten playing among stars in the night sky, with a bright star smiling nearby.
```

![](https://img-blog.csdnimg.cn/img_convert/c4b826405431c18950cf7fd8c9437a6c.png)


**艺术摄影**

提示词：年轻女子的侧脸肖像，黑白照片，85毫米，f1.8，柔和的自然光，优雅的姿态。

```
Prompt：
profile portrait of a young woman, black and white photo, 85mm, f1.8, soft natural light, elegant pose.
```

![](https://img-blog.csdnimg.cn/img_convert/124ce0448d250d2789cbac129c1ee8fc.png)

```
Prompt：
profile portrait of a young asian woman, color photo, 85mm, f1.8, soft natural light, elegant pose.
```

![](https://img-blog.csdnimg.cn/img_convert/513e286f38844d808282177407b64a31.png)

有一说一，Flux 在细节处理上已经足够逼真，但写实类的还打不过 SD 的垂类模型~



## 2. 免费 API 调用

API 文档：[https://docs.siliconflow.cn/reference/black-forest-labsflux1-schnell](https://docs.siliconflow.cn/reference/black-forest-labsflux1-schnell)

通过 REST API 调用服务，文档右侧有支持的模型列表，遗憾的是目前还不支持 Flux.1-dev 调用，可以期待一下~

![](https://img-blog.csdnimg.cn/img_convert/fb56c9dd972993314332318af73c6b81.png)

下面给出一段 Python 代码调用示例：

```
import requests

url = "https://api.siliconflow.cn/v1/black-forest-labs/FLUX.1-schnell/text-to-image"

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

print(response.text)
```
上述代码中需要在 `headers` 中加入 `"Authorization": "Bearer your_api_key"`，这里的 API 密钥在哪获取？

首页 - 账户管理，找到 API 密钥：

![](https://img-blog.csdnimg.cn/img_convert/b1544478c4aabc616d5d92e9f13d056b.png)


最后，我们看一下返回结果的格式：


```
{
"images":[{"url":"https://sf-maas-uat-prod.oss-cn-shanghai.aliyuncs.com/outputs/6512bc04-c5ab-447a-b26e-0b6c814d33c2_00001_.png"}],
"timings":{"inference":2.692},
"shared_id":"0"
}
```

把图片 url 贴出来给大家看下哈！


![](https://img-blog.csdnimg.cn/img_convert/6382c2850b2f26c915eed10953e9dbb1.png)


## 写在最后
FLUX 作为 AI 绘画界的新秀，最近火的不行。

咱不用掏钱买显卡，也不用费劲部署模型，硅基流动已经帮我们都干了!

虽说写实摄影还比不过 SD 的专业选手，但这细节处理的功力已经相当了得了!

如果你是个爱折腾的开发者，还有免费的 API 等你来调教，几行代码就能搞定！

快去试试吧，让你的想象力插上 FLUX 的翅膀飞向艺术新天地！

如果本文有帮助，不妨点个**免费的赞**和**收藏**备用。你的支持是我创作的最大动力。