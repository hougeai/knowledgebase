前段时间，分享了`低延迟小智AI服务端搭建`的 ASR、LLM 和 TTS 部分：
- [低延迟小智AI服务端搭建-ASR篇](https://zhuanlan.zhihu.com/p/1895438759719306293)
- [低延迟小智AI服务端搭建-ASR篇（续）](https://zhuanlan.zhihu.com/p/1896830194364445963)
- [低延迟小智AI服务端搭建-LLM篇](https://zhuanlan.zhihu.com/p/1897978035438874729)
- [低延迟小智AI服务端搭建-TTS篇](https://zhuanlan.zhihu.com/p/1900125186654700030)

这三个环节中，**成本最高的当属 TTS**。

`本地TTS`系列，模型选择的要求如下：

- **RTF<1** 
- **支持流式推理**
- **支持音色克隆**

目前，已更新两篇：

[低延迟小智AI服务端搭建-本地TTS篇：FishSpeech流式推理](https://zhuanlan.zhihu.com/p/1906675335778514702)

[低延迟小智AI服务端搭建-本地TTS篇：CosyVoice流式推理](https://zhuanlan.zhihu.com/p/1907352746098680072)

本篇，继续实测 `SparkTTS`，一款只需 3 秒音频即可音色克隆的 TTS。

聊聊如何优化推理延时。

## 1. 关于 SparkTTS

本地部署 `SparkTTS` 并搭建音色克隆服务，笔者之前有分享过：[最新开源TTS语音克隆，本地部署实测！跨语言、高保真](https://zhuanlan.zhihu.com/p/28969033095)。

有朋友问：`SparkTTS` 的 RTF 远大于 1，怎么会出现在`本地TTS`系列？

来看下面这张架构图，你就明白了：

![](https://i-blog.csdnimg.cn/img_convert/ec65fb9da7a23d719cc733b94de69270.png)

你看，`SparkTTS` 也是基于 LLM 的 TTS 模型，而大模型这部分，显然可以用 vLLM / SGlang / TensorRT-LLM 等推理引擎，实现推理加速。

**为什么选 vLLM？**

 加速性能不输其它框架，配置相对简单。

不多说，来测测看。

## 2. 推理加速

以下测试，均以单张 **RTX 4080** 显卡为推理设备，供参考。

### 2.1 原始推理

`SparkTTS` 支持两种形式的语音合成：

- 使用预训练的音色进行语音合成：
```
get prompt time: 0.000s
tokenize time: 0.012s
llm generate time: 6.537s
audio detokenize time: 1.694s
yield speech len 2.94, rtf 2.804
```

- 使用参考音频实现音色克隆：

```
get prompt time: 1.268s
tokenize time: 0.010s
llm generate time: 4.450s
audio detokenize time: 1.245s
yield speech len 2.82, rtf 2.473
```

你看，无论哪种方式，延时主要在 LLM 生成 token 部分，其中`音色克隆`因为不需要生成`<|bicodec_global_id|`，故延时相对小一些。

但 RTF 远远达不到实时应用要求。

### 2.2 vLLM 推理加速

`SparkTTS` 中采用的 LLM 是标准的 Qwen-2.5-0.5B。

在预训练权重的 config.json 可以看到该模型的描述：

![](https://i-blog.csdnimg.cn/img_convert/6109edab4dd27d6e786ff6ef3baa19c1.png)

vLLM 天然支持 "Qwen2ForCausalLM" 。

因此，更换推理方式，只需如下两步：

**Step 1**: 首先，替换模型加载方式。

vLLM 加载模型有两种方式：分别支持同步推理和异步推理，其中后者是 LLM 流式输出的关键。

同步推理相对简单：

```
from vllm import LLM
self.model = LLM(f"{self.model_dir}/LLM", device=self.device, gpu_memory_utilization=0.8)
```

异步推理需要引入 AsyncLLMEngine：

```
from vllm import AsyncEngineArgs, AsyncLLMEngine
engine_kwargs = dict(
    model=f"{self.model_dir}/LLM",
    max_model_len=32768,
    gpu_memory_utilization=0.9,
    device=self.device,
    dtype='bfloat16',
)
async_args = AsyncEngineArgs(**engine_kwargs)
self.model = AsyncLLMEngine.from_engine_args(async_args)
```

**Step 2**: 修改模型生成部分代码。

同步推理相对简单：

```
output_generator = self.model.generate(
    prompts={"prompt_token_ids": model_inputs.input_ids[0]},
    sampling_params=self.sampling_params
)
predicts = output_generator[0].outputs[0].text
```

异步推理，取最后一步结果：

```
output_generator = self.model.generate(
    prompt={"prompt_token_ids": model_inputs.input_ids[0]},
    sampling_params=self.sampling_params,
    request_id=uuid.uuid4()
)
async for output in output_generator:
    pass
predicts = output.outputs[0].text
```


最后，看下 vLLM 加速后的推理耗时：

```
Processed prompts: [00:00<00:00,  1.32it/s, est. speed input: 21.07 toks/s, output: 263.36 toks/s]

llm generate time: 0.763s

yield speech len 3.2, rtf 0.6169003774994053
```

模型输出吞吐量达到 `263.36 toks/s`，推理耗时从 **6.537s -> 0.763s**，实在恐怖！

RTF 直接干到 1 以下，完美解决实时应用需求！


### 2.2 vLLM INT8 量化

此外，为了进一步降低推理延时，笔者还尝试了模型的 INT8 量化。

vLLM 框架目前已支持多种主流的量化方法，以笔者使用的 0.7.3 版本为例：
> [https://docs.vllm.ai/en/v0.7.3/features/quantization/index.html](https://docs.vllm.ai/en/v0.7.3/features/quantization/index.html)

![](https://i-blog.csdnimg.cn/img_convert/b6aa01f81cb0a1184191efe0a6d13497.png)

本次量化采用 SmoothQuant 方法 - ”激活+权重“的8比特量化，vLLM 官方提供了示例代码：[https://github.com/vllm-project/llm-compressor/tree/main/examples/quantization_w8a8_int8](https://github.com/vllm-project/llm-compressor/tree/main/examples/quantization_w8a8_int8)


通常，模型量化需要以下三步：
- 加载模型
- 准备校准数据
- 应用量化

其中，最关键的是准备校准数据，须模型推理所使用的数据，否则量化后的进度无法保证。

然而，原始的 `Qwen-2.5` 专为文本生成任务，`SparkTTS` 中采用的 LLM，词表已经为语音合成任务，进行了针对性设计。

所以，我们需手动生成一批校准数据：

```
def prepare_data():
    from cli.SparkTTS import SparkTTS
    model = SparkTTS('./pretrained_models/Spark-TTS-0.5B')
    results = []
    for i in range(512):
        gender = random.choice(['male', 'female'])
        pitch = random.choice(['very_low', 'low', 'moderate', 'high', 'very_high'])
        speed = random.choice(['very_low', 'low', 'moderate', 'high', 'very_high'])
        text = random.choice(['Hello, my name is Spark-TTS. How can I help you?', 'I want to book a flight to New York. Can you help me?']) 
        prompt = model.process_prompt_control(gender=gender, pitch=pitch, speed=speed, text=text)
        model_inputs = model.tokenizer(prompt, return_tensors=None)
        result = {"input_ids": model_inputs.input_ids, "attention_mask": model_inputs.attention_mask}
        results.append(result)
    with open('data/data.json', 'w') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
```

确保你的每条数据格式如下，即可作为模型输入：

```
{'input_ids': [151644, 8948], 'attention_mask': [1, 1]}
```



然后，在示例代码中，替换数据集为刚刚生成的数据：

```
from datasets import load_dataset
ds = load_dataset("data/", split="train")
```

最后，开始量化并保存模型权重：

```
recipe = [
    SmoothQuantModifier(smoothing_strength=0.5),
    GPTQModifier(targets="Linear", scheme="W8A8", ignore=["lm_head"]),
]
# Apply quantization
oneshot(
    model=model,
    dataset=ds,
    recipe=recipe,
    max_seq_length=32768,
    num_calibration_samples=512,
)
save_dir = './pretrained_models/Spark-TTS-0.5B/LLM_sq'
model.save_pretrained(save_dir, save_compressed=True)
tokenizer.save_pretrained(save_dir)

```

量化日志如下：逐层 per_channel 量化，完成大概需要 8 mins。

![](https://i-blog.csdnimg.cn/img_convert/e6de0f1e4951dd3d24a1cc47dcad1f2f.png)


量化成功，问题来了：**延时能降多少**？

你看：

```
Using CutlassScaledMMLinearKernel for CompressedTensorsW8A8Int8
Processed prompts:[00:00<00:00,  1.25it/s, est. speed input: 20.04 toks/s, output: 231.75 toks/s]

llm generate time: 0.801s

yield speech len 3.2, rtf 0.6169003774994053
```

非常遗憾，一顿操作，量化了个寂寞。

量化后，支持的并发数量有所上升，但**推理延时并没有降低啊**！

难道是模型太小，量化带来的增益不明显？

懂的朋友，评论区求教啊！

## 3. 首包响应延时实测

和前两篇一样，我们还是把模型封装成服务，供客户端测试。

同样，我也实现了参考音频编码缓存，思路和前两篇一样，不再赘述。

采用 vLLM 加速后的模型，gpu_memory_utilization 调到最大，显存全部占满。

首包延时 **约 0.5s**：

![](https://i-blog.csdnimg.cn/img_convert/c8a37e67ced49e076a2d8f6c09568d82.png)

转成 wav 音频时，注意 `SparkTTS` 的音频采样率为 16K：

```
ffmpeg -f s16le -ar 16000 -ac 1 -i tts.pcm tts.wav
```

## 写在最后

本文分享了`小智AI服务端 本地TTS`的实现，对 `SparkTTS` 采用 vLLM 进行推理加速，并实践了 INT8 量化，最后对首包延时进行了实测。

如果对你有帮助，欢迎**点赞收藏**备用。

截止目前，`SparkTTS` 的首包延时是最低的，**约 0.5s**。

后续，我们将继续实测更多低延迟、支持流式推理的 TTS 模型！

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。
