
最近尝试了一件好玩的事儿~👇

![](https://i-blog.csdnimg.cn/img_convert/c5007d0d4496731257c8b81b118d5635.gif)

起因是这样的：

最近 AI 编程工具特别火，前有 Cursor 一骑绝尘，近有字节的 Trae 刷屏：

[字节 Trae 初体验，最强 Claude 3.5 / GPT 4o 无限免费用](https://zhuanlan.zhihu.com/p/24401396827)

说实话，这些先进生产力工具，着实让人兴奋！

特别是看到`全程没写一行代码，做了个xx应用`，很多零基础的朋友也想尝试 AI 编程，实操后却发现`门槛太高` `无从下手`。

我在想，对于零基础的朋友，有没有一条路径：快速把`浮现在脑海中的想法`落地到`提高生产效率的工具`？

今天把`近一周的尝试`分享给大家，希望给感兴趣的朋友一点参考和帮助。

整个过程并不复杂，抽象出来只需三步：

**1. 寻找对标应用**

**2. 确定技术选型**

**3. 实现功能模块**

有了思路，那做个啥呢？

之前分享过很多 AI 模型和工具，如果能搭建一个`集成各类 AI 工具`的网站，既方便自己，也能帮到有同样需求的小伙伴，何乐而不为？

**说干就干！**

## 1. 寻找对标应用

市面上这种 `AI 工具类的网站` 还挺多的，找找看，总有一款符合你的审美~

**假设你也想做一个和上图一样的网站**，但不知从何入手？

最简单的办法：截图复制给 GPT/Claude/Kimi 等任一款多模态模型。

甚至不用很复杂的提示词，比如：

```
帮我分析这张图片种的所有细节，我也想从零到一搭建一个类似的AI工具服务网站，我是编程小白，你帮我判断下我需要采用哪些技术和框架
```

![](https://i-blog.csdnimg.cn/img_convert/ea79889125adeb55392f71a15ee16355.png)

![](https://i-blog.csdnimg.cn/img_convert/373fd33b6de593937df88d1eae3e96a0.png)


实测发现，GPT/Claude 给到的建议都比较靠谱，我们来看：

**1. GPT 的回答：**

![](https://i-blog.csdnimg.cn/img_convert/abbc50abbb34be122f62ed6efd171e3c.png)

![](https://i-blog.csdnimg.cn/img_convert/416397f3081590154a22a94c91d907a8.png)

**2. Claude 的回答：**

![](https://i-blog.csdnimg.cn/img_convert/95a9ebb1f88d7b27dd742410de7b0cc0.png)

![](https://i-blog.csdnimg.cn/img_convert/fff8a2814d7b6dc58a2ec99db82cb797.png)

## 2. 确定技术选型

结合 2 个模型的建议，相信你心中就会大致有个谱，起码知道该从哪起步了。

比如`前端框架`：GPT 建议 React，而 Claude 则建议 `Vue.js`，上手更容易。

比如`界面设计`：GPT 和 Claude 都建议 `TailwindCSS`。

到这个阶段，再结合自己的知识背景进行技术选型，是不是容易了很多？

如果完全是技术小白，那就继续追问，让它给一个`适合技术小白`的可执行技术路线。

假设最终的技术选型如下：

- 前端：`Vue.js`；
- 后端：`FastAPI`；


## 3. 实现功能模块

有了思路，确定了技术选型，恭喜你，已经成功迈出了第一步！

接下来，无非就是搭积木，将脑海中想要实现的`功能`各个击破。

不过，在这之前，还是先划分下目录结构：

```
.
├── backend    # 后端代码（API、数据库、用户认证等）
├── frontend   # 前端代码（Vue、UI 组件等）
└── guide-docs # 文档（使用指南、API 文档等）
```

万事具备，开启你的前后端开发之旅吧。

### 3.1 搭建前端框架

还是和之前一样的套路，先让 AI 帮你搞定路线图：


```
这是一个基于 Vue 3 + Vite + TailwindCSS 构建的前端项目，需要实现以下功能：

1. 落地页设计 ( `LandingPage.vue` )
- 产品介绍
- 功能展示
- 动态打字效果
- 导航菜单
2. 用户认证系统
- 登录页面 ( `Login.vue` )
- 注册页面 ( `Register.vue` )
- 支持微信登录集成
3. 用户中心功能 ( `UserCenter.vue` )
- 总览面板
- 应用管理
- 奖励系统
- 操作日志
- 用户设置
- 深色/浅色主题切换
4. 定价系统 ( `PriceContent.vue` )
- 会员套餐展示
- 价格方案对比
- 功能特权说明
5. 通用功能
- 响应式设计（适配移动端和桌面端）
- 路由管理
- 状态管理 (Pinia)
- Toast 通知系统
- 404 错误页面
```


然后，让 AI 把脚手架搭好：

```
前端部分接下来怎么搞，我对vue不熟悉
```

![](https://i-blog.csdnimg.cn/img_convert/54ea1fd4e392fd05348e877333d6b090.png)


![](https://i-blog.csdnimg.cn/img_convert/f8612fc61d573b70ace6455cab5136fd.png)


你看，只需说人话，然后按照它给你的步骤执行就 OK 。

最终得到的目录结构：

```
└── src
│   ├── assets
│   │   ├── icons
│   │   └── images
│   ├── components
│   │   ├── landingpage
│   │   ├── login
│   │   └── usercenter
│   │       ├── app
│   │       └── tabs
│   ├── router
│   ├── store
│   ├── utils
│   └── views
├── tailwind.config.js
└── vite.config.js
```

有了路线图，再来搭建一个个页面是不是就清晰了很多？

比如`注册/登录`页面：

![](https://i-blog.csdnimg.cn/img_convert/dcd992f82b8237de16d68166bf8a3001.jpeg)

![](https://i-blog.csdnimg.cn/img_convert/38a5cf1eb5f17aed0038b3e9ee9840a6.jpeg)

比如`用户中心`页面：

![](https://i-blog.csdnimg.cn/img_convert/f9cd8490fcc2dd556b53b61d41bd3d55.png)

当然，这个过程中，你还会遇到各种问题。

逢山开路，遇水搭桥，你只需和 AI 说人话，一个不行，就问两个。


### 3.2 搭建后端框架

相比前端，后端更为复杂一些，难点主要在于数据库、表、字段的设计。

不过，根据 GPT 的建议，开发阶段可以使用 SQLite 结合 ORM 工具快速验证。

![](https://i-blog.csdnimg.cn/img_convert/ca6471142773a91a9652d3ddbf0e60f9.png)

**老规矩，先让 AI 帮你搞定目录结构**：

```
我决定采用 fastapi 进行后端开发，主要包括两个模块：
- 管理员后台：管理员登录，用户管理；
- 用户前端：用户注册，用户登录，应用管理
你可否先帮我梳理出项目目录结构
```

```
├── backend/                     # 后端目录（FastAPI）
│   ├── app/
│   │   ├── main.py             # 主入口文件
│   │   ├── api/
│   │   │   ├── __init__.py     # API 初始化
│   │   │   ├── admin.py        # 管理员相关接口
│   │   │   ├── user.py         # 用户相关接口
│   │   ├── core/
│   │   │   ├── __init__.py     # 核心模块初始化
│   │   │   ├── config.py       # 配置文件（数据库连接、JWT 配置等）
│   │   │   ├── security.py     # 安全模块（如认证、授权）
│   │   ├── models/
│   │   │   ├── __init__.py     # 数据模型初始化
│   │   │   ├── user.py         # 用户表模型
│   │   ├── schemas/
│   │   │   ├── __init__.py     # 数据验证模型初始化
│   │   │   ├── user.py         # 用户相关验证模型
│   ├── Dockerfile              # 后端 Docker 配置
│   ├── requirements.txt        # Python 依赖包
│   └── alembic/                # 数据库迁移工具
│       ├── versions/           # 数据库版本记录
│       └── env.py              # Alembic 配置
```

> 注：这个目录结构，完全可作为 FastAPI 后端开发的脚手架，方便复用，**建议收藏**！

其实，后端为前端服务，因此，在前端开发特定功能时，再逐一完成对应的后端服务即可。

当然，整个过程并非顺利！

即便是看似简单的`用户注册登录`模块，你也许就会遇到如下疑问：

**1. 如何存储密码，确保用户信息安全？**

![](https://i-blog.csdnimg.cn/img_convert/fda472a207d1cbedc9b3bdea05dac259.png)

**2. 如何注册企业邮箱，用于`用户注册` `密码重置`时发送验证码？**

![](https://i-blog.csdnimg.cn/img_convert/746aca21ce72941d6f9e294b936d9f48.png)

![](https://i-blog.csdnimg.cn/img_convert/a55392b741864bc3c1a48099dbd94419.png)

**3. 如何实现身份认证和授权？为何要双 Token 机制？**

这时再去了解 `JWT（JSON Web Token）`，就会容易很多。

![](https://i-blog.csdnimg.cn/img_convert/046e438aa9aa59fe4b42b17149da8519.png)

。。。

一旦开始，各种问题会接踵而来，但是解决问题的过程一定会很痛快，因为 AI 可能会把你带偏，这时就需要有个基本判断，调转船头，换个 AI 继续问，然后。。。`柳暗花明又一村`


### 3.3 优化网站界面

当网站的核心功能开发完毕，就是时候考虑这个问题了。

尽管网站的核心功能最重要，但一个良好的用户界面不仅能提升用户体验，还能增加留存和转化。

当然，有了 AI，UI 设计亦非难事，你只需发挥想象即可。

比如这里的`打字机`和`背景动画`效果，就是 GPT 帮我搞定的：

![](https://i-blog.csdnimg.cn/img_convert/c5007d0d4496731257c8b81b118d5635.gif)


## 写在最后

相信看到这里的你，一定想去动手试试。

一旦开始，你会发现，这一切，其实并没有那么难。

不吹不擂，有了 AI 加持，人人皆可打造自己的数字工具。

本文先打个样，如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。




