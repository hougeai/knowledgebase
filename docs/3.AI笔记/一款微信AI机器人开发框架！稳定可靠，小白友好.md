前段时间和大家陆续分享了几种`微信AI机器人`的实现：
- `chatgpt-on-wechat`: [手把手搭建微信机器人，帮你雇一个24小时在线的个人 AI 助理](https://zhuanlan.zhihu.com/p/707507951)
- `NGCBot`：[打造基于Hook机制的微信机器人，Windows本地部署](https://zhuanlan.zhihu.com/p/708579992)
- `智能微秘书`：[搭建微信机器人的第3种方式，我又造了一个24H在线的个人AI助理](https://zhuanlan.zhihu.com/p/715222311)
- `wechatbot-webhook`：[搭建微信机器人的第4种方式，免费开源，轻量高效](https://zhuanlan.zhihu.com/p/715452718)

其中，

- `NGCBot` 基于 [`WeChatFerry(wcf)`](https://github.com/lich0821/WeChatFerry) 框架，用 Windows PC 端微信；
- `chatgpt-on-wechat` 基于 `itchat` 框架，用网页端微信，不到一天就惨遭封号；
- `智能微秘书`和 `wechatbot-webhook` 都是 `wechaty` js 库实现。不过`智能微秘书`很多功能需付费，因此基于 `wechatbot-webhook` 写了接收消息的接口，<u>定制化打造了微信机器人-`小爱(AI)`</u>。

然而，前不久，微信对`网页端机器人`进行大规模清理，`小爱`也未能幸免。。。

---

`网页端微信`已被证明不安全了，急需寻找平替方案！

看到隔壁群里，基于 `(wcf)` 的机器人都还健在，于是打算用`wcf`把`小爱`复活，代码将全部开源。


**今日分享，带大家熟悉`wcf`框架，并从零打造`小爱`同款微信机器人。**


## 1. `wcf`简介
> 项目地址：[https://github.com/lich0821/WeChatFerry](https://github.com/lich0821/WeChatFerry)

**大白话原理**：`wcf`是一个“劫持”了PC端微信的工具，当微信收到消息时，在显示到页面前，先把消息拿来，通过自定义接口处理，当需要发送消息时，组装消息体，调用微信发消息的模块，发出去！

![](https://i-blog.csdnimg.cn/img_convert/cf56074f8acc6e7c957c8718caac0ab8.png)

`wechatbot-webhook` 拦截的是网页端微信，而 `wcf` 拦截的是PC端微信，原理类似。

所以你只需做两件事：

<u>1. 熟悉`wcf`框架；</u>

<u>2. 实现自定义接口，完成消息处理。</u>

本篇，先带大家熟悉`wcf`框架中的一些基本概念，为下一步`实现自定义接口`铺平道路。

不过，正式开发之前，还需做好如下准备工作。

不多说，先上车！

## 2. 准备工作

`wcf`基于 Windows 端微信进行实现，因此请准备好：一台 Windows 电脑或者服务器。

### 2.1 Windows PC

如果只是想体验一下，随便玩玩，笔记本和台式机就行，只要装上 Windows 就成！

也许你会关心：

**Q: 对配置有什么要求？**

A：亲测 2c4g 就能跑，4c8g 完全没问题。

**Q：PC 需要装什么系统？**

A：用的 win11，其他系统没测过。win10 官方都不再维护了，建议直接装 win11，安装也非常简单，不了解的小伙伴可看教程：[简单3步，搞定 Windows11 系统安装](https://zhuanlan.zhihu.com/p/708707594)

### 2.2 Windows Server

如果要用于生产环境，需要长期稳定运行，最好准备一台 Windows 服务器。

**有哪些方式呢？**

相比 Linux，Windows 系统对内存要求更高，至少确保 2c4g 哦。 

**方式一：云厂商购买**：以某云为例（仅供参考，不构成推荐）

![阿里云](https://i-blog.csdnimg.cn/img_convert/fe510a74c8fee16068407b61c02d2497.png)

![腾讯云](https://i-blog.csdnimg.cn/img_convert/0c8e814bd576496badf29b6ffd2bf87e.png)

选择上述对应配置后，注意系统镜像选择 Windows Server.

**方式二：搭建虚拟机**：

当然，如果你已经有一台高性能 Linux 服务器，也无需额外再买 Windows 服务器，可以选择在 Linux 上构建一台 Windows 虚拟机，篇幅有限，有机会再单独出一篇教程。

### 2.2 安装微信

`wcf` 不同版本，基于微信版本进行开发，因此需要指定版本的微信。

为减少新手入门受版本困扰，本教程将统一采用：当前最新的 `wcferry 39.3.3.2`，其对应的微信客户端版本为：
- [WeChatSetup-3.9.11.25.exe](https://github.com/lich0821/WeChatFerry/releases/download/v39.3.5/WeChatSetup-3.9.11.25.exe)

双击完成安装后，记得前往`设置`，关闭`自动更新`，否则后台会自动更新为新版本！

![](https://i-blog.csdnimg.cn/img_convert/dfb592916422afc2e4059f083627d2a5.png)

### 2.3 准备开发环境

本教程将基于 `wcf` 的 `Python` sdk 完成开发，当然 `wcf` 也支持 NodeJS 等其他开发语言。

为此，我们还需准备好 `Python` 开发环境，有需要的朋友可查看之前的教程：

[环境准备之Conda和VS code安装](https://zhuanlan.zhihu.com/p/688627817)。


## 3. 熟悉 `wcf`

> 项目文档：[https://wechatferry.readthedocs.io/zh/latest/autoapi/wcferry/index.html](https://wechatferry.readthedocs.io/zh/latest/autoapi/wcferry/index.html)

`wcf` 对操作微信进行了非常棒的封装，为此只需了解**两个类**即可上手开发。

**注：运行下述示例前，确保 PC 端微信已经成功登录。**
### 3.1 `Wcf` 类

`Wcf` 类，实现操作微信的各种功能，比如：
- 查询登录状态
- 获取登录账号信息
- 获取消息类型
- 获取联系人
- 查询数据库所有表
- 获取消息
- 发送消息（可 @）
- 转发消息
- 拍一拍群友

下面我们略举几例：

**获取登录账号信息：**
```
from wcferry import Wcf
wcf = Wcf()
wcf.get_user_info()
```
输出如下：
```
微信名：小爱
微信ID：wxid_xsh5ve62e98i12
手机号：138xxx
存储地址：C:\Users\vboxuser\Documents\WeChatFiles\
```

**获取消息类型：**
```
wcf.get_msg_types()
# 输出如下
{0: '朋友圈消息', 1: '文字', 3: '图片', 34: '语音', 37: '好友确认', 40: 'POSSIBLEFRIEND_MSG', 42: '名片', 43: '视频', 47: '石头剪刀布 | 表情图片', 48: '位置', 49: '共享实时位置、文件、转账、链接', 50: 'VOIPMSG', 51: '微信初始化', 52: 'VOIPNOTIFY', 53: 'VOIPINVITE', 62: '小视频', 66: '微信红包', 9999: 'SYSNOTICE', 10000: '红包、系统消息', 10002: '撤回消息', 1048625: '搜狗表情', 16777265: '链接', 436207665: '微信红包', 536936497: '红包封面', 754974769: '视频号视频', 771751985: '视频号名片', 822083633: '引用消息', 922746929: '拍一拍', 973078577: '视频号直播', 974127153: '商品链接', 975175729: '视频号直播', 1040187441: '音乐链接', 1090519089: '文件'}
```


**获取所有联系人列表**：

```
wcf.get_contacts() 
```
输出如下：

```
{'wxid': 'fmessage', 'code': '', 'remark': '', 'name': '朋友推荐消息', 'country': '', 'province': '', 'city': '', 'gender': ''}
{'wxid': 'medianote', 'code': '', 'remark': '', 'name': '语音记事本', 'country': '', 'province': '', 'city': '', 'gender': ''}
{'wxid': 'floatbottle', 'code': '', 'remark': '', 'name': '漂流瓶', 'country': '', 'province': '', 'city': '', 'gender': ''}
{'wxid': 'gh_3dfda90e39d6', 'code': 'wxzhifu', 'remark': '', 'name': '微信支付', 'country': 'CN', 'province': 'Guangdong', 'city': '', 'gender': ''}        
{'wxid': 'gh_09bce433cd27', 'code': '', 'remark': '', 'name': '猴哥的AI知识库', 'country': 'CN', 'province': '', 'city': '', 'gender': ''}   
{'wxid': '53532625158@chatroom', 'code': '', 'remark': '', 'name': '小爱测试群', 'country': '', 'province': '', 'city': '', 'gender': ''}
{'wxid': 'weixin', 'code': '', 'remark': '', 'name': '微信团队', 'country': '', 'province': '', 'city': '', 'gender': ''}
```

该接口会拉取微信本地数据库中所有联系人，其中`群聊`的`wxid`有`@chatroom`，据此可以获取所有`群聊`列表。

而要**获取所有好友列表**，可以直接调用：

```
wcf.get_friends()
```

具体实现为：把非好友过滤掉：

```
not_friends = {
    "fmessage": "朋友推荐消息",
    "medianote": "语音记事本",
    "floatbottle": "漂流瓶",
    "filehelper": "文件传输助手",
    "newsapp": "新闻",
}
```

更多接口功能，我们在开发过程，用到了再聊！


### 3.2 `WxMsg` 类

`WxMsg` 类，实现对各种微信消息的封装，其属性如下：

```
type (int): 消息类型，可通过 `get_msg_types` 获取
id (str): 消息 id
xml (str): 消息 xml 部分
sender (str): 消息发送人
roomid (str): （仅群消息有）群 id
content (str): 消息内容
thumb (str): 视频或图片消息的缩略图路径
extra (str): 视频或图片消息的路径
```

具体实现过程中，可能需要关注：
- `type (int)`：根据不同消息类型，触发不同的处理逻辑，比如文本、图像、语音等；
- `roomid`：群聊的wxid，如果是私聊，则`roomid`和`sender`保持一致。
- `content`：消息内容，非文本内容统一为 xml 格式。
- `thumb`和`extra`：接收到视频或图片消息，微信保存在本地的.dat格式数据，需解密后查看。


## 写在最后

本文分享了一款稳定可靠的微信机器人开发框架：`wcf`，了解其基本原理并快速上手，下篇将带大家实操，从零打造`小爱`同款微信机器人。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，`小爱`也活跃在群里，欢迎体验。公众号后台「联系我」，拉你进群。
