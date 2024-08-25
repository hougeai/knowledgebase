
上篇，给大家介绍了一款搭建微信机器人的开源项目：
[搭建微信机器人的第4种方式，我造了一个摸鱼小助手](https://blog.csdn.net/u010522887/article/details/141348878)

不同于需要付费的项目，它的定制化程度非常高~

问题来了：怎么接入 AI 能力呢？

考虑到大家对 Coze 智能体的接触更多一些，

今日分享，先带大家接入 `Coze` 的 AI 能力，打造更智能的个人 AI 助理！ 

全程无比丝滑，无需任何编程基础，只要跟着一步步实操，你也可以搞定!

## 1. 创建 Coze Bot

前往 [https://www.coze.cn/](https://www.coze.cn/)，点击 `创建 Bot`。

单 Agent 就行，大模型随便选一个，从实测体验来看，个人觉得 Kimi 普适性更强一些。

![](https://img-blog.csdnimg.cn/img_convert/bb694734a0fd96fd024ca6e8e1aed4f6.png)

最重要的来了，你需要添加一个插件：
![](https://img-blog.csdnimg.cn/img_convert/00dd376edc0c7d41e6b98838677b11a0.png)

插件市场根本找不到满足需求的插件啊~

这时，你需要自己创建👇

![](https://img-blog.csdnimg.cn/img_convert/c31a2e2090c02bb044096bf15e042527.png)

## 2. 创建插件

注意创建插件需要写一点代码，不用担心，很简单的几行代码就能搞定！

所以，需要选择 `在Coze IDE中创建`，在`IDE运行时`选择你熟悉的一种语言就行。

![](https://img-blog.csdnimg.cn/img_convert/7b919ced748dfdad143b9aa242b9eaaf.png)


然后点击`在 IDE 中创建工具`，进来后，首先左下侧 `+` 安装依赖包`requests`，代码区编写如下内容：

![](https://img-blog.csdnimg.cn/img_convert/1f4cf7fb2b56868d024b705e12179926.png)

这里的 url 就是我们在上篇中搭建的机器人的`发送消息的API`，其中最重要的三个参数和原始请求中保持一致！


此外，为了 AI 大模型可以准确执行任务，你还得把这些参数给它解释一下哦~


怎么搞？右侧填入元数据，把输入参数和输出参数通通给他`描述`一遍：

![](https://img-blog.csdnimg.cn/img_convert/da09c2c41ce60c441c05e455e518025c.png)

填入元数据后，右侧可以自动生成请求数据的实例，填入你想要发送的用户和内容，点击`运行`测试一下吧~

![](https://img-blog.csdnimg.cn/img_convert/1dd09da5aa88978fa73ca3c01659403b.png)


测试成功，就可以点击右上角的 **发布** 。

至此，你的工具就创建好了。

## 3. 智能体测试

首先，回到一开始的 Bot 配置界面，添加插件这里，找到`我的工具`，把你刚刚发布的插件添加进来即可。

![](https://img-blog.csdnimg.cn/img_convert/0b9e8e31d74da84aaaa95006ec884eb8.png)


![](https://img-blog.csdnimg.cn/img_convert/145d9797592acc0da5cdf2ba8b6c96c6.png)


最后，在右侧的`预览与调试`区域，测试一下吧~

**测试案例一**：

让它给我的`大号`微信讲一句土味情话，可以看到成功调用了刚刚添加的插件：

![](https://img-blog.csdnimg.cn/img_convert/bca94a0242903cffcd779b2bed7a003b.png)


来微信看看，成功发送！

![](https://img-blog.csdnimg.cn/img_convert/6232ad90a84ea0e811f852b27dd0fd1a.png)


还能怎么玩？

**测试案例二**：

让它帮我查询一下天气吧~

你还需要再给它加上一个天气插件 - `墨迹天气`，可以看到成功调用了两个插件：

![](https://img-blog.csdnimg.cn/img_convert/cba00f6627fde977c8facc8843a0cfa6.png)

来微信看看，成功发送！

![](https://img-blog.csdnimg.cn/img_convert/09b1b5e0fd324f6ead358f83ca27527d.png)

还能怎么玩？

尽情发挥你的创意吧~

## 写在最后

Coze 是一个非常强大的智能体开发平台，本文仅仅使用了其中的`创建插件`功能，还有诸如`知识库`等更丰富的功能，后续会陆续跟大家分享~

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。
