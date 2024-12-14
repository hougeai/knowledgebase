前段时间，陆续和大家分享了`Dify 搭建智能体`的实战系列文章：

- [Dify 保姆级教程之：零代码打造 AI 搜索引擎](https://zhuanlan.zhihu.com/p/4179408710)
- [Dify 保姆级教程之：零代码打造个性化记忆助手](https://zhuanlan.zhihu.com/p/4576860098)
- [Dify 保姆级教程之：零代码打造票据识别专家](https://zhuanlan.zhihu.com/p/5465385787)

本次分享，带大家熟悉 `Dify` 中另外两个重要概念 -- `智能体`+`工作流`，进而打造一个`图像生成专家`。

## 1. 聊天助手 VS 智能体

Dify 中，有几个概念不太容易区分，很多小伙伴问：

下图中`聊天助手`和`智能体`到底有什么区别？

`工作流` 又是啥？

![](https://img-blog.csdnimg.cn/img_convert/3458d5075136e4c373f5b4bd953c1397.png)

笔者一开始进来也懵，进去体验一番，也只能有个感性认识。

为了回答上述问题，特地去查了下官方文档，下面用大白话分享给大家：

- `聊天助手`：主要面向对话式应用，咱们前几篇教程都是基于`聊天助手`搭建。它有两种搭建方式：其中`基础编排`一个大模型就可以搞定，而`工作流编排`则适用于*多步逻辑/多个模型*的对话式应用。

![](https://img-blog.csdnimg.cn/img_convert/fbdad4904652cebca883e3e52791ba66.png)

- `文本生成应用`：这个就更简单了，只支持单次对话，适用于文章生成、翻译等任务。

- `Agent`：完全自主化的智能体，对复杂任务进行规划、拆解、工具调用、迭代。适用于要调用`外部工具`的场景。Dify 为`Agent`提供了 Function calling（函数调用）和 ReAct 两种推理模式。
  - Function calling：适用于**支持** Function call 的模型
  - ReAct：适用于**不支持** Function call 的模型。

- `工作流`：面向自动化和批处理情景，适合数据分析、电子邮件自动化等场景。

值得注意的是：`工作流`支持发布为工具，然后在`Agent`中调用。

下面，我们就来实操这个过程：用`工作流`的方式创建一个`图片生成工具`，然后在`图片生成Agent`中调用。

## 2. 创建工作流

### 2.1 图像生成API获取

AI 图像生成技术已经非常成熟，从 SD 到 Flux 再到最近的小熊猫，高质量、高分辨率且逼真的图像，已不再难求。

然而，这些模型通常比较大，本地部署成本非常高，为此，推荐大家前往[硅基官网](https://cloud.siliconflow.cn/?referrer=clxv36914000l6xncevco3u1y)注册一个账号，体验它的免费模型！

![](https://img-blog.csdnimg.cn/img_convert/640176631b0923be9954415edc1684dd.png)

注册成功后，新建一个 api_key，下面会用到。关于如何获取 api_key，猴哥之前多次分享，这里不再赘述！ 


### 2.2 新建工作流

在创建空白应用这里，选择`工作流`：

![](https://img-blog.csdnimg.cn/img_convert/8f486d3ff06b7717a148e1bec84969ae.png)


进来后，页面只有一个`开始`组件，给它添加上两个字段，用于后续请求图像生成API：

![](https://img-blog.csdnimg.cn/img_convert/ec08e59790ddad2f5dd0786a1b3c7d06.png)

**你怎么知道添加哪些字段呢？**
> 参考硅基的API文档：[https://docs.siliconflow.cn/api-reference/images/images-generations](https://docs.siliconflow.cn/api-reference/images/images-generations)

Body 内需要的字段，就是我们要准备的：

![](https://img-blog.csdnimg.cn/img_convert/d03325b5dbf3ccc62174de3496825feb.png)

### 2.3 添加HTTP请求节点
然后，在`开始`节点后面新建一个节点：`HTTP`请求，填写如下：

![](https://img-blog.csdnimg.cn/img_convert/383c1e2b0583eae99c72b26b884d12d0.png)

这里有几点需要注意：
- BODY：需选择 `Json` 格式，字段务必加上双引号。
- 鉴权：右上角鉴权位置，填写你在硅基申请的 api_key。否则无法成功调用。

![](https://img-blog.csdnimg.cn/img_convert/421e7ae7f76708f408693b54327afd4b.png)

### 2.4 添加代码执行节点
`HTTP请求`节点输出的标准的 response，为了提取其中 Body 中的内容，我们需要一个`代码执行`节点，把生成图片的 url 拿到。


`代码执行`节点，编辑如下：

![](https://img-blog.csdnimg.cn/img_convert/5780513fea38a4bc7b1b681b6e600fe1.png)

这里有几点需要注意：
- arg1：传入 http 请求得到的 body 字段。
- 代码：输入是字符串格式，用 json 转成 dict。
  - import json 需放入 main 函数里；
  - 函数返回值必须为 dict 格式。

### 2.5 添加结束节点

直接将`代码执行`节点的 url 字段输出：

![](https://img-blog.csdnimg.cn/img_convert/8f02b86955d7d80119348bb767b87657.png)

### 2.6 发布为工具
最后，点击右上角`发布`，记得最下方完成配置，才能发布为工具：

![](https://img-blog.csdnimg.cn/img_convert/a87ce6491f7b1e7ba8be3e2c3eb0a929.png)

如下图所示，给工具起一个英文名字，工具描述这里，尽可能详细，明确具体用途，方便大模型按需调用！

工具入参，也要加上描述，以便大模型能够生成对应的参数值，提高调用成功率！

![](https://img-blog.csdnimg.cn/img_convert/30627585d0a2d82cd907339fdb6f4ec4.png)

至此，一个`图像生成工具`就制作完成了。

下面，我们创建一个 Agent 来调用它。

## 3. 创建 Agent

### 3.1 实操步骤

创建应用，选这个：

![](https://img-blog.csdnimg.cn/img_convert/dc0181ff2ab04b60b45e765cdc443a14.png)

**Step 1:** 在下方把刚做好的`图像生成工具`加上：

![](https://img-blog.csdnimg.cn/img_convert/3685458383cd944dd90dd6c47c071850.png)

**Step 2:** 编写角色提示词：

![](https://img-blog.csdnimg.cn/img_convert/4741819b36e7e3a5f3d6cc535bdc0e3d.png)

**Step 3:** Agent 设置：

![](https://img-blog.csdnimg.cn/img_convert/ed61b237a1e3547e6ec76bb1ffade338.png)

![](https://img-blog.csdnimg.cn/img_convert/750191c28c666337c361dfac8322f070.png)

图中的大模型只支持 ReAct 方式实现函数调用，如果你的模型支持 Function call，可进行选择。


**Step 4:** 调试和预览：

![](https://img-blog.csdnimg.cn/img_convert/daef47fdf16b2bedbeb0783ea9e147bc.png)

**如果希望实时显示图像呢？**

来，修改一下提示词：

```
根据用户输入，生成给图像流工具{{generate_image}}的参数：提示词和图像尺寸，
获得最终的生成图像的url，并显示最终的图像
```

![](https://img-blog.csdnimg.cn/img_convert/37e69b64cb7a030d1c666b4dab3128fc.png)

如果我指定了尺寸，智能体会自动选择一个最匹配的尺寸参数，如下图所示：

![](https://img-blog.csdnimg.cn/img_convert/3b6c3315e1579283bb83c894c8a686f2.png)

**生成效果不咋样？**

对，提示词最好改为英文，以确保生成效果。

当然这一步也可以交给智能体，只需修改提示词如下：

```
根据用户输入，生成给图像流工具{{generate_image}}的参数：提示词和图像尺寸，获得最终的生成图像的url，并显示最终的图像
要求：
- 提示词：请从对话记录中找到和图片生成相关的词汇，生成给stable diffusion等图片生成模型的英文提示词；
- 图像尺寸：请从对话记录中找到和图像尺寸相关的词汇，并找到图像尺寸选项中最接近的一个，如果没有相关词汇，则默认选择768x1024
```

### 3.2 效果展示

![](https://img-blog.csdnimg.cn/img_convert/d35ff0d803a66cc7d92f3c85275e16ea.png)

![](https://img-blog.csdnimg.cn/img_convert/8cb5a6a12217404b031402ee62c75e92.png)


### 3.3 API调用

智能体发布后，就可以在后端调用它的 API。

不过，Dify 中 Agent 的 API 调用有点特殊：**只支持流式输出**！
*不知道为啥 Dify 这样设置，懂的小伙伴帮忙评论区解释一下。*

python 端的调用代码示例如下：

```
url = 'http://localhost:3006/v1/chat-messages'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

data = {
    "inputs": {},
    "query": "生成一张猫的图片，尺寸2:1",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "xiaoai",
}

response = requests.post(url, headers=headers, json=data)
events = []
for chunk in response.iter_lines():
    if chunk:
        chunk_data = chunk.decode('utf-8').replace('data: ', '')
        events.append(json.loads(chunk_data))
with open('data.json', 'w') as f:
    json.dump(events, f, indent=4, ensure_ascii=False)
```

## 写在最后

本文通过综合运用`工作流`和`Agent`，带大家实操了**Dify 搭建图像生成专家**。

前端使用还是很丝滑的，但后端调用时，因为流式输出，出现了各种问题。

篇幅有点长，下篇再来分享：如何采用`聊天助手-工作流编排`，实现`图像生成专家`的后端调用。

如果对你有帮助，欢迎**点赞收藏**备用。


--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近搭建的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。






