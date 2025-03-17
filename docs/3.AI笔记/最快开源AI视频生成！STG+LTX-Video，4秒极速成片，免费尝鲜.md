相对图片生成，AI 视频生成一直没有低成本的解决方案。

从快手的可灵、智谱的清影，再到 OpenAI的 Sora，但这些模型都是闭源的。

要问**开源界**有没有能打的？

之前有分享过三款：
- [EasyAnimate-v3 实测，阿里开源视频生成模型，5 分钟带你部署体验，支持高分辨率超长视频](https://zhuanlan.zhihu.com/p/710131990)

- [我把「国产Sora」接入了「小爱」，邀你免费体验](https://zhuanlan.zhihu.com/p/748148202)

- [开源视频生成 Pyramid Flow 本地部署实测](https://zhuanlan.zhihu.com/p/3489126869)

但，生成质量总归是差强人意，生成速度，也差点意思。

最近，当前最快的文生视频模型诞生了：LTX-Video。

先别管质量，至少速度上提高了一个数量级！

在 Nvidia H100，生成 5 秒时长的 24FPS 768x512 视频，只需 4 秒！

今日分享，带大家实战：最快 AI 视频生成项目 LTX-Video，并接入微信机器人。


## 1. LTX-Video简介

> 项目地址：[https://github.com/Lightricks/LTX-Video](https://github.com/Lightricks/LTX-Video)

LTX-Video 来自押注开源人工智能视频的初创公司 Lightricks，它是**首个**基于扩散变换器 (DiT) 架构的模型，参数量 2B，可在 RTX 4090 等消费级 GPU 上跑。（<u>**划重点：至少确保 24G 显存**</u>）


老规矩，简单介绍下项目亮点：

- **可扩展的长视频制作**：能够生成扩展的高质量视频，具有一致性和可扩展性，相对CogVideo 灵活性更高。
- **更快的渲染时间**：针对GPU和TPU系统进行优化，在保持高视觉质量的同时大幅缩短视频生成时间。
- **运动和结构一致性**：独特帧间学习确保了帧与帧之间的连贯过渡，消除了场景中的闪烁和不一致问题。

从官方放出的案例来看，效果还是相当惊艳的。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6c8d4ffa2c314cdb94a40800a625c107.png)


实测效果到底如何？

接着往下看！

## 2. LTX-Video 本地部署

>本地部署前，有两点需要注意：
>- **至少确保 50G 磁盘空间**；
>- **至少确保 24G 显存**。

参考项目首页，安装项目依赖。

```
git clone https://github.com/Lightricks/LTX-Video.git
cd LTX-Video
```


然后，最耗时的就是下载模型权重，包括两部分：
```
from huggingface_hub import snapshot_download

# 原始模型权重 - 33G
snapshot_download("Lightricks/LTX-Video", local_dir=model_path, local_dir_use_symlinks=False, repo_type='model')
# 文本编码器权重 - 17G
snapshot_download("PixArt-alpha/PixArt-XL-2-1024-MS", local_dir=model_path, local_dir_use_symlinks=False, repo_type='model')
```


如果希望进一步提高视频质量，可参考 STG 项目：[https://github.com/junhahyung/STGuidance](https://github.com/junhahyung/STGuidance)

STG 是一种用于增强扩散器的采样指导方法，无需下载额外的模型，只需修改模型中特定层的采样方法，即可得到更高质量的视频效果。

亲测有效，感兴趣的可以去试下。

## 3. LTX-Video API 调用

本地部署毕竟太吃资源了。

目前，硅基流动 SiliconCloud 已上线 LTX-Video，关键是**免费调用**。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c970293afa7a4d8dae466ec3c3aedf6a.png)


首先，前往 [硅基流动](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y) 注册账号，并生成一个 API key。

然后，查看 [API文档](https://docs.siliconflow.cn/api-reference/videos/videos_submit)：视频生成是异步服务，也即：首先获取请求 ID，再根据请求 ID 轮询生成状态。

为此，Python 端的示例代码如下：

```
def test_video():
    headers = {
        "Authorization": "Bearer <token>",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Lightricks/LTX-Video",
        "prompt": "A gust of wind blows through the trees, causing the woman’s veil to flutter slightly.",
        "seed": 2024,
    }
    
    response = requests.request("POST", "https://api.siliconflow.cn/v1/video/submit", json=payload, headers=headers)
    if response.status_code == 200:
        rid = response.json()['requestId']
        while True:
            response = requests.request("POST", "https://api.siliconflow.cn/v1/video/status", json={"requestId": rid}, headers=headers)
            if response.status_code == 200 and response.json()['status'] == 'Succeed':
                return response.json()['results']['videos'][0]['url']
            time.sleep(5)
```


> 需注意的是：LTX-Video 也支持`图生视频`，但如果用 SiliconCloud 的API，`文生视频`免费，`图生视频`是要付费的哦。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0d3d7bb1bf3b47b197cbf235912e407e.png)

## 4. 接入微信机器人

前端时间，搭建了一个微信机器人-`小爱`，接入的视频生成能力，来自本地部署的 CogVideo。

现在，无论从生成质量，还是生成速度，都有必要把 CogVideo 换了。

流程还是一样：首先采用 LLM 润色，得到英文提示词，然后交由视频生成模型。

来看看测试效果吧：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d0fdf2758aa4449c800aeb190fed7a8a.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1fd856f31df244b2974d93c1e601e787.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9f7a66252f4e4c23ae82f4cf13fb1fd2.png)

## 写在最后

本文带大家实操体验了最新开源的**AI 视频生成**项目，LTX-Video，并成功接入了微信机器人-`小爱`，邀你围观体验。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，`小爱`也在群里，公众号后台「联系我」，拉你进群。

