
上篇分享了`小智AI服务端ASR`的几种实现方案，并对`本地部署-GPU推理`方案的配置和成本进行了估算。

[低延迟小智AI服务端搭建-ASR篇](https://zhuanlan.zhihu.com/p/1895438759719306293)


不可否认，`GPU推理`的成本，足以让大部分玩家却步了。

如果你：

- 对高成本及其厌恶；
- 个人玩家，不关心用户体验。

可以试试接下来的`CPU推理`方案。

本篇将首先介绍 `sherpa-onnx`，一款高性能的语音处理开源项目。

然后，选择其中的模型，实现`小智AI服务端ASR`的`实时CPU推理`。

## 1. sherpa-onnx 简介
> [https://github.com/k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)

`sherpa-onnx` 是一款跨平台、多语言的语音处理工具包，使用 onnxruntime 实现。支持的功能非常丰富，包括：

- 语音活动检测
- 语音转文本
- 文本转语音
- 说话人分割

老规矩，简单介绍下亮点：

- **跨平台兼容**：包括 Windows、macOS、Linux以及Android和iOS等操作系统。它还支持各种嵌入式系统。

- **多语言API**：提供11种主流编程语言接口。

- **高性能**：基于ONNX运行时，适合在各种计算能力的设备上部署。

## 2. 模型选择

> 模型列表：[https://k2-fsa.github.io/sherpa/onnx/pretrained_models/index.html](https://k2-fsa.github.io/sherpa/onnx/pretrained_models/index.html)

根据上篇的实测，VAD 模型参数量较少，延时可忽略。

因此，VAD 模型选择和上篇保持一致。

### 2.1 ASR 模型

要想 ASR 识别效果不拉跨，模型参数量少不了。

同时还得尽可能满足低延迟。

综上，`ASR`模型，我们可以考虑选择支持流式推理的 `paraformer`，这也是阿里云上的流式推理模型。

![](https://i-blog.csdnimg.cn/img_convert/697c476927bff3e59f148ee3b820389e.png)


### 2.2 声纹向量模型

考虑到模型参数量和推理延时正相关，为了兼顾性能和延时，可以选择 `3dspeaker_speech_campplus_sv_zh_en_16k-common_advanced`

![](https://i-blog.csdnimg.cn/img_convert/cb0815bf6e3409847a70ee34497b520d.png)


## 3. CPU 推理方案

### 3.1 模型加载

VAD 模型加载和上篇保持一致，ASR 和 声纹识别模型，采用 `sherpa-onnx` 的方式加载。

```
class ModelManager:
    def __init__(self):
        self.vad_model = None
        self.asr_model = None
        self.sv_model = None

    def load_models(self):
        self.vad_model = AutoModel(model="ckpts/speech_fsmn_vad_zh-cn-16k-common-pytorch")
       
        model_dir = "ckpts/sherpa-onnx-streaming-paraformer-bilingual-zh-en"
        self.asr_model = sherpa_onnx.OnlineRecognizer.from_paraformer(
            encoder=f'{model_dir}/encoder.int8.onnx',
            decoder=f'{model_dir}/decoder.int8.onnx',
            tokens=f'{model_dir}/tokens.txt')

        model_dir = "ckpts/3dspeaker_speech_campplus_sv_zh_en_16k-common_advanced.onnx"
        config = sherpa_onnx.SpeakerEmbeddingExtractorConfig(model=model_dir)
        self.sv_model = sherpa_onnx.SpeakerEmbeddingExtractor(config)
```

### 3.2 模型推理

服务的核心逻辑是：

当 VAD 检测到有活动音频时，asr_model 创建音频流`self.stream`：

```
if self.stream is None:
    self.stream = self.model_manager.asr_model.create_stream()
    self.input_stream(self.audio_buffer)
```

然后，每来一个音频片段，都压入音频流：


```
def on_audio_frame(self, frame):
    frame_fp32 = np.frombuffer(frame, dtype=np.int16).astype(np.float32) / 32768
    if self.stream:
        self.input_stream(frame_fp32)
```

实测发现，`streaming-paraformer`所谓的的流式推理是：每 10 个 60ms 音频会触发一次解码。

而单次解码耗时 < 0.3s。

**因此，rtf 确实可以做到 < 1。**

为此，把音频数据压入一个消费队列，进行异步处理，理论上完全可以做到实时推理。

**改造过程如下**：

首先，音频数据不再直接解码，而是实时压入队列：

```
#  self.input_stream(frame_fp32)
self.asr_queue.put(frame_fp32)
```


然后，创建一个 worker 异步消费队列中的音频：

```
def _decode_worker(self):
    while True:
        try:
            # 使用阻塞方式获取音频数据
            chunk = self.asr_queue.get(timeout=0.01)
            if self.stream:  # 确保stream存在
                self.running = True
                self.input_stream(chunk)
        except Empty:
            self.running = False  # 清除解码事件
            continue  # 队列为空时继续等待
        except Exception as e:
            logging.error(f"Error in decode worker: {e}", exc_info=True)
```

最后，声纹向量模型获取音频特征：


```
def generate_embedding(self):
    if self.audio_buffer.shape[0] == 0:
        return []
    # last 3 seconds for speaker embedding
    stream = self.model_manager.sv_model.create_stream()
    stream.accept_waveform(SAMPLE_RATE, self.audio_buffer[-SAMPLE_RATE*3:])
    stream.input_finished()
    embedding = self.model_manager.sv_model.compute(stream)
    return embedding 
```


### 3.3 延时测试
`streaming-paraformer`流式推理：每 10 个 60ms 音频会触发一次解码：

| 模型          | CPU 推理 (秒) |
|---------------|---------------|
| paraformer    | 0.09-0.25         |
| paraformer-int8 | 0.08-0.09      |


`声纹向量`模型，音频时长最长3s，单次推理：

| 模型         | CPU 推理 (秒) |
|---------------|---------------|
| 3dspeaker    | 0.09         |


### 3.4 服务器配置和成本

上述三个模型加载进来，占用内存 1.0 G+。

所以，如果不考虑高并发的情况，虚拟机配置需至少确保 2c2g。

如果考虑主流云厂商，包年包月的价格如下：

> 阿里云：[https://www.aliyun.com/minisite/goods?userCode=ggqtukm3](https://www.aliyun.com/minisite/goods?userCode=ggqtukm3)

![](https://i-blog.csdnimg.cn/img_convert/59b992dc37fdb30331544a49058c4c0b.png)

> 腾讯云：[https://curl.qcloud.com/BLm2fgkN](https://curl.qcloud.com/BLm2fgkN)

![](https://i-blog.csdnimg.cn/img_convert/342d26d819061a62bd3c37f4d2a273ac.png)


当然，如果只是想玩玩，压根没想用上一年啊。

推荐试试 `sealos` 的产品，根据使用资源，按需付费。

> 注册体验：[https://cloud.sealos.run/?uid=QDGJoX2_Qp](https://cloud.sealos.run/?uid=QDGJoX2_Qp)

新人注册送 10 元余额，足够玩一阵了。

我们以 **2c2g** 为例，并挂载一块 **20G** 的磁盘，**每天的费用大概在 1.5 元左右**，不用时关掉就好。

![](https://i-blog.csdnimg.cn/img_convert/7e8123771d7b0c26cf94000c48530026.png)


## 写在最后

本文分享了`小智AI服务端ASR`的`CPU推理`方案，并对配置和成本进行了估算。

如果对你有帮助，欢迎**点赞收藏**备用。

下篇将给出 `低延迟小智AI服务端搭建-LLM 篇`，明天见。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

