
现在家里各种品牌的电器都带智能联网，但各自为政——

小米、海尔、美的各管各，还都配了个语音助手：小爱、小优、小美……

智能生活没体验到，APP 倒是装了七八个。

如果你也受够了这种割裂，请花一个周末，跟我用 Home Assistant，搭建一个真正的全屋智能中枢。

## 1. Home Assistant

> 开源地址：https://github.com/home-assistant/core

**Home Assistant（HA）** 是一个开源的智能家居平台，它的核心能力是：

✅ **跨品牌整合**：米家、海尔、美的...统统接入  
✅ **本地控制**：断网也能用，响应速度 < 100ms  
✅ **高度自定义**：自动化、场景联动，想怎么玩就怎么玩  
✅ **API 开放**：提供完整的 REST API，可以对接自己的平台

比如，我的设备：

- 小米智能摄像机 3 3K
- 米家净水器 1000G Plus
- 小米智能插座 × 3
- Yeelight 智能灯 × 5
- 海尔空调 × 2

**全部接入 HA 后**，小爱、小优、小美也不用再吵架了，统一由 HA 调度。

---

## 2. 快速安装

### 2.1 前置要求

**硬件（三选一）**

| 方案           | 推荐      | 说明                                                             |
| -------------- | --------- | ---------------------------------------------------------------- |
| 树莓派 4B/5    | ⭐ 最推荐 | 功耗 5W，24 小时开机无压力，二手 200 出头                        |
| 闲置小主机     | 性能党    | N100 迷你主机，能顺手跑 NAS/青龙                                 |
| 旧手机刷 Linux | 折腾党    | PostmarketOS/Linux Deploy 可跑 Docker，但设备兼容性有限，需 root |

> 旧手机方案：Termux 不行——Android 内核缺 cgroups/namespace，Docker daemon 起不来。

首推树莓派等Arm开发板，功耗低，24 小时开机无压力。比如我手头这块：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ef642f147ee04d258dc69fddf0d0e938.png)

**软件**

- Docker（[保姆级教程](https://zhuanlan.zhihu.com/p/690038228)）
- 能连上路由器的网络

**注：**

- HA 容器用 `host` 网络模式——mDNS 设备发现、Wake-on-LAN 等功能依赖它
- 树莓派需 32G 以上的 SD 卡，建议用 A2 级别，否则写入慢影响体验

### 2.2 Docker 安装 HA

HA 支持多种安装方式，推荐 **Docker 安装**（最灵活）：

```bash
# 1. 创建安装目录
mkdir -p ~/homeassistant && cd ~/homeassistant
```

```bash
# 2. 创建 docker-compose.yml
services:
  homeassistant:
    container_name: homeassistant
    image: ghcr.io/home-assistant/home-assistant:stable
    network_mode: host  # 关键：同局域网发现智能家居设备
    volumes:
      - ./config:/config
      - ./data:/data
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro  # 可选：支持蓝牙
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
    privileged: true
```

```bash
# 3. 启动
docker compose up -d
```

启动成功后，HA 会自动生成配置文件等，目录结构如下：

```
~/homeassistant/
└── config/
    ├── configuration.yaml    # 主配置文件（核心，后面要改）
    ├── automations.yaml      # 自动化规则
    ├── scripts.yaml          # 脚本
    ├── scenes.yaml           # 场景
    ├── secrets.yaml          # 敏感信息（密码等）
    ├── home-assistant.log    # 运行日志（排查问题看这里）
    ├── home-assistant_v2.db  # 状态历史数据库（SQLite）
    ├── .storage/             # HA 内部数据（UI 配置、设备注册表等，别改）
    ├── deps/                 # Python 依赖缓存
    ├── tts/                  # 语音合成缓存
    └── custom_components/    # 自定义组件（后面装 HACS 会创建）
```

在主机上执行：

```bash
# 树莓派
hostname -I
# 输出类似：192.168.1.100 172.17.0.1，第一个就是局域网 IP
```

等待 3-5 分钟后访问：`http://主机IP:8123`，打开 HA 前端控制台。

如果 8123 端口被占用，可修改 `~/homeassistant/config/configuration.yaml`：

```yaml
http:
  server_port: 8124 # ✅ 改成 8123 以外的任意空闲端口
```

### 2.3 首次配置指南

浏览器打开 `http://主机IP:8123`，首次访问会进入引导向导，跟着走就行：

**第 1 步：欢迎页**

直接点"创建我的智能家居"，不用管其他选项。

外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传

**第 2 步：创建管理员账号**

> 这个账号是 HA 的超级管理员，后续管理设备、装插件都用它登录。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f36d35d967f3493eaa966e89e9cd9557.png)


**第 3 步：设置位置**

在地图上搜索你家地址，拖动标记点到准确位置。这一步别跳过——后面要用到：

- **天气**：HA 会根据位置自动拉当地天气
- **日出日落**：自动化场景常用，比如"日落自动开灯"
- **时区**：自动根据位置推断

**第 4 步：完成**

点完成后会进入 HA 主界面，此时设备列表是空的。

![](https://i-blog.csdnimg.cn/img_convert/88407cac95dc1a9c5911d1d53d8d4593.png)

> 如果访问 `http://主机IP:8123` 打不开，检查：
>
> 1. 电脑和主机是否在同一个 WiFi/局域网
> 2. 主机防火墙是否放行 8123 端口（树莓派默认不拦，小主机可能要手动放）

### 2.4 安装扩展：官方集成 + HACS 社区商店

HA 接入设备/服务靠"集成（Integration）"，分两类：

| 类型     | 来源                       | 例子                            | 是否预装        |
| -------- | -------------------------- | ------------------------------- | --------------- |
| 官方集成 | HA 自带，2000+ 个          | Electricity Maps、HomeKit、MQTT | ✅ 装完 HA 就有 |
| 社区集成 | 第三方开发，需通过 HACS 装 | Xiaomi Miot（米家本地控制）     | ❌ 要手动装     |

**官方集成**直接在"添加集成"里搜就有，不用额外操作。

以 **Electricity Maps** 为例——

它能实时获取你所在电网的碳排放强度和化石燃料占比，让智能家居「知道电网现在有多脏」，从而自动选择低碳时段运行高耗电设备：

- 午间光伏出力高峰，电网碳排放低 → 空调、洗衣机大胆开
- 检测到电网当前碳强度高 → 洗碗机等非 urgent 设备延后到低碳时段

如何安装？

设置 → 设备与服务 → 添加集成 → 搜 "Electricity Maps" → 填 API Key → 选区域（中国大陆选 `CN`），完成。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cfd11ed6047846b8afe7e13e4d12bfb0.png)


API Key 去 [Electricity Maps 开发者平台](https://app.electricitymaps.com/developer-hub) 注册获取——邮箱注册即可，无需密码，用 Token 鉴权，免费额度够个人用。

**社区集成**要先装 HACS（Home Assistant Community Store）——它相当于 HA 的"应用商店"，装完才能一键安装社区开发的插件。

#### 安装 HACS

```bash
# 进入 HA 配置目录
cd ~/homeassistant/config

# 创建 custom_components 目录（没有的话）
mkdir -p custom_components

# 下载 HACS 并解压
wget -O hacs.zip https://github.com/hacs/integration/releases/latest/download/hacs.zip
unzip hacs.zip -d custom_components/hacs

# 重启 HA
docker restart homeassistant
```

重启后回到 HA 界面：设置 → 设备与服务 → 添加集成 → 搜 "HACS" → 按提示绑定 GitHub 账号（只需一个 GitHub 账号，不用创建仓库），等待初始化完成（首次可能需 1-2 分钟）。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1b52e679fa9241c08314e28b33ed9034.png)

进入全部勾选，点击提交。

![](https://i-blog.csdnimg.cn/img_convert/0e5bf57f501215dcdba898087bf19101.png)

安装完成，左侧导航栏就会多一个HACS。

> HACS 本身不是插件，是"插件商店"。装完它，后面才能在 HACS 里搜索安装 Xiaomi Miot 这类社区插件。

## 3. 接入各品牌设备

### 3.1 米家设备

通过 HACS 安装 Xiaomi Miot。

重点：不要用官方集成！用社区的 Xiaomi Miot，支持本地控制。

```
HA 界面 → HACS → Integrations → 搜索 "Xiaomi Miot" → 下载安装 → 重启
```

![](https://i-blog.csdnimg.cn/img_convert/9784f20a1fee3de6985a6970bbea3034.png)

重启后，同样需要添加集成，流程如下：

```
设置 → 设备与服务 → 添加集成 → 搜索 "Xiaomi Miot" →
```

注意，要选择 "Add devices using Mi Account" → 输入小米ID和密码（来自米家APP）

![](https://i-blog.csdnimg.cn/img_convert/d7b03802074458499ca4b94a19b9474b.png)

> 核心误区澄清：很多人以为“账号集成 = 纯云端控制”，这是错的。Xiaomi Miot 插件的账号登录仅用于自动发现设备 + 自动提取 Token + 建立设备映射。添加完成后，控制指令默认优先走局域网直连，不经过小米云服务器。

登录过程中，如果跳转到新链接获取验证码，验证码要回填在本页面，不是链接打开的页面：

![](https://i-blog.csdnimg.cn/img_convert/4ffb001a130db5b5e21c846f6946840b.png)

筛选设备：
![](https://i-blog.csdnimg.cn/img_convert/a595011b4108054701abcec010fc85b8.png)

添加完成，即可在首页看到加载进来的全部小米设备。

### 3.2 海尔设备

**别装错插件**：HACS 搜索 "haier" 可能先看到 [gvigroux/hon](https://github.com/gvigroux/hon)，那个只支持海外的 hOn 平台，国内海尔登不上。

![](https://i-blog.csdnimg.cn/img_convert/ecf134d3576554defff8106c440440c6.png)

国内海尔走海尔智家 APP（U+ 平台），用这个插件：[banto6/haier](https://github.com/banto6/haier)（1100+ star，活跃维护）

**支持设备**：空调、洗衣机、热水器等海尔智家 APP 里能看到的设备（覆盖 switch/climate/sensor/select 等实体类型）

**安装**：

1. HACS → 自定义仓库 → 添加 `https://github.com/banto6/haier`

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/01d95aca57594f7e96df378273de9796.png)


安装 → 重启 HA，然后点击：设置 → 设备与服务 → 添加集成 → 搜 "Haier"

![](https://i-blog.csdnimg.cn/img_convert/0a04c6120d379a02918a448c48112eb7.png)

海尔授权不是用账号密码，而是通过令牌验证。

因此需要抓包工具获取上图中的 client Id 和 refresh token。

> 抓包工具我放在文末，需要的朋友自取。

首先打开抓包工具`Reqable`，

然后微信搜索小程序 “海尔智家官方”，进去登录：

![](https://i-blog.csdnimg.cn/img_convert/a8b4507f83f8c6977bc2e3564c2fcba1.png)

在抓包工具中搜索 login 请求：

![](https://i-blog.csdnimg.cn/img_convert/baa20ccd62914c4e523f0b0f4786c7fb.png)

下方响应体中找到：

```
"refreshToken": "db4aa0a99e96419d83b5722dcd",
"clientId": "WindowsUnknownx64178185",
```

填入账号设置并提交，即可添加海尔集成：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3943c80f27054204981a0e388b4f0d95.png)

### 3.3 美的设备

美的设备可以通过官方插件进行集成。直接在 HACS 中搜索 "midea" 即可找到。

![](https://i-blog.csdnimg.cn/img_convert/cccbd2edd2fd6fa349ee18eb16036d3c.png)

**安装**重启，然后点击：设置 → 设备与服务 → 添加集成 → 搜 "Midea"

登录成功后，需要逐一添加设备。

### 3.4 海信设备

海信走 ConnectLife（聚好连）平台，有官方插件。直接在 HACS 中搜索 "hisense"：

> ConnectLife 就是为海信智能家电做的云平台 + App

![](https://i-blog.csdnimg.cn/img_convert/3f1caca32a1962a73c9908c368bbf947.png)

**支持设备**：空调、除湿机、热泵、水暖等品类（电视、冰箱、洗衣机不在列）

**安装**重启，然后点击：设置 → 设备与服务 → 添加集成 → 用 ConnectLife 账号登录

### 3.5 格力设备

格力是国产品牌里少数有 HA **官方核心内置集成**、且走**纯局域网**控制的方案，不用 HACS、不用登云账号。

> 集成名：`Gree Climate`，从 HA 0.117 起内置。通信方式为 Local Polling，不走云端。

**配网前提**：空调要先下载 **格力+** App 把 WiFi 配好，让空调接进你局域网。配网完 App 可卸载，集成本身不需要登账号。

**安装**：设置 → 设备与服务 → 添加集成 → 搜 `Gree Climate` → 自动发现或手动填空调 IP
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/df2fe9999c944357b721a63502d0472a.png)

**暴露的实体**：

| 实体     | 类型    | 功能                                                             |
| -------- | ------- | ---------------------------------------------------------------- |
| Climate  | climate | 开关机、目标温度、HVAC 模式、风速、摆风、预设（Away = 8°C 制热） |
| 面板灯   | switch  | 控制前面板灯光                                                   |
| 静音模式 | switch  | 开关静音                                                         |

![](https://i-blog.csdnimg.cn/img_convert/b9a77c31e36004d78c300df172eb9e00.png)

### 3.6 接入特斯拉

除了各品牌家电，如果你是**特斯拉**车主，HA 还可以通过 MQTT 接入你的**车机数据**。

完整的联动只需4步：

**第 1 步：部署 MQTT Broker（搭建传话筒）**

先在 Docker 环境里跑一个 MQTT 服务器（最常用、最轻量的是 Eclipse Mosquitto）。
- 作用：数据中转站。TeslaMate 把数据扔给它，HA 从它拿数据。

**第 2 步：Docker 部署 TeslaMate（启动数据源）**

详情可参考：[特斯拉车主都在偷偷用的开源工具，电池衰减、充电成本一目了然](https://mp.weixin.qq.com/s/ro5SF2e0On-6phRBOrg-RQ)
- 作用：TeslaMate 从特斯拉云端拉取车辆数据，然后发布到 MQTT 服务器里。

**第 3 步：在 HA 中配置原生 MQTT 集成（打通底层通道）**

在 HA 的“设置 -> 设备与服务 -> 添加集成”里，搜索并添加 HA 自带的官方 MQTT 集成，填入你的 MQTT Broker 地址。
- 作用：让 HA 连上这个“传话筒”，打通底层的通信通道。

**第 4 步：在 HA 中安装 TeslaMate 集成（一键生成实体）**

通过 HACS 下载并安装 TeslaMate 集成，重启 HA 后添加该集成。
- 作用：这个集成会自动去 MQTT 里监听 `teslamate/cars/...` 开头的主题，并在 HA 里生成上百个实体（电量、温度、位置、车门状态等），完全不需要手写 YAML 代码。

## 4. 远程访问与手机 APP

到这步为止，你的 HA 只能在家里 Wi-Fi 下访问。一出门就失联——远程开个空调都做不到。

这章解决两件事：**从公网访问 HA**，以及**让手机 App 内外网自动切换**。

### 4.1 内网穿透

HA 默认只监听局域网。从外网访问需要把它"暴露"出去，常见方案对比如下：

| 方案                      | 难度        | 是否需公网 IP          | 月费           | 适合谁                                             |
| ------------------------- | ----------- | ---------------------- | -------------- | -------------------------------------------------- |
| **Nabu Casa**（HA Cloud） | ⭐ 零配置   | ❌ 不需要              | $6.5/月        | 怕折腾、想要官方支持的人                           |
| **Cloudflare Tunnel**     | ⭐⭐ 简单   | ❌ 不需要              | 免费           | 有自己域名、想白嫖的人                             |
| **Tailscale**             | ⭐⭐ 简单   | ❌ 不需要              | 免费（个人版） | 只给自己/家人用、不在乎公网可访问                  |
| **frp**                   | ⭐⭐⭐ 中等 | ❌（但需一台公网 VPS） | VPS 费用       | 手里有 VPS、想完全自主可控、不想依赖第三方服务的人 |

#### Cloudflare Tunnel（免费，推荐）

适合有自己域名的用户。不需要公网 IP，不需要开端口，Cloudflare 边缘节点回源到你家 HA：

```bash
# 1. 在 Cloudflare 控制台创建 Tunnel，拿到 token
# 2. 用官方镜像跑 cloudflared，token 替换成你自己的
docker run -d --name cloudflared --restart unless-stopped \
  cloudflare/cloudflared:latest tunnel --no-autoupdate run --token YOUR_TOKEN
```

然后在 Cloudflare 控制台的 Public Hostname 页面把 `ha.yourdomain.com` 指向 `http://HA的内网IP:8123`，访问 `https://ha.yourdomain.com` 即可。

详细教程可参考：[【白嫖 Cloudflare】之 免费内网穿透，让本地AI服务，触达全球](https://zhuanlan.zhihu.com/p/716891964)

#### frp（适合有 VPS 的玩家）

经典内网穿透工具，需要一台带公网 IP 的服务器当中转。好处是**完全自主可控**，不依赖 Cloudflare/Tailscale 的服务条款。

详细教程可参考：[86K Star！又一款内网穿透利器，开源免费+小白友好](https://zhuanlan.zhihu.com/p/6970357613)

### 4.2 手机 APP

HA 官方有个 App，**装上之后比网页版强一大截**：

- 能用手机传感器（GPS、电量、运动状态）做自动化触发
- 接管通知通道，HA 推送直接进系统通知栏
- 集成 Android Auto / CarPlay / Apple Watch / Wear OS
- **关键：支持内外网自动切换**

#### 下载

| 平台    | 渠道                                                                  |
| ------- | --------------------------------------------------------------------- |
| iOS     | App Store 搜 "Home Assistant"                                         |
| Android | 国内可去 GitHub Releases 下 APK                                       |

源码：
- https://github.com/home-assistant/iOS
- https://github.com/home-assistant/android

#### 内外网自动切换

这是手机 App 的核心体验。配好后在家走内网 IP（响应快、不走流量），出门自动切外网域名，全程无感。

**第一步**：HA 后端允许代理转发（`configuration.yaml`）。

> **注：只在用了反向代理（改 HTTP 头）时才需要**。判断标准：你前面那层是 Nginx/Caddy/cloudflared → 需要；frp 纯 TCP 转发、Nabu Casa、Tailscale → 不需要。

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1 # 本机反代（比如 Nginx 跑在 HA 同一台机器）
    - ::1       # IPv6 的 localhost
    - 172.16.0.0/12 # Docker 容器网段，见下方说明
```

`172.16.0.0/12`：如果用 Docker 跑 cloudflared / Nginx / Caddy，这些容器会拿到一个 Docker 分配的内网 IP。想确认 Docker 容器实际用哪个网段：执行 `docker network inspect bridge | grep Subnet`

**为什么要把代理 IP 写进 trusted_proxies**：`X-Forwarded-For` 是个 HTTP 头，**任何人都能伪造**。HA 的安全设计是——"只有来自白名单里这些 IP 的请求，我才信它带的 `X-Forwarded-For`"。否则攻击者伪造一个 `X-Forwarded-For: 127.0.0.1` 就能假装内网请求绕过登录。把代理 IP 写进白名单，意思就是"只信我自己部署的反代，别人伪造的头一概不认"。


**这步的作用**：反向代理（Nginx/Caddy/cloudflared）会把真实客户端 IP 塞进 `X-Forwarded-For` 请求头。HA 默认不读这个头，只看 TCP 连接来源（也就是代理自己的 IP）。配上之后 HA 才会去读这个头，拿到真实客户端 IP。


**第二步**：App 里填两个地址

打开 App → 设置 → 连接（Connection）：

![](https://i-blog.csdnimg.cn/img_convert/918e52c60b00cec89695579be2b96f08.png)                         

App 会自动判断当前 Wi-Fi：连上家里 Wi-Fi 时用内网地址，否则用外网地址。

**记得开启 App 的位置权限**，不然 App 不知道啥时候算"在家"。

至此，无论是在家还是外出，都能通过手机控制全部家庭设备了。

## 5. 自动化

前面把设备都接进来了，只是"能用"。

**自动化的意义在于：让设备自己知道什么时候该干什么**

不用掏手机、不用喊语音助手，家里的事自己就办了。

HA 自动化的核心结构是三段式：

```
触发器 (Trigger)  →  条件 (Condition)  →  动作 (Action)
什么时候开始       满足什么条件才执行     具体做什么
```

- **触发器**：必须有。可以是状态变化、时间到、太阳升落、人进入区域等
- **条件**：可选。比如"只在晚上""只在工作日""只在家时"
- **动作**：必须有。调用服务，比如开灯、关窗帘、发通知

入口：设置 → 自动化与场景 → 自动化 → 右下角"+"创建。

略举两例：

### 5.1 回家自动开灯

**场景**：晚上回家，手机连上家里 Wi-Fi（或进入家区域），玄关灯自动亮起，30 秒后自动关。

#### 前置条件

- 手机装了 HA App，并授予系统级位置权限
- 装上 App 后 HA 会**自动生成**一个 `device_tracker.你的手机名` 实体，状态为 `home` / `not_home`；

如何查看：设置 -> 开发者工具 -> 状态 -> 搜索 `device_tracker`：

![](https://i-blog.csdnimg.cn/img_convert/6c0cfc2d4cce2d70777cc0f99be8d382.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/271240dfd5464cf59e86a07f2119e74a.png)

#### UI 编辑器配置

在哪配置：设置 → 自动化与场景 → 自动化 → 右下角"+"按钮。

![](https://i-blog.csdnimg.cn/img_convert/2678a57229b18577d0fe99ad1d486bfc.png)

页面分三块（触发器 / 条件 / 动作），每块点"添加"按钮选择类型再填参数。

| 字段 | 填什么 |
|------|--------|
| **触发器** | 添加触发器 → 选"实体" → 状态 `device_tracker.my_phone` → 属性从 `not_home` 变成 `home` |
| **条件** | 添加条件 → 选"太阳" → 选"之后：日落" |
| **动作** | 添加动作 → 选"灯光" → 打开灯光 → 添加目标 |

![](https://i-blog.csdnimg.cn/img_convert/6798630d16bb902a8713fc7796ae185c.png)

填完"保存"，在自动化列表就可以看到记录，右侧点击"运行动作"，测试一下看看。

![](https://i-blog.csdnimg.cn/img_convert/0780da2a7df946a1544cb8e4322eb348.png)

这时，在 `config/automations.yaml` 中也可以看到新增的自动化记录：

![](https://i-blog.csdnimg.cn/img_convert/d79065e33792ecb07aa12eb7dadd9725.png)

### 5.2 日落自动关窗帘

**场景**：太阳落山时，自动关闭客厅和卧室窗帘，晚上保护隐私。

#### 前置条件

- HA 已配置地理位置（设置 → 系统 → 通用 → 位置，Sun 集成默认启用）
- 窗帘已接入，生成 `cover.xxx` 实体（米家窗帘电机、杜亚、Aqara 等都支持）
- 假设有 `cover.living_room` 和 `cover.bedroom` 两路

#### UI 编辑器配置

| 字段 | 填什么 |
|------|--------|
| **触发器** | 类型选"日出/日落" → 事件 `sunset` → 偏移 `-00:15:00`（日落前 15 分钟）|
| **条件** | 无，或加"状态： `input_boolean.guest_mode` = off" |
| **动作** | 调用服务 `cover.close_cover` → 目标选两个窗帘实体 |

### 5.3 调试技巧

写完自动化不知道为什么不触发？

**看执行日志**：设置 → 自动化与场景 → 点开具体自动化 → "追踪"标签，能看到每次触发的 trigger/condition/action 执行情况和耗时

![](https://i-blog.csdnimg.cn/img_convert/f57ea0bd41e56e8b2fab95b545162b2d.png)


## 6. API 控制（高阶）

前面讲的自动化、UI、App 都是 HA 内部的能力。

此外，HA 还**对外暴露完整的 REST API**——

你可以拿它对接任何外部系统：自己的后端服务、语音助手、定时脚本、监控系统……

只需三步：拿令牌、调接口、接进自己的平台。

### 6.1 获取长期访问令牌

HA 的 API 用**长期访问令牌**。

**获取步骤**：

```
HA 左下角点你的头像 →  安全 → 拉到底部"长期访问令牌" → "创建令牌"
```

> ⚠️ 令牌**只在创建时显示一次**，务必立刻复制保存。

### 6.2 REST API 调用

所有请求都要带 Header：

```
Authorization: Bearer 你的令牌
Content-Type: application/json
```

API 根地址就是 HA 的访问地址，端口默认 8123。

#### 接口速查表

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/` | 测试 API 是否在线 |
| GET | `/api/states` | 拉取所有实体状态 |
| GET | `/api/states/<entity_id>` | 查单个实体状态 |
| POST | `/api/services/<domain>/<service>` | 调用服务（开灯、关窗帘等）|
| POST | `/api/states/<entity_id>` | 写入状态（只改 HA 内部表示，不控设备）|

> 关键区别：`POST /api/states/xxx` 只改 HA 里的状态记录，不会真正去控设备。控设备必须走 `POST /api/services/<domain>/<service>`，比如 `light.turn_on`。

### 6.3 接入AI

前面是"人写代码调 API"。

但更好玩的是——**把这些 API 封装成 MCP**，岂不是可以让 AI 能"看懂"和"操控"家里设备？

## 写在最后

本文把七八个割裂的 App，收敛成一台 HA，并介绍了 REST API——让 HA 从"自己玩"的中枢，变成能被外部调用的设备后端。

如果对你有帮助，不妨**点赞收藏**备用。

下篇，我们将这套封装到**小智**上，语音指挥 HA 里的所有设备。

