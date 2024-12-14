如果你想让本地 AI 服务，触达全球，那么一定得了解下内网穿透。

前段时间和大家分享过两款内网穿透方案：

- [Cloudflare：免费内网穿透，让本地AI服务，触达全球](https://zhuanlan.zhihu.com/p/716891964)
- [LanProxy：免费内网穿透，手把手搭建，三步搞定](https://zhuanlan.zhihu.com/p/711445796)

有一说一：
- Cloudflare 的内网穿透服务还是很香的，无需自己购买服务器中转。唯一的缺点就是不太稳定，经常出现 Tunnels 无法建立隧道的问题。
- LanProxy 需要拥有一台具有公网 IP 的机器作为中转，最近发现访问量大了之后也不稳定。

今日分享，继续带来一款强大的内网穿透方案 - frp，github上已有86.4k star，且项目一直在持续迭代中。

## 1. 什么是内网穿透

一句话：把只能内网访问的服务，暴露到公网。

关于内网穿透的基本原理，可以翻看之前的教程：[免费内网穿透，手把手搭建，三步搞定](https://zhuanlan.zhihu.com/p/711445796)，这里就不赘述了。

## 1. frp 简介
> 项目地址：[https://github.com/fatedier/frp](https://github.com/fatedier/frp)

frp 采用 Golang 编写，支持跨平台，你仅需下载对应平台的二进制文件即可，无需任何依赖，堪称小白利器。

目前最新版本为 0.61.0，前往官方 releases 页面下载即可。

> [https://github.com/fatedier/frp/releases](https://github.com/fatedier/frp/releases)

![](https://img-blog.csdnimg.cn/img_convert/37e373896cd155cc785aafca5d66a831.png)

frp 专注于内网穿透，支持 TCP、UDP、HTTP、HTTPS 等多种协议，可将内网服务通过具有公网 IP 的机器中转，暴露到公网。

所以，首先要准备一台有公网 IP 的机器，笔者之前已分享过多篇相关内容，可以翻看。

接下来，我们上实操。


## 2. frp 实现内网穿透

### 2.1 frp 安装
不像 ngrok 需要编译，frp 安装的非常简单，只需前往上方官方 releases 页面下载对应系统的安装包，解压出来就能用。

以 Linux 操作系统为例：

```
#下载
wget https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz
#解压
tar -zxvf frp_0.61.0_linux_amd64.tar.gz
#进入目录
cd frp_0.61.0_linux_amd64/
```

文件夹中，有两个二进制文件frpc（c代表client）和frps（s代表server），分别是客户端程序和服务端程序。


```
frp_0.61.0_linux_amd64$ ls
frpc  frpc.toml  frps  frps.toml  LICENSE
```

因此，客户端（即内网服务器）和服务端（即公网服务器），需要准备好对应文件。


### 2.2 服务端配置和启动

首先，修改服务端配置文件`frps.toml`：

```
# 服务端配置
bindPort = 7000
webServer.addr = "0.0.0.0"
webServer.port = 7500
```

其中，`bindPort` 用于监听客户端，`webServer.port` 是服务端的管理界面。

然后，采用如下命令一键启动：

```
nohup ./frps -c frps.toml > server.log 2>&1 &
```

注：frp 默认采用 IPv6，不过会同时监听IPv4和IPv6地址，但你用 netstat 只看到 IPv6 被监听，实际上是通过了 IPv4-Mapped IPv6 Address 同时兼听了IPv4地址。

所以，如果你发现端口不通的时候，**一定记得去看看端口防火墙有没打开**。

看看端口能否连接？

```
sudo apt install telnet
telnet server_ip 7000
```

查看并打开端口防火墙：

```
sudo ufw status
sudo ufw allow 7500 
sudo ufw allow 7000
# sudo ufw delete allow 7000
```

最后，浏览器输入 `server_ip:7500`，即可看到管理界面：

![](https://img-blog.csdnimg.cn/img_convert/f3123d605d8faebea3cdfe9348a976f4.png)

这里我有一个客户端已经接入，并映射了3个端口。

接下来，我们就来完成客户端配置。


### 2.3 客户端配置和启动

首先，修改服务端配置文件`frps.toml`：

```
serverAddr = "serve_ip"
serverPort = 7000

[[proxies]]
name = "ollama"
type = "tcp"
localIP = "127.0.0.1"
localPort = 3002
remotePort = 3002
```

其中，`serverPort` 要对应 服务端的 `bindPort`。我们以`把 ollama 映射到公网可访问` 为例，新增配置如上方代码块：`localPort`和`remotePort`分别是本地服务的端口，和要映射到服务端端口。

注：如果有多个端口要映射，只需把`ollama`的复制一份，指定不同端口即可。

然后，采用如下命令一键启动：

```
nohup ./frpc -c frpc.toml > client.log 2>&1 &
```

日志如下：

![](https://img-blog.csdnimg.cn/img_convert/ac834dca17c2bed6b7c4578a8a84e1f0.png)

至此，frp 内网穿透服务搭建完毕。

以上通过一个简单案例，带大家快速跑通流程。更多配置，可参考官方文档：[https://gofrp.org/zh-cn/docs/](https://gofrp.org/zh-cn/docs/)

## 写在最后

本文实操带大家走完了`frp搭建内网穿透`的全部流程。

作为一款开源免费的服务，frp 配置简单，非常适合小白上手。

如果对你有帮助，不妨**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近搭建的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。

