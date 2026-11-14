前两篇，分享了`低延迟小智AI服务端搭建`的 ASR 部分：
- [低延迟小智AI服务端搭建-ASR篇](https://zhuanlan.zhihu.com/p/1895438759719306293)
- [低延迟小智AI服务端搭建-ASR篇（续）](https://zhuanlan.zhihu.com/p/1896830194364445963)

从实测来看，当音频采用流式输入，VAD + ASR 部分的延时几乎可忽略。

接下来，压力给到 LLM 部分。

**本篇，继续实测 LLM 流式推理，聊聊如何把延时降到最低。**


## 1. 技术方案选型

因为是对话任务，所以对模型的情商要求较高，LLM 参数量小不了。

据公开报道，小智团队基于 Qwen 微调了一个 Emotion 模型，参数规模在 72B。

> 有微调需求的朋友可参考教程：[定制你的DeepSeek专家：Unsloth 大模型微调教程](https://zhuanlan.zhihu.com/p/31437081152)

除了本地部署模型，还可以选用各大厂商的在线 API，大部分都兼容了 OpenAI 格式。

在笔者看来：
- **本地部署**：适合特定垂类场景下的问答任务，需微调训练，然后采用 vLLM 部署，支持高并发。
- **在线 API**：场景通用，快速上线测试。

此外，如果从成本出发：**LLM 本地部署**，单论推理成本，就足以劝退绝大部分玩家，更遑论`数据采集、模型训练`的研发投入。


## 2. 流式推理实现

为了`低延迟`的目标，LLM 需采用流式推理。

此外，为了服务于后续 TTS，还需对 LLM 的流式输出文本，进行简单的拼接：**根据标点符号进行断句**。

关于如何处理 LLM 的流式输出，可回看之前的教程：

[如何实现大模型流式输出？OpenAI+Ollama 实战](https://zhuanlan.zhihu.com/p/844999354)

下面给出 node.js 的实现，原理和上面 python 实现一样。

```
sendMessageStream(text) {
    this.updateSystemTimePrompt(); // 更新时间
    const stream = new EventEmitter();
    const messages = [...this.context]; 
    messages.push({ role: 'user', content: text });
    const punct_list = ['。', '！', '？', '；', '.', '!', '?', ';'];
    let text2tts = '';
    this.abortController = new AbortController();  // 创建一个新的中断控制器
    this.openai.chat.completions.create({
        model: this.model,
        messages: messages,
        stream: true,
        signal: this.abortController.signal // 传递给 OpenAI API 的信号
      }).then(async response => {
        try {  // 添加 try-catch 以处理中断异常
          for await (const chunk of response) {
            const content = chunk.choices[0]?.delta?.content;
            text2tts += content;
            for (const punct of punct_list) {
              if (content.includes(punct)) {
                const parts = text2tts.replace('\n', '').split(punct);
                for (let i = 0; i < parts.length - 1; i++) {
                  const front = parts[i];
                  if (front) {
                    stream.emit('data', front + punct);
                  }
                }
                text2tts = parts[parts.length - 1];
                break;
              }
            }
          }
          if (text2tts) {
            stream.emit('data', text2tts);
          }
          stream.emit('end');
        } catch (error) {
          if (error.name === 'AbortError') {
            console.log(new Date(), 'LLM 请求被中断');
            stream.emit('end');  // 确保在中断时也触发 end 事件
          } else {
            stream.emit('error', error);
          }
        }
      }).catch(error => {
        console.error('OpenAI API error:', error);
        if (error.name !== 'AbortError') { // 只在非中断情况下触发错误
          stream.emit('error', error);
        }
      });
    return stream;
  }
```


## 3. 延时实测

推理测试，我们的目标是：**从输入到获得首句回复的时长**。

因为只有这部分延时才会影响用户体验，只要 tts 做到实时，后续生成，用户是无感知的。

代码描述如下：

```
const client = new ClientOpenAI(process.env.OPENAI_URL, process.env.OPENAI_KEY, process.env.MODEL_NAME, config.sys_chat);

const first_sentence = '你好，介绍下你自己。'
const stream = client.sendMessageStream(first_sentence);
console.log(new Date(), 'llm: start stream');

let llm_response = '';
stream.on('data', data => {
  llm_response += data;
  console.log(new Date(), 'llm:', data);
});

await new Promise((resolve, reject) => {
  stream.on('end', () => {
    console.log(new Date(), 'llm: end');
    client.addContext(first_sentence, 'user');
    client.addContext(llm_response, 'assistant');
    resolve();
  });
  stream.on('error', error => {
    console.error('llm: error', error);
    reject(error);
  });
}); 
```

在线 API 分别测试了：**阿里**和**智谱**两个厂商。

首先是 qwen-max：如果以句号进行截断，首句返回需要 **1.5s**，显然 pass。

![](https://i-blog.csdnimg.cn/img_convert/b11b21a83bc87969c138bce56f29407c.png)

如果以逗号进行截断，首句依旧需要 **0.7s**:

![](https://i-blog.csdnimg.cn/img_convert/39278241076dd610643bc6d31c7e2267.png)

改用 qwen-plus 测试：降为 **0.5s**:

![](https://i-blog.csdnimg.cn/img_convert/7ef9fba27af2bd0038893b50056871c0.png)

再看价格，qwen-max 可贵不少，模型参数量更大，性能指标更佳！

![](https://i-blog.csdnimg.cn/img_convert/75ed1d892f0ceda54b709a2b2a51b2f0.png)

最后，笔者还测试了本地 vLLM 部署的 **32B-int4 量化版模型**：

推理需要 24G 显存，**首句延时可以到 0.27s**，供感兴趣的朋友参考。

## 写在最后

本文分享了`小智AI服务端 LLM`的实现，对`流式推理`方案的延时进行了实测。

如果对你有帮助，欢迎**点赞收藏**备用。

接下来，压力给到 `TTS 部分`，下篇见。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

