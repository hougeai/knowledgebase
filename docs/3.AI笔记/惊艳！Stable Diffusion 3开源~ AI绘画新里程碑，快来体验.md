
继 ComputeX 2024 上宣布 6 月 12 日将发布 Stable Diffusion(SD) 3 模型，Stability.AI 果然没有跳票，按时开放了 SD3 的中型模型-Medium。

就在刚刚，SD3 Medium 如约而至。

### 笔记本也能玩的 SD3 Medium

据 Stability AI 官方博客介绍，SD3 Medium 模型包含 20 亿个参数，却能够生成更高质量的图像。

由于模型尺寸较小，SD3 Medium 尤其适合在消费级 GPU 上运行，平均生成图片时间在2—10秒左右推理效率非常高。

第一波下载模型的网友已经开始玩疯了~ 给大家展示几张生成效果图：
【图片】

### SD3 Medium 有哪些亮点？

SD3 Medium 代表了生成式 AI 发展的一个重大里程碑，坚持了 AI 民主化这一强大的技术承诺。SD3 Medium 突出之处：

- **照片级真实**：克服了手和脸部常见的伪影问题，无需复杂流程即可生成高质量图像。

- **指令遵循**：能够理解涉及空间关系、构图元素、动作和风格的复杂提示语。

- **图文混排**：借助 DiT 架构，可以无伪影且无拼写错误地生成前所未有的文本。

- **容易微调**：能够从小型数据集中吸收细微细节，非常适合定制。

### SD3 Medium 有哪些更新？
## 架构细节
对于文本到图像生成，模型须同时考虑文本和图像两种模态，这种新架构被称为 MMDiT，指的是其能够处理多种模态。

与之前的 Stable Diffusion 不同的是，使用三种不同的文本嵌入器——两个 CLIP 模型和 T5 来编码文本表示，并使用一种改进的自动编码模型来编码图像。

SD3 架构建立在扩散变换器(Diffusion Transformer,"DiT")的基础之上，与Sora相同。
【图片】

由于文本和图像嵌入在概念上存在很大差异，SD3 为这两种模态使用了两套独立的权重，在注意力操作时将两种模态的序列连接起来。

通过使用这种方法，图像和文本 tokens 之间的信息可以相互流动，从而提高生成输出的整体理解能力和图文混排质量。

## 训练数据
据了解，在训练 SD3 Medium 上，Stability AI 还是花了不少心思的。

训练数据包括两个部分：合成数据和筛选过的公开数据。预训练数据达到了惊人的 10 亿张图片。

此外，微调数据集包含 3000 万张针对特定视觉内容和风格的高质量美学图片，以及 300 万张基于偏好的数据图片。

【图片】

### SD3 Medium 在哪体验？
> 模型地址：https://huggingface.co/stabilityai/stable-diffusion-3-medium
>
> 在线体验：https://huggingface.co/spaces/stabilityai/stable-diffusion-3-medium


模型权重可以到上方模型地址获取。 

权重文件的结构如下：
```
├── comfy_example_workflows/
│   ├── sd3_medium_example_workflow_basic.json
│   ├── sd3_medium_example_workflow_multi_prompt.json
│   └── sd3_medium_example_workflow_upscaling.json
│
├── text_encoders/
│   ├── README.md
│   ├── clip_g.safetensors
│   ├── clip_l.safetensors
│   ├── t5xxl_fp16.safetensors
│   └── t5xxl_fp8_e4m3fn.safetensors
│
├── LICENSE
├── sd3_medium.safetensors
├── sd3_medium_incl_clips.safetensors
├── sd3_medium_incl_clips_t5xxlfp8.safetensors
└── sd3_medium_incl_clips_t5xxlfp16.safetensors
```
上述权重文件结构怎么理解？

SD3 Medium 提供了三种封装，每种封装都具备相同的 MMDiT 和 VAE 权重，每种封装的区别如下：

- **sd3_medium.safetensors** 包含 MMDiT 和 VAE 权重，但不包括任何文本编码器。
- **sd3_medium_incl_clips_t5xxlfp16.safetensors** 包含所有必需的权重，包括 T5XXL 文本编码器的 fp16 版本。
- **sd3_medium_incl_clips_t5xxlfp8.safetensors** 包含所有必需的权重，包括 T5XXL 文本编码器的 fp8 版本。
- **sd3_medium_incl_clips.safetensors** 包含所有必需的权重，除了 T5XXL 文本编码器。它的资源需求最低，但是模型的性能将因为缺少 T5XXL 文本编码器而有所差异。
- **text_encoders** 文件夹包含三个文本编码器。
- **example_workfows** 文件夹包含示例 comfyui 工作流程。

### 写在最后

总的来说，Stable Diffusion 3 可以说是AI生图领域的里程碑式的存在，不仅在技术上进行了重大改进，而且免费开源，相信更多的开发者会基于这一强大模型开发出更多有意思的应用。

目前市面上已经出现了很多免费的AI绘画工具，其底层模型基本都是 Stable Diffusion。

为了帮助大家更好上手，猴哥会单独出一个专栏，分享如何免费使用这些工具。

欢迎追更！
