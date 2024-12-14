前段时间，陆续和大家分享了`Dify 搭建智能体`的实战系列文章：
- [Dify 保姆级教程之：零代码打造 AI 搜索引擎](https://blog.csdn.net/u010522887/article/details/143382888)
- [Dify 保姆级教程之：零代码打造个性化记忆助手](https://blog.csdn.net/u010522887/article/details/143445416)

相信实操过的同学对 `Dify` 的基本组件已有所了解，本篇我们继续熟悉 `Dify` 中另外一个重要概念 -- `条件分支`，带你零代码打造一个`票据识别专家`。

自从有了 `Dify`，代码小白也可以轻松打造智能体，你需要做的只是在web页面`点点点`而已！ 

先给大家展示下搭建完成的`流程图`：

![](https://img-blog.csdnimg.cn/img_convert/f9ea8d93832caaa1a63685e5afb0ead5.png)

这里面大致流程：用户上传一张发票图片，`发票类型识别大模型`判断发票类型，然后通过`条件分支`分发给不同的`票据识别`大模型，给出识别结果。

接下来，我们一步一步搞定它！

## 1. 单类型票据识别

### 1.1 新建聊天助手
首先，我们来搞定单个分支，跑通`单类型票据识别`的流程。

和上篇一样，我们先创建一个空白应用，选择工作流编排：

![](https://img-blog.csdnimg.cn/img_convert/eb2247dee22ef3a38b9fe562619cd97a.png)

进来后，默认已给你配置了一个最简单的工作流：

![](https://img-blog.csdnimg.cn/img_convert/d65d937f8711b60b745baf78290dabd2.png)

### 1.2 修改 LLM 组件
现在，需要做的就是修改下 LLM 组件的角色提示词，在`SYSTEM`中填入：

```
根据图片识别内容，给出json格式的结构化信息，包括：起始站，终点站，车次，乘车日期，出发时间，票面价格，身份证号，姓名。
```

因为我们的任务非常简单，因此无需复杂的提示词，只要把你的要求清晰表达出来即可。

不过，这里需要选择支持`多模态输入`的大模型，不了解如何接入大模型的小伙伴可以翻看之前的教程。

我这里先尝试了 `google` 的 `gemini-1.5-flash`，记得在下方把`视觉`选项打开，否则 Dify 默认不启用多模态能力。
 
![](https://img-blog.csdnimg.cn/img_convert/252180722addce24c64d73f7e6e8eae1.png)


就这么简单，一个火车票识别智能体就搭建完了。

![](https://img-blog.csdnimg.cn/img_convert/8676f04d47952e89af9207085880bf84.png)

来试试效果咋样吧？

![](https://img-blog.csdnimg.cn/img_convert/671b12ba2db17596ff7648e1a309f545.png)

从上图可以发现，`gemini-1.5-flash` 始终无法 get `车次`的概念，即便我指示了`车次`在图中的位置。

没招了，只能更换底层大模型！

市面上支持`多模态输入`的大模型还有很多，实测下来，发现`Qwen/Qwen2-VL-72B-Instruct`的错误率最低，推荐大家使用！

### 1.3 更换大模型 Qwen2-VL 

`72B` 的模型，本地部署的成本可太高了。如果你只是想体验一把，可以前往[硅基官网](https://cloud.siliconflow.cn/?referrer=clxv36914000l6xncevco3u1y)注册一个账号，新用户有赠费，体验它的付费模型，妥妥够了！

因为硅基的模型兼容 OpenAI 格式，因此注册拿到 API Key 之后，回到 `Dify` 模型配置这里，选择 `OpenAI-API-compatible` 类型：

![](https://img-blog.csdnimg.cn/img_convert/ecb8455346a7a6b47856fe9401ccf740.png)

注意如下字段的填写，模型名称填入``Qwen/Qwen2-VL-72B-Instruct``，API endpoint URL 一定是 `https://api.siliconflow.cn/v1`：

![](https://img-blog.csdnimg.cn/img_convert/7418d6a21e310f0984c9ec6dce0f507c.png)


拉到下方，将 `Vision` 支持选上，最后记得保存！

![](https://img-blog.csdnimg.cn/img_convert/4ffec9ff4842cd39779606d9fa6bb830.png)


最后，回到我们的工作流，把 LLM 模型换过来：

![](https://img-blog.csdnimg.cn/img_convert/188eb09cc9878164f615baa492d3bc98.png)

终于，成功搞定：

![](https://img-blog.csdnimg.cn/img_convert/49b254febb84baed3c6fd876b1ff10bc.png)

看来，对于火车票这种类型图片，海外模型总归水土不服，还得国产的上！

## 2. 多类型票据识别
有了`单类型票据识别`，要能识别多种类型，咋搞？

总得要判断语句吧，怎么判断呢？

遇事不决，交给大模型。

只需加一个`发票类型识别`的LLM即可：

![](https://img-blog.csdnimg.cn/img_convert/9939df6a02efc6710e8cc44b06f2f431.png)

比如，这里以`两个发票类型`举例，提示词如下：

```
你是发票识别专家，根据用户上传的发票图像，给出发票类型。只需返回指定的发票类型对应的序号，无需其他任何内容。
发票类型包括：
1.火车票
2.增值税电子发票
如果无法判断，直接输出0。
```
### 2.1 添加条件分支 

然后，在工作流种添加一个`条件分支`：

![](https://img-blog.csdnimg.cn/img_convert/84f9fa94932e5fd3ab985a83fbdf9012.png)

`条件分支`会根据`发票类型识别大模型`的输出，路由到不同的`识别大模型`。

为此，我们再来添加一个`电子发票识别`的大模型，提示词结构和`火车票`一样，唯一的区别就是输出内容，你改下即可：

```
根据图片识别内容，给出json格式的结构化信息，包括：发票标题，发票号码，开票日期，购买方信息名称，购买方统一社会信用代码/纳税人识别号，销售方信息名称，销售方统一社会信用代码/纳税人识别号，项目名称，规格型号，单位，数量，单价，金额，价税合计（小写），备注。
```

### 2.2 添加变量聚合器

最后，我们可以把不同`识别大模型`的输出，都统一路由到一个叫`变量聚合器`的组件中：

![](https://img-blog.csdnimg.cn/img_convert/c04c731a9e7aaf0b7dfa771ee09e4779.png)

否则，你要为每个`识别大模型`分支新建一个`输出`组件，岂不是很麻烦？

搭建完毕，点击上方`预览`来测试下：

![](https://img-blog.csdnimg.cn/img_convert/0b7c6baab637372b74c7a0235a9942ce.png)


至此，一个支持`多类型票据识别`的智能体就搞定了，整体流程如下：

![](https://img-blog.csdnimg.cn/img_convert/f9ea8d93832caaa1a63685e5afb0ead5.png)

怎么样，是不是很简单？

### 2.3 附：导入工作流

为了方便有需要的朋友参考，完整的 DSL 发给大家，公众号后台，发送`票据识别`自取。

你只需要，在新建聊天助手时，选择从这里导入：

![](https://img-blog.csdnimg.cn/img_convert/49df47ba4b9516ab96620d01f11e8ed8.png)

![](https://img-blog.csdnimg.cn/img_convert/f2be4f728a4c2ca14be3b6238b20180b.png)

## 3. 智能体发布
拿到这些结构化数据后，如果要在后端做进一步处理，比如接入数据库、接入微信等，就需要把智能体发布，并拿到 Dify 的 API。

之前的教程中有实操：[Dify 保姆级教程之：零代码打造 AI 搜索引擎](https://blog.csdn.net/u010522887/article/details/143382888)，在此不再赘述。

## 写在最后

本文通过一个简单案例，带大家实操了**Dify 搭建票据识别专家**。

整体流程比较简单，相信看到这里的你，一定还有很多想法要去实现，快去试试吧~

如果对你有帮助，欢迎**点赞收藏**备用。


--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近搭建的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。





