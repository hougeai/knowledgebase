前面分享了，给小智 AI 接入 ASR：

[低延迟小智AI服务端搭建-ASR篇](https://zhuanlan.zhihu.com/p/1895438759719306293)

[低延迟小智AI服务端搭建-ASR篇（续）](https://zhuanlan.zhihu.com/p/1896830194364445963)

延迟是关键，为了抛弃对 GPU 的依赖，接入了火山引擎的`流式语音识别API `：

[小智AI接入火山引擎ASR：双向流式+负载均衡](https://zhuanlan.zhihu.com/p/1925803820572705898)

ASR 部分的流程图如下：

![](https://i-blog.csdnimg.cn/img_convert/0872416a9bc3f816d8b8845bbdeea767.png)

其中，`VAD` 之前采用的模型来自 FunASR。

最近在把 `小智AI服务端` 拆成各个独立的微服务，封装成 Docker 镜像，目标是所有微服务都可以在 CPU 上跑起来。

不过这个 `VAD` 需要依赖 `torch`，打包后的镜像体积来到了 `1.59G`，这能忍？

急需寻找 `VAD` 的平替方案！

今日分享：一款轻量高效的 `VAD` 方案 -- `TEN-VAD`，并给出对比实测，给类似需要的朋友一点点参考！


## 1.TEN-VAD 简介
> 项目地址：[https://github.com/TEN-framework/ten-vad](https://github.com/TEN-framework/ten-vad)

TEN-VAD 是一个低延迟，**高准确率**语音活动检测模型，来看官方效果图：

![](https://i-blog.csdnimg.cn/img_convert/a0818a588aeac48a6863ecd57baf1b1f.png)

有哪些亮点？

**1. 跨平台兼容：**

TEN VAD 开源了 Linux（.so）、Windows（.dll）、macOS & iOS（.framework）、Android（.so）、Web（.wasm）所需的二进制文件及示例代码，开箱即用。

![](https://i-blog.csdnimg.cn/img_convert/2f38a475dc82fea2d06425f21d53ab4e.png)

**2. 轻量级：**

Linux 平台下的动态库链接，低至 306KB：

![](https://i-blog.csdnimg.cn/img_convert/d76a8053d4a9f62dbe47994e48c1e23a.jpeg)

## 2. TEN-VAD 使用

本文将基于 Linux 平台进行实测。

### 2.1 工作原理

官方提供了动态链接库 - `libten_vad.so`，它是由编译型语言编写，并编译成机器码的二进制文件。

而 Python 中，可以通过 ctypes 模块，调用 C/C++ 编写的动态库：

```
from ctypes import CDLL
self.vad_library = CDLL("ckpts/libten_vad.so")  # 加载动态库
```

调用过程如下：

```
Python 代码 → ctypes → libten_vad.so → 执行 C/C++ 代码 → 返回结果
```

从而实现：用简单的 Python 语言，充分利用  C/C++ 的性能优势。

**注意**：系统中需安装`libc++1`：
```
sudo apt update
sudo apt install libc++1
```

### 2.2 实现逻辑

官方提供了 Python 调用的示例代码，位于`include/ten_vad.py`。

无需任何复杂依赖，只要环境中有 `numpy` 即可跑起来！

核心功能函数如下：

```
def process(self, audio_data: np.ndarray):
        input_pointer = self.get_input_data(audio_data)
        self.vad_library.ten_vad_process(
            self.vad_handler,
            input_pointer,
            c_size_t(self.hop_size),
            POINTER(c_float)(self.out_probability),
            POINTER(c_int32)(self.out_flags),
        )
        return self.out_probability.value, self.out_flags.value
```

输入是 `np.int16` 类型的 PCM 音频格式，长度等于 `hop_size`（默认256个采样点）。

**注意**：输入必须是 16kHz 采样的音频数据，因此 256 采样点对应 16ms 的音频。

输出是语音概率和标志位，用于判断每个小段音频是否包含语音活动。

### 2.3 流式输入

**问题来了**：如何用它实时检测流式输入音频中的语音活动？

要实现的功能如下：

1. 语音段检测
- 将输入的长音频分割成小块（每块 hop_size 个采样点）
- 逐块检测是否包含语音活动
- 记录语音段的开始和结束时间

2. 连续处理与缓存
- 支持流式处理（通过 truncated 参数控制）
- 维护 vad_cache 缓存，保存历史检测结果
- 处理跨批次的语音段连接

以下给出笔者的实现，供大家参考：

```
    def generate(self, input: np.ndarray, truncated=False):
        '''process audio data trunks'''
        if truncated:
            self.last_pos = 0
            self.vad_cache = []
        num_frames = input.shape[0] // self.hop_size
        speech_segments = []
        current_segment_start = None
        for i in range(num_frames):
            audio_data_trunk = input[i * self.hop_size: (i + 1) * self.hop_size]
            _, out_flag = self.process(audio_data_trunk)
            # 计算当前chunk的时间戳（毫秒）
            current_time_ms = self.last_pos + i * self.hop_size // 16  # 采样率为16kHz
            if out_flag == 1 and current_segment_start is None:
                # 如果检测到语音且当前没有记录起始位置，则记录起始位置
                current_segment_start = current_time_ms
            if out_flag == 0 and current_segment_start is not None:
                # 如果检测到非语音且之前有语音段，则结束当前段
                speech_segments.append([current_segment_start, current_time_ms])
                current_segment_start = None
        # 处理最后一段语音（如果结束时仍在语音中）
        if current_segment_start is not None:
            speech_segments.append([current_segment_start, -1])
        # 处理vad_cache
        if len(self.vad_cache) > 0 and self.vad_cache[-1][1] == -1:
            if len(speech_segments) == 0:
                self.vad_cache[-1][1] = self.last_pos
            else:
                self.vad_cache[-1][1] = speech_segments[0][1]
                speech_segments = speech_segments[1:]
        self.vad_cache.extend(speech_segments)
        self.last_pos += num_frames * self.hop_size // 16
        return self.vad_cache
```


### 2.4. 延时实测

输入为 240ms 的音频片段，延时实测效果如下：

- 方案一：FunASR 中的 VAD模型：
```
Time cost: 0.16324639320373535s [] 
Time cost: 0.007938146591186523s [[0, -1]] 
Time cost: 0.007047176361083984s [] 
Time cost: 0.006856679916381836s [] 
Time cost: 0.006888389587402344s [[-1, 930], [930, -1]]
```
- 方案二：TEN-VAD 模型：

```
Time cost: 0.004173994064331055s [[208, -1]] 
Time cost: 0.003608226776123047s [[240, -1]] 
Time cost: 0.004375457763671875s [[480, 656]] 
Time cost: 0.0036001205444335938s [] 
Time cost: 0.004243135452270508s [[1040, -1]] 
```

可以发现，对于 240ms 的音频输入，延时稳定在 `3-4ms`，只有方案一的一半。

由于抛弃了对 `torch` 的依赖，整个 ASR 镜像的体积也降到了 `342MB`：

```
REPOSITORY                IMAGE ID          SIZE
espbot-asr-worker       af4487d1b92c       1.59GB
espbot-asr-worker-ten   6960580c9785       342MB
```

## 3. 接入小智AI

由于 VAD 部分的延时几乎可忽略，整个处理过程的延时基本等于设置的`静音时长`：

![](https://i-blog.csdnimg.cn/img_convert/deec7146d02fd1e830c97500707821ee.png)

而 ASR 这里采用`流式识别`，延时也几乎可忽略，因此整个方案的延时约等于0。

## 写在最后

本文主要分享了一款轻量高效的 `VAD` 方案 -- `TEN-VAD`，并给出了对比实测。

如果对你有帮助，欢迎**点赞收藏**备用。


