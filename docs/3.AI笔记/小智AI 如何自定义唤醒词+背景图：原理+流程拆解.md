小智AI 从 `v2.0.x` 版本开始，支持用户自定义`唤醒词+表情包+背景图`：

![](https://i-blog.csdnimg.cn/img_convert/43a5a65cc8f930c8fdb2e53e2b9fc6f1.png)

实现效果如下：


![](https://i-blog.csdnimg.cn/img_convert/c3e39f0ddb8da44eb06a6973215a5bf1.jpeg)



有朋友好奇：如何实现的？

本文，将尝试拆解这部分的`基本原理`和`实现思路`。

## 1. 设备端

首先，我们要了解 ESP32 芯片中的数据是如何存储的，已了解的朋友可跳过。

以常见的 `ESP32s3-N16R8` 为例，这里的 `N16R8` 分别代表啥？

### 1.1 ESP32中的存储

按照是否在芯片上，存储分两种：

**1. 片上存储器（On-chip Memory）**

- 内部ROM（384KB）：存储启动代码和关键的系统函数
- 内部SRAM（512KB）：用于运行时变量、堆栈等，访问速度快，断电后数据丢失
- RTC存储器（16KB）：8KB快速存储器，8KB慢速存储器

可以理解为计算机的内存。

**2. 片外存储器（Off-chip Memory）**

- Flash存储器：容量通常为8MB或16MB，用于存储程序代码、常量数据和文件系统
- PSRAM（可选）：伪静态随机存储器，用于扩展运行时内存，通过SPI接口连接

可以理解为计算机的硬盘、虚拟内存。

`N16R8` 就代表 16M 的 Flash 和 8M 的 PSRAM。

硬盘空间有限，为了充分利用，有了分区的概念。

### 1.2 Flash中的分区

以 `ESP32s3` 的 16M 为例，它的分区表如下： 
```
# Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,    0x4000,
otadata,  data, ota,     0xd000,    0x2000,
phy_init, data, phy,     0xf000,    0x1000,
ota_0,    app,  ota_0,   0x20000,   0x3f0000,
ota_1,    app,  ota_1,   ,          0x3f0000,
assets,   data, spiffs,  0x800000,  8M
```
上表中，`Offset` 代表分区的起点，`Size` 代表分区的大小。

那为啥 `nvs` 是从 `0x9000` 开始呢？

因为，`0x1000-0x9000` 另有他用：

- `Bootloader`（0x1000-0x8000）：存储启动引导程序

- `分区表`（0x8000-0x9000）：描述Flash中各分区的信息

这些分区分别是干啥呢？

- `NVS分区`（0x9000开始，16KB）：存储配置参数和键值对数据
- `OTA数据分区`（0xd000开始，8KB）：存储OTA更新相关的元数据
- `PHY初始化数据`（0xf000开始，4KB）：存储射频校准数据
- `OTA固件分区`（两个，约3.9MB）：存储主应用程序代码，支持固件更新和回滚
- `Assets分区`（8MB）：存储资源文件（图片、音频、字体等）

上述分区，有哪些优势？

- 充分利用 Flash 的所有空间；
- ota_0 和 ota_1 交替使用，当前分区处于"活动"状态，另一分区接收新固件；
- 分区分工明确，`OTA固件分区`和`Assets分区`独立更新，互不干扰

而用来自定义唤醒词+表情包+背景图的，正是这里的 `Assets分区`。

问题来了，`Assets分区`里放的啥，设备端又如何接收更新呢？

下面来看，服务端要做哪些工作。

## 2. 服务端

### 2.1 前端交互页面

> 前端代码已开源：[https://github.com/78/xiaozhi-assets-generator](https://github.com/78/xiaozhi-assets-generator)

首先，服务端会读取的设备系统信息：

![](https://i-blog.csdnimg.cn/img_convert/ab4ef7c129fc0126f578f5c9314566ff.png)

然后，用户可以自定义的选项如下：
- 唤醒词：内置 esp32 官方训好的唤醒词
- 字体
- 表情
- 背景图

![](https://i-blog.csdnimg.cn/img_convert/7b20eab82faddf1502fa7116db023c89.png)

最后，前端否则把上述文件打包成`assets.bin`:

![](https://i-blog.csdnimg.cn/img_convert/5c7225fe390fe9eceec91aa827482437.png)

这个 `assets.bin` 就是塞进`Assets分区`的文件。

问题来了，放在你浏览器中的 `assets.bin` 如何送到设备中去的？

### 2.2 后端处理逻辑

先看流程图：

![](https://i-blog.csdnimg.cn/img_convert/61164b15e8858644a3fbc3590d2082a5.png)

具体执行步骤如下:

**step 1**：前端和后端保持 websocket 长连接，将 `assets.bin` 发送到后端服务器，生成一个 `url`

**step 2**：通过 `callMcpTool` 实现工具调用，本质是给后端发 POST 请求。

**step 2.1**：调用 `self.assets.set_download_url` 把 `url` 送给设备端。

云端调用该工具后，设备端会将`url`保存到设置中。

```
AddUserOnlyTool("self.assets.set_download_url", "Set the download url for the assets",
    PropertyList({
        Property("url", kPropertyTypeString)
    }),
    [](const PropertyList& properties) -> ReturnValue {
        auto url = properties["url"].value<std::string>();
        Settings settings("assets", true);
        settings.SetString("download_url", url);
        return true;
    });
```

**step 2.2**：调用 `self.reboot`，设备重启。

**step 2.3**：设备重启后，根据 `url` 下载 `assets.bin` 到 `Assets分区`。

自此，设备端更新生效。

问题来了，上述工具调用，不都是 MCPTool 吗？

而要实现 `tool/call`，底层还得通过 `MQTT`，所以前端给后端发了 POST 请求后，后端是给 `MQTT broker` 的 topic 发了这条指令，最终这条指令，被设备端执行。

![](https://i-blog.csdnimg.cn/img_convert/544fa88b98d9077fb041d48412f8824b.png)


## 写在最后

本文分享了`小智AI: 自定义唤醒词+表情包+背景图`的基本原理和实现思路。

篇幅有限，关于 `MQTT + MCP` 实现设备远程控制的原理，我们下篇见。

如果对你有帮助，不妨**点赞收藏**备用。

`小智Pro`下一版本更新，也将支持设备远程控制，有任何想法，欢迎来聊👇：
> [https://ai.feishu.cn/wiki/IfTawES0mi0YTqk8GQ4cw4qOnD3](https://ai.feishu.cn/wiki/IfTawES0mi0YTqk8GQ4cw4qOnD3)
