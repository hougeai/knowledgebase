`CodeBuddy`，腾讯出的 AI 编程工具。

从 Cursor 到 Trae，这类产品可太多了。

这几天，铺天盖地的 `CodeBuddy` 推文，忍不住，笔者也实测了一把。

真有那么神？

**不吹不擂**，今日分享 `CodeBuddy` 的一手体验：

- 1. 快速上手

- 2. 做个应用

- 3. 部署起来

- 4. 个人感受

## 1. 快速上手
> 地址：[https://www.codebuddy.ai/](https://www.codebuddy.ai/)

![](https://i-blog.csdnimg.cn/img_convert/3c8e1815f4fb591c02d3a528f07acadf.png)

目前给邀请码还挺慷慨，500 次 Claude-4 额度，有需要的朋友，走过路过别错过。

UI 设计酷炫，情绪价值拉满：

![](https://i-blog.csdnimg.cn/img_convert/465ef657c23a863a1330530e2029961e.jpeg)

基于 `VSCode` 打造，因此页面布局和 `Cursor/Trae` 等 `AI IDE` 如出一辙，尽可能降低用户上手门槛，和竞品抢占用户心智。

重点是弹药库充足：把宇宙最强编程模型都给你上了，而且国内直达：

![](https://i-blog.csdnimg.cn/img_convert/c83787c585bd74ca1f7a15dedf1add31.png)

对于 Windows 用户，如果觉得命令行太难用：

![](https://i-blog.csdnimg.cn/img_convert/e319ab3e694a0971e416fde3cd257ec7.png)

左侧状态栏，可以切换到 SSH 远程登录：

![](https://i-blog.csdnimg.cn/img_convert/fff63b81226ca8950c34754cc586eb11.png)

如果没有 Linux 虚拟机，推荐你试试同样是腾讯出品的 WebIDE：

[免费GPU算力本地跑DeepSeek R1，无惧官方服务繁忙！](https://blog.csdn.net/u010522887/article/details/145403554)


## 2. 做个应用

### 2.1 准备工作

既然定位为`一站式产品开发平台`，显然少不了后端集成，因此 `CodeBuddy` 目前集成了：
- 海外的 `Supabase`（主要是数据库）；
- 自家的 `CloudBase` （产品更全）；

我们首先连到腾讯云 `CloudBase`，后续可以用这里的免费服务:

![](https://i-blog.csdnimg.cn/img_convert/767974938935556ed629900e4069aa51.png)

成功后会在当前目录下自动生成`AI 规则文件`：

![](https://i-blog.csdnimg.cn/img_convert/ba65f3b2b14d0672703c9e38316e037e.png)

这个 `AI 规则文件`怎么理解？

其实就是`提示词工程`，用来给 `CodeBuddy` 在开发过程中定规矩：

![](https://i-blog.csdnimg.cn/img_convert/8564a6637cdedeae13ced29567ed537c.png)

所以，`CodeBuddy` 会首先识别要开发的项目类型，然后再去遵守对应的开发文档。

私以为这套提示词工程非常棒，值得借鉴！

当然，如果你不想用腾讯家的产品`CloudBase`，也可以自定义规则，右上角这里：

![](https://i-blog.csdnimg.cn/img_convert/e9d5b241a397b77cdb5f695cb107c2d3.png)

下面，我们以官方案例，实测下 `CodeBuddy` 能力几何！

### 2.2 需求描述

需求应该尽可能明确，比如要用到的技术栈：

```
创建一个在线投票系统，支持创建投票、参与投票、结果统计；

前端使用vue3+javascript+tdesign组件库+unocss+pnpm+eslint+prettier；

先和我确认需求，用中文和我对话，最后完成部署。
```

当然，即便你觉得需求非常明确了，AI 也未必听话照做，还得不断调教它。

### 2.3 开始开发

发送之前，记得勾选这里的 Plan 模式：

![](https://i-blog.csdnimg.cn/img_convert/5f134a4f34fe364831c80155f4be55f9.png)

你看，AI 开始查看规则了：

![](https://i-blog.csdnimg.cn/img_convert/54e142d0f8d14e01cd6da20a360c090d.png)

不过 `Claude 4` 并没有听话照做-`用中文回答我`。

AI 看完了，帮我生成了需求文档：

![](https://i-blog.csdnimg.cn/img_convert/be59f80bfdf902c2cd6e2b40f8383fdc.png)

不明确的地方，主动向我询问：

![](https://i-blog.csdnimg.cn/img_convert/06a8645c9980b47efd5d3afdefa39b4c.png)


开始打工了，首先是逐步安装依赖：

![](https://i-blog.csdnimg.cn/img_convert/6df551471861437a37ae0a72a4ea4dcd.png)


然后，进行项目配置：

![](https://i-blog.csdnimg.cn/img_convert/4ceae021421ec728818dd01757bf0f95.png)

开始创建连接`CloudBase`的环境：

![](https://i-blog.csdnimg.cn/img_convert/6b5e7b4e9abe7048f0844370c7e850a4.png)

下面正式进入代码环节！

首先是创建路由配置文件：

![](https://i-blog.csdnimg.cn/img_convert/d8ad828d8bffcf47e353dcff5c923cb9.png)

然后，创建Pinia状态管理配置:

![](https://i-blog.csdnimg.cn/img_convert/312d44e151482bfc5c7e7b0b1d4be26c.png)

然后，创建页面布局：

![](https://i-blog.csdnimg.cn/img_convert/2692e81ba672a5296f143446e63bfbce.png)

创建不同页面：

![](https://i-blog.csdnimg.cn/img_convert/7168728dfa5de3b68f6656a94d95131d.png)

修改css样式：

![](https://i-blog.csdnimg.cn/img_convert/28ba71d75f41078bb9f4366309a206b6.png)

最后创建 README.md文件:

![](https://i-blog.csdnimg.cn/img_convert/22310138853537fc227409efdcc55bb2.png)

至此，对新手来说，看着 AI 打工，起码能学到基本的前端开发流程；

对于有一定前端开发经验的工程师，依然赏心悦目！

最后的最后，创建`CloudBase`配置文件，以便于项目的部署和管理：

![](https://i-blog.csdnimg.cn/img_convert/d41cf53c2677f0edf7611dd8c3e0c057.png)

运行项目试试看：

![](https://i-blog.csdnimg.cn/img_convert/4bbe012df04637e5ca948b7712b9c782.png)

这里，它让你前往腾讯云`CloudBase`，对于新手来说还是很贴心的：

![](https://i-blog.csdnimg.cn/img_convert/a8a27459aad346f1983ea409c93f7120.png)

###  2.4 开始 Debug

没有页面怎么办？

发现报错怎么办？

直接问`CodeBuddy` ：

```
修改 src/utils/cloudbase.js 文件中的环境ID
修改 cloudbaserc.json 文件中的环境ID
已完成，你用的什么数据库啊，我在哪创建数据库啊
```

这个项目的后端数据库，`CodeBuddy` 选择的文档型数据库 `MongoDB`，还是挺合理的，方便后续扩展。

在`CloudBase`中同时支持`关系型`和`文档型`数据库：

![](https://i-blog.csdnimg.cn/img_convert/6e4b78e1690e96ba5f31713e3ffe9b77.png)

此外，`自有数据库`是让你把其他产品的数据库迁过来，就怕你不来~


然后，我们在文档型数据库中，创建项目用到的三个集合：

![](https://i-blog.csdnimg.cn/img_convert/c8225d96e9e9772640d40fbdfdd5dce5.png)


数据库配置好之后，前端页面就可以成功展示了，只是差点意思：

![](https://i-blog.csdnimg.cn/img_convert/190e6902caba0ed18ad8cdb20132276f.png)

你看看这个布局~

你怎能奢望它一气呵成，给你完整的项目？

没招，一步步来吧~

在 `Claude-4` 被我喷了无数次后，终于把布局的 bug 给修好了：

![](https://i-blog.csdnimg.cn/img_convert/27ed5eeb883530e91c2365c7a575bef1.png)

`CodeBuddy` 中比较贴心的一点：调整前端页面时，可以选择页面元素进行调整：

![](https://i-blog.csdnimg.cn/img_convert/a136630f1c54d946e6e2592628ada0f4.png)

即便如此，这个项目中 bug 依旧很多，略举两例：
- 路由不统一：

![](https://i-blog.csdnimg.cn/img_convert/15458114827cfcb6d2b552248968d7c7.png)

- 重复页面：

![](https://i-blog.csdnimg.cn/img_convert/22e33b448d8d1f60da47c0f2421ad227.png)

`Claude-4` 小心翼翼地修 bug，任劳任怨，但经常原地转圈，纯纯`有苦劳没功劳`。光缓存就干到了 8MB：

![](https://i-blog.csdnimg.cn/img_convert/02dff29e7a3f497fe315d28d97d507ca.png)

在我的不断鞭策下，注册登录等基本功能 OK 了。

还有一堆 Bug，懒得修了，先部署起来吧~

## 3. 部署起来

因为后端只用到了 `CloudBase` 的数据库，所以编译打包后，可以把 `dist` 放到任意一台服务器上。

```
npm run build
```


不过，`CloudBase` 也提供静态网站部署能力，藏的有点深：

![](https://i-blog.csdnimg.cn/img_convert/17974ac0790edc2bc424123f754d66f5.png)

命令行部署超级简单，也即把静态文件上传到云端。

具体流程如下：

```
# 安装 CLI 工具
npm install @cloudbase/js-sdk
# 先登录，等待网页端授权
tcb login
# 设置环境变量
export envId=cloud1-xxx
# 获取静态网站服务信息
tcb hosting detail -e $envId
# 将文件上传到静态网站的存储空间中的指定路径
tcb hosting deploy ./dist . -e $envId
# 删除文件/文件夹
tcb hosting delete -d vote -e $envId
# 查看文件列表
tcb hosting list -e $envId
```

![](https://i-blog.csdnimg.cn/img_convert/b4431a03d714050458ab71289a157494.png)

上传成功，在哪查看文件？

需要前往腾讯云控制台：
> [https://console.cloud.tencent.com/](https://console.cloud.tencent.com)

![](https://i-blog.csdnimg.cn/img_convert/1e0117af9dea4990c34f60a6aa28e75f.png)

等待一段时间，CDN 缓存就绪后，上方域名即可访问：

[https://cloud1-3gvpnlgk5f856f4b-1327613494.tcloudbaseapp.com/](https://cloud1-3gvpnlgk5f856f4b-1327613494.tcloudbaseapp.com/)

## 4. 个人感受

实测结论：

- `CodeBuddy` 和其他竞品相比，单就编程能力，并无显著优势，但并不妨碍它成功出圈。

不是 `CodeBuddy` 不行，不是 `Trae` 不行，而是背后的 LLM 还有很长的路要走。

面对群狼环伺的 `AI IDE` 市场，如何从一众竞品中站稳，腾讯花了很大心思。尤其是和自家的云原生开发平台 `CloudBase` 深度绑定。

因此，不只是 `AI IDE` 市场。

`AI IDE` 只是很好的入口，腾讯想要的是，元原生时代，广阔的`AI+应用落地市场`。

## 写在最后

本文分享了腾讯的 `AI IDE` 编程工具`CodeBuddy`，并进行了实测。

`AI IDE` 是工具，是助手，可以极大提高开发效率，只需要储备一点点基础，然后掌控它。

如果对你有帮助，不妨**点赞收藏**备用。
