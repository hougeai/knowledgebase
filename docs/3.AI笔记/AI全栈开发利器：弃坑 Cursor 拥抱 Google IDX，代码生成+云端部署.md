最近，AI 编程工具非常火爆，不仅极大降低了开发者的工作量，也为编程新手快速入门，提供了极大的便利。
 
提到 AI 编程工具，Cursor 绝对是其中的顶流。

不过直到今天，笔者也未用过 Cursor，原因无它：**Cursor 需下载安装使用**！

且 Cursor 的免费 Token 额度有限，有朋友分享过无限白嫖的方法：**通过注销账号重新注册实现无限免费使用**。

不过，这个漏洞也被 Cursor 堵上了，而平替 Windsurf/Bolt.new 同样需要付费订阅。

**有没有其它工具，可以兼顾强大功能和免费体验？**

最近，Google 频放大招，除了媒体关注的多模态大模型 Gemini2.0，还推出了新一代 **AI 代码编辑器 - IDX**。

今日分享，带大家全面了解这款工具，并通过一个简单的案例，实测 IDX 效果到底如何。

## 1. IDX 简介
和 Cursor 不同的是，IDX 无需下载安装，它是一款云端集成开发环境（IDE），目前还处于 Beta 版阶段。

支持云端进行全栈、多平台应用开发。

下图展示了其支持的多种开发框架，甚至可以直接 import 你的 github 仓库进行开发。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/60873f9289eb427e98262ddb205069c4.png)


从首页来看，和我们前面分享的 Bolt.new 非常类似，不过当前 IDX **完全免费**！

老规矩，简单列出它的核心亮点：

- **多框架支持**：内置模板丰富，支持 Angular、Flutter、React、Vue 等各种框架。

- **AI 助力**：底层大模型 Gemini，支持代码生成、优化、测试等功能

- **在线模拟器**：内置 iOS 和 Android 模拟器，无需安装即可测试和调试移动端应用。

- **一键部署**：支持项目一键部署，省去复杂的部署步骤。

## 2. IDX 实操

> [https://idx.google.com/](https://idx.google.com/)


本文通过一个简单的案例，带大家快速上手 IDX 的基本用法：*实现带有积分功能的贪吃蛇游戏。*

**step 1: 项目创建**

选择最简单的 Html 模板即可。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/5db1238d3ee04e49afc1d86ed2773b14.png)


稍等片刻，IDX 会自动生成项目空间，并配备好前端三件套：html/js/css。中间是代码区，右侧是预览区。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/51c2b3b932fa435d9a9c481ecd06bd1a.png)


**step 2: 项目生成**

在底栏可以调取 Gemini，开始给它安排任务吧： 

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c3df328f0cfb4e9c9a5378a314933c21.png)



第一轮代码编写完成，预览区刷新一下，即可运行！

看，控制台报错了：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f24b3c9cf9b447c998a25a5fc4ebb5f4.png)


原来是 body 里调用的`initGame()`函数来自`main.js`，但第一轮中 Gemini 并没有在 `main.js` 中写入任何内容。

```
<body onload="initGame()">
    <h1>Snake Game</h1>
    <button id="startButton">Start Game</button>
    <div id="score">Score: 0</div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <script src="main.js"></script>
</body>  
```

怎么搞？参考上方红色箭头，继续让 Gemini 修改！

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8b33b758c635477d834b413383b8a3a2.png)


**step 3: 项目迭代**

继续迭代，它会贴心告诉你：修改了哪里，为何要修改？

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e801036a4a14459896943e70ef4c4419.png)


等代码逻辑没问题了，可以继续让它帮忙修改 css：

```
最后帮我修改css，把界面打造的更漂亮一些
```

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3fd10b210be34d4288154ff20637d242.png)


鸡肋的是，它只更新了 .css 文件，而 html 中没有做对应更新，需要进一步追问后，才搞定！

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9f707c3df88d4d09806edeb169de02a7.png)



**step 4: 效果预览**

右上角图标点击，可以找到 IDX 帮你生成的 web url。扫下方的二维码，也可在手机端体验。


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/e0e4e659e5d7465b8b454d7431694fcf.png)



最后，让它修改了下 css 样式，整体色调调整下，一个粗糙的`贪吃蛇`游戏的 Web 界面出炉了：


![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6f5532736b9049f29c7e495f90d81b03.png)



**step 5: 项目管理**

回到项目首页，在工作空间中可以看到刚才创建的项目，可以选择删除或者继续修改：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/41cb43d766c3435488626c6476882518.png)


## 写在最后

本文带大家实操了 AI 编程工具-IDX，凭借云端优势，Google 为开发者提供了无与伦比的开发体验。当然，由于 Genimi 国内无法访问，需自备梯子使用。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入，公众号后台「联系我」，拉你进群。

