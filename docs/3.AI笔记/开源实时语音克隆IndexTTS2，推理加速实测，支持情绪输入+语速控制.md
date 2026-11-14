
`IndexTTS` 是B站语音团队开源的一系列语音克隆模型。

早期版本，在多场景应用中均表现惊艳，笔者也有过部署实测：

[低延迟小智AI服务端搭建-本地TTS篇：IndexTTS+vLLM加速推理](https://zhuanlan.zhihu.com/p/1908795805793486607)

字错率和克隆相似性，均出于当时领先水平。

经过 vLLM 推理加速，RTF 可以低至 0.15，因此也是笔者**首选**的语音克隆模型服务。

**不过还有硬伤：**

- 情感表达不够，AI 味依旧浓郁；
- 不支持语速控制，更像在读稿。

刚好最近项目中需要解决以上痛点，寻找了一圈解决方案，兜兜转转还是来到了 `IndexTTS` 。

因为当前市面上，无论开源 还是 闭源的语音克隆方案，上述两点都没有很好解决。

早在去年 9 月，B站就开源了 `IndexTTS-2.0` ，号称**情感丰富**和**时长可控**。

刚好借此机会，实测一番，分享给各位。

## 1. IndexTTS-2简介
> 官方仓库：[https://github.com/index-tts/index-tts](https://github.com/index-tts/index-tts)

### 1.1 模型架构
相比 v1 版本，模型架构发生了不小变化：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2Fdc9856d8-6167-49c5-b82e-6914bcd1c607.png&pos_id=img-lKEZr1ix-1769736135739)

简言之：

`IndexTTS2` 由三个核心模块组成：`Text-to-Semantic（T2S）` 、`Semantic-to-Mel（S2M）` 以及 `BigVGANv2` 声码器。
- T2S 模块：
  - 输入：源文本、风格提示、音色提示、目标语音token数；
  - 输出：语义 token 序列。
  - 模型：GPT2自回归模型

- S2M 模块：
  - 输入：语义 token、音色提示；
  - 输出：梅尔频谱图。
  - 模型：基于流匹配的非回归生成框架
  
- BigVGANv2 声码器：
  - 输入：梅尔频谱图
  - 输出：高质量的语音波形。

### 1.2 亮点介绍
> 论文：[https://arxiv.org/abs/2506.21619](https://arxiv.org/abs/2506.21619)

有哪些亮点？

- **支持语速控制**：提出一种“时间编码”机制，首次解决了传统 AR 模型难以精确控制语音时长的问题。允许用户显式指定生成的token数量，从而实现语速控制。

- **支持情感表达**：提出音色与情感解耦机制，也就是支持用户同时指定音色参考与情感参考，实现更加灵活、细腻的情感表达。

此外，模型还具备基于文本描述的情感控制能力。

如何实现？

首先定义7种标准情感，并建立对应的情感embedding。用户输入自然语言，微调 Qwen3-0.6b 输出情感概率分布，加权得到最终的情感embedding。

### 1.3 核心代码解读

对应模型架构部分：

```
# 核心模块
GPT 模型 (UnifiedVoice)：负责从文本和音色参考生成语义码（codes）。

Semantic 模型（基于 w2v-BERT 2.0）：提取参考音频的语义嵌入。
- get_emb函数：输入w2v-bert特征和掩码，取第17层隐藏状态作为语义特征

Semantic codec：将语义嵌入量化为离散码本索引。

S2Mel 模型：包含 length_regulator、cfm（Flow Matching 扩散模型）等，用于从语义码生成梅尔频谱。

CampPlus：提取参考音频的风格向量（全局音色特征）。

BigVGAN：声码器，将梅尔频谱转为波形。

QwenEmotion：情感分析模型，可从文本生成情感向量。

TextNormalizer & TextTokenizer：文本规范化与分词（BPE）。

# 缓存机制
缓存参考音频的语义条件、风格向量、梅尔频谱等，避免重复计算。

# 模型加载
self.qwen_emo = QwenEmotion(os.path.join(self.model_dir, self.cfg.qwen_emo_path))会加载qwen模型

self.gpt = UnifiedVoice(**self.cfg.gpt, use_accel=self.use_accel)加载GPT模型，use_deepspeed用户加速gpt

self.s2mel = MyModel(self.cfg.s2mel, use_gpt_latent=True) 会使用enable_torch_compile，将模型转换为更高效的执行图，减少推理时间和显存占用

self.bigvgan = bigvgan.BigVGAN.from_pretrained 会用 use_cuda_kernel 启用自定义 CUDA 加速。

self.normalizer = TextNormalizer(enable_glossary=True)文本标准化实例，启用术语表，有具体使用示例
self.tokenizer = TextTokenizer(self.bpe_path, self.normalizer) 文本分词器，使用BPE分词算法和标准化器

self.emo_matrix 加载feat2.pt，共8种表情向量，每种有多条
self.spk_matrix 加载feat1.pt，内置的音频向量，和上面对应

self.mel_fn：梅尔频谱计算函数（根据配置初始化）

# 语音处理工具：
- remove_long_silence：压缩过长的静音 token，得到的还是codecs
- interval_silence / insert_interval_silence：在句子之间插入指定长度的静音段，前者生成静音，后者插入静音。
- _load_and_cut_audio：加载音频，截断到15s

# 推理函数
infer：如果是流式输出，返回迭代器；非流式输出：返回分句的音频列表
infer_generator：
- 先判断情感控制：
qwen大模型会输出:{'happy': 0.0, 'angry': 0.0, 'sad': 0.99, 'afraid': 0.0, 'disgusted': 0.0, 'melancholic': 0.0, 'surprised': 0.0, 'calm': 0.01}；若无外部情感参考音频，则使用音色参考音频作为情感参考。
  - 从emo_matrix中提取向量和emo_vector相乘，得到emovec_mat
  - 输入情感参考音频：得到语义嵌入emo_cond_emb；如果没有就和参考音频一样

- 再处理参考音频：如果参考音频变了，则重新加载
  - 16kHz 音频 → w2v-BERT 特征 → 语义嵌入spk_cond_emb →  codec量化得到 S_ref → 经过s2mel得到prompt_condition。
  - 22kHz 音频 → 梅尔频谱 ref_mel。
  - 16kHz 音频 → FBank 特征 → CampPlus →  风格向量 style

- 开始文本分词和分句：max_text_tokens_per_segment决定分几句
- 循环生成每段语音：
  - GPT 生成语义码（codes）：合并音色与情感cond，再合并emovec_mat，得到emovec，再调用 gpt.inference_speech 生成codes，用 self.gpt 对码和文本做一次前向，得到 latent（用于后续扩散模型条件）。
  - Flow Matching 扩散模型生成梅尔频谱：s2mel模型得到vc_target，其中的target_lengths用1.72控制梅尔频谱的长度，从而控制语速
  - BigVGAN 声码器合成波形：将梅尔频谱转为波形， clamp 到 int16 范围。
  - 收集波形和静音：生成一句wav，默认生成一段200ms静音，生成sampling_rate必须是22050
```

### 1.4 效果展示

相比 v1，`IndexTTS2` 在音色相似度上有了质的飞跃：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F489560e9-db14-4793-af07-4eed5fc6f526.png&pos_id=img-1rZL1lSc-1769736135741)

在情感控制上，相比 CosyVoice2 也强不少：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F96379364-8704-4a9e-8199-cc95d8853db1.png&pos_id=img-1DqH2IBW-1769736135741)


## 2. 推理加速测试

以下均在 RTX 4080 显卡上进行实测。

在不进行任何推理加速的情况下，模型加载后的显存占用：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F51223e18-519e-44d3-a7a7-8c9500e318a1.png&pos_id=img-OAVjBI7v-1769736135741)


`IndexTTS2` 的T2S模块依旧采用的是GPT2自回归模型架构，不过层数更多，因此极大增加了推理延时，实测RTF值如下：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F501d3197-3d43-45ca-aef2-6d23e44b398e.png&pos_id=img-nN4xyA4E-1769736135742)

多次测试：
```
>> RTF: 5.8614
>> RTF: 3.6096
>> RTF: 3.6241
>> RTF: 3.2211
>> RTF: 3.8663
```

显然，无法满足实时应用需求。

这里最耗时的有两个部分：
- 最重的是 GPT2 推理 
- 其次是 s2mel

后者可通过 `torch.compile` 将模型转换为优化的执行图，减少运行时开销，实测提速 2x。

下面重点解决 GPT2 推理。

### 2.1 vLLM 加速推理

`IndexTTS2` 的T2S模块是 GPT2，因此可通过 vLLM 引擎进行加载，从而实现推理加速，实测加速效果如下：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2Fd25a474c-c214-4388-8a1a-c52368a05630.png&pos_id=img-vPkCdQHU-1769736135742)

在 `gpu_memory_utilization` 设置为 0.25 的情况下，显存占用：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F7fd2d519-9f28-41bf-89e9-59f9d9ceaa89.png&pos_id=img-ez3TJvLr-1769736135742)

### 2.2 Deepspeed加速推理

官方仓库采用 uv 管理环境，安装 `deepspeed`：

```
uv sync --extra deepspeed
```
同时需要安装 `flash_attn`：

`flash_attn`安装坑比较多，推荐找到对应版本的安装包进行本地安装：
> [https://github.com/Dao-AILab/flash-attention/releases/](https://github.com/Dao-AILab/flash-attention/releases/)

```
wget https://github.com/Dao-AILab/flash-attention/releases/download/v2.8.3/flash_attn-2.8.3+cu12torch2.8cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
uv pip install flash_attn-2.8.3+cu12torch2.8cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
```

加速效果如下：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2Fb96461a2-4487-4f3c-8deb-ae4953708206.png&pos_id=img-e6likhMS-1769736135742)

`GPT2 推理`部分，加速效果相比 `vLLM` 更有性价比。

显存占用如下：

![外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传](https://img-home.csdnimg.cn/images/20230724024159.png?origin_url=https%3A%2F%2Ffiles.mdnice.com%2Fuser%2F47548%2F2727fd49-fa49-4ef0-a432-342457885a22.png&pos_id=img-HJxuTXEE-1769736135742)


## 3. 推理服务部署

### 3.1 方案选型

尽管 `vLLM` 支持并发，但单发都无法做到实时，根本不可用啊。

而 `DeepSpeed` 加速，可以将 RTF 干到0.5以下，却不支持并发。因为 `DeepSpeed` 的KV缓存机制为单个推理流程服务，在多线程并发访问时会产生内存冲突。

所以，只能选择在 FastAPI 这一层实施：
- GPU 推理串行化
- HTTP 请求异步化

也就是服务层面支持并发调用，但推理还是队列化处理的，确保不把服务打崩。

举例而言，假设同时来了 10 个请求：

```
[请求1] 成功 - 耗时: 3.63s
[请求2] 成功 - 耗时: 5.99s
[请求6] 成功 - 耗时: 9.20s
[请求3] 成功 - 耗时: 12.32s
[请求0] 成功 - 耗时: 14.61s
[请求4] 成功 - 耗时: 17.14s
[请求7] 成功 - 耗时: 19.65s
[请求8] 成功 - 耗时: 22.03s
[请求5] 成功 - 耗时: 24.44s
[请求9] 成功 - 耗时: 26.87s
```

先抢到资源的先推理，服务不忙的时候，可满足实时推理需求。

### 3.2 请求示例

请求示例如下：

```
class TTSRequest(BaseModel):
    voice_id: Optional[str] = None      # 参考语音的id
    tts_text: Optional[str] = None      # 待合成的文本
    emo_vec: Optional[list] = [0] * 8   # 情绪向量
    max_tokens: Optional[int] = 80    # 单句文本最大长度
    speed: Optional[float] = 1.0
```

- `voice_id` 会提取注册为音色，进行缓存，避免每次请求都要重新提取特征；
- `tts_text` 待合成的文本，支持无限长，服务内部会进行分句；
- `max_tokens` 分句做到最大长度；
- `emo_vec` 情绪向量，输入范围[0-1]：代表`["喜", "怒", "哀", "惧", "厌恶", "低落", "惊喜", "平静"]`




## 写在最后

本文分享了`实时语音克隆IndexTTS2`的技术方案，对两种推理加速方案进行了实测。

如果对你有帮助，欢迎**点赞收藏**备用。

另外，`IndexTTS2.5` 的技术报告已出，相比 `IndexTTS2` 速度更快，支持语种更多，敬请期待： 

[https://index-tts.github.io/index-tts2-5.github.io](https://index-tts.github.io/index-tts2-5.github.io)



