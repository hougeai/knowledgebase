上篇，分享了`小智AI 接入视觉能力`的服务端实现：

[小智AI 接入视觉能力：原理拆解+服务端实现](https://zhuanlan.zhihu.com/p/1922233664944738738)

不过这玩意儿，有门槛，得硬件设备跟上啊。

有朋友讲，手头只有最古早的面包板：

![](https://i-blog.csdnimg.cn/img_convert/6f4dc316221b87bd98f083e370203fdd.jpeg)

别扔！

本文，分享一种`低成本的改造方案`，给你的`小智`装上眼睛。

## 1. 硬件准备

只需换一块开发板：
- 原来：ESP32-S3-DevKitC-1
- 改为：ESP32-S3-`CAM开发板`，**带OV2640摄像头**

![](https://i-blog.csdnimg.cn/img_convert/5d66e2469a1cc150ff5651506d7dd4b7.png)


其它模块和最早的面包板硬件一致：

- 数字麦克风：INMP441 模块
- 功放：MAX98357A
- 腔体喇叭：8Ω 2~3W  或 4Ω 2~3W 
- 屏幕：128x32 I2C(IIC) 液晶显示屏，SSD1306 驱动
- 400 孔面包板 2 块

## 2. 接线方案

`CAM开发板`和之前的核心板，引脚发生了很大变化，因为摄像头占用IO较多，所以可用的IO少了不少。

不过，只需接入麦克风、功放和屏幕，也够用了。

接线方案有很多种，这里给出一种，供有需要的朋友参考：

**连接功放：**

| ESP32S3 开发板引脚 | 功放 MAX98357A 引脚 | 功能描述 |
| :------------ | :------------------- | :--------------- |
| GPIO39        | DIN                  | 数字信号             |
| GPIO40        | BCLK                 | 位时钟              |
| GPIO41        | LRC                  | 左/右时钟            |
| 3V3/3.3V      | Vin                  | 电源正极，短接 SD     |
| GND           | GND                  | 接地，短接 GAIN 增益|


**连接麦克风：**

| ESP32S3 开发板引脚 | 麦克风 INMP441 引脚 | 功能描述 |
| :------------ | :---------------- | :-------------- |
| GPIO1         | WS                | 数据选择            |
| GPIO2         | SCK               | 数据时钟            |
| GPIO42        | SD                | 数据输出            |
| 3V3           | VDD               | 电源正极 3.3V        |
| GND           | GND               | 接地，短接 L/R 左/右声道 |

**连接屏幕：**

| ESP32S3 开发板引脚 | 屏幕 128x32 (IIC)引脚 | 功能描述 |
| :------------ | :---------------- | :--- |
| GPIO48        | SDA               | 数据线  |
| GPIO47        | SCK               | 时钟线  |
| 3V3           | VCC               | 电源正极 |
| GND           | GND               | 接地  |


接线图示例：

![](https://i-blog.csdnimg.cn/img_convert/c95c9f08336798a0261210609fdd4960.jpeg)

硬件接上后的示例：

![](https://i-blog.csdnimg.cn/img_convert/7ce6e2a08f208aa85cde05f351d76833.jpeg)



## 3. 制作固件

要让小智 AI 客户端适配你搭建的板子，需进行一番配置。

主要分 3 步：

**step 1**：新增板子配置文件

`main/boards/`中，每一种板子对应一个文件夹，假设板子定义为：

```
main/boards/bread-compact-wifi-s3cam-oled/
├── compact_wifi_board_s3cam_oled.cc
└── config.h
```

其中，

- `.cc` 定义了板子初始化相关函数
- `config.h` 定义了硬件配置和引脚映射

**step 2**：修改`main/Kconfig.projbuild`

`Kconfig.projbuild` 中定义了项目特有的配置选项，这里需要修改两处：

- 新增 BOARD_TYPE 板子

![](https://i-blog.csdnimg.cn/img_convert/b13eac4568a3888fd263d5d8f895d899.png)

- 新增 DISPLAY_OLED_TYPE 对板子的支持

![](https://i-blog.csdnimg.cn/img_convert/04b8fe2057d3cbfa1ae39c1b51435130.png)


**step 3**：修改`main/main/CMakeLists.txt`

新增对板子的编译支持：

```
# 根据 BOARD_TYPE 配置添加对应的板级文件
if(CONFIG_BOARD_TYPE_BREAD_COMPACT_WIFI)
    set(BOARD_TYPE "bread-compact-wifi")
elseif(CONFIG_BOARD_TYPE_BREAD_COMPACT_WIFI_CAM_OLED)
    set(BOARD_TYPE "bread-compact-wifi-s3cam-oled")
```

最后，在构建固件前，`menuconfig` 配置时，别忘了勾选新增的 `Board Type`：

![](https://i-blog.csdnimg.cn/img_convert/143564dc64ea52a7883718e098398161.png)


## 写在最后

本文分享了 `低成本改造小智AI面包板，并接入视觉能力` 的一种方案。

如果对你有帮助，欢迎**点赞收藏**备用。

暂不给官方仓库提 PR 了，需要板子配置文件的朋友，公众号后台回复`camera`，免费发你。

---

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。

