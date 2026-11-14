从某个版本开始，小智 AI 从 IoT 协议切换到 MCP 协议！

可玩性更高，想象空间更大了~

不管是 IoT 协议，还是 MCP 协议，本质上都是给小智扩展更多外部能力，只不过 MCP 生态越发壮大，这是大势所趋。

问题来了，有了 MCP ，都能干点啥呢？

目前，社区中对`定时闹钟提醒`的呼声很高，后台也接到了很多朋友的咨询。

今日分享：**如何通过 MCP 为小智 AI 接入 `定时闹钟提醒` 能力？**

先看效果：
> 当闹钟触发时：云端下发语音提醒，随后循环播放本地音乐，直到用户唤醒。

[https://www.bilibili.com/video/BV1sfHvzjE4o/](https://www.bilibili.com/video/BV1sfHvzjE4o/)

全文目录：

![](https://i-blog.csdnimg.cn/img_convert/ee4c6fc4ca8d7a6636a8c0f915d4e4e8.png)


## 1. 需求分析

`定时闹钟提醒` 其实可以拆解为三类需求：
- 倒计时功能：类似`番茄学习法`，比如工作 25min 后提醒我休息；
- 定时闹钟功能：比如`晚上 8 点提醒我睡觉`；
- 重复闹钟功能：比如`每天早 8 点提醒我起床`

**以什么方式提醒呢？**
- 屏幕显示；
- 播放本地音乐，直到唤醒；
- 云端下发语音通知；

**如果设备断电了，怎么确保 `定时闹钟提醒` 依然准时触发？**
- 云端存储：每个 `定时闹钟提醒` 在云端备份，设备通电后，再次同步；
- 设备端存储：nvs 持久化存储，无需依赖云端。

## 2. 实现思路

`定时闹钟提醒` 其实非常考验 LLM 的语义理解和工具调用能力。

为了提高成功率，现阶段还是不能对 LLM 抱有太高期望，因此任务定义越明确、越简洁，自然效果越好。

最简单，就是 LLM 在工具调用时，给设备端下发一个 `延时 delay`，设备端新增一个定时器，到点自动触发！

至于触发后，要完成什么动作，那还不是你说了算？

循环播放本地音乐，当然 OK！

向云端发请求，然后云端下发语音提醒，当然也 OK，只是相对复杂一些。

### 2.1 倒计时功能

首先，我们需要定义一个闹钟的结构体：

```
struct Alarm {
    time_t time;        // 开始提醒时间
    std::string name; // 提醒内容
};
```
当云端下发了`延时 delay`参数，更改闹钟触发的具体时间：


```
time_t now = time(NULL);
alarm.time = now + delay;
```

当需要调度闹钟时，再次计算`delay`：

```
CreateAndStartTimer(alarm_->time - now);
```

这种方式对`倒计时任务`完全没问题，但是对`定时闹钟`完全就抓瞎了，比如：

![](https://i-blog.csdnimg.cn/img_convert/9030083069e6298e5f8ecb5b322ea1ee.png)

你看，给了个完全错误的`delay`!

再次提醒它，给算成 10 小时之后的闹钟了：

![](https://i-blog.csdnimg.cn/img_convert/8f3e652b569d82842f98ac4a8ef7ec89.png)

必须先提醒它当前时间，才能算正确：

![](https://i-blog.csdnimg.cn/img_convert/158025f4e28df4615ee04b7fde317ec2.png)

显然这么做，用户体验太差，必须改造~

### 2.2 定时闹钟功能

除了 `delay` 参数，可以再加两个参数：

```
"hour: int, 如早上7点 the hour can be 7"
"minute: int, 如早上7:00， the minute can be 0"
```

那么，设置闹钟时，就可以根据下发参数进行判断：

```
if ((hour >= 0 && hour < 24) || (minute >= 0 && minute < 60)) {
        // 计算距离最近的指定hour和minute的开始时间
        struct tm* target_time = localtime(&now);
        // 设置目标时间的小时和分钟
        target_time->tm_hour = (hour >= 0 && hour < 24) ? hour : 0;
        target_time->tm_min = (minute >= 0 && minute < 60) ? minute : 0;
        // 转换为time_t
        time_t alarm_time = mktime(target_time);
        alarm.time = alarm_time;
    } else {
        alarm.time = now + delay;
    }
```

![](https://i-blog.csdnimg.cn/img_convert/7013d691d1388b035f66f50f0ad06c56.png)

你看，虽然给出了错误的 `delay` 参数，不过我们可以根据 `hour` 参数进行设置了~

这样，定时闹钟就没问题了~

如果还要重复提醒呢？


### 2.3 重复闹钟功能

继续加两参数：

```
"repeat: int , 重复次数；如果没说则默认1次，否则为具体的次数，最多重复10000次"
"interval: int, 间隔时间，单位为秒；repeat > 0时生效，比如每小时提醒我，interval can be 3600"
```

这时，完整的闹钟结构体定义如下：

```
struct Alarm {
    time_t time;        // 开始提醒时间
    int repeat;   // 重复次数，0表示不重复，大于0表示重复次数
    int interval; // 提醒间隔（秒）
    std::string name; // 提醒内容
};
```

当清除闹钟时，需要根据 `repeat` 参数判断：

```
it->repeat--; // 次数减去1
if (it->repeat > 0) {
    it->time += it->interval; // 设定下次闹钟时间
    ++it;
} else {
    it = alarms_.erase(it); // 删除过期的闹钟
}
```

![](https://i-blog.csdnimg.cn/img_convert/592ed118d323d601c07a76b8816293e7.png)

你看，LLM 成功给出了 `interval` 参数，86400s 刚好是 24h。


如果还要删除闹钟呢?


### 2.4 删除闹钟

怎么判断要删除的是哪一个闹钟呢？

用户最无感的，自然是根据关键词删除：

![](https://i-blog.csdnimg.cn/img_convert/e865c96492d698674b39363af3df5b4d.png)

但问题是，容易抓不准关键词：

![](https://i-blog.csdnimg.cn/img_convert/dd885359c40b9b6b50fc92d30a4d08e6.png)

怎么解决？

给每个闹钟一个 ID 吧，让 LLM 理解所有闹钟的上下文，然后根据 ID 删除：

![](https://i-blog.csdnimg.cn/img_convert/095bc8b1bfc2355fd0b6e0de678b5e35.png)


### 2.5 持久化存储

小智客户端中，所有需要持久化存储的数据，采用 NVS 存储，功能封装在 `Settings` 类中，它允许以键值对的形式存储和读取数据，如字符串、整数和布尔值。

为此，我们只需创建一个实例（对象）：

```
Settings settings_("alarm_clock", true);
```

传入两个参数：

- `alarm_clock`：这是命名空间，用于在 NVS中标识存储区域
- `true`：表示该实例具有读写权限

> 注：ESP-IDF中 NVS 键名的最大长度是15个字符（包括结尾的空字符）

然后，设置闹钟时，同时写入 NVS：
```
settings_.SetString("alarm_" + std::to_string(i), alarm.name);
settings_.SetInt("alarm_time_" + std::to_string(i), alarm.time);
settings_.SetInt("alarm_rpt_" + std::to_string(i), repeat);
settings_.SetInt("alarm_itv_" + std::to_string(i), interval);
```

设备重启后，从 NVS 读出来：

```
alarm.name = settings_.GetString("alarm_" + std::to_string(i));
alarm.time = settings_.GetInt("alarm_time_" + std::to_string(i));
alarm.repeat = settings_.GetInt("alarm_rpt_" + std::to_string(i));
alarm.interval = settings_.GetInt("alarm_itv_" + std::to_string(i));
```


### 2.6 效果测试

定时提醒：

```
>> 2分钟后提醒我出发。
```

![](https://i-blog.csdnimg.cn/img_convert/49fbe0aea57158175b37698628e5d4a4.png)

重复闹钟：

```
>> 每天8点叫我起床。
```

![](https://i-blog.csdnimg.cn/img_convert/eb5175984a10336dc60f1f5bbd1f4b2c.png)

查询闹钟提醒：

```
现在有哪些闹钟提醒？
```

![](https://i-blog.csdnimg.cn/img_convert/ce106efceee48f70bbfd73073647c1a2.png)

删除闹钟提醒：

![](https://i-blog.csdnimg.cn/img_convert/5db28090a8807764e268bca8703ad7fd.png)

断电重启：

![](https://i-blog.csdnimg.cn/img_convert/e644524edebac83d4182a86f746a0b60.png)

查询所有闹钟：


![](https://i-blog.csdnimg.cn/img_convert/ce9f864f9cc8289875fd27d02756c3c4.png)


## 写在最后

本文分享了`小智 AI + 闹钟提醒` 的具体实现思路。

如果对你有帮助，不妨**点赞收藏**备用。

有了定时触发，可玩的就不仅仅是`闹钟提醒`，一切可以自动化执行的任务，都可以交给它：

比如：每天帮你爬取热点资讯，整理后发到你微信。。。

尽情发挥你的想象吧~
