前段时间，给微信 AI 小助理-小爱接入了文生视频的能力：

[我把「国产Sora」接入了「小爱」，邀你免费体验](https://blog.csdn.net/u010522887/article/details/142625882)

采用的是智谱开源的 CogVideo 模型，最近开源社区新出了一款视频生成模型 - `pyramid-flow-sd3`，社区反馈效果要优于 CogVideo。

今日分享，手把手带大家在本地部署，实测看看是否如宣传一般惊艳。

## 1. Pyramid Flow 简介
> 项目地址：[https://github.com/jy0205/Pyramid-Flow](https://github.com/jy0205/Pyramid-Flow)

老规矩，先来简单介绍下~

Pyramid Flow 有哪些亮点？
- 仅需 2B 参数，可生成768p分辨率、24fps的10秒视频；
- 支持「文本到视频」 和 「图像到视频」 ；
- 自回归生成，基于先前帧来预测生成后续帧，确保视频内容的连贯性和流畅性；
- 金字塔式的多尺度架构，在不同分辨率的潜变量之间进行插值，因此生成效率更高：
![](https://img-blog.csdnimg.cn/img_convert/ae2a0e8bde872f277e36721c278dd99a.png)


官方评测结果：除了`semantic score`，其它指标均优于开源方案 CogVideo：

![](https://img-blog.csdnimg.cn/img_convert/f9278471337ef54a8dae6f819b30139e.png)


## 2. 在线体验
> 在线体验地址：[https://huggingface.co/spaces/Pyramid-Flow/pyramid-flow](https://huggingface.co/spaces/Pyramid-Flow/pyramid-flow)

Pyramid Flow 已上线 huggingface，无需本地部署，即刻在线体验！

如无法访问，可参看官方的生成样例：[https://pyramid-flow.github.io/](https://pyramid-flow.github.io/)

接下来，我们把模型在本地跑起来。

## 3. 本地部署

### 3.1 环境准备

首先准备 Pyramid Flow 环境：

```
git clone https://github.com/jy0205/Pyramid-Flow
cd Pyramid-Flow
conda create -n pyramid python==3.8.10
conda activate pyramid
pip install -r requirements.txt
```

然后，把模型下载到本地，方便调用：

```
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download rain1011/pyramid-flow-sd3 --local-dir ckpts/
```

其中，模型权重包括 768p 和 384p 两种版本。384p版本支持 5 秒长的 24 FPS视频，而 768p 版本则可以生成 10 秒。

### 3.2 推理测试

首先，加载模型进来：

```
import os
import torch
from PIL import Image
from pyramid_dit import PyramidDiTForVideoGeneration
from diffusers.utils import export_to_video

os.environ['CUDA_VISIBLE_DEVICES'] = '2'

model = PyramidDiTForVideoGeneration('ckpts/', 'bf16', model_variant='diffusion_transformer_384p')

model.vae.enable_tiling()
# model.vae.to("cuda")
# model.dit.to("cuda")
# model.text_encoder.to("cuda")
# if you're not using sequential offloading bellow uncomment the lines above ^
model.enable_sequential_cpu_offload()
```

如果把模型都加载进 GPU，至少需要 19G 显存，否则建议采用上述代码！

然后，测试**文本生成视频**：

```
def t2v():
    prompt = "A movie trailer featuring the adventures of the 30 year old space man wearing a red wool knitted motorcycle helmet, blue sky, salt desert, cinematic style, shot on 35mm film, vivid colors"
    with torch.no_grad(), torch.amp.autocast('cuda', dtype=torch.bfloat16):
        frames = model.generate(
            prompt=prompt,
            num_inference_steps=[20, 20, 20],
            video_num_inference_steps=[10, 10, 10],
            height=384,     
            width=640,
            temp=16,                    # temp=16: 5s, temp=31: 10s
            guidance_scale=9.0,         # The guidance for the first frame, set it to 7 for 384p variant
            video_guidance_scale=5.0,   # The guidance for the other video latent
            output_type="pil",
            save_memory=True,           # If you have enough GPU memory, set it to `False` to improve vae decoding speed
        )
    export_to_video(frames, "./text_to_video_sample.mp4", fps=24)
```
测试**图片生成视频**：
```
def i2v():
    image = Image.open('assets/the_great_wall.jpg').convert("RGB").resize((640, 384))
    prompt = "FPV flying over the Great Wall"
    with torch.no_grad(), torch.amp.autocast('cuda', dtype=torch.bfloat16):
        frames = model.generate_i2v(
            prompt=prompt,
            input_image=image,
            num_inference_steps=[10, 10, 10],
            temp=16,
            video_guidance_scale=4.0,
            output_type="pil",
            save_memory=True,           # If you have enough GPU memory, set it to `False` to improve vae decoding speed
        )
    export_to_video(frames, "./image_to_video_sample.mp4", fps=24)
```

Pyramid Flow 对显存要求较高，否则生成 5 秒视频，至少 13 分钟：

```
100%|████| 16/16 [13:11<00:00, 49.45s/it]
```

生成效果咋样？


[video(video-KxAcd3Fb-1730075465441)(type-csdn)(url-https://live.csdn.net/v/embed/430176)(image-https://img-blog.csdnimg.cn/img_convert/96dfe088361250e483f3d049be2aa407.jpeg)(title-pyramid_flow_t2v)]


实测来看，并未和 CogVideo 拉开差距。。。

## 写在最后

本文带大家本地部署并实测了最新开源的视频生成模型 - `Pyramid Flow`。

AI 应用大体可分为：文本、语音、图片、视频，其中语音已被硅基生物攻破。

而 AI 视频生成，从当前效果来看。。。依然任重道远！

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。

