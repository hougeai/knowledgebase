前段时间，和大家分享了一个`免费内网穿透`的工具：[免费内网穿透，手把手搭建，三步搞定](https://blog.csdn.net/u010522887/article/details/140761164)

相信大家对`内网穿透`的基本原理已经有所了解。

后台有小伙伴问：我没有公网服务器进行转发，怎么搞？

最近一直在摸索 `Cloudflare` 家的产品，发现它的另一项免费服务 - `Cloudflare Tunnel`，可以完美解决！

本文将手把手带你用 `Cloudflare Tunnel` 实现`免费内网穿透`。

首先介绍 `Cloudflare Tunnel`的基本原理，然后实操两种配置方式：网页端配置 和 本地配置，大家根据个人偏好自选即可~
@[TOC](本文目录-按需取用)
## 1. Cloudflare Tunnel 简介
Cloudflare Tunnel，可以为云与设备之间打通一条加密通道，这样 Cloudflare 的 CDN 就可以通过这条加密通道访问到部署在内网的服务，包括Web、SSH等。

你有没有公网 IP 都无所谓！

重点是，免费！

![](https://img-blog.csdnimg.cn/img_convert/40dc2f787f30bd2c6dc23ab0b97a1cd4.png)

基本原理：在内网运行一个 Cloudflare 守护程序，与 Cloudflare 云端通信，将云端请求数据转发到内网的 IP + 端口。


## 2. 网页端配置
### 2.1 基础配置5步走 
网页端配置非常简单，共分为以下 5 步：

1. 进入 Cloudflare 主页，左侧找到 Zero Trust，点进去，随便写个域名，后面可以修改。

2. 创建 Cloudflare Zero Trust ，选择免费计划。需要绑定信用卡，如果你之前看过
[Cloudflare R2 免费对象存储申请指南](https://blog.csdn.net/u010522887/article/details/141586984)，肯定已经绑过卡了。

![](https://img-blog.csdnimg.cn/img_convert/d1f3bc53b5598eda3177a57a8d831a40.png)

3. 绑卡完成后，在 Network-Tunnels 中，创建一个 Tunnel。

![](https://img-blog.csdnimg.cn/img_convert/73cacdc31fff6a4b48c5673aa64cb83e.png)

4. 选择 Cloudflared 部署方式，因为Tunnel 需要通过 Cloudflared 来建立云端与本地网络的通道。

![](https://img-blog.csdnimg.cn/img_convert/468002e04ba116d4173bdb1ae2b0976f.png)

这里推荐两种方式进行部署：

![](https://img-blog.csdnimg.cn/img_convert/e9eb0ed44003e4b86587ab902c1a5a22.png)

**方式一：命令行部署**

首次使用，需要安装 Cloudflared，首次启动耗时较长。
```
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb 
sudo cloudflared service install xxx
```
上述指令会将 Cloudflared 注册为系统服务，Cloudflared 会被配置为随系统启动而自动运行。

安装完成后，可以通过如下命令查看服务状态：

```
systemctl status cloudflared
```
状态是 Active，则说明服务正常！

![](https://img-blog.csdnimg.cn/img_convert/b636ff20eedb689c2a65fcd899a00296.png)


**方式二：docker 部署**

![](https://img-blog.csdnimg.cn/img_convert/9b2017ea5407ac0e1e678b444dce2917.png)

点击复制 docker 指令，此外，还可以加上 `--name cloudflared -d --restart unless-stop` 为 Docker 容器增加名称、后台运行和自动重启。

```
docker run --name cloudflared -d --restart unless-stop cloudflare/cloudflared:latest tunnel --no-autoupdate run --token xxx
```

安装成功后，在 Tunnel 页面下方可以看到，已经连接成功！

![](https://img-blog.csdnimg.cn/img_convert/edf619e7f1d126b4ef0b143cc6a4d0ba.png)

推荐**一台服务器新建一个 Tunnel** ，不同端口的服务都通过这个 Tunnel 映射！


5. 映射域名 & URL

进入 Tunnel 页面，找到 `Public hostname`。

一个服务配置一个子域名（Subdomain），域名（Domain）需要在 cloudflare 完成 DNS 解析。

URL 处填写内网服务的 IP 加端口号，如果是转发到 80 端口，可以不用端口号。

Type 建议使用 HTTP，因为 Cloudflare 会自动为你提供 HTTPS。

![](https://img-blog.csdnimg.cn/img_convert/e2f896500541dc74d10ba3a4dc5367b3.png)

上面，我是用之前部署的 Dify 来举例：[本地部署 AI 智能体，Dify 搭建保姆级教程](https://zhuanlan.zhihu.com/p/715835878)。

最后，在浏览器中输入你的二级域名：https://dify.xx.xx.xx，搞定！

![](https://img-blog.csdnimg.cn/img_convert/e0ebe40b9812545974a2c46a3b63cd3d.png)

是的，你没看错，Cloudflare 已经自动为域名提供了 https 证书。

此外，一个 Tunnel 支持添加多条域名，来跳转到不同的内网服务（不同端口），在 Tunnel 页面 Public Hostname 中新增即可。

![](https://img-blog.csdnimg.cn/img_convert/87aae625a44c64e87146bf22ec4c4697.png)

### 2.2 添加额外验证

如果不想让所有人访问内网服务怎么办？

Cloudflare 提供了 Application 功能为服务添加额外的安全验证👇

![](https://img-blog.csdnimg.cn/img_convert/8b868f93e1b9c5446f4c8c4ff3c8b419.png)

这里选择 self-hosted：

![](https://img-blog.csdnimg.cn/img_convert/3b01fe505f6639f29b0d2073336ab149.png)

Subdomain/Domain 和刚刚创建的 Tunnel 服务要保持一致：

![](https://img-blog.csdnimg.cn/img_convert/4a12cbcacb8506943da458024d479306.png)


在 Include 区域选择一个验证规则吧：比如你只想让公司员工访问，完全可以用企业邮箱来进行限制，下面我是拿 gmail 举了个例子！

![](https://img-blog.csdnimg.cn/img_convert/3dab2fe1231410ac9b7ccaedd74207b5.png)

添加成功后，再打开之前的域名，你看，需要使用刚才规则中的邮箱，验证后才能访问了。

![](https://img-blog.csdnimg.cn/img_convert/0109eb72217ddb8fbd4a2ee5032f15d4.png)


## 3. 本地配置

如果没有公网 IP，也可以选择在本地配置。

### 3.1 终端登录

1. 参考上一部分完成 cloudflared 安装后，执行如下指令登录：

```
cloudflared tunnel login
```

输入命令后，终端会给出一个登陆地址，我们拷贝到浏览器里面打开，选择需要授权的域名。

![](https://img-blog.csdnimg.cn/img_convert/039f1f947fcf000696bf889466ee615c.png)

看到如下界面，代表授权成功。

![](https://img-blog.csdnimg.cn/img_convert/f795826110711aa76793d0cd7a9d0c44.png)

证书会自动下载到你根目录 `~/.cloudflared` 文件夹下。

但是如果未下载成功，需手动复制下方链接到浏览器，下载证书，然后把内容复制到 `~/.cloudflared/cert.pem` 中。

![](https://img-blog.csdnimg.cn/img_convert/55a69a49e697053f2a4b9c60db78044a.png)


### 3.2 创建隧道

```
# cloudflared tunnel create <你的隧道名字>
cloudflared tunnel create cvlab
```

搞定后，会返回一个隧道 id，这个 id 后面配置的时候会经常用到。
```
Tunnel credentials written to /home/xxx/.cloudflared/14c1b535-78f5-4291-8e0e-0598020c98ea.json. cloudflared chose this file based on where your origin certificate was found. Keep this file secret. To revoke these credentials, delete the tunnel.

Created tunnel cvlab with id 14c1b535-78f5-4291-8e0e-0598020c98ea
```

再回到 Tunnel 主页，可以看到隧道已经加进来了。

![](https://img-blog.csdnimg.cn/img_convert/4ab999b6ce3946e60750c1b69a16d7b1.png)

### 3.3 创建域名

搞定隧道，我们就可以创建内网转发域名了:

```
# cloudflared tunnel route dns <隧道名字> <域名>
cloudflared tunnel route dns cvlab cv.houge.us.kg
```

添加成功后，回到你的域名 DNS 记录表，可以看到新增了一条 DNS 记录：

![](https://img-blog.csdnimg.cn/img_convert/63688a0f7d3a196ac02daaab129becdb.png)

### 3.4 配置 Config 文件

添加好想要穿透的域名后，我们就可以开始映射了。

```
tunnel: <隧道 id>
credentials-file: /home/xxx/.cloudflared/<隧道 id>.json
protocol: h2mux
ingress:
  # 第一个网站，连接到本地的7860端口
  - hostname: cv.houge.us.kg
    service: http://localhost:7860
  - service: http_status:404
```
注：最后的 `- service: http_status:404` 一定要加，这是兜底的规则。

如果需要更多的协议支持，可以查看 cloudflare [官方文档](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/local/local-management/ingress/#supported-protocols)。

配置完以后，可以测试下配置文件是否有问题。

```
cloudflared tunnel ingress validate
```

再测试下单条映射是否命中：

```
cloudflared tunnel ingress rule https://cv.houge.us.kg
```

如果没问题，一切妥当，我们开启服务：

```
cloudflared --loglevel debug --transport-loglevel warn --config ~/.cloudflared/config.yml tunnel run 14c1b535-78f5-4291-8e0e-0598020c98ea
```

再回到 Tunnels 主页，就可以看到刚刚新建的 Tunnel 状态已变成 `Healthy`。

浏览器打开：`https://cv.houge.us.kg`，穿透成功！

![](https://img-blog.csdnimg.cn/img_convert/38fd4c2086dbd743528fcbfbbca6bb80.png)

测试成功后，ctrl+c 退出测试，刚才启动的服务会被停掉。

### 3.5 创建系统服务

为了让服务稳定运行，我们需要把 Cloudflared 注册成系统服务。

```
# 首先需要把 config.yml 复制到 /etc/cloudflared/
sudo cp ~/.cloudflared/config.yml /etc/cloudflared/
# 服务启动
sudo cloudflared service install
# 系统重启，自动启动，反过来 disable
sudo systemctl enable cloudflared 
# 查看服务状态
sudo systemctl status cloudflared
```

![](https://img-blog.csdnimg.cn/img_convert/50d0eb2792348396ce54931624a0c053.png)

如果修改了配置文件`/etc/cloudflared/config.yml`，需要重启服务：

```
sudo systemctl restart cloudflared
```

如果想停止服务：

```
sudo systemctl stop cloudflared
```

### 3.6 迁移到网页端

回到 Tunnel 主页，它会提示你：是否需要迁移到网页端控制面板。

![](https://img-blog.csdnimg.cn/img_convert/30bcfae5aa8c52b714b78950f73cb4da.png)

注意：一旦迁移成功，无法取消。后面也可以直接在网页端直接配置，比如添加一个服务。

![](https://img-blog.csdnimg.cn/img_convert/a94b534eecdf0da117137fe7697987ae.png)


### 3.7 配置嫌麻烦？-开启临时隧道

上面的配置实在太麻烦~

如果你只是想临时用一下，有没有更简单的方法？

有的，`开启临时隧道`！

参考之前的教程：[FLUX.1 实测，堪比 Midjourney 的开源 AI 绘画模型，无需本地显卡，带你免费实战](https://blog.csdn.net/u010522887/article/details/140977067)

用 cloudflared 开启一个监听隧道：

```
cloudflared tunnel --url http://127.0.0.1:8188
```

它会返回一个临时的 url，点击即可访问，只是不能一直有效！

## 写在最后

本文是`白嫖 Cloudflare 系列`教程之一：又一个免费的内网穿透方案，搞定！

除了支持 http 服务之外，Tunnel 还支持 RDP、SSH 等协议转发，有待继续探索。

作为一款免费的服务，配置简单，非常适合小白玩家尝试。

不过，因为用的 Cloudflare 自家 CDN，在国内访问有可能受限（暂时还没发现）。

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

你学会了吗？有任何问题欢迎通过公众号找到我，一起打怪升级。
