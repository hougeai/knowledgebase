
前两天，搞了个微信 AI 小助理-`小爱(AI)`，爸妈玩的不亦乐乎。
- [零风险！零费用！我把AI接入微信群，爸妈玩嗨了，附教程（下）](https://blog.csdn.net/u010522887/article/details/141882177)

最近一直在迭代中，挖掘`小爱`的无限潜力:
- [链接丢给它，精华吐出来！微信AI小助理太强了，附完整提示词](https://blog.csdn.net/u010522887/article/details/141924070)
- [拥有一个能倾听你心声的「微信AI小助理」，是一种什么体验？](https://blog.csdn.net/u010522887/article/details/141986065)
- [小爱打工，你躺平！让「微信AI小助理」接管你的文件处理，一个字：爽！](https://blog.csdn.net/u010522887/article/details/142023012)
- [我把多模态大模型接入了「小爱」，痛快来一场「表情包斗图」！不服来战！](https://blog.csdn.net/u010522887/article/details/142038164)

有朋友问：`小爱`能 AI 绘画么？

`小爱`：害，不过是接个模型的事儿~ 扶我来战！


今日分享，继续带大家实操：如何让`小爱`理解用户需求，并生成满足需求的图片！

要实现`AI 绘画`功能，我们先来拆解下步骤：
- **识别用户意图**：从用户输入中识别出`AI 绘画`的意图；
- **生成绘画提示词**：根据用户输入，生成给绘画模型的提示词；
- **生成图片**：调用图片生成模型的接口，返回图片 url。


## 1. 识别用户意图

在[零风险！零费用！我把AI接入微信群，爸妈玩嗨了，附教程（下）](https://blog.csdn.net/u010522887/article/details/141882177)的基础上，我们只需在`意图列表`中新增一条：`图片生成`。

提示词如下：
```
intentions_list = ['天气', '步行规划', '骑行规划', '驾车规划', '公交规划', '地点推荐', '图片生成']
intentions_str = '、'.join(intentions_list)

sys_intention_rec = f'''
  你是意图识别专家，我会给你一句用户的聊天内容，帮我分析出他的意图。
  要求：
  1. 只有当你非常明确意图来自以下类别：{intentions_str}，才能回答，否则请回复“其它”。
  2. 直接回答意图标签即可，无需回答其它任何内容。
  '''
```

这样，LLM 从用户输入中识别到`图片生成`后，就直接路由到指定的处理逻辑。

## 2. 生成绘画提示词

由于用户输入是非结构化，这就需要提取出和`绘画提示词`相关的内容。

不过，这事简单，直接交给 LLM 就行，你只需给它合适的角色提示词就行：
```
if intention == '图片生成':
    messages = [
        {'role': 'system', 'content': '根据用户输入，生成给stable diffusion等图片生成模型的提示词，只回答提示词内容，无需回答其它任何内容'},
        {'role': 'user', 'content': f'{user_content}'}
    ]
    res_prompt = unillm(['gemini-1.5-flash', 'glm4-9b'], messages=messages)
```

你别看就这么个简单任务，参数量小一点的模型压根搞不定！

实测下来，还是`gemini-1.5-flash`靠谱一些，推荐大家使用。

## 3. 生成图片
有了`绘画提示词`，终于到最后一步：生成图片了。

用啥模型生成图片呢？

本地部署个 `Stable Diffusion`？

都 2024 了，`AI 绘画`的风口在 `FLUX` 这里，强烈推荐你去体验一下👉[FLUX + LoRA 实测，AI 绘画开启新纪元，5分钟带你部署体验](https://blog.csdn.net/u010522887/article/details/141218266)。

现在 `FLUX` 的生态已经越来越完善了，但是本地部署对很多小白来说还是有点门槛。

为了让大家能快速跑通流程，我们选用[siliconflow](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y)提供的免费接口。

核心代码如下，一键接入 `AI 绘画`模型：

```
def generate_image(prompt='a cat', model='flux', img_size='1024x576', batch_size=1):
    url = f"https://api.siliconflow.cn/v1/{model}/text-to-image"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer xxx"
    }
    data = {
        'prompt': prompt,
        'image_size': img_size,
        'batch_size': batch_size,
    }
    response = requests.post(url, json=data, headers=headers)
    img_urls = [img['url'] for img in response.json()['images']]
    return img_urls
```

当然，[siliconflow](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y)也开放了`Stable Diffusion`系列模型，不过从实测来看，`FLUX` 更香，不知大家体验如何，欢迎评论区交流。

如果有更多`AI绘画`的定制化需求，只能本地部署 LoRA + ControlNet 模型。想咋玩，你说了算！


## 4. 效果展示

来一波测试案例：

![](https://img-blog.csdnimg.cn/img_convert/28c291d0ee3478929d2409b4878d1950.png)

![](https://img-blog.csdnimg.cn/img_convert/735dfc9bb9b91988a020209a74ee1497.png)

![](https://img-blog.csdnimg.cn/img_convert/e51c75e976ac8f9522a99b13d09a2d61.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9f98425f864f4999a75201e6ae3fc289.png)


最后，我们来看下日志：

![](https://img-blog.csdnimg.cn/img_convert/65f353ef6f40b31bf973766169e758e7.png)

意图识别没问题！

此外，`gemini`还会帮我把`绘画提示词`润色一下。这下，你还担心`不会写提示词`么？

## 写在最后

本文通过简单三步为`小爱`接入了`AI 绘画`能力。

从此，写公众号，再也不用费劲找封面图了，`小爱`直出，灵感无限！

大家有更好的想法，欢迎评论区交流。

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

想和`小爱`互动的小伙伴，可以通过公众号找到我，拉你进群体验。

--- 
为了方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

`小爱`也在群里，想进群体验的朋友，公众号后台「联系我」即可，拉你进群。

