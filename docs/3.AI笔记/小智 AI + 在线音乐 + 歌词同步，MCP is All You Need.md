`小智AI + MCP` 系列陆续更新中：
- [小智 AI + 闹钟提醒 + 定时任务，设备端MCP实现，想象空间巨大](https://zhuanlan.zhihu.com/p/1950126555238991207)
- [小智 AI + 知识库RAG，打造私人定制专家](https://zhuanlan.zhihu.com/p/1951896126836945879)

本文是该系列的第 3 篇，聊聊：

**如何通过 MCP 接入 `音乐播放` 能力？**

先看效果：
> 交互逻辑：用户请求音乐 → LLM 工具调用 → 下载/播放/歌词同步 → 用户唤醒，中断播放
> 
[https://www.bilibili.com/video/BV1AcWAzXEcJ/](https://www.bilibili.com/video/BV1AcWAzXEcJ/)

目录如下：

![](https://i-blog.csdnimg.cn/img_convert/b42a8940543edeabb1d44f07e63e2c31.png)


## 1. 需求分析

### 1.1 功能需求
在线音乐播放，至少要满足以下核心功能：

- 语音控制：通过语音指令播放指定歌曲，支持指定歌手
- 流媒体播放：在线流式播放，边下载边播放
- 歌词同步：播放音乐时，同步显示对应的歌词

### 1.2 技术需求
- 音频格式支持：支持 MP3 等格式音频流的解码播放
- 网络请求处理：通过HTTP协议获取音乐和歌词数据
- 内存管理：资源有限情况下，高效管理音频缓冲区

### 1.3 用户体验
- 支持打断：用户可以通过唤醒，打断音乐播放
- 状态反馈：设备需要向用户反馈播放状态和相关信息
- 错误处理：在网络异常或资源不可用时，提供友好错误提示

## 2. 实现思路

### 2.1 系统架构设计

采用三层架构：

- 应用层：Application 统一管理任务调度；
- 协议层：MCP Server 提供标准化接口；
- 播放层：Esp32Music 负责具体的音频处理；

整体交互逻辑如下：

![](https://i-blog.csdnimg.cn/img_convert/1f0af769ff1ac055ff6f1e86b38e80c2.png)


### 2.2 MCP工具接口设计

小智 AI 接入 MCP 有两种方式：

1. 设备端新增 MCP tool；
2. 通过官方暴露的 MCP 接入点；

考虑到设备端需要下载音频+歌词，我们在设备端新增 MCP Tool：

```
AddTool("self.online_music.play",
    "当用户要求播放音乐时使用此工具\n"
    "Args:\n"
    "  `song_name`: 要播放的歌曲名称。\n"
    "  `singer`: 歌手名称（默认为空）。\n"
    "返回:\n"
    "  播放状态信息。",
    PropertyList({
        Property("song_name", kPropertyTypeString),
        Property("singer", kPropertyTypeString, "")
    }),
    [](const PropertyList& properties) -> ReturnValue {
        auto& app = Application::GetInstance();
        auto song_name = properties["song_name"].value<std::string>();
        auto singer = properties["singer"].value<std::string>();
        
        if (!app.music_->Download(song_name, singer)) {
            return "{\"success\": false, \"message\": \"获取音乐资源失败\"}";
        }
        return "{\"success\": true, \"message\": \"音乐开始播放\"}";
    });
```

注：这里只用到两个参数，可根据需求复杂度，新增更多参数。

举个例子：
- 用户语音指令："播放周杰伦的青花瓷"
- LLM 解析并调用 `self.online_music.play` 工具
- 传递参数：song_name="青花瓷", singer="周杰伦"
- 返回是否下载成功

![](https://i-blog.csdnimg.cn/img_convert/82e591d6d1e5f52bf17d14adc970c106.png)

### 2.3 音频流式处理架构

因为设备资源有限，且要保证交互的流畅性，当然得`边下载 边播放`。

因此，这里采用`生产者-消费者模式`：
- `下载线程`：负责从网络流式下载音频数据；
- `处理线程`：负责解码音频，并发送到 `audio_servive` 的播放队列；

此外，如何实现和音频同步显示歌词呢？

那就再加一个`实时歌词同步`线程：获取播放队列中，音频帧对应的时间戳，定期检查并更新显示对应歌词。


以`青花瓷`为例：

歌词文件中有时间戳，解析出来如下：

![](https://i-blog.csdnimg.cn/img_convert/346ebda4655348564566bab6c20a042a.png)


![](https://i-blog.csdnimg.cn/img_convert/06a08487aed4d4c863f4b62d879c368d.png)

可以看到，总共 44 句歌词~

当音频开始播放后，就要根据音频的时间戳，切换对应的歌词：

![](https://i-blog.csdnimg.cn/img_convert/99081fbd830107315ed46fe53e4d952f.png)

可以看到，播放到第 17 句时，音频下载完成：

![](https://i-blog.csdnimg.cn/img_convert/b09741faac2990894ac97565b0fcbf06.png)

但是`实时歌词同步`线程还得继续，直到音乐播放完成~

### 2.4 资源清理机制

当用户唤醒设备，希望中断播放，此时需要
- 清理音乐相关的线程;
- 清空播放队列：


```
void Application::OnWakeWordDetected() {
      if (music_) {
          ESP_LOGI(TAG, "Stopping music streaming due to wake word detected");
          music_->StopStreaming();
          audio_service_.ResetDecoder();
      }
      // 继续处理语音交互...
}
```

## 写在最后

本文分享了`如果通过 MCP 为小智 AI 接入在线音乐播放`，实现了有限资源下，流畅的音乐播放，以及精准的歌词同步。

如果对你有帮助，不妨**点赞收藏**备用。

`小智AI + MCP`系列，将陆续分享更多实用、好玩的 MCP 工具。

敬请关注~



