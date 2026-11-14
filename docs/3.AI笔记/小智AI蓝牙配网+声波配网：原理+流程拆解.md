小智AI 最新版固件更新到 `2.1.0`，相比 `2.0.5` 有哪些重大更新？

今天扫了一遍新增 `commit`，发现：

架构更新主要有：
- **设备状态更新机制**：调整为`设备状态机`
- **音频编解码器重构**：用 ESP-IDF 官方音频组件 `esp_audio_codec` 和 `esp_audio_effects` 替换原来的的 `78opus` 编解码器。内存占用更低。

功能更新主要有：
- WIFI配网新增了两种方式：**蓝牙配网和声波配网**

相比原先的**AP配网**，这两种方式的用户体验都更友好。

所以，

今日分享，聊聊**蓝牙配网和声波配网**的基本原理和通信流程。


## 1. 蓝牙配网

> 一句话简介：通过 BLE 低功耗蓝牙将 Wi-Fi 的 SSID 与密码从手机传输至设备。

### 1.1 整体架构

从设备端代码上看，简单画个流程图：

![](https://i-blog.csdnimg.cn/img_convert/05bf552990d93c8cd22fd89469df4214.png)

具体而言，

**Step 1: 配网模式的触发**

当设备状态不是 `Starting` 且未处于说话状态时，调用 `StartWifiConfigMode()` 进入配网模式。


**Step 2: 停止 Station 模式**

设备断开和当前 Wifi 的连接


**Step 3: 状态机切换到配网状态**

将设备状态机切换到配网状态。

**Step 4: 启动蓝牙配网**

在 WifiBoard::StartWifiConfigMode() 中，根据 Kconfig 配置选项选择并启动具体的配网方式。

![](https://i-blog.csdnimg.cn/img_convert/a2a8fd1243cde225448962d06ce36442.png)


**Step 5: 初始化 BLE 控制器**

在 Blufi::init() 中调用 _controller_init()，完成 ESP-BT-Controller 的初始化，并打印版本信息、时钟源、Feature 配置及 MAC 地址。

**Step 6: 初始化 BluFi Profile 并开始广播**

### 1.2 配网通信流程

配网数据流程图（手机→设备）：

![](https://i-blog.csdnimg.cn/img_convert/73f77411c5928f57a8850df3a64cfc44.png)

Wi-Fi 术语里，有两种工作模式：

**STA（Station）模式**：

设备作为“站点”连接到现有的无线路由器（AP，Access Point），这种模式下 ESP32 相当于一个客户端，去连接路由器上网。

**AP（Access Point）模式**：

设备自己创建 Wi-Fi 热点，让其他设备（如手机）连进来，
这时 ESP32 相当于一个小型路由器。



**问题来了：BluFi App 在哪下载？**

`BluFi` 是乐鑫官方提供的基于 BLE 的 Wi-Fi 配网协议。

> 参考文档：[https://docs.espressif.com/projects/esp-idf/zh_CN/stable/esp32/api-guides/ble/blufi.html](https://docs.espressif.com/projects/esp-idf/zh_CN/stable/esp32/api-guides/ble/blufi.html)
>
> Android 版应用下载：[https://github.com/EspressifApp/EspBlufiForAndroid/releases](https://github.com/EspressifApp/EspBlufiForAndroid/releases)

使用非常简单：
- 打开手机蓝牙
- 打开 BluFi App
- 扫描 ESP32 设备

点击 **配网** 进入网络配置界面。BluFi 支持以下三种模式：

- Station: 连接至现有 Wi-Fi 网络。

- SoftAP: 创建 Wi-Fi 热点。

- SoftAP/Station: 同时启用 SoftAP 和 Station 模式。

选择 `Station` 模式，点击刷新按钮，选择目标 Wi-Fi 名称，并输入密码。

![](https://i-blog.csdnimg.cn/img_convert/4f1e209cc50b184f21bdd62f73dc5468.png)


点击 **确定** 按钮完成配置。成功连接后，串口中打印日志如下：

```
I (2369270) BLUFI_CLASS: BLUFI ble connect
I (2432200) BLUFI_CLASS: BLUFI Set WIFI opmode 1
I (2432210) WifiManager: Starting station
I (2432210) wifi:mode : sta (98:3d:ae:e6:83:d0)
I (2432210) wifi:enable tsf
I (2432210) WifiBoard: WiFi scanning
I (2432290) BLUFI_CLASS: Recv STA SSID: 12_404
I (2432370) BLUFI_CLASS: Recv STA PASSWORD : 18xx
I (2432410) BLUFI_CLASS: BLUFI request wifi connect to AP via esp-wifi-connect
I (2438210) BLUFI_CLASS: BLUFI ble disconnect
I (2438210) BLUFI_CLASS: BLUFI deinit finish
I (2438230) BLUFI_CLASS: connected to WiFi
```




## 2. 声波配网
> 一句话简介：利用浏览器播放经 FSK 调制的音频信号，设备通过麦克风采集并解调出 Wi-Fi 信息。

**优点**：不依赖 BLE 或热点，只要手机/电脑扬声器就能完成配网。



### 2.1 整体架构

和`蓝牙配网`的整体基本一致：如果选择声波配网，会创建一个 `FreeRTOS` 任务 `acoustic_wifi`，并调用 `ReceiveWifiCredentialsFromAudio()`


### 2.2 配网通信流程

流程图如下：

![](https://i-blog.csdnimg.cn/img_convert/e63befe5e8fc9d93d6d5e88ef3ba0c55.png)

简言之：

- 手机把 WiFi 信息编码成音频信号播放；
- 设备用麦克风采集音频，通过 AFSK 解调算法解析出 SSID/密码；
- 像 BluFi 一样存到 SsidManager 并启动 WifiStation 连接；
- 根据连接结果反馈成功或失败。

项目根目录下 `scripts/sonic_wifi_config.html` 就是配网页面，直接拉到本地浏览器中即可：

![](https://i-blog.csdnimg.cn/img_convert/69355b440c34c18041fefa4fd35680b2.png)

如果嫌麻烦，戳这个链接：[https://iqf7jnhi.pinit.eth.limo](https://iqf7jnhi.pinit.eth.limo)

当进入配网模式时，串口日志如下：

```
I (2718) WifiBoard: Starting acoustic WiFi provisioning, channels: 1
I (2818) AUDIO_WIFI_CONFIG: Entering Waiting state
I (3478) AUDIO_WIFI_CONFIG: Entering Receiving state
W (11248) AUDIO_WIFI_CONFIG: Buffer overflow, clearing buffer
I (11398) AUDIO_WIFI_CONFIG: Entering Waiting state
```

配网成功后，串口日志如下：

```
I (664048) AUDIO_WIFI_CONFIG: Entering Receiving state
I (665728) AUDIO_WIFI_CONFIG: Received text data: 12_404
18205109389
I (665728) AUDIO_WIFI_CONFIG: WiFi SSID: 12_404, Password: 18xx
I (665728) SsidManager: compare [12_404:6] [12_404:6]
W (665738) SsidManager: SSID 12_404 already exists, overwrite it
I (665738) AUDIO_WIFI_CONFIG: WiFi credentials saved successfully
```

## 写在最后


本文分享了`小智AI`的`蓝牙配网+声波配网`的基本原理和通信流程。

如果对你有帮助，不妨**点赞收藏**备用。

`One More Thing`：`小智Pro` 设备端固件，已全面适配最新版`v2.1.0`：
> [https://github.com/hougeai/xiaozhiPro/releases](https://github.com/hougeai/xiaozhiPro/releases)

![](https://i-blog.csdnimg.cn/img_convert/8ee1b8ecdd9d6b43e109022ef13a1a12.png)


戳下方链接，免费体验`小智Pro`👇：

> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

有问题，欢迎来聊。





