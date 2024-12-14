上篇和大家分享了用 Dify 搭建一个简单的 AI 搜索引擎：

[Dify 保姆级教程之：零代码打造 AI 搜索引擎](https://blog.csdn.net/u010522887/article/details/143382888)

今天继续分享 `Dify 智能体搭建`的相关内容。

最近在关注大模型`长期记忆`的问题，前天分享了阿里开源的 MemoryScope 项目：

[如何赋予AI智能体长期记忆？阿里开源 MemoryScope 实战，全程免费](https://blog.csdn.net/u010522887/article/details/143354689)

无奈本地配置环境略显繁琐，对小白不是特别友好。

有没有可能在 Dify 上搭建一个类似的智能体，实现大模型`长期记忆`？

琢磨之余，发现 Dify 的官方案例中就有一款类似的智能体。

**今日分享，把搭建过程拆解后分享出来，希望对有类似需求的你，有所启发。**

参考上篇教程，相信你已完成 Dify 本地安装，若资源有限，也可使用官方的在线体验地址。

## 1. 官方案例
在 Dify 首页，第一个 Tab，官方内置了众多搭建好的智能体案例：

![](https://img-blog.csdnimg.cn/img_convert/9a4824055001a885cfd52d43fd79e8bf.png)


![](https://img-blog.csdnimg.cn/img_convert/4e9e713dfacc5c8ee8038adc7d82199b.png)


其中，有一个`个性化记忆助手`的智能体，点击`添加到工作区`：

![](https://img-blog.csdnimg.cn/img_convert/822a1a08e698005a3c22c39efbc6b017.png)

在自己的`工作室`，可以看到这个智能体已复制进来：

![](https://img-blog.csdnimg.cn/img_convert/ac4690d1715a236bcbb529054bc87356.png)

点进来，就可以看到所有的编排逻辑，然后可根据自己需求进行修改：

![](https://img-blog.csdnimg.cn/img_convert/b2235685f0fdb11647e9f5001e01face.png)



## 1. 了解会话变量

Dify 中内置了一个全局变量 -- `会话变量`，在右上角：

![](https://img-blog.csdnimg.cn/img_convert/dfe37042de2ca0e6e821b88db6321c67.png)

这个`会话变量`具体有什么用？

和多轮对话的内容一样，它也可以作为 LLM 的上下文，不过它的自定义程度更高。

比如在本文的智能体中，就定义了`memory`这样的`会话变量`，用来存储需要大模型记忆的信息。

问题来了：`memory`是怎么发挥作用的？

下面我们一起去探一探。

## 2. 智能体拆解

**step 1 信息过滤**: 判断用户输入中是否需要记忆的信息：

![](https://img-blog.csdnimg.cn/img_convert/285a21a57fe86da212034d079b59aea8.png)

从上面的提示词，可以看出，这个节点上大模型只需输出 Yes 或 No，所以下个节点应该是条件判断。

**step 2 条件判断**：根据上一步大模型输出的 Yes 或 No，分别路由到不同的分支，如果有需要记忆的信息，则执行上方`提取记忆`的分支，否则走下面的分支。

![](https://img-blog.csdnimg.cn/img_convert/b9b6611b588cd69ea3bd28f2ecbaadbd.png)

**step 3 提取记忆**：通过大模型的角色设定，从用户输入中提取出`值得`记忆的信息。

![](https://img-blog.csdnimg.cn/img_convert/b95a860349bdeb83a9d62635d8860543.png)

在提示词中，指定了提取的三种类型记忆：

```
"facts": [],
"preferences": [],
"memories": []
```

**step 4 存储记忆**：这一步是代码节点，通过编写简单的 Python 代码，将上一步的记忆信息，保存到一开始定义的`会话变量` - `memory`中。

![](https://img-blog.csdnimg.cn/img_convert/eb90a88d52253561f8934079ac34e7bb.png)


**step 5 根据记忆回复**：把`会话变量` - `memory`转换成字符串，也就是下图中的`{x}result`，放到角色提示词中，让大模型根据记忆，进行答复。

![](https://img-blog.csdnimg.cn/img_convert/2131bcdefe18566d48ddbb8e6f4a787f.png)

至此，基于`对话内容中有需要缓存的记忆`，上方`提取记忆`的分支就搞定了。


如果`step 2`判断为 `No`，则直接基于已有记忆进行答复，也即下方分支，流程图如下：

![](https://img-blog.csdnimg.cn/img_convert/bd71e5e291d91799a1d9e9638d43231f.png)


## 3. 效果展示

我在和它进行了几轮对话之后，点开右上角的`会话变量`，可以发现`memory`中已经缓存了多条事实类的`记忆`：

![](https://img-blog.csdnimg.cn/img_convert/af4e27ed5b86e13ff3f0c86e9fecddd5.png)

完美！

真的完美么？

相比`直接把多条聊天记录作为上下文`，这种方式要优雅很多，且极大减少了 Token 消耗量。

不过，个人认为至少还有两点缺陷：
- 随着记忆内容的增多，每次对话，把所有记忆内容都作为上下文，会显得十分冗余，这里可以结合 RAG 来做；
- 每次都从单论对话中提取记忆，缺乏足够的上下文，容易导致记忆内容的断章取义，理想的方式应该从多轮对话中提取有价值的信息；

这时，强烈建议你去试试上篇分享的 MemoryScope：

[如何赋予AI智能体长期记忆？阿里开源 MemoryScope 实战](https://blog.csdn.net/u010522887/article/details/143354689)

## 写在最后

本文通过一个简单案例，带大家拆解并实操了**Dify 搭建个性化记忆助手**，整体流程比较简单，相信看到这里的你，一定还有很多想法要去实现，快去试试吧~

如果对你有帮助，欢迎**点赞收藏**备用。

之前微信机器人`小爱(AI)`的多轮对话，是通过本地缓存上下文信息实现，其实完全可以用本文的智能体替代，后面抽空改造后，再和大家分享！

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。


