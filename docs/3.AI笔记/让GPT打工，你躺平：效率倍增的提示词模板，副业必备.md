GPT火爆很久了，可是，我观察到身边很多人似乎还没能完全用好它，真正提高自己的工作效率。

所以，我决定开辟一个专栏-GPT提示词从入门到精通，详细展示我调教GPT的思路，全程干货不废话，希望能帮到更多人。

如果不知道怎么用免费的GPT4，出门右拐看这里👉：[免费白嫖GPT4，无次数限制，5分钟带你上手](http://mp.weixin.qq.com/s?__biz=MzkzMzY2MTkyNw==&mid=2247483970&idx=1&sn=327fca3a902ef029ca2faab40db91c16&chksm=c2485fcaf53fd6dc38dffa24aa45684816f5a507b3b3ebd5e4bdd872a8502f5f7b818426cad3&scene=21#wechat_redirect)

如果你还订阅了付费版的GPT4，却不能发挥它的最大价值，这笔钱何不省下来，去给自己搞一顿大餐？

话接上篇：[轻松搞定10w+：小白易上手的提示词模板，GPT很强，但请温柔以待!](http://mp.weixin.qq.com/s?__biz=MzkzMzY2MTkyNw==&mid=2247484017&idx=1&sn=f3c2b7d7e646a0f5ba7835620e7f0d45&chksm=c2485ff9f53fd6ef90c92d23f8df1efb177a649f9f5c0f8e359036443f9deec58c98d04f27f2&scene=21#wechat_redirect)

今天继续分享一个亲测好用、小白易上手的“GPT提示词模板”- LangGPT。

### **01 写提示词，完全不会啊**

经常遇到这样一种情况：群里收到一个 pdf 文档，可是太长了，自己不想打开看，但是不看吧，又怕错过有用的内容。

扔给GPT？

你会发现他还是没法给你想要的东西，关键是它每次给你的内容都很不稳定！ 

能不能把GPT改造成一个专门完成这个任务的小助手？

这就是你经常听到的 **GPTs**。

简单理解GPTs: 就是把用于特定任务的**人设提示词**（比如你在gpt对话框中，希望它是一个**pdf提炼和总结专家**）固定下来，这样你下次打开这个对话框时，它还能以**pdf提炼和总结专家**的人设和你交流，不用重新输入**人设提示词**。

问题是：怎么快速获得满意的**人设提示词**呢？

### **02 有请提示精灵小黑熊**

上链接：https://chatgpt.com/g/g-yJMQaiBnm-ti-shi-jing-ling-xiao-hei-xiong-structured-prompt-pet

> PS：上述链接需要科学上网，如果没法解决，可以接着往下看。

**提示精灵小黑熊**也是一个 GPTs，它能干啥？

它可以根据你简单的描述，帮你采用 LangGPT 的结构，写出一个符合你需要的**人设提示词**。

详细使用方式：打开上面的链接，直接把你的需求扔给它。

比如我现在需要一个**pdf提炼和总结专家**。

我可以给它如下的提示词：

```
我需要一个pdf总结提炼专家，它能根据我上传的pdf，仔细阅读全部内容后，完成以下几个事情：
1、能快速总结pdf一共讲了几章内容
2、提炼总结每章节讲述的3-5个核心观点（可根据该章节具体情况来，比如某章节重点观点只有1个，就总结1个；如果有10个就总结10个）
3、完成1、2后，如果用户对某个观点感兴趣，可引用pdf的内容和数据给用户进一步解释和说明，达到加深用户认知的目的
4、全程将用户视为该领域的小白，所以给用户总结、回答解释pdf内容时，务必注意一定要通俗易懂，让用户能快速吸收知识
```

接下来**提示精灵小黑熊**他会问一些问题，如果你不想回答这些问题，直接回答“没有问题”即可。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/hg7FIPq4qNRsnnxbvtOQ6r1jE7yINMvh6SQ2Jd9swLJ2TTdHyczXdvZbOZMuef589GYHtJZ9xoicicnEmZYbRsHQ.jpg)



它会预设一个宽泛通用的场景，然后快速帮我们生成**pdf提炼和总结专家**的人设提示词。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/hg7FIPq4qNRsnnxbvtOQ6r1jE7yINMvhDib6afwGC6gWr0F8VfhK3BzWfehxiagVhMRtiady8cGyocXic3r2FCCRqg.jpg)



文字版如下，可以拿去直接用：

```
# Role
PDF总结提炼专家
- 基本信息：你是一位擅长阅读和总结PDF内容的专家，能够快速提取关键信息，并以通俗易懂的方式向用户解释。你的目标是帮助用户快速理解和吸收PDF中的核心内容。

## Profile
- 作者: 财猫的提示精灵小黑熊
- 版本: 0.1

## Goals
- 快速总结PDF文档的章节结构
- 提炼总结每章节的核心观点
- 根据用户的进一步需求，引用PDF内容和数据解释核心观点
- 以通俗易懂的方式帮助用户理解和吸收知识

## Constraints
1. 保证总结和提炼的内容准确，并覆盖每个章节的主要观点。
2. 在解释和回答用户问题时，务必使用通俗易懂的语言，避免使用过于专业的术语。
3. 遵循用户上传的PDF文档格式，保持引用内容和数据的准确性。
4. 若某章节的重点观点数量不符合3-5个的要求，可根据实际情况调整总结的数量。

## Skills
1. 深入理解和快速阅读PDF文档的能力：能够在短时间内抓住PDF文档的主要内容和结构。
2. 信息提炼和总结能力：能够将每个章节的核心观点清晰地提炼出来，并进行简明扼要的总结。
3. 通俗易懂的解释能力：能够将专业内容用简单明了的语言向用户解释，帮助用户快速理解。
4. 数据引用和解释能力：能够根据用户需求，引用PDF中的具体内容和数据，进一步说明和解释核心观点。

## Workflow
1. 阅读用户上传的PDF文档，快速了解其章节结构。
2. 总结PDF文档的章节数量和每个章节的标题。
3. 提炼总结每个章节的3-5个核心观点，根据实际情况调整总结的数量。
4. 如果用户对某个观点感兴趣，引用PDF中的内容和数据，进一步解释和说明该观点，确保通俗易懂。
5. 确保全程使用简明扼要的语言，帮助用户快速吸收知识。

# Initialization:
您好, ChatGPT, 接下来, Let's think step by step, work hard and painstakingly, 请根作为一个拥有专业知识与技能(Skills)的角色(Role)，严格遵循步骤（Workflow）step-by-step, 遵守限制(Constraints), 完成目标（Goals）。这对我来说非常重要, 请你帮帮我，谢谢！让我们开始吧。
```

把你觉得不满意的地方调整一下，就可以直接用了。

### **03 固定人设提示词**

有了这份提示词，我重开一个ChatGPT窗口，然后把这个人设提示词给它。且看它的回答：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/hg7FIPq4qNRsnnxbvtOQ6r1jE7yINMvhr0XX5gqJ3F9V9F8l1YKib4Z28Fag7KzZSaPI17J15M5Nvf7J4Tk1vaQ.jpg)

比如我拿《学会写作》这本书给它，让它帮我提炼总结这本书主要讲了啥。

> PS：如果需要这本书，可以在我公众号后台回复“写作”即可。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/hg7FIPq4qNRsnnxbvtOQ6r1jE7yINMvhicgUqfJUW5PaNSpTmjeF1NH2QCT1QOEK3tZU16Ssfu4d9nGndQN9OZg.jpg)

接下来，你还接着继续问他你想要了解的内容，比如：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/hg7FIPq4qNRsnnxbvtOQ6r1jE7yINMvhNmJRXT1X9gEpLyMTWia2x9FlaNMPSeiahJwlBWCFgkkibNib7nQaFkqbxg.jpg)

当然你可以继续向他询问你想要的内容，怎么样，够简单吧。

关键是一次写好，多次复用，以后有任何pdf，都可以扔给它，给你总结，给你解答~

最后，我们来拆解下 LangGPT 的结构，以后你遇到复杂任务，只要套用这个模板去写，写出一个80分的提示词，绝对没问题。

### **04 LangGPT 提示词模板**

从**提示精灵小黑熊**给返回的提示词中可以发现，其实 LangGPT 提示词模板主要由以下几个部分组成：

```
## Role
角色

## Profile
角色简介

## Goals
目标

## Constraints
要求

## Skills
角色具备的能力

## Workflow
工作流程

# Initialization:
初始化
```

如果你无法访问**提示精灵小黑熊**这个GPTs，也没关系。

只要按照上面这个模板，把你希望GPT要完成的任务描述清楚就 OK 了。

就这么简单~

如果对你有帮助，欢迎点亮【赞和在看】，让GPT服务好更多身边的朋友。