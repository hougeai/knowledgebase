前文，分享了【小智Pro】系列文章：

[30天，AI 陪我写了3万行代码，上线一款应用，3点血泪教训](https://zhuanlan.zhihu.com/p/1970051780579660673)

[零门槛为小智接入MCP，小智Pro焕新上线：MCP广场+自定义服务](https://zhuanlan.zhihu.com/p/1980594562268427220)

得益于 ESP32 的强大，小智 AI 的生态不断壮大，接入的开发板琳琅满目：

![](https://i-blog.csdnimg.cn/img_convert/f6ceefc49367e71f9aa7b7334811d25b.jpeg)

除了语音对话，还能干点啥？

这正是`小智Pro`一直在探索的。

除了`闹钟、音乐、知识库、记忆、天气`等`实用价值`。

还应该提供`情绪价值`！

前两天，朋友寄来了一块开发板 - `zhengchen-eye`：

![](https://i-blog.csdnimg.cn/img_convert/ba25dc4085f36660f610504d5b303d21.jpeg)


相比其它开发板，有两大特点:
- 两块圆形串联LCD屏，可显示 gif 动图
- 两块触摸板，可感知触摸强度

这两天，设备端调试成功，已加到`小智Pro`支持列表中，先看效果：

[demo展示](https://link.zhihu.com/?target=https://www.bilibili.com/video/BV1vkmeBBEKp/?vd_source=cc29c4ba51b0e6b0472256fe6a96da6d)

今日分享，和大家聊聊：这两个功能的`基本原理`和`具体实现`。


## 1. 眼神交流

视频中的眨眼动作，本质上是写到设备中的 `gif 动图`。

因此，只需要设备端，为`zhengchen-eye`，自定义一份`display`即可。

下面上实操。

### 1.1 代码结构设计
`xiaozhi-esp32` 的 `display` 模块，采用面向对象的继承体系设计，清晰、可扩展。

核心是通过抽象基类，定义通用接口，然后根据不同类型的显示设备进行具体实现，层次结构如下：

```
Display (抽象基类)
└── LvglDisplay (基于LVGL库的通用显示实现)
    ├── LcdDisplay (LCD显示屏通用实现)
    │   ├── SpiLcdDisplay (SPI接口LCD显示屏)
    │   ├── RgbLcdDisplay (RGB接口LCD显示屏)
    │   └── MipiLcdDisplay (MIPI接口LCD显示屏)
    ├── OledDisplay (OLED显示屏实现)
    └── EmoteDisplay (基于EMOTE引擎的表情显示实现，esp-box-3用到)
```

`zhengchen-eye`接入的是 LCD 屏，只需继承`LcdDisplay`，进行定制化开发即可：

```
LcdDisplay (LCD显示屏通用实现)
└── ZhengchenEyeLcdDisplay (针对zhengchen-eye开发板的定制实现)
```
因为是特定板子的定制代码，我们放到 `boards/`目录下：

```
./zhengchen-eye
├── zhengchen_eye_lcd_display.cc
└── zhengchen_eye_lcd_display.h
```

### 1.2 基类代码详解
`Display`（display.h）是整个显示系统的抽象基类，定义了所有显示设备都应该具备的基本功能接口，比如：
- 状态显示 (SetStatus)
- 通知显示 (ShowNotification)
- 表情显示 (SetEmotion)
- 聊天消息显示 (SetChatMessage)
- 状态栏更新 (UpdateStatusBar)

`LvglDisplay` 是 `Display` 的子类，实现了基于 LVGL 图形库的具体显示功能：
- 基于 LVGL 的 UI 元素管理
- 通知、状态栏等通用 UI 组件

`LcdDisplay` 在 `LvglDisplay` 的基础上，针对 LCD 显示屏，增加了更多相关功能：
- LCD 面板初始化和配置
- LVGL 与 LCD 硬件的对接
- GIF 动画支持

### 1.3 自定义显示

在 `display` 模块初始化时，会调用 `SetupUI` 来实现基于 LVGL 的 UI 元素管理。

不过，基类中的 `SetupUI` 不是虚方法。

在不改变通用代码的情况下，我们重写`SetupUI` 函数，新增显示标签`gif_label_`：


```
void ZhengchenEyeLcdDisplay::SetupUI() {
    ESP_LOGI(TAG, "Starting UI setup");
    DisplayLockGuard lock(this);
    /* overlay */
    overlay_container = lv_obj_create(container_);
    lv_obj_add_flag(overlay_container, LV_OBJ_FLAG_HIDDEN); // 默认隐藏   
    
    gif_label_ = lv_gif_create(overlay_container);
    lv_gif_set_src(gif_label_, &happy);
}
```

然后，在板子初始化时，调用一次：


```
display_ = new ZhengchenEyeLcdDisplay(panel_io, panel,
            DISPLAY_WIDTH, DISPLAY_HEIGHT, DISPLAY_OFFSET_X, DISPLAY_OFFSET_Y, DISPLAY_MIRROR_X, DISPLAY_MIRROR_Y, DISPLAY_SWAP_XY);
display_->SetupUI();    
```

接下来，如何显示不同的 `gif 表情包` ？

重写 `SetEmotion` 函数！

主程序会调用 `SetEmotion` 来显示不同的 `emoji`，因此，只需把 `emoji` 改成 `gif` 就 OK 了。

下面用注释给大家解释下具体实现逻辑：

```
void ZhengchenEyeLcdDisplay::SetEmotion(const char* emotion) {
  // idle状态且 neutral 情绪 - 隐藏表情层，显示正常界面
  // 否则显示表情层
  // 根据emoji查找匹配的表情
}
```

效果如下：

![](https://i-blog.csdnimg.cn/img_convert/cb9116e9c5d46f23c094de9dd9216f0b.png)
  
![](https://i-blog.csdnimg.cn/img_convert/a98d5aa72fe195ae52e43b52ce6a1b57.png)

## 2. 触摸感应

### 2.1 工作原理

ESP32 内置`电容式触摸传感器`，基于电容变化，实现触摸检测：

- 电容构成: 每个触摸引脚与地之间存在寄生电容。
- 触摸效应: 当手指靠近或触摸电极时，人体作为额外的电容，总电容值就会增大

因此，看电容值大小，不就知道`是否触摸`了？

**看效果：**

> 未触摸状态：电容保持在 3w-
![](https://i-blog.csdnimg.cn/img_convert/8c764f0384dc6a83c5925a8475b0814e.png)

> 触摸：电容增大到 13w+
![](https://i-blog.csdnimg.cn/img_convert/c4d5f69aa64aa5d57234b22b012c58e4.png)

> 松手：电容减少到 2w+
![](https://i-blog.csdnimg.cn/img_convert/e268cac4439c66a4d90605355ed2f120.png)


### 2.2 功能实现

ESP32 官方文档中，触摸传感器共有 10 个 IO 口。

`zhengchen-eye`这块板子用了两个：

```
void touch_init() {
        touch_pad_init();
        touch_pad_config(TOUCH_PAD_NUM4); // 配置 GPIO4 为触摸引脚
        touch_pad_config(TOUCH_PAD_NUM5); // 配置 GPIO5 为触摸引脚
    }
```

然后，我们新增一个定时任务，实现触摸数据读取：

```
static void touch_read_task(void* arg) {
        zhengchen_eye* self = static_cast<zhengchen_eye*>(arg);
        while (1) {
            touch_pad_read_raw_data(TOUCH_PAD_NUM4, &self->touch_value);
            touch_pad_read_raw_data(TOUCH_PAD_NUM5, &self->touch_value1);
            ESP_LOGI(TAG, "Touch pad 4: %d, pad 5: %d", self->touch_value, self->touch_value1);
            vTaskDelay(2000 / portTICK_PERIOD_MS);
        }
    }
```

问题来了，`小智` 怎么知道我有没有触摸呢？

### 2.3 两大使用场景

换句话说，这个`触摸感应`到底可以用在什么场景？

笔者认为，至少可以有**两大使用场景**：

**一是，**`小智` 在和用户互动时，通过 MCP 发起主动问询！

放在设备端即可：

![](https://i-blog.csdnimg.cn/img_convert/d2312da0edb681da9b57dcf87ece4e5c.png)

当然，为了避免 `小智` 偷懒，让它每轮对话发起主动调用，更新提示词如下：

![](https://i-blog.csdnimg.cn/img_convert/7fbd6f17c3f43a1e7ddfd3d170e5bbe2.png)

**二是，** `定时任务`中加个判断，发生触摸动作时，主动上传到`服务端`，服务端每日统计触摸值，可作为 AI 和用户的 `亲密度` 属性。

当然，还有更多使用场景，欢迎大开脑洞，评论区聊~


## 写在最后

本文分享了`小智AI: 眼神交流+触摸感应`的基本原理和具体实现。

如果对你有帮助，不妨**点赞收藏**备用。

固件已做好，放到 `小智Pro` 官方文档，免费自取👇：

> [https://ai.feishu.cn/wiki/IfTawES0mi0YTqk8GQ4cw4qOnD3](https://ai.feishu.cn/wiki/IfTawES0mi0YTqk8GQ4cw4qOnD3)

有任何想法，欢迎来聊👇：

![](https://i-blog.csdnimg.cn/img_convert/61ebb7d56cfc18e0c420c9b10d3114f0.png)

