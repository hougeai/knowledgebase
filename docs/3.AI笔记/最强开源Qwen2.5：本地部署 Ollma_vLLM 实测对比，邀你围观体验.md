最近 Qwen2.5 特别火，72B 模型性能超越 Llama3.1 405B，稳居全球最强开源大模型。

既然这么强，咱必须给它整起来啊。

前两天分享了：[手机端跑大模型：Ollma/llama.cpp/vLLM 实测对比](https://blog.csdn.net/u010522887/article/details/142310279)

Ollama 完胜 llama.cpp！奈何 vLLM 比较傲娇，在 arm 架构上搞不赢，还没能一睹它的芳容~

今天，刚好借 Qwen2.5 的东风，**实测 Ollma//vLLM 本地部署大模型**，到底该怎么选？


## 1. Qwen2.5 有哪些亮点
**模型规模多元**：分别为0.5/1.5/7/14/32/72B，分base和instruct两个版本。

**海量训练数据**：训练数据总量高达18T个token，具备强大的知识储备。

**指令遵循出色**：实测结构化输出（如json）遵循不错，其它指令遵循待测试。

**支持语种丰富**：支持超过29种语言，中文、英语、法语、西班牙语、德语、日语等。


## 2. Ollama 部署实测

当前 **Ollama**的 Library 中已支持 Qwen2.5 下载。

### 2.1 Ollama 安装

不了解 Ollama 的小伙伴，可翻看之前的教程：[本地部署大模型?Ollama 部署和实战，看这篇就够了](https://blog.csdn.net/u010522887/article/details/140651584)

这里，我们依然采用 Docker 安装，用官方最新镜像，拉起一个容器：

```
# CPU
sudo docker run -d -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama ollama/ollama
```

如果有 GPU，那就用如下命令，把 GPU 用上，跑大模型还是很吃算力的：
```
# GPU 单卡
sudo docker run -d --gpus "device=3" -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama ollama/ollama
# GPU 多卡
sudo docker run -d --gpus '"device=2,3"' -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama ollama/ollama
```

*友情提醒：docker 容器中指定多张 GPU，命令行中 `'"device=2,3"'` 需要加两个引号！*

### 2.2 Qwen2.5 下载

Ollama 容器启动成功后，进入容器，下载模型并运行：

```
sudo docker exec -it ollama /bin/bash
```

我这里下载了7/14/32b(资源有限，搞不定72b)：
```
ollama run qwen2.5:7b
ollama run qwen2.5:14b
ollama run qwen2.5:32b
```

这三个模型，资源占用情况如何？**先抛结论**：

```
NAME           显存占用   SIZE           
qwen2.5:32b    24 G      19 GB           
qwen2.5:14b    11 G      9.0 GB        
qwen2.5:7b     6 G       4.7 GB   
```

- qwen2.5:7b 模型权重大小 4.7GB，运行 **6G 显存**就够。

![](https://img-blog.csdnimg.cn/img_convert/b4267ab82c2bfb9b7924142e2bef99f5.png)

- qwen2.5:14b 模型权重大小 9GB，运行需要 **11G 显存**。

![](https://img-blog.csdnimg.cn/img_convert/908f8301efe19b2b62e2348671af475b.png)

- qwen2.5:32b 模型权重大小 19GB，运行需要 **24G 显存**。

![](https://img-blog.csdnimg.cn/img_convert/7bc8e57ea339f8006069b7fb057f9854.png)

注：单张 16G 显卡，只够跑 14b 模型，所以我这里用了两张 4080 跑 32b 模型，**Ollama 会自动将模型分配到两张卡上**。此外，如果启动一段时间没有调用，**Ollama 会自动释放显存**，简直不要太友好。


### 2.3 接入OneAPI

如果要接入兼容 OpenAI 格式的应用，可考虑将 Ollama 的模型接入 OneAPI。

不了解 OneAPI 的小伙伴，可参考这篇教程：[OneAPI-接口管理和分发神器：所有大模型一键封装成OpenAI协议](https://zhuanlan.zhihu.com/p/707769192)

新建一个渠道，把我们刚部署的三个模型接进来：

![](https://img-blog.csdnimg.cn/img_convert/93845f12f86b16716605a0b5ae6ed835.png)

**注意**：渠道最后的代理位置，需要要填主机的**公网 IP 地址**。

如果没有公网 IP 咋办？

可参考之前教程：[【白嫖 Cloudflare】之 免费内网穿透，让本地AI服务，触达全球](https://blog.csdn.net/u010522887/article/details/141621570)，把内网服务穿透出来。

### 2.4 推理速度对比

以下是 Ollama 原生调用：
```
Ollama 原生调用 -- GPU：
第1次调用：3.02秒, token/s:121.90
第2次调用：2.84秒, token/s:122.96
第3次调用：3.16秒, token/s:122.59
第4次调用：2.62秒, token/s:121.59
第5次调用：2.68秒, token/s:126.79
---
Ollama 原生调用 -- CPU：
第1次调用：36.59秒, token/s:11.59
第2次调用：34.16秒, token/s:13.94
第3次调用：32.24秒, token/s:12.78
第4次调用：40.60秒, token/s:13.08
第5次调用：22.18秒, token/s:13.93
```
**可见 GPU 推理速度是 CPU 的 10+ 倍!**

接入 OneAPI 是方便集成了，但速度会受影响么？

显然的。。。内网穿透，数据都经过海底隧道走了两圈了，能不慢么？来看看吧：

```
Ollama 接入 OneAPI -- localhost调用:
第1次调用：3.47秒, token/s:105.99
第2次调用：3.44秒, token/s:118.40
第3次调用：3.14秒, token/s:109.80
第4次调用：2.33秒, token/s:107.97
第5次调用：2.98秒, token/s:106.32
---
Ollama 接入 OneAPI -- 域名调用：
第1次调用：23.06秒, token/s:11.54
第2次调用：3.56秒, token/s:101.78
第3次调用：3.67秒, token/s:99.89
第4次调用：4.01秒, token/s:94.40
第5次调用：3.60秒, token/s:99.56
```



## 3. vLLM 部署实测
vLLM 只支持从 huggingface/modelscope 等平台下载的模型文件。

考虑到大家访问外网受限，ModelScope 提供了和 huggingface 类似的丝滑体验，我们就从 ModelScope 拉模型。

### 3.1 Qwen2.5 下载
前往：[https://modelscope.cn/models/qwen/Qwen2.5-7B-Instruct](https://modelscope.cn/models/qwen/Qwen2.5-7B-Instruct)

ModelScope 上下载模型有两种方式：

**方式一：git lfs**
```
git lfs install
git clone https://www.modelscope.cn/qwen/Qwen2.5-7B-Instruct.git
```

**方式二：modelscope 命令**

```
# 先安装ModelScope
pip install modelscope
# 下载完整模型
modelscope download --model qwen/Qwen2.5-7B-Instruct
# 如果只需下载单个文件
modelscope download --model qwen/Qwen2.5-7B-Instruct README.md
```

两种方式有什么区别？亲测速度没啥区别，方式二的优势是，可以实时显示下载进度，所以更推荐大家用方式二。

不过，这下载速度，相比 Ollma，简直不能忍👇

![](https://img-blog.csdnimg.cn/img_convert/d63f2a1d12e8a9b3125ecce7c800578b.png)

下载的模型默认保存在下面地址，7b 的模型占了 15G 磁盘空间。
```
~/.cache/modelscope/hub/qwen/Qwen2___5-7B-Instruct
```

### 3.2 vLLM 安装
参考文档：[https://docs.vllm.ai/en/latest/getting_started/installation.html](https://docs.vllm.ai/en/latest/getting_started/installation.html)

如果你本地已准备好 CUDA12.1 环境，可采用如下命令一键安装：
```
pip install vllm
```
当前最新版 `vllm-0.6.1`，依赖`torch-2.4.0`，下载过程中会安装 `nvidia_cudnn_cu12` 等一众依赖，所以最好配合虚拟环境使用，耐心等吧！


### 3.3 vLLM 实测

参考文档：[https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

命令行一键启动 OpenAI 服务：
```
vllm serve ~/.cache/modelscope/hub/qwen/Qwen2___5-7B-Instruct --dtype auto --api-key 123 --port 3003 --tensor-parallel-size 2
```
单卡 16G 显存，加载 7b 模型，居然 ` CUDA out of memory` 了？

你知道 Ollama 只需 6G 显存，懂的小伙伴帮忙评论区解释下~

无奈，只要加上`--tensor-parallel-size 2`，用两张卡并行跑吧。

终于，起来了，但看显存占用👇

![](https://img-blog.csdnimg.cn/img_convert/082dabd2dcb84ffeab2b8a6aa445ca81.png)


这资源占用，用 Ollama 跑 32b 模型，不香？

资源占用大，难道推理速度要起飞？

来测了看看：

```
第1次调用：2.23秒, token/s:95.30
第2次调用：3.32秒, token/s:98.05
第3次调用：4.34秒, token/s:99.02
第4次调用：3.81秒, token/s:92.54
第5次调用：3.69秒, token/s:93.59
```

同样是 7 b 模型，和 Ollama 差距可不小。。。

还有什么理由用 vLLM？

## 写在最后

本文以 Qwen2.5 为例，实测了 Ollama/vLLM，回答了本地部署大模型该用哪款框架。

综合来看，Ollma 在**存储、计算、效率**三方面，均完爆 vLLM。

不知道大家体验咋样，欢迎评论区交流。

如果对你有帮助，不妨**点赞收藏**备用。

--- 

最近一直在打造微信机器人`小爱(AI)`，目前也已接入 `qwen2.5:32b`。

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

`小爱(AI)`也在群里，如需体验，公众号后台「联系我」即可，拉你进群。

--- 

猴哥的文章一直秉承`分享干货 真诚利他`的原则，最近陆续有几篇`分享免费资源`的文章被CSDN下架，申诉无效，也懒得费口舌了，欢迎大家关注下方公众号，同步更新中。


