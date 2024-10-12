上篇，带大家玩转高德开放平台 API，为大模型提供和本地生活相关的可靠信息。

本文将带大家，结合**免费的大模型API**，基于**微信机器人开发框架**，打造完整的 Bot。

>友情提醒：注册一个小号使用，严禁用于违法用途（如发送广告/群发/诈骗、色情、政治等内容），否则封号是早晚的事哦。

## 0. 开发框架选择

之前给大家分享过三种微信机器人的搭建方案，要么账号容易被封禁，要么需要付费使用。

有没有**零风险，零付费**的方案？

有的，本文将基于：[搭建微信机器人的第4种方式，免费开源，轻量高效](https://blog.csdn.net/u010522887/article/details/141348878) 中的框架进行实现，占用资源不多，而且可定制化程度非常高！

## 1. 大模型准备

尽管免费的 API 有速率限制，不过对于个人使用而言，完全足够！

前天，给大家盘点了[免费且靠谱的大模型 API，统一封装，任性调用](https://blog.csdn.net/u010522887/article/details/141731878)，赶紧用起来！

为了在应用中，任意切换各种大模型 API，我这里接入了所有兼容 OpenAI 格式的大模型，并进行统一封装，下面给出示例代码：

```
from openai import OpenAI
model_dict = {
    'gemini-1.5-pro': {
        'api_key': server_api_key,
        'base_url': server_url,
        'model_name': 'gemini-1.5-pro'
    },
    'ernie-128k': {
        'api_key': server_api_key,
        'base_url': server_url,
        'model_name': 'ERNIE-Speed-128K'
    },
}

class UniLLM:
    def __init__(self):
        model_names = list(model_dict.keys())
        self.models = {name: LLM_API(api_key=model_dict[name]['api_key'], base_url=model_dict[name]['base_url'], model=model_dict[name]['model_name']) for name in model_names}

    def __call__(self, model_name, messages, temperature=0.7):
        model = self.models.get(model_name)
        return model(messages, temperature=temperature)
```

## 2. 微信机器人开发

参考：[搭建微信机器人的第4种方式](https://blog.csdn.net/u010522887/article/details/141348878)，相信看到这里的你，已经把服务部署好了。

首先，进行需求分析：一个完整的 Bot 应该具备哪些功能？

- 基本功能：
  - 自动发送消息；
  - 自动接收消息并处理。
- 特色功能：
  - 定时任务；
  - 本地生活服务。

为了快速实现 MVP 版本，这里优先完成以上功能。

来吧，一起一步步把 Bot 搭建好。 

## 2.0 服务部署

参考上篇，采用 docker 一键部署，如果运行过程中遇到问题，可打印最后几行日志查看：
> PS：如需更多定制化功能，也可选择源码部署，不过坑略多，下篇跟大家分享。

```
sudo docker logs --tail 40 wx
```

如果运行过程中新建了群，需要重启容器：

```
sudo docker restart wx # 容器名称 or 容器 id 均可
```

## 2.1 发送消息接口

这个比较简单，服务部署后就有了，再贴下代码：

```
def send_message(to='user', content='hello', isRoom=False):
    url = f'http://129.150.39.xxx:3001/webhook/msg/v2?token=123'
    data = {
        "to": to,
        "isRoom": isRoom,
        "data": {"content": content}
    }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code == 200:
        print(response.json())
    else:
        print('发送接口调用失败')
```

## 2.2 接收消息接口

接收消息的接口，需要部署一个服务，这里我们选用 FastAPI 搭建。

接口定义如下：

```
app = FastAPI()

@app.post("/receive")
async def receive_message(request: Request):
    # 处理请求数据
    data = await request.form()
    message_type = data.get("type")
    content = data.get("content")
    source = data.get("source")
    is_from_self = data.get("isMsgFromSelf")
    try:
        # 填写处理逻辑-开始
        handle_message(message_type, content, source, is_from_self)
        # 填写处理逻辑-结束
        return JSONResponse(content={"status": True, "data": {"type": "text", "content": "success"}})
    except Exception as e:
        return JSONResponse(content={"status": False, "data": {"type": "text", "content": "failed"}})
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
```

注意：上述接口需指定返回值，否则报错。

接下来，我们需要接收消息后的处理逻辑：

```
def handle_message(message_type='text', content='', source='', is_from_self="0"):
    # 初版只处理文本
    if message_type != "text":
        return
    source = json.loads(source)
    from_name = source['from']['payload']['name']
    if source['room']:
        if '@小爱' not in content: # 群聊中非@消息
            return
        content = content.replace("@小爱", "")
    # 处理逻辑-content
    bot_answer = get_bot_answer(content)
    if source['room']:
        bot_answer = f'@{from_name} {bot_answer}'
        send_message(to=source['room']['payload']['topic'], content=bot_answer, isRoom=True)
    else:
        send_message(to=from_name, content=bot_answer, isRoom=False)
    return bot_answer
```

具体回复什么内容，封装在 `get_bot_answer()` 函数中，下面我们就来搞定它！

## 2.3 本地生活服务

上一篇中，我们已经搭建好了利用**高德开放平台**提供的**本地生活服务API**。

为了能够让 LLM 认识它们，并且合理调用他们，我拆解成了三个步骤：

1. 首先，根据用户输入，判断用户意图；
2. 然后，根据意图调用相应的API接口，获取可靠的本地生活信息；
3. 最后，基于API返回的信息，LLM 整理后，回复用户。

我们一步步来搞定它！

### 2.3.1 意图识别

我这里预先定义了 6 种意图：`['天气', '步行规划', '骑行规划', '驾车规划', '公交规划', '地点推荐']`，如果识别结果不在意图列表中，则直接调用 LLM 进行回答。

```
# 1. 首先判断意图
intention = intention_rec(user_content)
print(f'意图识别结果：{intention}')
if intention not in intentions_list:
    messages = [
        {'role': 'system', 'content': sys_base_prompt},
        {'role': 'user', 'content': user_content}
    ]
    res = unillm(model_name=model_name, messages=messages)
    return res.strip() if res else f'小爱有点累了，稍候再试吧'
```

给大家展示下`意图识别`的日志：

![](https://img-blog.csdnimg.cn/img_convert/60309bc5adfce5fb41df13b21347385a.png)

### 2.3.2 调用本地生活接口

接下来，根据`意图识别`结果调用对应的本地生活接口，下面以`天气预报`为例：

首先需要LLM 提取出`用户输入`中的地址信息；

然后请求天气预报接口`get_weather`获取天气；

最后 LLM 进行整理，返回给用户。

```
# 2. 根据意图进行相应的操作
## 2.1 天气预报
if intention == '天气':
    # 提取地址
    messages = [{'role': 'user', 'content': f'{user_content}，提取这句话中的地址信息，只需回答地址'},]
    res_address = unillm(model_name='glm4-9b', messages=messages)
    res_address = res_address.strip()
    wea_cast = get_weather(res_address, extensions='all')
    if not wea_cast:
        return '未找到该地址的天气信息，建议地址信息：省/市/区/'
    forecasts = wea_cast['forecasts'][0]['casts']
    today_cast = json.dumps(forecasts[0], ensure_ascii=False)
    future_cast = json.dumps(forecasts[1:], ensure_ascii=False)
    # 调用 LLM
    messages = [
        {'role': 'system', 'content': sys_weather_report},
        {'role': 'user', 'content': f'地名：{res_address}；今日天气：{today_cast}；未来三天：{future_cast}；用户问题：{user_content}'},
    ]
    res_weather = unillm(model_name=wea_model_name, messages=messages)
    return res_weather if res_weather else f'小爱有点累了，稍候再试吧'
```

### 2.3.3 效果对比

比如我问他：`周末不知道干点啥好`

下面是没有`意图识别`的结果：

![](https://img-blog.csdnimg.cn/img_convert/bf9091e68da4a9405d17f43e9c6c1da1.png)

收不住啊，胡诌了个`鲤中步行街`给我，这是什么地方？

接下来是`意图识别`的结果（地点推荐）：基于高德的检索信息，LLM 给我答复如下。

![](https://img-blog.csdnimg.cn/img_convert/6851679d5cf8e8f1fe63abda4f619b0a.png)


## 2.4 定时任务实现

我们简单实现两个定时任务：

- 每天播报指定地区的天气信息；
- 根据成员的生日日期，自动发送生日祝福。

如果你的服务部署在海外，强烈建议为服务器设置时区：

```
# 查看当前时区
timedatectl
# 设置
sudo timedatectl set-timezone Asia/Shanghai
# 验证
timedatectl
```

执行后，就不用像上篇那样在代码中指定时区了。

### 2.4.1 每日天气播报

指定要发送的群聊名称，和要播报的地区：

```
def send_weather(to='机器人测试', addresses=['上海杨浦区',]):
    for add in addresses:
        content = weather_forecast(add)
        send_message(to=to, isRoom=True, content=content.strip())
```

![](https://img-blog.csdnimg.cn/img_convert/6613cdc34441be6ba4687b41791f6caf.png)


### 2.4.2 定期生日祝福

首先定义一个字典，用于存放群成员的生日信息：

```
birthday_dict = {
    '爸爸': '07-25',
    '大哥': '07-25',
    '二哥': '07-25',
    '妈妈': '07-25',
    '大姐': '07-25',
}
```

考虑到国内大部分小伙伴，常用阴历生日，这里可以设置一下阳历/阴历转换：

```
from lunarcalendar import Converter, Solar, Lunar
# 阴历转换为阳历
def lunar_to_solar(date, leap_month=False):
    year, month, day = date.split('-')
    lunar_date = Lunar(int(year), int(month), int(day), leap_month)
    solar_date = Converter.Lunar2Solar(lunar_date)
    date = f'{solar_date.year}-{solar_date.month:02d}-{solar_date.day:02d}'
    return date
```

每天定时遍历，如果今天有某位群成员的生日，则调用 LLM 发送生日祝福：

```
def send_birthday_wish(to='机器人测试'):
    today = str(datetime.now().date())
    today_lunar = solar_to_lunar(today)
    today_lunar = '-'.join(today_lunar.split('-')[1:])
    if today_lunar in birthday_dict.values():
        for name, birthday in birthday_dict.items():
            if birthday == today_lunar:
                content = birthday_wish(name, solar=today, lunar=today_lunar)
                send_message(to=to, isRoom=True, content=content.strip())
```

最后，把所有定时任务放到后台去跑吧：

```
if __name__ == '__main__':
    # 每天发送天气预报
    group_name = 'xxx'
    schedule.every().day.at("06:30").do(lambda: send_weather(to=group_name))
    # 设置生日祝福任务
    schedule.every().day.at("06:00").do(lambda: send_birthday_wish(to=group_name))
    while True:
        schedule.run_pending()
        time.sleep(1)
```

给大家看下测试效果：

![](https://img-blog.csdnimg.cn/img_convert/401d87e9a3bed5c717a94bd40de3bc28.png)

![](https://img-blog.csdnimg.cn/img_convert/491e34cd17dfacb18a095cdf86b146f0.png)

还不知道怎么给家人发生日祝福？问问`小爱`吧~

## 写在最后

汇集各路大模型 API，以及高德提供的本地生活接口，终于把一个简单的微信机器人捏完了。

项目还在迭代中，大家有更好的想法，欢迎评论区交流。

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

--- 
为了方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

`小爱`也在群里，想进群体验的朋友，公众号后台「联系我」即可，拉你进群。


