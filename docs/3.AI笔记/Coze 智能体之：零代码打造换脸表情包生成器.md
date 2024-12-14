前两篇，和大家分享了如何用 Dify 搭建`图像生成智能体`：

- [Dify 保姆级教程之：零代码打造图像生成专家（上）](https://blog.csdn.net/u010522887/article/details/143874061)
- [Dify 保姆级教程之：零代码打造图像生成专家（下）](https://blog.csdn.net/u010522887/article/details/143905893)

后台有小伙伴留言，建议试试 `Coze 图像流`。。。

好家伙，好久没打开 Coze，简直打开新天地。

不吹不擂，Coze 的插件生态做的真心非常棒。

应该说，Dify和Coze各有优势。当然，工具选择，关键在于哪个能更快解决手头问题。

下图是，Coze 图像流的内置能力，任何一个放到 Dify 中，都得去写个 API 来调用吧。

![](https://img-blog.csdnimg.cn/img_convert/dea930b0a51576192cdc608a7352c3bc.png)

今日分享，就通过一个简单案例-`换脸表情包生成器`，带大家快速上手 Coze 图像流，相信看完本文的你，一定能打造更多有创意的`AI图像生成应用`。


先看下最终效果：

![](https://img-blog.csdnimg.cn/img_convert/aa74053391c873f01f5e21d80fd54f4a.png)

这里用马老板来举例，你想换谁的人脸，都是分分钟的事。

话不多说，上实操！

## 1. 新建图像流
> coze 国内地址：[https://www.coze.cn/](https://www.coze.cn/)

Coze 中的`图像流`设置比较隐蔽。注册登陆后，左侧工作空间找到资源库，右上角点击添加资源。

![](https://img-blog.csdnimg.cn/img_convert/252cc81c55ba428dee4957350a7917bc.png)

名称必须用英文，描述也尽可能讲清该图像流的具体用途，方便大模型调用：

![](https://img-blog.csdnimg.cn/img_convert/05e7ca722ae917b061085481314d093c.png)

刚进来只有两个节点：

![](https://img-blog.csdnimg.cn/img_convert/24258b1b6de66453887366510c15fff9.png)

接下来需要做的，就是在`开始`和`结束`节点之间，发挥你的创意！比如，`换脸表情包生成器`最终的流程图如下：

![](https://img-blog.csdnimg.cn/img_convert/626396e56c7f3ea2897781a32c0b6e84.png)

来，一起搞定它！

### 1.1 开始节点

本次任务，我们需要三个输入：
- **要换脸的图**：比如上面马老板的人脸；
- **表情包底图**：比如熊猫脸的表情包；
- **表情包文字**：渲染到表情包上的文字。

为此，需在开始节点新增三个字段，描述也要尽可能清晰明确，便于后面大模型理解：

![](https://img-blog.csdnimg.cn/img_convert/71ff0e3a8742f9fe315288db840211f8.png)

### 1.2 智能换脸节点

Coze 中集成了智能换脸能力，你需要做的只是动动手拖进来，然后和`开始`节点连接：

![](https://img-blog.csdnimg.cn/img_convert/11e0d07a5172c379c49d11d569e88f63.png)

注意：图像有两种来源：引用和上传，我们这里采用`引用`，也即把`开始`节点中的变量传递过来，`上传`顾名思义，就是允许你手动上传一张图片，Coze 会帮你缓存到云端。


### 1.3 画板节点

**怎么才能把文本渲染到图像中？**

Coze 图像流贴心给你准备了`画板`节点，拖进来，然后新增`文本`和`换脸后的图像`变量：

![](https://img-blog.csdnimg.cn/img_convert/f3c9475f99a547615ceaaa9de0586d6d.png)

下方`画板编辑`可以调整文本位置，注意要把文本图层置顶，否则文本无法显示哦。

![](https://img-blog.csdnimg.cn/img_convert/e54019f95b102f1f46876cedf760d561.png)

最后，把`画板`节点和`结束`节点连接起来，大功告成！

### 1.4 测试和发布

点击右上角`试运行`，测试看看，没问题就可以发布了。

![](https://img-blog.csdnimg.cn/img_convert/6084e0710a55cb084fc1cc3f95435a97.png)

发布成功，它就相当于你的一个自定义工具，可以在智能体中调用了。


## 2. 新建智能体

左侧工作空间找到项目开发，右上角创建智能体。

![](https://img-blog.csdnimg.cn/img_convert/59f98686c8f0d928269b6cb118aa2a0f.png)


接下来，**最重要的就是编写角色提示词**。


提示词其实并不复杂，你只需把你想要做的事情描述清楚就可以，比如我们这个任务，我给到的提示词如下：

```
首先，要求用户上传：
- 一张需要换脸的图片，作为swap_face；
- 一张表情包底图，作为base_face；
- 渲染在表情包上的文字，作为text。
确保用户已经上传上述三个内容后，调用swap_face生成一张图像，直接在终端显示。
```
然后，右上角点击提示词优化，让大模型帮你润色一番：

![](https://img-blog.csdnimg.cn/img_convert/93d729c1daddd2b9129936317b28fe3f.png)

挺像回事了吧~

中间，把刚刚创建的图像流工具添加进来：

![](https://img-blog.csdnimg.cn/img_convert/21dc29d4d5f86ed761b8965161f527e3.png)

注意：这里确保你的图像流工具已发布：

![](https://img-blog.csdnimg.cn/img_convert/106a40b17dbfc5101ebb5773d57a3aeb.png)


搞定，就这么简单！

来测试下效果吧：

![](https://img-blog.csdnimg.cn/img_convert/7ddb1a198a4c7519e3cb4469767cd3f1.png)

![](https://img-blog.csdnimg.cn/img_convert/aa74053391c873f01f5e21d80fd54f4a.png)

完美，右上角点击发布！

去试试吧：[https://www.coze.cn/s/iAwaJ4HR/](https://www.coze.cn/s/iAwaJ4HR/)

## 写在最后

本文通过一个简单案例，带大家实操了**Coze 图像流**。

有了这些底层能力，可玩的空间可太大了，比如制作海报、小红书爆款文案图片等。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入，公众号后台「联系我」，拉你进群。




