前文，分享了【小智Pro】系列文章：

[30天，AI 陪我写了3万行代码，上线一款应用，3点血泪教训](https://zhuanlan.zhihu.com/p/1970051780579660673)

[小智Pro：智能闹钟提醒 + 云端同步，端云协同方案](https://zhuanlan.zhihu.com/p/1970446275288741797)

[小智Pro：在线点歌+歌词同步，支持打断和搜索，端云协同方案](https://zhuanlan.zhihu.com/p/1971130142131730137)

今天来聊：如何给`小智`接入【知识库】，让它从此告别一问三不知！

关于【知识库】的设备端 MCP 实现，前文已有分享：

[小智 AI 外挂知识库RAG，打造私人定制专家](https://zhuanlan.zhihu.com/p/1951896126836945879)

为了降低大家的使用门槛，`小智Pro` 现已接入【知识库】功能。

下面上实操：

## 1. 平台知识库

### 1.1 创建知识库

点击左上角`创建知识库`，默认选择`平台自研知识库`：

![](https://i-blog.csdnimg.cn/img_convert/bd385c49b1ad22d3764d0f42881f112e.png)

### 1.2 设置知识库

![](https://i-blog.csdnimg.cn/img_convert/88846cb72a6526b372963a5829b09173.png)

**step 1**: 点击上方按钮区的`知识库设置`，弹出右侧抽屉


**step 2**: 配置模型（必填）

> 推荐前往硅基流动获取免费模型：[https://cloud.siliconflow.cn/i/DrgxdqSF](https://cloud.siliconflow.cn/i/DrgxdqSF)

**模型名称**：点击模型卡片 右上角 复制

**Base URL**：https://api.siliconflow.cn/v1

**API Key**：硅基流动-左侧导航栏-账户管理-API密钥

免费模型参考：
- 文本模型：Qwen/Qwen3-8B
- Embed 嵌入模型：BAAI/bge-m3
- Rerank 重排模型：BAAI/bge-reranker-v2-m3
- 多模态模型：THUDM/GLM-4.1V-9B-Thinking

**step 3**: 测试模型

这一步是为了确保模型公网可访问。

**step 4**: 保存模型

测试通过后，点击保存，自动生成模型ID。

![](https://i-blog.csdnimg.cn/img_convert/b1e2d3dfaf265dc35710fc7a9cd4149a.png)

**step 5**: 4个模型成功生成模型ID 之后，右下角点击`保存`，自动生成知识库 ID。


### 1.3 添加知识

知识库创建成功后，即可添加知识内容，当前支持两种类型：

- 本地文件：支持 PDF、Word、Markdown、TXT 和图片格式；
- 网页URL：确保公网可访问；

![](https://i-blog.csdnimg.cn/img_convert/7b520e38baf2d217440666875294475f.png)

上传后，需等待后端完成向量提取和索引构建：

![](https://i-blog.csdnimg.cn/img_convert/12d4c81a4e0d78bd2031b33906fef643.png)

前端会定期轮询后端索引状态，并更新：

![](https://i-blog.csdnimg.cn/img_convert/ad33938ceb97e2c68c9adb20cde4c85e.png)

当状态变更为`已索引`，代表该知识可用。

### 1.4 检索测试

在设备端使用之前，可以在前端先测试一下：

![](https://i-blog.csdnimg.cn/img_convert/c23f92ca52ed85fd897f3a78f6ead016.png)

### 1.5 设备端测试

前端检索没问题后，设备端`小智`即可通过 MCP 调用这里的知识库，获取相关上下文来回答你的问题了:

```
硅迹流动针对学生有哪些活动？
```

![](https://i-blog.csdnimg.cn/img_convert/a94a09faa61339d27243591a50c964fd.png)

```
那针对企业有哪些活动？
```

![](https://i-blog.csdnimg.cn/img_convert/0817475d5ca5b606edc739e814c1966e.png)

> PS：如果小智无法调用 MCP 检索知识库内容，可以在`小智控制台`-`配置角色`，添加提示词，比如：

![](https://i-blog.csdnimg.cn/img_convert/79e13b3ff199e4668bf89654614a0022.png)

或者提示它：调用知识库后回答：

![](https://i-blog.csdnimg.cn/img_convert/1bfd393a1714b490b86d540ebcbc4451.jpeg)



## 写在最后


本文分享了`小智Pro: 知识库搭建+设备端检索`的完整流程。

如果对你有帮助，不妨**点赞收藏**备用。

欢迎体验 `小智Pro` 更多功能，请戳👇：

> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

有任何问题，欢迎进群交流：

![](https://i-blog.csdnimg.cn/img_convert/2eaa3d03b2d60e53cd5310a415414878.png)

