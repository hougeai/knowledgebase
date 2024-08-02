不得不说，AI 视频生成界最近非常火热~

前有快手「可灵」开放内测，一下子带火了老照片修复，全网刷屏：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-61a311d6889558718d4bbaeba2177c13_1440w.png)





添加图片注释，不超过 140 字（可选）

怕是你还没拿到内测资格，被称为 “国货之光” 的「可灵」就结束了免费无限量模式。每天只有66点的免费额度，对应 6 次 5 秒视频，也就够你尝个鲜~

就在昨天，国产大模型头部玩家**智谱**震撼出手，推出了自家的视频生成工具 -「清影」，底层是自家的视频生成大模型 CogVideo。

划重点：**全民免费，不用排队，不限次数！** 连 API 都开放了，开发者的福音。

生成速度怎么样？

据官方介绍，6s 的 1440x960 视频，只需 30s，这推理速度，杠杠的~

要知道，前天分享的 [EasyAnimate-v3 实测，阿里开源视频生成模型，支持高分辨率超长视频](https://zhuanlan.zhihu.com/p/710131990)，猴哥本地亲测，足足需要 188s !

话不多说，上链接，感兴趣的小伙伴可以去试试~

> https://chatglm.cn/video

## 实测体验

首次使用，需要申请内测资格，不到 5 分钟就审核通过了。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-17222afc1bb78b9686e538a145b554fd_1440w.png)





添加图片注释，不超过 140 字（可选）

## 功能介绍

目前支持「文生视频」和「图生视频」，两个 Tab 切换，非常简洁，简单是小白零门槛。

- 文生视频：只需要输入提示词，选择视频风格、情感氛围、运镜方式，点「生成视频」即可

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-cbda1ef38fadc46b8b131ca58b0efce6_1440w.png)





添加图片注释，不超过 140 字（可选）

- 图生视频：需要上传一张底图，输入提示词，点「生成视频」即可。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-a3e9f1ee9e5c51d8075a4c9efcb0d82b_1440w.png)





添加图片注释，不超过 140 字（可选）

万事俱备，只差输入提示词了~ 可是：我不会写提示词，怎么办？

其实，无论是 AI 对话，AI 绘画，还是这里的 AI 视频生成，提示词的套路都有一个核心原则:

那就是：**结构化**！结构化还有一个好处，就是让你的思路变得条理清晰。

对于 AI 视频生成 而言：

- 简单结构：[摄像机移动]+[建立场景]+[更多细节] 
- 复杂结构：[镜头语言] + [光影] + [主体 (主体描述)] + [主体运动] +[场景 (场景描述)] +[情绪/氛围/风格] 

为了帮助大家写好 提示词，官方还贴心地出了份文档，需要的小伙伴可以前往查看：

> https://zhipu-ai.feishu.cn/wiki/MFxywuqcbiKmOrkXwJzcEuqwnJd

怕你连文档都没时间看，官方直接制作了两个「帮你写提示词」的智能体！免费取用~

- 文生视频：https://chatglm.cn/main/gdetail/669911fe0bef38883947d3c6

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-9e05af085e2fd410d95ba536344dc361_1440w.png)





添加图片注释，不超过 140 字（可选）

输入简单的描述，智能体就给出了 3 个不同风格的提示词。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-9e00b2546d03273f9856925b54969772_1440w.png)





添加图片注释，不超过 140 字（可选）

“您是否需要更换 3 个风格？” 不满意，随意换！

- 图生视频：https://chatglm.cn/main/gdetail/669fb16ffdf0683c86f7d903

使用方法也是类似的，输入图像主体，选择一个风格即可。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-09bffb01f068f3ffabb83da3965a20ce_1440w.png)





添加图片注释，不超过 140 字（可选）

就目前的体验而言，尽管视频只有6s，无论从流畅度、可控性来看，基本可以达到以假乱真的程度了，那么「清影」是怎么做到的？

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-9aca5e011ce863fb2533e4dbf10ceb9c_1440w.png)





添加图片注释，不超过 140 字（可选）

## API 调用

对于开发者而言，最关心的还是：有没有开放的 API，方便集成到自己的应用中。

答案是肯定的，前往智谱 AI 开放平台注册一个账号，新用户会赠送 18 元额度，后续使用中注意账户余额哦，不过体验是绰绰有余了~

>  智谱 AI 开放平台：https://open.bigmodel.cn/ 

接下来，需要拿到智谱的 API Key。

如果之前注册过，直接在这里取用：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-6f5aa98e89f11192d58f636b29312145_1440w.png)





添加图片注释，不超过 140 字（可选）

如果没有，点击这里，新生成一个：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-69e69543159f8d33f8a6ea9556dd6047_1440w.png)





添加图片注释，不超过 140 字（可选）

拿到 API Key 之后，我们前往模型中心，发现CogVideoX已经上线了：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-85e71e57ddecdc48ae2b979d38707178_1440w.png)





添加图片注释，不超过 140 字（可选）

由于视频生成时间较长，所以该接口是异步调用的。

也就是返回给你的是一个任务订单号-id，然后你根据这个 id 去查询是否生成成功。

这里我们以 Python 为例，实现 文生视频 功能：

```
from zhipuai import ZhipuAI
  client = ZhipuAI(api_key="") # 请填写您自己的APIKey

  response = client.videos.generations(
    model="cogvideox",
    prompt="比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"
)
print(response)
```

如果是图生视频，还需要传入底图的 image_url，支持通过 URL 或 Base64 编码传入图片，图片大小不超过 5 M。

返回的 response 的示例：

```
id='8868902201637896192' request_id='654321' model='cogvideox' task_status='PROCESSING'
```

接下来，我们根据这个 id 去查询结果（注意不是 request_id）：

```
from zhipuai import ZhipuAI
 client = ZhipuAI(api_key="") # 请填写您自己的APIKey

response = client.videos.retrieve_videos_result(
    id="8868902201637896192"
)
print(response)
```

返回的 response 示例：

```
{
    "model": "cogvideox",
    "request_id": "8868902201637896192",
    "task_status": "SUCCESS",
    "video_result": [
        {
            "cover_image_url": "https://sfile.chatglm.cn/testpath/video_cover/4d3c5aad-8c94-5549-93b7-97af6bd353c6_cover_0.png",
            "url": "https://sfile.chatglm.cn/testpath/video/4d3c5aad-8c94-5549-93b7-97af6bd353c6_0.mp4"
        }
    ]
}
```

## 写在最后

Sora 的出现引爆了 AI 视频生成，那时国内的视频生成工具还屈指可数~

直至今天，AI 视频生成已经在国内遍地开花，比如字节跳动的即梦（Dreamina），快手的可灵，爱诗科技的 PixVerse。

智谱的清影，继续为国产 AI 视频生成 **+ 1**！

后续打算出一篇汇总文： 盘点那些好用的 AI 视频生成工具，包括国外的、国内的；开源的、闭源的...

感兴趣的小伙伴敬请关注~
