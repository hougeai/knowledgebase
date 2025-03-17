最近，语音克隆领域精彩迭出！

前段时间刚分享过升级版 FishSpeech：

[17k star！开源最快语音克隆方案，FishSpeech 焕新升级，本地部署实测](https://zhuanlan.zhihu.com/p/14730071942)

最近看到阿里开源的 CosyVoice 又发布了重大更新。

今日分享，将介绍 CosyVoice 2.0，并带大家本地部署体验，为本地 TTS 选型提供参考。

## 1. CosyVoice 简介
> 项目简介：[https://funaudiollm.github.io/cosyvoice2/](https://funaudiollm.github.io/cosyvoice2/)

与已有 TTS 方案相比，CosyVoice 在多语言语音生成、零样本语音生成、跨语言语音生成、富文本和自然语言细粒度控制方面，表现出色。可见之前的分享：

[CosyVoice 实测，阿里开源语音合成模型，3s极速语音克隆](https://zhuanlan.zhihu.com/p/713350242)

**相比旧版，CosyVoice 2.0 有哪些亮点？**
- **离线和流式一体化建模**：成功实现双向流式语音合成，目前主流方案(CosyVoice，F5-TTS，MaskGCT，GPT-SoViTs等)均不支持流式，FishSpeech 1.5 除外。

![](https://i-blog.csdnimg.cn/img_convert/90d381e9256e4a02197e719836e4fdb9.png)

- **多语言支持**：中文、英文、日语、韩语等，以及多种中国方言（粤语、四川话、上海话、天津话、武汉话等）
- **跨语言支持**：支持跨语言的零样本语音克隆。
- **超低延迟**：接收5个文字即可合成首包音频，延迟低至 150 毫秒；
- **超高精度**：在Seed-TTS评估集的硬测试集上取得最低的字符错误率。
- **音色一致性**：确保零样本和跨语言语音合成的可靠语音一致性。
- **韵律和音质**：在韵律、音质和情感对齐方面显著增强，MOS评分从5.4提高到5.53，接近商业化TTS水平。
- **可控音频生成**：支持更精细的情感控制和方言口音调整，可模仿机器人、小猪佩奇的风格讲话。

本次更新，预训练模型同样开源。

**下面我们实操本地部署，看看效果如何？**


## 2. 本地部署

> 项目地址：[https://github.com/FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)

首先，下载项目仓库，安装环境依赖。

```
git clone https://github.com/FunAudioLLM/CosyVoice
cd fish-speech
```

然后，下载模型权重：

```
git clone https://www.modelscope.cn/iic/CosyVoice2-0.5B.git pretrained_models/CosyVoice2-0.5B
```

这里只需下载 CosyVoice 2.0 的模型权重，一个模型支持多种推理方式。


### 2.1 模型测试
CosyVoice 2.0 支持多种推理方式，我们一一来介绍：

首先是模型加载：

```
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'third_party/Matcha-TTS'))
from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav
import torchaudio

cosyvoice = CosyVoice2('pretrained_models/CosyVoice2-0.5B', load_jit=True, load_onnx=False, load_trt=False)

print(cosyvoice.sample_rate) # 24000
```

有如下几种推理方式：

**1. 预定义音色**：

需要先将`CosyVoice-300M-SFT`模型中`spk2info.pt`的下载到`CosyVoice2-0.5B`权重文件夹下，测试代码如下：
```
spks = cosyvoice.list_available_spks()
print(spks)
tts_text = '收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的祝福让我心中充满了甜蜜的快乐，笑容如花儿般绽放。'
for j in cosyvoice.inference_sft(tts_text=tts_text, spk_id='中文男', stream=False):
    torchaudio.save('outputs/zero_shot.wav', j['tts_speech'], cosyvoice.sample_rate)
```


**2. 音色克隆**：

```
# zero_shot usage
prompt_speech_16k = load_wav('zero_shot_prompt.wav', 16000)
prompt_text = '希望你以后能够做的比我还好呦。'
for j in cosyvoice.inference_zero_shot(tts_text=tts_text, prompt_text=prompt_text, prompt_speech_16k=prompt_speech_16k, stream=False):
    torchaudio.save('outputs/zero_shot', j['tts_speech'], cosyvoice.sample_rate)
```

**3. 细粒度控制**：

```
# fine grained control, for supported control, check cosyvoice/tokenizer/tokenizer.py#L248
tts_text = '在他讲述那个荒诞故事的过程中，他突然[laughter]停下来，因为他自己也被逗笑了[laughter]。'
for j in cosyvoice.inference_cross_lingual(tts_text=tts_text, prompt_speech_16k=prompt_speech_16k, stream=False):
    torchaudio.save('outputs/fine_grained_control.wav', j['tts_speech'], cosyvoice.sample_rate)
```

支持的`细粒度控制`提示词包括：

![](https://i-blog.csdnimg.cn/img_convert/ec654ee9507927d7e210505e72ac18fe.png)

**4. 提示词控制**：


```
tts_text = '收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的祝福让我心中充满了甜蜜的快乐，笑容如花儿般绽放。'
instruct_text = '用四川话说这句话'
for j in cosyvoice.inference_instruct2(tts_text=tts_text, instruct_text=instruct_text, prompt_speech_16k=prompt_speech_16k, stream=False):
    torchaudio.save('outputs/instruct.wav', j['tts_speech'], cosyvoice.sample_rate)
```
### 2.2 服务端部署

项目中没有提供部署代码，这里我们采用 FastAPI 完成服务端。（*完整代码，可在文末自取*）

首先，定义一个数据模型，用于接收POST请求中的数据：
```

class TTSRequest(BaseModel):
    spk_id: Optional[str] = None       # 预训练语音id
    ref_audio: Optional[str] = None    # 参考语音 base64编码的音频文件
    ref_text: Optional[str] = None      # 参考语音的文本
    ref_tag: Optional[str] = None       # 参考语音的标签
    tts_text: Optional[str] = None      # 待合成的文本
    instruct_text: Optional[str] = None  # 指令文本
    stream: Optional[bool] = False    # 是否使用流式合成
    speed: Optional[float] = 1.0         # 语速
    mode: Optional[str] = 'sft'     # 合成模式，默认模式为 'sft'，可选模式为 'sft' 'zero_shot' 'cross_lingual' 'instruct'
```
因为模型支持流式输出，所以我们的接口采用异步实现，以 `sft` 模式推理为例：

```
@app.post("/cosyvoice")
async def tts(request: TTSRequest):
    headers = {
            "Content-Type": "audio/pcm",
            "X-Sample-Rate": "24000",  # 假设采样率是 24kHz
            "X-Channel-Count": "1"     # 假设单声道
        }
    if request.mode == 'sft':
        if not request.spk_id:
            return {'message': 'spk_id is required for sft mode'}
        async def generate():
            for out in cosyvoice.inference_sft(tts_text=request.tts_text, spk_id=request.spk_id, stream=request.stream, speed=request.speed):
                raw = (out['tts_speech'].numpy() * 32767).astype(np.int16).flatten() # 原始输出 [-1, 1] 之间的float32，需要转为 16 位 PCM
                yield raw.tobytes()
        return StreamingResponse(generate(), media_type="audio/pcm", headers=headers)
```

**注意：模型原始输出为 torch.tensor，需要转换为 numpy，并转成 int16 以 pcm 格式输出。**

最后，启动服务：

```
export CUDA_VISIBLE_DEVICES=1
nohup uvicorn server_cosyvoice:app --host 0.0.0.0 --port 3005 > server.log 2>&1 &
```


### 2.3 客户端请求

服务端成功启动后，客户端请求主要包括两个部分：

**1. response 数据接收**：重点关注下是否需要流式输出：

```
def test_tts():
    spk_id = "中文男"
    tts_text = "2024年12月，随着大军缓缓前进，他忍不住琢磨起了回京之后会被派到什么艰苦的地方顶缸。要知道皇帝一向就是这么干的，几乎没让他过过什么安生日子。"
    stream = True
    data = {
        "spk_id": spk_id,
        "tts_text": tts_text,
        "stream": stream,
        "speed": 1.0,
    }
    st = time.time()  
    if stream:
        response = requests.post("http://localhost:3005/cosyvoice", json=data, stream=True)
        print(f"请求耗时：{time.time() - st}s")
        audio_content = b''
        for chunk in response.iter_content(chunk_size=1024):
            audio_content += chunk
    else:
        response = requests.post("http://localhost:3005/cosyvoice", json=data)
        print(f"请求耗时：{time.time() - st}s")
        audio_content = base64.b64decode(response.content)
    pcm2wav(audio_content)
```
**2. pcm 转 wav**

```
def pcm2wav(pcm_data):
    with wave.open('outputs/gen_audio.wav', "wb") as wav:
        wav.setnchannels(1)          # 设置声道数
        wav.setsampwidth(2)      # 设置采样宽度
        wav.setframerate(24000)       # 设置采样率
        wav.writeframes(pcm_data)           # 写入 PCM 数据

```

## 3. 性能实测

### 3.1 显存占用

实测推理显存占用情况如下：

![](https://i-blog.csdnimg.cn/img_convert/567fc3fbd67242360185e884251dbc9d.png)

请**至少确保 4G 显存**，相比上篇的 FishSpeech1.5 占用显存更低！


### 3.2 速度测试
TTS 中通用的速度评估指标为 rtf，也即 `推理耗时/生成音频耗时`，**指标越低**，代表推理速度越快！

**非流式推理：**
![](https://i-blog.csdnimg.cn/img_convert/8c4e7bd846d5241d171a61282b86533d.png)
**流式推理：**
![](https://i-blog.csdnimg.cn/img_convert/7ea5e2cf4c3e7c48945b3ffa5ada8bc9.png)

相比上篇的 FishSpeech1.5，就太慢了。。。

### 3.3 效果展示

由于插入音频比较麻烦，这里不展示测试音频结果，感兴趣的朋友可前往官网查看：[https://funaudiollm.github.io/cosyvoice2/](https://funaudiollm.github.io/cosyvoice2/)

从实测体验而言，对于`数字播报`这一老大难问题，CosyVoice 2.0 会统一转换成中文进行合成，目前还没遇到翻车的现象。

不知大家体验如何，欢迎评论区交流！

## 写在最后

本文和大家分享了一款强大的语音克隆工具：CosyVoice 2.0，**就生成质量而言**，可谓已有开源方案中的顶流。

如果对你有帮助，欢迎**点赞收藏**备用。

本文`服务部署代码`已上传云盘，有需要的朋友，公众号后台回复`cosyvoice`自取！

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。


