
前不久，微信对`网页端机器人`进行大规模清理，我基于 `webhook`开发的微信机器人-`小爱(AI)`也惨遭射杀。。。

这不，平替方案来了！

上篇和大家了基于 Windows 端微信的方案 - [`WeChatFerry(wcf)`](https://github.com/lich0821/WeChatFerry) ：

- [一款微信AI机器人开发框架！稳定可靠，小白友好](https://zhuanlan.zhihu.com/p/18006455210)

相信看过上篇的你，对 `wcf` 框架已经有了基本了解。 

今日分享，和大家汇报下：基于 `wcf` 框架，复活 `小爱` 的完整过程。

相比之前方案，可玩性更高，放几张效果图：

- 对`交流群`的广告行为零容忍！
![](https://i-blog.csdnimg.cn/img_convert/9fe413554f25cfd29c904c3b9ee87e48.png)

- `关键词`自动邀请入群：

![](https://i-blog.csdnimg.cn/img_convert/804365143bc77553421fcd7a2757521b.jpeg)

![](https://i-blog.csdnimg.cn/img_convert/811fbd8310d80014499104a4395de8aa.png)



代码放 GitHub 了，感兴趣的朋友自取！

- [https://github.com/hougeai/wcf-wechatbot](https://github.com/hougeai/wcf-wechatbot)

不多说，先上车，再完善。

## 1. 搭建框架

> 项目框架参考了开源项目 [NGCBot](https://github.com/ngc660sec/NGCBot)，在此向 NGCBot 开发团队致谢！

代码结构如下：

```shell
├── data
│   ├── room.db                 # 群数据库
│   ├── user.db                 # 用户数据库
│   └── zaobao_template.json    # 早报模板
├── logs
│   └── app_20250110101504.log  # 日志文件
├── config.yaml                 # 项目配置文件
├── main.py                     # 启动文件
├── requirements.txt            # 项目依赖
├── servers
│   ├── api_server.py           # 接口服务
│   ├── db_server.py            # 数据库服务
│   ├── msg_server.py           # 消息服务
│   └── schedule_server.py      # 定时任务服务
└── utils
    ├── common.py               # 公共函数
    ├── llm.py                  # LLM 接口
    └── prompt.py               # 提示词配置 
```
其中，
- `data`文件夹：用于存放数据库文件，以及项目需要用到的一些模板文件；
- `log`文件夹：用于存放日志文件，便于调试；
- `servers`文件夹：用于各种接口的实现；
- `utils`文件夹：用于通用函数实现。

### 1.1 安装项目依赖

采用 conda 管理项目依赖：

```
git clone https://github.com/hougeai/wcf-wechatbot.git
cd wcf-wechatbot
conda create -n wcf python==3.10.11
pip install -r requirements.txt
```

特别留意下 wcf 版本，和微信客户端版本要对应（参见上篇）：

```
wcferry==39.3.3.2
```


### 1.2 编写配置文件

项目中所有用到的外部参数，均采用 .yaml 文件进行配置，方便统一管理，可根据自己需求重新定义。

`config.yaml` 已制作好模板，复制一份即可：

```
cp config.yaml.example config.yaml
```

AI 对话、外部接口等，都需要用到 Key，因此只有填入对应字段，对应功能才能生效：

**超级管理员配置**：

填入你的微信号，便于接收机器人的通知消息等。上一篇中有提到，用 wcf 即可获取。

```
Administrators:
  - 'wxid_xsh5ve62e98i12'
```

**定时任务配置**：

定义要实现的任务列表，以及发送时间：
```
scheduleConfig:
  # 定时任务列表
  taskList:
   早报推送: 'morningPage'
   摸鱼日历: 'fishPage'
  # 早报推送时间
  morningPageTime: '10:20'
  # 摸鱼日记推送时间设置
  fishTime: '18:00'
```

**进群关键词配置**：

设置不同关键词，进行自动拉群。
```
roomKeyWord:
  加群:  58060988515@chatroom 
```


**API接口服务配置**：

用于定义各种接口对应的 Key 和 URL，需前往对应官网进行申请。

比如，要获取天气、定理位置等信息，可采用高德地图提供的接口信息，有需要的朋友可参考教程：[高德 API 接入](https://zhuanlan.zhihu.com/p/717945448)

```
apiServer:
  # 高德 Key
  gaoDeKey: 'xxx'
```

**LLM 接口服务配置**:

本项目用到的 LLM 主要采用 OneAPI 统一管理，可参考教程：[OneAPI-接口管理和分发神器：所有大模型一键封装成OpenAI协议](https://zhuanlan.zhihu.com/p/707769192) 。

```
llmServer:
  # OneAPI配置
  oa_api_key: 'sk-x'
  oa_base_url: 'http://xxx:4000/v1'
  model_name_list:
   - 'gemini-1.5-flash'
   - 'gemini-1.5-pro'
```

此外，也预留了硅基流动 API key，同样兼容 OpenAI 格式。

```
  # 硅基流动API配置
  sf_api_key: 'sk-x'
```


你只需前往 [硅基流动](https://cloud.siliconflow.cn?referrer=clxv36914000l6xncevco3u1y) 注册账号，并生成一个 API key。

### 1.3 项目启动

准备好配置文件后，确保 PC 端微信已经成功登录。

项目根目录下 `main.py` 提供了程序入口，一键运行：

```
python main.py
```

看到如下日志，说明成功启动：

![](https://i-blog.csdnimg.cn/img_convert/50d67ed2ce9ecd3dfd20d55591d28103.png)

`MainServer` 实例中，主要完成如下任务：

```
class MainServer:
    def __init__(self):
        self.wcf = Wcf()
        self.wcf.enable_receiving_msg() # 开启全局接收
        self.initDateBase()
        self.rmh = RoomMsgHandler(self.wcf)
        self.smh = SingleMsgHandler(self.wcf)
        self.sts = ScheduleTaskServer(self.wcf)
        Thread(target=self.sts.run, name='定时推送服务').start()
```

- `initDateBase()`：初始化需要用到的数据库；
- `RoomMsgHandler`：群聊消息处理；
- `SingleMsgHandler`：私聊消息处理；
- `ScheduleTaskServer`：定时任务处理；

`processMsg` 是一个无限循环任务，用于帮你：**接收微信消息、处理消息、回复消息**。

基本逻辑是：判断消息类型，来自群聊，则交给`RoomMsgHandler`处理，来自私聊，则交给`SingleMsgHandler`处理。

```
# 群聊消息处理
if '@chatroom' in msg.roomid:
    Thread(target=self.rmh.mainHandle, args=(msg,)).start()
# 私聊消息处理
elif '@chatroom' not in msg.roomid and 'gh_' not in msg.sender:
    Thread(target=self.smh.mainHandle, args=(msg,)).start()
```


基于上述框架，再来填充相应模块，就相对简单了。

接下来，我们一个一个搞定！

## 2. 丰满灵魂

### 2.1 数据库
> 文件位置：`servers/db_server.py`

本项目的数据库实现采用 sqlite，由于比较简单，故没采用 ORM 实现。用 3 个类完成数据管理任务：

- `DbInitServer`：初始化数据库和表结构；
- `DbUserServer`：好友库的增删改查；
- `DbRoomServer`：微信群的增删改查。

### 2.2 消息处理
> 文件位置：`servers/msg_server.py`

消息处理的逻辑相对复杂，需要根据不同的消息类型，进行针对处理。且私聊和群聊也要区分开。

因此，先准备一个消息处理的通用类 `MsgHandler`，实现私聊和群聊都需要的功能。

然后，分别针对私聊和群聊，实现两个类：

- `SingleMsgHandler`
- `RoomMsgHandler`

对于`私聊`，`mainHandle`实现的功能如下：
- 超级管理员功能
- 处理加好友请求（当前需微信手机端打开自动通过好友）
- 处理进群请求
- 判断是否有私聊权限
- 处理消息，目前已支持：
  - 文本消息
  - 图片消息
  - 引用消息
  - 公众号/视频号消息

对于`群聊`，`mainHandle`实现的功能如下：
- 判断是否为白名单群聊
- 管理员功能
- 新人入群欢迎
- 处理消息，和`私聊`一样


### 2.3 定时任务

> 文件位置：`servers/schedule_server.py`

定时任务采用`schedule`库实现，封装为`ScheduleTaskServer`类，每新增一个定时任务，只需添加一个对应函数即可。

比如，要实现早报功能，只需：

```
def pushMorningPage(self):
    page = self.ams.getMoringPage()
    if not page:
        logger.error('获取早安页面失败')
        return
    room_items = self.drs.showPushRoom(taskName='morningPage')
    logger.info(f'准备推送给群: {room_items}')
    for room_id, room_name in room_items:
        self.wcf.send_image(path=page, receiver=room_id) # 传本地文件
        logger.info(f'早安页面推送给{room_name}成功')
```

然后，在 `run()`中添加一行：
```
def run(self):
    configData = returnConfigData()['scheduleConfig']
    schedule.every().day.at(configData['morningPageTime']).do(self.pushMorningPage)
```

### 2.4 更多功能

更多实现细节，可参考项目源码：

[https://github.com/hougeai/wcf-wechatbot](https://github.com/hougeai/wcf-wechatbot)

相信看到这里的您，一定还有更多想法待实现，去试试吧~

## 写在最后

本文基于 `wcf` 框架，复活了微信机器人-`小爱`，把完整实现过程捋了一遍。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，`小爱`也活跃在群里，欢迎体验，公众号后台「联系我」，拉你进群。
