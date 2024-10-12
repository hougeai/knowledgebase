上篇带大家在 Jetson Ori Nano 开发板上，成功利用 GPU 实现了大模型推理加速。
- [Jetson 开发系列：如何用GPU跑本地大模型？](https://blog.csdn.net/u010522887/article/details/142722395)

尽管有了 GPU 加持，推理速度依然很慢，怎么搞？

**流式输出！**

相比全部生成后再输出，**流式输出**生成一句就播报一句，大大减少了用户的等待时间。

主流大模型推理 API 包括：
- OpenAI 格式：沿袭 ChatGPT 的云端 API，多用于线上模型；
- Ollama 格式：用于本地部署的大模型推理。

本次分享，将带大家实战：OpenAI 和 Ollma 下的大模型流式输出。

## 1. OpenAI 流式输出

当前大部分大模型的推理 API 都兼容了 OpenAI 格式。

如果没有，强烈推荐你用 OneAPI 进行管理：[一键封装成OpenAI协议，强推的一款神器！](https://zhuanlan.zhihu.com/p/707769192)

和非流式输出相比，只需新增一个参数：`stream=True`。

不过，为了方便后续进行语音合成，我们需要对大模型的流式输出进行一番处理！

首先，定义一个标点符号列表：punct_list = ['。', '！', '？']，遇到这里的标点，则立即输出。

具体实现如下，供参考：
```
class LLM_API:
    def __init__(self, api_key, base_url, model):
        self.client =  OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
  def stream(self, messages):
      completion = self.client.chat.completions.create(
          model=self.model, messages=messages, stream=True
      )
      text2tts = ''
      for chunk in completion:
          text = chunk.choices[0].delta.content
          text2tts += text
          for punct in punct_list:
              if punct in text:
                  front, back = text2tts.replace('\n', '').rsplit(punct, 1)
                  yield front + punct
                  text2tts = back
                  break
      if text2tts:
          yield text2tts
```

上述代码使用 yield 关键字定义一个生成器函数。

## 2. Ollama 流式输出
有关 Ollama 的使用，可参考：[本地部署大模型？Ollama 部署和实战，看这篇就够了](https://blog.csdn.net/u010522887/article/details/140651584)

Ollama 的 API 和 OpenAI 略有区别，但核心逻辑是一样的，直接上代码：
```
def stream(self, messages):
    data = {
        "model": self.model, "messages": messages, "stream": True
    }
    response = requests.post(self.base_url, json=data, stream=True)
    text2tts = ''
    for line in response.iter_lines():
        data = json.loads(line.decode('utf-8'))
        text = data['message']['content']
        text2tts += text
        for punct in punct_list:
            if punct in text:
                front, back = text2tts.replace('\n', '').rsplit(punct, 1)
                yield front + punct
                text2tts = back
                break
    if text2tts:
        yield text2tts
```

调用时，可以用 for 循环来迭代生成器对象，每次迭代，生成器会执行到下一个 yield 语句，并返回当前值：

```
ollama_api = OLLAMA_API(ollama_url, 'qwen2.5:7b')
messages = [{ "role": "user", "content": "天空为什么是蓝色的"}]
for text in ollama_api.stream(messages):
    print(text)
```
输出效果如下：

```
天空之所以呈现蓝色，主要是因为大气中的气体分子和其他细小颗粒对太阳光的散射作用。
这种现象被称为瑞利散射（Rayleigh scattering），由英国物理学家威廉·汉斯·瑞利爵士在19世纪末发现。
当阳光进入地球的大气层时，其中的各种颜色（不同波长）的光线都会受到气体分子、水蒸气和尘埃等微粒的影响。
然而，这些微粒对较短波长的光（如蓝色和紫色）散射得更为强烈。
由于人眼对蓝光比紫光敏感得多，所以我们看到的是天空呈蓝色。
实际上，太阳本身发出的白光包含了所有颜色的光。
当阳光进入大气层时，其中的蓝色光线因散射作用被分散到各个方向，在我们看来，天空就呈现出蓝色。
而太阳和天空在白天看起来呈现不同的颜色（例如：日出和日落时天边的橙红色或紫色），则是由于此时光线需要穿过更多的大气层，蓝光几乎都被散射掉了，只有红、橙等较长波长的光线能够直接到达我们的眼睛。
总之，正是这种自然现象造成了天空呈现出蓝色。
```

实测：在 Jetson Orin Nano 上使用本地部署的 qwen2.5:7b，流式输出 + 语音合成播报，体验基本无延迟！

## 写在最后

本文带大家实操了大模型流式输出，在 OpenAI 和 Ollama API 中的具体实现。

如果对你有帮助，欢迎**点赞收藏**备用。

本系列文章，会陆续更新 Jetson AI 应用开发的相关教程，欢迎感兴趣的朋友关注。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。


