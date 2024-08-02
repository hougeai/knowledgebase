
前天，带大家体验了用 Ollama 在本地部署了大模型：

[本地部署大模型？Ollama 部署和实战，看这篇就够了](https://blog.csdn.net/u010522887/article/details/140651584)

不过为了带大家快速跑通流程，只用了最小的 `qwen:0.5B` 进行演示~

就在昨天，Meta 宣布 LlaMa 3.1 正式开源，叫板 OpenAI 闭源的 GPT-4o。

一经发布，LlaMa 3.1 就刷爆了各大自媒体平台~

# Llama3.1 强在哪？

Llama 3.1 共包含 8b、70b 和 405b 三种模型，它们都有 128k 最大上下文，就这一点，已经强于一众大模型了。

从性能上来看，405b 模型在通识、数学、翻译等一系列方面，都能力压 GPT-4o一头，甚至和 Claude3.5-sonnet 不分伯仲。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ef3362181ee7f8614a47add97059962e.png)

即便是参数量更小的 8b 和70b 模型在同等参数规模的选手中依然优势明显：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/376302fab7d147540c53316cfb4c652e.png)


# 部署体验

强不强，用了才知道！

今天就带大家尝个鲜，手把手在本地把 Llama3.1 的 8B 版本跑起来。

不需要有任何技术背景，只需几步走，小白也能完成。

## 1. 环境准备

Ollama 是目前最便捷的大模型本地部署工具。

还没搭建好的小伙伴，可以先参考猴哥前天的教程准备好环境：

[本地部署大模型？Ollama 部署和实战，看这篇就够了](https://blog.csdn.net/u010522887/article/details/140651584)

Ollama 准备好之后，即刻启程~

## 2. 模型下载

特意上 Ollama 的模型库看了一眼，12 小时刚上线，已经有 154.4K 的下载量了，这火热程度，可见非凡~

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/19fc015ffa39397795290e1711c1c5f0.png)

不过，并不需要你手动下载，Ollma 已经通过极简的命令帮你搞定了，接着往下看。


## 3. 一键启动

如果你是采用 Docker 镜像部署的，首先需要进入容器：

```
docker exec -it ollama /bin/bash
```

如果你是裸机部署的，可以采用如下命令一键运行 llama3.1
```
ollama run llama3.1
```

默认下载 8b 模型，等待模型下载完成，终端输出如下，它来了。。。

```
pulling manifest 
pulling 87048bcd5521... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████▏ 4.7 GB                         
pulling 8cf247399e57... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████▏ 1.7 KB                         
pulling f1cd752815fc... 100% ▕██████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  12 KB                         
pulling 56bb8bd477a5... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████▏   96 B                         
pulling e711233e7343... 100% ▕███████████████████████████████████████████████████████████████████████████████████████████████████████████████▏  485 B                         
verifying sha256 digest 
writing manifest 
removing any unused layers 
success 
>>> Send a message (/? for help)
```

当弹出提示：Send a message，你就可以与它进行互动了。

我们简单测试一下：
```
>>> 你是谁？
我是一款基于语言模型的人工智能-chatbot，我可以用自然语言理解并生成文本。
>>> Send a message (/? for help)
```

```
>>> 你可以教我学习 Python 么？
非常高兴地回答是！

我可以提供许多帮助您学习Python的资源：

1. **基本语法**: 我可以解释Python的基本语法，包括变量、数据类型、控制结构等。
2. **实例代码**: 我可以提供很多例子，帮助您理解如何使用Python来解决实际问题。
3. **常见问题**: 我可以回答您可能遇到的常见问题，如安装问题、错误处理等。
4. **学习指南**: 我可以推荐一些在线资源和教材，帮助您系统地学习Python。

您想要从哪里开始学习？

（例如：基础语法？实例代码？特定主题？）
```


我的服务器是用的甲骨文云的示例，配置 1C16G，跑 8B 的模型还是毫无压力的，不过速度嘛~ 还是不太能忍。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/1b12341beef3f6579ba37c61f2386edf.png)


## 4. Open WebUI 使用
进入 Open WebUI ，可以看到 llama3.1 模型已经注册好了。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/20a7ca7cab65464a80cf4581f280b213.png)


我们来问他一个最经典的问题：*3.9 和 3.11 哪个大？*


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3522bbea851f725da07c5c2c936f17ba.png)

哎，看来这个难倒一众 LLM 的问题，*llama3 也未能幸免~*

即便是用上 `反问` 的策略，它也在像模像样地胡说八道~

也许，换用最强的 llama3.1 405B 会好很多，感兴趣且有资源测试大模型的小伙伴，快去试试吧~ 评论区等你。。。🤟🏻

目前解决这类问题还是得上 function call。在大模型没有完全解决幻觉问题之前，也许调用外部函数，是当前最靠谱的思路。

# 写在最后

作为开源大模型界的扛把子，LlaMA 从 1.0 成长到 3.1，造福了无数开发者和创业公司，很多垂类大模型都是基于 LlaMA 训练/微调。

正如 Meta 的 CEO 扎尔伯格所说：开源是 AI 前进的方向。

希望 AI 不再是束之高阁的黑科技，希望能帮到更多人学好/用好 AI，激发创造，丰富生活。

猴哥的文章偏实操，大家跟着走，可以一步一步学起来~

如果本文对你有帮助，欢迎**点赞收藏**备用！你的支持是我创作的最大动力。


