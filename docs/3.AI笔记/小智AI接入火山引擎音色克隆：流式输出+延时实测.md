
前面分享了，小智 AI **接入 TTS** 的系列文章：
- 两家云厂商的 TTS 服务：

[低延迟小智AI服务端搭建-TTS篇](https://zhuanlan.zhihu.com/p/1900125186654700030)

- 本地部署 TTS+语音克隆 服务：

[低延迟小智AI服务端搭建-本地TTS篇：FishSpeech流式推理](https://zhuanlan.zhihu.com/p/1906675335778514702)

[低延迟小智AI服务端搭建-本地TTS篇：CosyVoice流式推理](https://zhuanlan.zhihu.com/p/1907352746098680072)

[SparkTTS 音色克隆 + vLLM INT8量化加速推理](https://zhuanlan.zhihu.com/p/1908123507746931028)

[低延迟小智AI服务端搭建-本地TTS篇：IndexTTS+vLLM加速推理](https://zhuanlan.zhihu.com/p/1908795805793486607)


下表总结了，以上所有 TTS 的首包延时：

| TTS服务来源 | 模型名称          | 延迟时间(s) |
| :------ | :------------ | :------ |
| 阿里百炼    | CosyVoice     | 0.4-0.5 |
| 火山引擎    | 大模型语音合成       | 0.3-0.4 |
| 本地部署    | FishSpeech1.5 | 2.0     |
| 本地部署    | CosyVoice2.0  | 1.3     |
| 本地部署    | SparkTTS      | 0.5     |
| 本地部署    | IndexTTS      | 0.4-0.5 |

为了进一步降低本地音色克隆的首包延时，前文给出了`音色缓存`的两种思路：

[低延迟小智AI服务端搭建-本地TTS篇：音色缓存](https://zhuanlan.zhihu.com/p/1927331892807598673)

可以看到，音色克隆，我们采用的都是本地部署方案。

有什么缺点：依赖 GPU 推理，成本高，不太适合项目早期阶段。

最近看到，火山引擎上线了`声音复刻2.0`，支持流式输出。

今日分享：

如何接入火山引擎的`声音复刻大模型`，并对延时进行实测！

## 1. 火山引擎-声音复刻简介
> 文档：[https://www.volcengine.com/docs/6561/1204182](https://www.volcengine.com/docs/6561/1204182)

从 api url 上可以发现，火山引擎的`声音复刻2.0`，其语音大模型就是字节前段时间开源的：`MegaTTS`。

模型架构和数据处理逻辑，和其它语音大模型基本类似。

模型输入需要两部分：
- 参考音频：10-15s即可，用于提取音频特征，实现声音复刻
- 合成文本：不宜超过 60s，正常语速下小于300字

为此，API 接入上，需要完成两部分工作：
- 创建音色；
- 调用语音合成；

正式接入之前，还需要完成以下准备工作。

## 2. 接入准备
> 控制台：[https://console.volcengine.com/speech/app](https://console.volcengine.com/speech/app)

控制台创建应用，然后勾选`声音复刻大模型`：

![](https://i-blog.csdnimg.cn/img_convert/fd27e3996b7db89cb006d8a9bfd1f7e9.png)

在应用中，获取以下 4 个接口参数：

![](https://i-blog.csdnimg.cn/img_convert/5d1bedece973800b49a726ba13e15934.png)

创建完成，免费赠送一个音色，能够进行10次训练以及合成5000字符。
> PS：这里压根不会执行任何训练，上传音频，是为了提取音频特征，作为大模型的 prompt 输入；如果多次上传，则对所有音频特征取平均？

如需新的音色，需进行购买：

![](https://i-blog.csdnimg.cn/img_convert/a83d361bef4c4e856023121be53a92d0.png)

## 3. 声音克隆 API 接入

### 3.1 创建音色

拿到上面的应用参数，即可通过调用接口完成音频上传：

```
def voice_upload():
    file_path = '1.wav'
    with open(file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
        encoded_data = str(base64.b64encode(audio_data), "utf-8")
        audio_format = os.path.splitext(file_path)[1][1:]  # 获取文件扩展名作为音频格式
    url ="https://openspeech.bytedance.com/api/v1/mega_tts/audio/upload"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer;" + 'token',
        "Resource-Id": "volc.megatts.voiceclone",
    }
    audios = [{"audio_bytes": encoded_data, "audio_format": audio_format}]
    data = {"appid": '41xx', "speaker_id": 'S_xx', "audios": audios, "source": 2,"language": 0, "model_type": 1}
    response = requests.post(url, json=data, headers=headers)
    print("headers = ", response.headers)
    print(response.json())
```

音频上传成功后，调用接口，查看云端是否准备就绪：

```
def get_voice_status():
    url = "https://openspeech.bytedance.com/api/v1/mega_tts/status"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer;" + 'token',
        "Resource-Id": "volc.megatts.voiceclone",
    }
    body = {"appid": '4166067500', "speaker_id": 'S_lKZjXSAt1',}
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        status = response.json().get('status', 0)
        # 0: 未发现 1: 训练中 2: 训练完成 3: 训练失败 4: active
        print(f"voice status: {status}")
```

回到控制台查看状态：

![](https://i-blog.csdnimg.cn/img_convert/b990f5780f0094aa3c6859cee6910630.png)

此外，状态查看接口，还会返回如下字段：

```
{
  "BaseResp": {"StatusCode": 0, "StatusMessage": ""},
  "create_time": 1751449452000,
  "demo_audio": , # 会有过期时间
  "icl_speaker_id": "ICL_5dc70e6ea3ca", # 文档中提到用于双向流式API，但现在似乎弃用了
  "language": 0,
  "speaker_id": "S_lKZjXSAt1", # 用于声音复刻API
  "status": 2,
}
```

音色准备就绪，接下来就可以尝试调用 TTS 接口，使用该音色，合成音频。

接口提供 websocket/HTTP 两种协议。

不过，流式输出，得采用 websocket。 


### 3.2 语音合成-websocket

WebSocket 协议下，提供 submit 和 query 两种操作类型：

- submit
  - 用途：你发送文本内容，服务端会异步处理并返回音频流。
  - 场景：用于实时合成、需要立即拿到音频的场景。

- query
  - 用途：只需提供任务的 reqid，服务端会返回该任务的音频（如果已完成）。
  - 场景：适合异步任务、轮询获取结果，或者断点续传等场景。

值得注意的是，接口**不支持双向流式**：每个 WebSocket 连接只能处理一次合成（一次 submit）。

以 python 代码为例，大致流程如下：

```
async with websockets.connect(api_url, extra_headers=header, ping_interval=None) as ws:
        await ws.send(full_client_request) # 发送合成请求
        while True:
            res = await ws.recv() # 等待服务端响应
            done = parse_response(res, file_to_save)
            if done: # 收到最后一个音频包
                file_to_save.close()
                break
        print("\nclosing the connection...")
```


如果要合成多句文本：
- 必须每次都新建 WebSocket 连接，
- 合成结束后（收到最后一包音频），关闭连接
- 新建连接进行下一次合成。


## 4. 接入小智 AI
### 4.1 实现思路
在小智 AI 对话应用中，LLM 生成的文本，是一句一句发过来的。

为此，可以建立一个 TtsSession 会话来统一处理。

那么，如何在一个session中实现多句文本合成呢？

下面给出一种思路：

- 维护一个队列：write(text) 只入队，不处理；
- 循环处理队列：每次建立一个 ws 连接，合成一条，收到 done 后再处理下一句；
- 所有文本合成完：触发 'finished' 事件，反馈给上游。

以下是调用流程图：

![](https://i-blog.csdnimg.cn/img_convert/6f6aff0842ebd12d26704aa560094634.png)


### 4.2 延时实测

服务端是 node.js 写的，以下是实测数据：

![](https://i-blog.csdnimg.cn/img_convert/0617c0c52c233f873b85326c67e0e1c8.png)

![](https://i-blog.csdnimg.cn/img_convert/15b8134853484ed0bfead7f85757b477.png)

可以看到，首包延时高达 **0.6-0.8s**，其中建立 ws 连接就需要 0.1s！

显然，这么搞不合理啊！

不过，就在本文完成前，

笔者看到火山的`双向流式API`也支持`声音复刻2.0`了。

于是动手改造了一番，实测延时如下：

![](https://i-blog.csdnimg.cn/img_convert/a2a6e5b3e4dbacef9fefd53e8abf9934.png)

你看，首包延时 **0.4-0.5s**，比没有声音克隆的 tts 略慢，符合预期！

## 写在最后

本文分享了`小智AI服务端接入火山引擎-音色克隆`的实现，并对`流式推理的延时`进行了实测。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。


