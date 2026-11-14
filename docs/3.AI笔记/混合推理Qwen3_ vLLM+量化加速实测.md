一个月前，阿里发布了 Qwen3 模型，同样是登顶全球最强开源模型。

但，社区反响却远不如 Qwen2.5 的发布。

也许，是大家对它的期待太高了。

即便如此，Qwen3 的开源，依旧可圈可点。

本文，对 Qwen3 进行本地部署实测，为各位技术选型提供参考。

## 1. Qwen3 有哪些亮点

`Qwen3` 共 8 款模型，包括6款 Dense 模型和2款 MoE 模型：

![](https://i-blog.csdnimg.cn/img_convert/cb0cacbb520481195a72ff814d11d511.jpeg)

混合专家（MoE）架构是其最大亮点，以最大的 `235B-A22B` 为例，模型总参数量有 235B，但激活部分只有 22B，从显存占用和推理延时来看，都非常有吸引力。

模型训练包括：预训练和后训练两个阶段。

重点在后训练部分，小模型就是在后训练部分，通过大模型蒸馏得到的：

![](https://i-blog.csdnimg.cn/img_convert/58405c2cf23c55aa232ade4ca1ee1fb5.png)

### 1.1 国内首个“混合推理模型”

将`慢思考`与`快思考`集成到同一个模型。

相当于是 `QwQ` 和 `Qwen2.5` 的综合体。 

在同一模型内无缝切换：
- **思考模式**：适用于复杂的逻辑推理、数学和编码；
- **非思考模式**：适用于高效、通用的对话。

且，

在数学、代码生成和常识逻辑推理方面，超越了 `QwQ`（思考模式）和` Qwen2.5` 指令模型（非思考模式）。

### 1.2 精通代理能力

原生支持外部工具调用，并在复杂代理任务中达到开源模型中的领先性能。

### 1.3 多语言支持

预训练数据高达 36T Tokens，包含119种语言和方言。

所以，原生支持 100 多种语言，例如简体中文、繁体中文、粤语等，具备强大的多语言指令执行和翻译能力。

以上三点，在笔者看来，都非常亮眼，下面我们用 vLLM 在本地部署起来，实测效果如何。

## 2. vLLM 部署实测
> 官方文档：[https://docs.vllm.ai/en/latest/](https://docs.vllm.ai/en/latest/)

关于 vLLM 的安装使用，之前教程有介绍过。

本篇重点关注：如何开启和关闭思考模式，以及如何进行工具调用。


### 2.1 模型下载

vLLM 支持从 huggingface/modelscope 等平台下载的模型文件。

以下载`Qwen/Qwen3-0.6B`为例：

```
# 从 modelscope 下载
modelscope download --model Qwen/Qwen3-0.6B --local_dir ./ckpts/qwen3-0.6b
# 或者
# 从 huggingface 下载
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download Qwen/Qwen3-0.6B --local-dir ./ckpts/qwen3-0.6b
```

### 2.2 启动推理服务

`Qwen3` 需在最新版 vLLM 中才提供支持，版本太低会报错：

```
Model architectures ['Qwen3ForCausalLM'] failed to be inspected
```

此外，注意当前目录下不要有 `vllm` 目录和 `vllm.py`，避免模块引入冲突。


安装成功后，可通过如下命令查看各个参数的含义：

```
vllm serve --help # 查看指令  --max-num-seqs
```

还以`Qwen/Qwen3-0.6B`为例，启动命令如下：

```
export CUDA_VISIBLE_DEVICES=0
MODEL="qwen3-0.6b"
nohup vllm serve ckpts/$MODEL --api-key 123 --port 3002 --tensor-parallel-size 1 --max-model-len 8192 --served-model-name $MODEL > logs/vllm-$MODEL.log 2>&1 &
```

如果显存不够，重点关注以下几个参数：
- `--tensor-parallel-size`：如果显存都不足以加载模型权重，就需要多卡负载；
- `--max-model-len`：模型输出长度，决定了 kv cache，这部分同样要占用显存，如果显存不够，可以降低这个参数。
- `--max-num-seqs`：vLLM在初始化引擎时会默认进行256个并发的虚拟测试。

> `Qwen3`原生支持最长 32,768 的上下文长度。在模型权重文件的 `config.json` 中可以看到 max_position_embeddings 默认为 40,960。输出预留 32,768 个令牌，以及提示词预留 8,192 个令牌。


### 2.3 关闭/开启思考模式

对于逻辑推理、数学和编码等任务，需要开启`思考模式`。

这一模式由 Deepseek-R1 带来，也就是前置的推理过程：

```
<think>
...
</think>
```

要知道，这部分会带来极大的延时。

对于简单的对话应用来说，压根不需要这个推理过程。

比如一句简单的问候`你好`，这种场景显然不需要`thinking`：
```
# 开启 thinking
<think>
嗯，用户发来“你好”，这是一个常见的问候语。首先，我需要确认用户的需求是什么。可能他们只是想测试我的反应，或者有具体的问题需要帮助。
</think>

你好！很高兴见到你！😊 有什么我可以帮你的吗？无论是解答问题、提供建议，还是闲聊，我都很乐意帮忙！
耗时： 3.062495231628418
# 关闭 thinking
你好！很高兴见到你。有什么我可以帮你的吗？😊
耗时： 0.27060484886169434
```

你看，关闭`thinking`，耗时只有原来的 1/10.

**如何关闭它？**

有两种方式：

**1. 软关闭**

也即在调用时关闭：入参`{"enable_thinking": False}`

![](https://i-blog.csdnimg.cn/img_convert/87c4b04cdc5c15d0f5e6482f98ebe6b4.png)

```
def single_request_nothinking():
    response = client.chat.completions.create(
        model="qwen3-14b-int4",
        messages=[{'role': 'user', 'content': '1995年七月初十生，今年是2025年，了解未来五年的运势'}],
        stream=False,
        temperature=0.7,
        top_p=0.8,
        presence_penalty=1.5,
        extra_body={
            "top_k": 20, 
            "chat_template_kwargs": {"enable_thinking": False},
        },
    )
    print(response.choices[-1].message.content)
```

**2. 硬关闭**

也即在部署时就关闭`thinking`！
> 参考：[https://qwen.readthedocs.io/en/latest/deployment/vllm.html#thinking-non-thinking-modes](https://qwen.readthedocs.io/en/latest/deployment/vllm.html#thinking-non-thinking-modes)

只需在上述启动命令的基础上加一个输入模板参数：
```
--chat-template data/qwen3_nonthinking.jinja 
```

注意：请求参数需参考官方建议：

```
response = client.chat.completions.create(
        model="qwen3-14b-int4",
        messages=[{'role': 'user', 'content': '你好'}],
        stream=False,
        temperature=0.7,
        top_p=0.8,
        presence_penalty=1.5,
        extra_body={
            "top_k": 20, 
        },
    )
```


### 2.4 支持工具调用
> 参考：[https://qwen.readthedocs.io/en/latest/deployment/vllm.html#parsing-tool-calls](https://qwen.readthedocs.io/en/latest/deployment/vllm.html#parsing-tool-calls)

只需在上述启动命令的基础上加两个参数：

```
--enable-auto-tool-choice --tool-call-parser hermes 
```
> 注：实测发现，**14b 以及以下的模型**，工具调用的成功率，太低了，几乎不可用。

## 3. 显存占用情况

以笔者的 RTX 4080 16G 为例：8b 及以上模型需采用量化版模型。

**量化能节省多少显存？**

- int4 大约为原模型的1/4
- int8 大约为原模型的1/2

**量化会带来多少精度损失？**
- 8位权重-激活量化（W8A8）和4位权重量化（W4A16）能够在大多数任务中实现无损性能。
- 但量化误差会随着推理长度的增加而累积。

**量化方法怎么选？**
- AWQ 在权重量化中表现最佳，其性能与GPTQ相当，但实现更高效。


**不同尺寸模型显存占用如何？**
- `Qwen3-4B`：16G x 1
- `Qwen3-8B`：16G x 2
- `Qwen3-14B-Int4`：16G x 1，不过 `max-model-len` 不能超过 22,064
- `Qwen3-30B-A3B-Int4`：16G x 4
- `Qwen3-32B-Int4`：16G x 4


## 4. 推理速度测试

以 `Qwen3-14B-Int4` 为例：

单发测试：

![](https://i-blog.csdnimg.cn/img_convert/3dc93b031ec752f21be72f5de194273d.png)

并发测试（20）：
![](https://i-blog.csdnimg.cn/img_convert/3be98cdab5532dfefade307e6e4362f3.png)

并发测试（256）：

![](https://i-blog.csdnimg.cn/img_convert/1f42b8d28a72257c3eb2f1f0599aedd2.png)

输出来到了恐怖的 `2000+ tokens/s`！


如果不接入任何函数调用，流式输出，首包延时**不到 0.3 s**：

![](https://i-blog.csdnimg.cn/img_convert/495623c237985c42c47c6a4a822da6e8.png)

这个速度足以吊打一众云端 API。

切换到 `Qwen3-4B`，首包延时来到 `0.2s`：

```
2025-06-12T05:58:52.248Z llm: start stream
2025-06-12T05:58:52.458Z llm: 你好！
2025-06-12T05:58:52.460Z llm: 今天天气不错，
```

再看工具调用情况：

`14b` 以下全部拉跨：

![](https://i-blog.csdnimg.cn/img_convert/19b4506d54d3870bfba79d9e370c562d.png)

要么压根就没有调用，要么就是输出调用参数不全！

## 写在最后


本文分享了 `混合推理模型 Qwen3` 的实现方案。

本来对 `Qwen3` 的工具调用能力还是挺期待的，结果，有点失望。

说白了，还是指令遵循不到位，看来蒸馏后的小模型还是不行，如果要用小模型进行工具调用，进一步的指令微调是免不了了。

如果对你有帮助，欢迎**点赞收藏**备用。
