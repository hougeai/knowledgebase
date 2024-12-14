
昨天，利用 `Dify` 打造了一个`图像生成智能体`：

- [Dify 保姆级教程之：零代码打造图像生成专家（上）](https://blog.csdn.net/u010522887/article/details/143874061)

无奈后端调用不够丝滑，今天：将上篇的智能体，换用`聊天助手-工作流编排`的方式搭建，从而将`图像生成专家`接入微信机器人-`小爱(AI)`，方便大家体验。

先看下搭建完成后的`流程图`（有需要的朋友，文末自取）：

![](https://img-blog.csdnimg.cn/img_convert/c43c6c80ef917d082f4aba56f65a5dac.png)

大致流程：用户输入生成生成图片的诉求，`大模型LLM`分析后，输出结构化的：`绘图提示词`、`图片尺寸`等信息，然后通过`HTTP请求`调用`绘图大模型`，最终给出生成图片。

话不多说，上实操！

## 1. 聊天助手-工作流编排

**Step 1:** 创建应用

![](https://img-blog.csdnimg.cn/img_convert/24578df8c8c325fac90b95fdc4921827.png)

**Step 2:** 修改 LLM 节点，编写提示词如下：
```
根据用户聊天记录和用户输入{{#sys.query#}}，生成给图像生成工具的参数：提示词和图像尺寸。
- 提示词：请从对话记录中找到和图片生成相关的词汇，生成给stable diffusion等图片生成模型的英文提示词，提示词内容尽可能丰富；
- 图像尺寸：请从对话记录中找到和图像尺寸相关的词汇，并找到和图像尺寸选项中最接近的一个，如果没有相关词汇，则默认选择1024x576。图像尺寸选项有：1024x1024, 512x1024, 576x1024, 1024x576
要求：
最终只需输出json格式的文本，内容格式如下：
{”prompt“:"english prompt", "image_size":"1024x576"}
```

![](https://img-blog.csdnimg.cn/img_convert/1a82b7d72a87327b34084d6583e0f00f.png)

**Step 3:** 添加`代码执行`节点，编写代码如下，把大模型的输出，变成结构化的字典：

```
def main(arg1: str) -> dict:
    import json
    data = json.loads(arg1)
    return {
        "prompt": data['prompt'],
        "image_size": data['image_size']
    }
```

这一步，我们将获得两个变量：
- prompt：给绘画模型的英文提示词，经过了 LLM 的润色；
- image_size：期望生成的图片尺寸，由 LLM 决策。

![](https://img-blog.csdnimg.cn/img_convert/06f04d3d10333fbad6803718096db8d9.png)

**Step 3:** 添加`HTTP请求`节点，和上篇一样，我们还是采用[硅基](https://cloud.siliconflow.cn/?referrer=clxv36914000l6xncevco3u1y)的绘图API，编辑如下：

![](https://img-blog.csdnimg.cn/img_convert/61e00fddf24c03189309aa1255788a6b.png)

**Step 4:** 添加`代码执行2`节点，这一步是为了提取`HTTP请求`，也即绘图API生成的图像 url：

![](https://img-blog.csdnimg.cn/img_convert/025c078b52a83df50467f1da01b406a9.png)

**Step 5:** 添加`直接回复`节点，为了在web端显示图像，需要将图像 url 转成 markdown 格式：`![](url)`:


![](https://img-blog.csdnimg.cn/img_convert/e1a9dbffbcf2802cb0ef61edbb36c348.png)


至此，一个完整的`图像生成`工作流就搭建完了，如下：

![](https://img-blog.csdnimg.cn/img_convert/c43c6c80ef917d082f4aba56f65a5dac.png)

## 2. 效果展示

搞定工作流，我们点击`预览`来测试下。

**第一轮：生成猫的图像**

![](https://img-blog.csdnimg.cn/img_convert/722592f6a84c858e46c6cc066a7a17e6.png)

**第二轮：要求尺寸9:16**

![](https://img-blog.csdnimg.cn/img_convert/082e5851e5bfc11e8d6b8957c12c4081.png)


**第三轮：要求在草地上奔跑**

![](https://img-blog.csdnimg.cn/img_convert/38c15664875052c3b06b8a20c54a7037.png)

**因为 Dify 工作流内置了记忆，默认支持 10 轮连续对话，所以，你只需不断提需求，逐步生成你想要的图像。**

## 3. API 调用

关于如何调用 API，可以参考之前的分享。

不过，有一点需要注意：如果要实现多轮对话，传参一定要加上：`user`和`conversation_id`。

而`conversation_id`是系统在第一次对话后自动生成的UUID（Universally Unique Identifier，通用唯一识别码），不可手动传入。

为此，需要把`conversation_id`缓存到数据库，否则每次调用都将是一次新的对话。

大致流程，可以表示如下：


```
# 从数据库中获取conversion_id
conversion_id = get_conversation_id(uname=from_name, agent_name='image', start_time=start_time)
# 基于conversion_id请求绘画模型
image_url, conversion_id = generate_dify_image(text=content, user=from_name, conversation_id=conversion_id)
# 把conversion_id缓存到数据库
if conversion_id:
    add_conversation_id(conversation_id=conversion_id, uname=from_name, agent_name='image', timestamp=datetime.now().strftime("%Y%m%d%H%M%S"))
```
## 4. 接入小爱
最后，我们把做好的绘画智能体，接入到微信机器人-`小爱(AI)`：

![](https://img-blog.csdnimg.cn/img_convert/5a2ad27aec2d74ae8e482a17a1a32a0e.png)

![](https://img-blog.csdnimg.cn/img_convert/08849158aeb3a31bec55303c96121364.png)

## 写在最后

本文带大家实操了**Dify 搭建图像生成专家**，并实现了后端调用。

如果对你有帮助，欢迎**点赞收藏**备用。

> PS：本文工作流完整的 DSL，分享给有需要的朋友，公众号后台，发送`图像生成`自取。
>
> 关于 DSL 如何导入，可参考：[Dify 保姆级教程之：零代码打造票据识别专家](https://zhuanlan.zhihu.com/p/5465385787)

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。


