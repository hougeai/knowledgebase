前段时间，分享了`低延迟小智AI服务端搭建`的 ASR、LLM 和 TTS 部分：
- [低延迟小智AI服务端搭建-ASR篇](https://zhuanlan.zhihu.com/p/1895438759719306293)
- [低延迟小智AI服务端搭建-ASR篇（续）](https://zhuanlan.zhihu.com/p/1896830194364445963)
- [低延迟小智AI服务端搭建-LLM篇](https://zhuanlan.zhihu.com/p/1897978035438874729)
- [低延迟小智AI服务端搭建-TTS篇](https://zhuanlan.zhihu.com/p/1900125186654700030)

这三个环节中，**成本最高的当属 TTS**。

`本地TTS`系列已更新3篇：

[低延迟小智AI服务端搭建-本地TTS篇：FishSpeech流式推理](https://zhuanlan.zhihu.com/p/1906675335778514702)

[低延迟小智AI服务端搭建-本地TTS篇：CosyVoice流式推理](https://zhuanlan.zhihu.com/p/1907352746098680072)

[SparkTTS 音色克隆 + vLLM INT8量化加速推理](https://zhuanlan.zhihu.com/p/1908123507746931028)

本篇，继续实测`IndexTTS`，B 站最新开源的 TTS 模型，延时和效果都非常惊艳。

## 1. 关于 IndexTTS

IndexTTS 由 B 站在今年 3 月份推出，最近社区反响比较热烈，非常值得推荐给大家。

先来感受下 **SOTA**，吊打一众模型：

首先，错误率干到底：

![](https://i-blog.csdnimg.cn/img_convert/6b39c88ecd3431a2db8fe3aeaf11acf9.png)

![](https://i-blog.csdnimg.cn/img_convert/7d8e513e5db313362bb09e67b83abddc.png)

然后，音色克隆相似性：

![](https://i-blog.csdnimg.cn/img_convert/e277a0e538dde2d0ec536cf26837d309.png)

**怎么做的？**

看下方系统架构图，还是基于 LLM 的 TTS 算法，包括三大件：`text/audio tokenizer`, `text-speech langugae model`, `speech decoder`。

![](https://i-blog.csdnimg.cn/img_convert/5d19a30923e0f140bc8f8dd45cbc9666.png)


**有哪些亮点？**

- **产业级落地：推理不需要`参考文本`**

已有的 zero-shot 音色克隆算法，在输入`参考音频`时，通常都需要严格对应的`参考文本`，尽管有 ASR，但获取完全准确的`参考文本`依然不易。所以 IndexTTS 抛弃了这一设计，推理时只需要输入`参考音频`即可。

- **可控发音：tokenizer 引入"拼音"和"汉字"**

已有的 TTS 算法都会设计复杂的文本前端来处理待合成的文本，比如 E2TTS 就提出将英文单词和音素同时建模，受此启发，IndexTTS 在处理中文时，对于多音字，就用相应的拼音来作为输入，从而控制发音。

![](https://i-blog.csdnimg.cn/img_convert/8f45a8fd97c9b7034fa4605e9394f928.png)

为此，IndexTTS 的 text tokenizer 的词表大小为12000，其中有 8400 个汉字和 1721 个拼音，其余的为英文单词和一些特殊符号。

- **推理高效：speech decoder采用BigVGAN**

为了加速推理，IndexTTS 模型没有采用 CosyVoice 的 flow-matching 结构, 而是用 BigVGAN2 作为解码器，直接将 LLM 的最后一层 hidden state 转成音频波形。

最近，IndexTTS 更新了新版模型权重 - IndexTTS 1.5，不过模型架构没变，只是 LLM 部分 gpt2 的层数和参数量增加了。

下文实测数据，均以 IndexTTS1.0 展开。

## 2. 推理测试
> 项目地址：[https://github.com/index-tts/index-tts/](https://github.com/index-tts/index-tts/)

参考官方 README.md，装好环境，下载权重，即可完成推理测试。

```
git clone https://github.com/index-tts/index-tts.git
conda create -n index-tts python=3.10
conda activate index-tts
pip install -r requirements.txt
```

以下是在 **RTX 4080** 显卡上，原始模型的推理日志：

```
>> Reference audio length: 11.88 seconds
>> gpt_gen_time: 15.74 seconds
>> gpt_forward_time: 0.12 seconds
>> bigvgan_time: 0.86 seconds
>> Total inference time: 16.85 seconds
>> Generated audio length: 28.93 seconds
>> RTF: 0.5825
```

你看，除了生成效果出色，IndexTTS 的 `RTF` 依然吊打一众开源模型！

在没有任何加速加持下，`RTF` 已小于 1。

## 3. 加速推理

由于模型效果出色，社区出现了各种加速推理方案，笔者实测后，数据统计如下：

![](https://i-blog.csdnimg.cn/img_convert/fd0794b650ec67ec6d3d1f4cf0b223a5.png)

测试环境：
- 参考音频：11.88s；
- 生成音频：28.93 - 31.15s；
- 推理设备：RTX 4080 16G

此外，模型每次推理都需要处理参考音频，以 11.88s 的参考音频为例，这部分的耗时统计如下：

![](https://i-blog.csdnimg.cn/img_convert/2ca6d70be481a4186246738e1792f6f4.png)

显然，这部分 0.3-0.4s 的延时也可以干掉！

## 4. 流式推理服务

为了和云端 TTS 的 API 接口对齐，需封装一个 webscoket 服务，接收 fastapi 服务输出的音频流，并发送给客户端。

实现思路和前几篇一样，不再赘述。

## 5. 硬件配置和响应延时

采用 vllm 加速，gpu_memory_utilization 设置为 0.5，服务启动后的显存占用情况：

![](https://i-blog.csdnimg.cn/img_convert/aaa61f95adb2e823b8971eb8591ec5a3.png)

因为 vllm 会保留 kv 缓存，显存占用相比原模型高了近一倍。

以下是在 **RTX 4080** 显卡上，流式推理，首个音频包到达客户端的延时情况。

参考音频编码缓存的情况下，首包延时 **不到0.5s**：

![](https://i-blog.csdnimg.cn/img_convert/e195ef46e8648a37d78ed8565497c14c.png)

![](https://i-blog.csdnimg.cn/img_convert/466a4f54fcb6a4030dd346457273fb73.png)

## 写在最后

本文分享了`小智AI服务端 本地TTS`的实现，对`IndexTTS`的首包延时进行了实测。

如果对你有帮助，欢迎**点赞收藏**备用。

从 FishSpeech、CosyVoice、SparkTTS，到 IndexTTS，首包延时终于到 0.5s 以内了。

后续，我们将继续实测更多低延迟、支持流式推理的 TTS 模型，大家有推荐的，评论区聊！

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。


