前文，分享了【小智Pro】系列文章：

[30天，AI 陪我写了3万行代码，上线一款应用，3点血泪教训](https://zhuanlan.zhihu.com/p/1970051780579660673)

[小智Pro：智能闹钟提醒 + 云端同步，端云协同方案](https://zhuanlan.zhihu.com/p/1970446275288741797)

[小智Pro：在线点歌+歌词同步，支持打断和搜索，端云协同方案](https://zhuanlan.zhihu.com/p/1971130142131730137)

[小智Pro：给小智装上"知识外挂"，从此告别一问三不知](https://zhuanlan.zhihu.com/p/1972219653188194715)

[小智Pro：接入 Dify 知识库，告别重复建库](https://zhuanlan.zhihu.com/p/1972940870450951890)

[小智Pro：自定义屏显，天气/节气/黄历... 你的桌面你做主](https://zhuanlan.zhihu.com/p/1973649349654364314)


以上所有工具，均基于设备端 MCP 实现。

我们知道，要让小智 AI 接入 MCP，有两种方式：

1. 设备端代码新增 MCP tool；
2. 通过官方暴露的 MCP 接入点；

两种方式各有利弊：
- 前者需要制作固件，适用于批量生产；
- 后者无需制作固件，定制化程度高，可玩性高，但需要自己接入服务；

关于`通过接入点接入MCP服务`，具体原理，可见笔者前文：

[小智AI如何接入你搭建的MCP Server？](https://zhuanlan.zhihu.com/p/1916061081077539780)

尽管官方给出了示例教程，对于缺乏编程基础的小伙伴来说，接入门槛还是略高。

为了让大家`零门槛给小智接入MCP`，`小智Pro`进行了焕新升级：

在`设备端MCP`的基础上，新增`接入点MCP`一级目录：

![](https://i-blog.csdnimg.cn/img_convert/5886082d7f5c7d5eb4107c97362460d3.jpeg)

欢迎体验👇：
> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

今日分享，聊聊：
- 用户侧：`接入点MCP`的核心功能，用户如何接入
- 平台侧：`接入点MCP`的架构设计，平台如何实现


## 1. ‘接入点MCP’核心功能

当前实现了两个界面：
- MCP广场
- MCP绑定管理

为用户提供 MCP 服务管理、设备绑定一条龙服务。

无需编写一行代码，在`小智Pro`平台，简单**四步**，即可为你的`小智`接入 MCP 服务：


![](https://i-blog.csdnimg.cn/img_convert/7e7accfdf5c98163626180a978696b5e.png)

### 1.1 MCP广场 

MCP广场分为两个标签页：

- **公共MCP服务**：平台所有用户的公开MCP服务
- **我的MCP服务**：当前用户创建的私有MCP服务

![](https://i-blog.csdnimg.cn/img_convert/d87eb89ff07f0164ae86593ebdc47f1f.jpeg)

每个MCP服务以卡片形式展示，包括服务名称、描述、标签等信息。

**MCP服务交互操作**：

- 查看：点击眼睛图标，查看MCP服务详情
- 点赞：对公共MCP服务表示认可和支持
- 绑定：将MCP服务绑定到指定设备


![](https://i-blog.csdnimg.cn/img_convert/a7806dd6018326b15d5b95c45c5e5e30.png)


除了平台接入的**公共MCP服务**，**我的MCP服务**标签页，支持用户根据自己的需求，创建定制化的MCP服务。

![](https://i-blog.csdnimg.cn/img_convert/99d66a0cf77c298e3508e9272de65b4d.png)

对于自定义 MCP 服务，目前支持主流的 MCP 协议：

![](https://i-blog.csdnimg.cn/img_convert/111ad35e43f337c5c73442833bbea991.png)


### 1.2 MCP绑定管理

MCP绑定管理页面，专注于设备与MCP服务之间的关联。

**设备选择与连接状态监控**：

该页面展示当前账户下的所有设备，可以选择特定设备查看MCP绑定情况。

![](https://i-blog.csdnimg.cn/img_convert/f04d5126669b6182bbd390a4da768738.png)


**接入点配置**：

前往小智控制台(xiaozhi.me)，复制当前设备的接入点地址：

![](https://i-blog.csdnimg.cn/img_convert/5607f98dd65bf5af545c948f5067b6ba.png)

绑定成功后，支持修改。


**连接状态控制**：

点击设备卡片上的`连接状态`，切换`连接和断开`状态，控制设备与MCP接入点的通信。

![](https://i-blog.csdnimg.cn/img_convert/50ce52176be99a5578e9dd2918a298d9.png)

连接成功后，前往小智控制台查看：

![](https://i-blog.csdnimg.cn/img_convert/99a0173201d90a074a01888db5496f39.png)


## 2. ‘接入点MCP’架构设计

### 2.1 概览

整体采用前后端分离的设计模式，前端负责用户交互和可视化管理，后端提供 API 接口和服务治理，底层通过WebSocket和进程管理实现实时通信。

![](https://i-blog.csdnimg.cn/img_convert/b963df031ffeff7098b9d58b1c09d318.png)



### 2.2 核心组件

**MCP管理器**：负责协调和管理所有的MCP连接。

主要功能包括：

- 测试连接
- 连接管理
- 断开连接
- 自动重连
- 资源清理

**进程管理器**：负责管理MCP服务的本地实例。
- 启动和监控MCP服务进程
- 管理进程的输入输出管道
- 终止不再需要的进程实例
- 为不同设备提供共享进程

**共享进程**：

实测发现，每个 MCP 服务占用的资源并不低：


```
root 25130  0.0  0.7 306088 61192 pts/4   python -m mcp_proxy https://mcp.xx.net/5x/sse
root 5204  0.0  1.1 11687744 96600 pts/4  node /root/.bin/12306-mcp
```

`sse` 类服务需 61 MB 内存，而 `stdio` 类服务占用内存更高。

因此生产环境中，每个 MCP 服务，必须采用**共享进程**模式运行。

这样，所有调用该 MCP 服务的设备，都会复用同一个进程，大幅减少系统资源消耗。

![](https://i-blog.csdnimg.cn/img_convert/b1fb143c2a21b4c856f59e2315ab51d6.png)



### 2.3 MCP协议支持

后端支持主流的 MCP 通信协议，以适应不同类型MCP服务：

- STDIO协议: 通过标准输入输出与本地进程通信
- SSE协议: 通过Server-Sent Events实现实时推送
- StreamableHttp协议: 通过HTTP请求进行异步通信

## 写在最后

本文分享了`小智Pro: 零门槛为小智接入MCP`的核心功能和架构设计。

如果对你有帮助，不妨**点赞收藏**备用。

欢迎体验 `小智Pro` 更多功能，请戳👇：

> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

有任何问题，欢迎进群交流：


![](https://i-blog.csdnimg.cn/img_convert/ffc37aec1ce3acdd2b378f6bd0eaddd6.png)

