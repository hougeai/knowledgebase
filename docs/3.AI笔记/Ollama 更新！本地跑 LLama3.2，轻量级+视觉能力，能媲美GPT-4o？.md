前段时间，Meta 开源了 Llama 3.2 轻量化模型，为移动端跑大模型提供了新选择！

同时，Llama 3.2 视觉模型（Llama 3.2 Vision）也正式开源，号称媲美 GPT-4o。

前两天，Llama 3.2 Vision 在 Ollama 上也正式上线！

今日分享，就对 Llama 3.2 Vision 实测一番。

最后，应用到我们上篇的`票据识别`任务中，看看效果真有官宣的那么惊艳么？


## 1. Llama 3.2 亮点

老规矩，还是简短介绍下：**Llama 3.2 都有哪些亮点**？

一句话：轻量化 + 视觉多模态能力！

具体点：

- 文本模型：有 1B 和 3B 版本，即便参数少，也支持128k tokens的上下文长度；基于LoRA和SpinQuant 对模型进行深度优化，**内存使用量减少41%**，**推理效率翻了2-4倍**。
- 多模态模型：有 11B 和 90B 版本，在视觉理解方面，与Claude3 Haiku和GPT 4o-mini 可 PK。

## 2. Llama 3.2 实测

Ollama 是面向小白友好的大模型部署工具，为此本篇继续采用 Ollama 跑 Llama 3.2。

不了解 Ollama 的小伙伴，可翻看之前的教程：

[本地部署大模型？Ollama 部署和实战，看这篇就够了](https://zhuanlan.zhihu.com/p/710560829)

### 2.1 环境准备

参考上述教程，假设你在本地已经准备好 Ollama。

当前 Ollama Library 中已支持 Llama 3.2 下载，因此，一行命令把 llama3.2-vision 拉起来。

```
ollama run llama3.2-vision
```

**如果遇到如下报错：**

```
pulling manifest 
Error: pull model manifest: 412: 

The model you are attempting to pull requires a newer version of Ollama.
```

**说明你的 ollama 版本需要更新了。**

如果你也和我一样，采用 docker 安装，则需要删除容器，重新下载最新镜像进行安装：

```
docker stop ollama
docker rm ollama
docker image rm ollama/ollama
# 注：海外镜像，国内用户需自备梯子
docker pull ollama/ollama
```

可以发现，当前最新版本为 0.4.1：
```
ollama --version
ollama version is 0.4.1
```


然后，再起一个容器：

```
docker run -d --gpus "device=2" -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama ollama/ollama
```

注：我这里指定 `--gpus "device=2"`，如果单张显存不够，需指定多张卡，Ollama 会帮你自动分配。

**显存占用情况如何？**

### 2.2 文本模型

进入容器，并下载模型 llama3.2 3B版本：
```
docker exec -it ollama /bin/bash
ollama run llama3.2
```

显存占用：请确保至少 4 G 显存。

![](https://img-blog.csdnimg.cn/img_convert/11001aa83325512337e28ec7f41db5b7.png)

### 2.3 多模态模型

进入容器，并下载模型 llama3.2-vision 11B版本：
```
docker exec -it ollama /bin/bash
ollama run llama3.2-vision
```

显存占用：请确保至少 12 G 显存。 
![](https://img-blog.csdnimg.cn/img_convert/90223701dfdcf12f6ae715f19533c9c7.png)

**注：ollama 中模型默认采用了 4bit 量化。**

## 3. 接入 Dify
### 3.1 模型接入
要把 Ollama 部署的模型接入 Dify 有两种方式。


首先，找到设置 - 模型供应商。

**方式一：**
找到 Ollama 类型，然后进行添加，记得把`Vision`能力打开：

![](https://img-blog.csdnimg.cn/img_convert/2b5aebe9eb91acb2eecaf48fcf8cd76b.png)

**方式二：**

把 Ollama 模型接入 OneAPI，然后在模型供应商这里选择 `OpenAI-API-compatible`。

![](https://img-blog.csdnimg.cn/img_convert/5ccb45a0d98fa3c51582df0608f6a835.png)

不了解 OneAPI 的小伙伴可以回看教程：[OneAPI-接口管理和分发神器：大模型一键封装成OpenAI协议](https://zhuanlan.zhihu.com/p/707769192)

个人更推荐 **方式二**，你会体会到接口统一的快乐~

### 3.2 应用集成

最后，我们在上篇的基础上，把用到 Qwen2-VL 的组件，LLM 全部替换成刚刚接入的 llama3.2-vision，如下图：

![](https://img-blog.csdnimg.cn/img_convert/7fd5d53d39be46fd27f114e5ac49311c.png)


实测效果咋样？

![](https://img-blog.csdnimg.cn/img_convert/0bbcef5b150396a4881a1dc5a87497f5.png)

嗯~ o(*￣▽￣*)o 价格等基本信息还是抓到了。

不过，相比上篇实测的 Qwen2-VL 就差点意思了：
- 从中文指令遵循上看：给到同样的提示词，llama3.2-vision 压根不按你的意图来；
- 从识别结果上看：中文 OCR 也被 Qwen2-VL 甩开好几条街。

当然，换用 90B 的模型会不会好很多？感兴趣的朋友可以试试~

**结论：现阶段，对于票据识别这个任务而言，综合考虑成本和效果，还是调用云端的 Qwen2-VL-72B 吧。**

## 写在最后

本文带大家本地跑了 Meta 最新开源的 Llama 3.2，并在票据识别任务上进行了实测。

个人体验而言：Llama 系列，都得在中文指令数据上微调后，才能中文场景中使用，同等参数规模下，国产大模型其实更具性价比。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近搭建的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。

