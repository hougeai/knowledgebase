最近入手一台 arm 开发板，内置安装了 Android 13 系统。

拿到手后，当务之急就是给它联网。

原本以为 so easy 的一件事，却折腾了我半天。

接入 WIFI，**“已连接，但无法访问互联网”**？

今天分享一下问题解决的过程，希望给遇到类似问题的朋友，一些参考。

## 前置准备

拿到板子，首先需要登录设备，这里简单介绍两种方式。

**方式一：**找一根 HDMI 线，连接到显示器；有线鼠标和有线键盘连接到板子的 USB 口，开机启动。

**方式二：** 如果觉得方式一麻烦，可以选择使用投屏软件，在本地电脑控制开发板：
- 投屏可以用免费开源的 [QtScrcpy](https://github.com/barry-ran/QtScrcpy/releases)，本地电脑下载，无需安装，内置 `adb` 工具;
- 找一根 type c 线连接开发板和本地电脑；
- 双击 QtScrcpy.exe，打开访问界面。

![](https://i-blog.csdnimg.cn/direct/2c0c24e74e734c36a28c8a8159dc118a.png)


## 问题描述：

连接 WIFI 后，如果你也遇到下面的问题，那么可以继续看下去了。

![](https://img-blog.csdnimg.cn/img_convert/f6211042e15758054bf856f6c5deae13.png)



## 尝试思路1：Captive portal 配置
> 参考：[https://www.evil42.com/index.php/archives/17/](https://www.evil42.com/index.php/archives/17/)

Captive Portal 是安卓 5 引入的一种检测网络是否正常连接的机制，通过 HTTP 返回的状态码是否是 204 来判断是否成功，如果访问得到了 200 带网页数据，那你就可能处在一个需要登录验证才能上网的环境里，比如说校园网和酒店，如果连接超时就在 WiFi 图标和信号图标上加一个感叹号。

首先，本地电脑打开一个终端，确认 `adb` 能否识别到你的设备：

```
adb devices
```


接下来，通过如下命令通过修改系统设置来控制这种行为。

```
# 将 captive_portal_mode设置为0（不使用系统默认的 URL 进行检测）
adb shell settings put global captive_portal_mode 0
#查看当前状态：
adb shell settings get global captive_portal_mode
```

如果还是不行，试试更新下用于检测互联网连接状态的两个 URL。
```
#分别修改两个地址
adb shell settings put global captive_portal_http_url http://captive.v2ex.co/generate_204
adb shell settings put global captive_portal_https_url https://captive.v2ex.co/generate_204

# 或者下面地址
adb shell settings put global captive_portal_https_url https://connect.rom.miui.com/generate_204
adb shell settings put global captive_portal_http_url http://connect.rom.miui.com/generate_204

```

修改后，`无法访问互联网`的提示没了，不过依然无法打开网页。

DHCP 自动分配的 IP 地址，应该没问题啊，要不试试设置一个静态 IP ？



## 尝试思路2：静态 IP 配置
DHCP 自动分配的 IP 地址是和设备的 MAC 地址相关的，是否是 IP 地址冲突了？

为此尝试修改 IP 地址，默认网关和 DNS 还是和之前一致！

在本地电脑，通过如下命令查看局域网内设备：

```
arp -a
```

发现是可以发现这个设备的：

![](https://img-blog.csdnimg.cn/img_convert/2f393b64931fe2926e2876d2d78647c8.png)

但是，依然无法访问互联网。

那么，会不会是 DNS 的问题？

## 尝试思路3：DNS 配置

我发现 DHCP 自动分配的 DNS 是 192.168.1.1，这个是路由器的 IP 地址。

我把 DNS 改成了 8.8.8.8，这是 Google 的公共 DNS 服务器。

终于，可以成功打开网页了！

果然，是 DNS 的锅~

虽然可以访问互联网，但新问题又来了：在本地局域网却 ping 不通这个 IP 地址，这就意味着在内网无法调用开发板上部署的任何服务。

莫非是路由器的问题？

于是，我用手机开了一个热点，连上热点网络后，压根不存在上面这些问题！

到这一步，是 WIFI 网络的问题，实锤了！

怎么解决?

找路由器去！

## 最终方案：路由器配置

在路由器背面找到 局域网 IP 地址(LAN IP)。

浏览器中打开，登录成功后，可以发现设备已经成功接入了。

![](https://img-blog.csdnimg.cn/img_convert/ce12cb68d439c0f59756f3737abf4685.png)

不同品牌的路由器应该大同小异，找到 `上网方式`。

![](https://img-blog.csdnimg.cn/img_convert/b5ad49462f2b43ca1d39619130a6d2cc.png)

我这里之前默认的是 `Bridge(AP)` 方式，把它改成`自动获取 IP (DHCP)`，设备重新连接这个 WIFI，完美解决！

为什么改变 `上网方式`解决了问题？

- Bridge（桥接模式）AP（接入点模式）：通常用于扩展现有网络的 WiFi 覆盖范围。这种模式下，本地路由器不负责分配IP地址和管理网络，而是将这些任务交给上层路由器。路由器仅作为网络的中继，设备之间的通信依赖于主路由器。如果主路由器对IP地址通信有限制（如客户端隔离），设备就无法相互通信。
- DHCP模式下：本地路由器负责为每个连接的设备分配IP，确保每个设备都有唯一的IP，并通过网络地址转换（NAT）来管理外部和内部网络通信。

因此，通过将路由器从 Bridge 模式切换到 DHCP 模式，路由器重新承担起管理和分配网络的任务，确保了局域网内设备的正常通信，和访问外网。

## 写在最后

总体来说，在给 Android 开发板联网过程中，我们可能会遇到:

- 连接WiFi成功但无法上网 - 可能是Captive Portal的问题，需要配置检测设置；
- 局域网内无法ping通设备 - 可能由于IP地址冲突或者DNS问题；
- 外网正常但局域网通信异常 - 很可能就是路由器设置的问题了！

以上，希望给遇到类似问题的朋友，一点参考。

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

下一篇，我们将给这个开发板接入 `AI` 能力，敬请期待！

---

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，想进群体验的朋友，公众号后台「联系我」即可，拉你进群。

