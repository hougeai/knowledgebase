前几天，和大家分享了：

[玩转云服务：Oracle Cloud甲骨文永久免费云服务器注册及配置指南](https://blog.csdn.net/u010522887/article/details/140223094)

相信很多同学都卡在了这一步：
```
可用性域 AD-1 中配置 VM.Standard.E2.1.Micro 的容量不足。请在其他可用性域中创建实例，或稍后重试。
```

永久免费的云服务器没搞到，只好申领一台付费的。

不过，慷慨的海外云厂商还有很多，比如微软Azure、亚马逊AWS等。但对比了一圈后发现，原来**最良心的竟然是谷歌云**（Google Cloud，GCP）：
> 2023 年 9 月 谷歌云就宣布每月免费 200 GB 标准层互联网数据传输。这 200G 配合上 **永久免费** 的实例，可香否？

本次分享，就带着大家在谷歌云上，跑通账号注册，申请一台虚拟机实例，完成服务器配置，体验谷歌的永久免费云服务。

# 1.有哪些限制条件？
身为云服务器行业翘楚，谷歌云（GCP）的免费体验活动还是相当慷慨的，新用户注册会有 300 赠金，免费使用 90 天。

90天后呢？

赠金使用完 or 90天到期后，只要升级为付费账号（需要一张外币信用卡），依然可以白嫖每月 200GB 流量的服务器，**只要你不过它的免费限额，就无需付费**。看下图：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b2db463266fae292a34bc1181d0fd44a.png)

更多免费计划详情可参考官方文档：[Google Cloud 免费计划](https://cloud.google.com/free/docs/free-cloud-features?hl=zh-cn#free-tier-usage-limits)

接下来，给大家划个重点，有关虚拟机计算实例，具体有哪些限制条件：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a6f0114f054d2793fa9990b3397ea50a.png)

- 地区限制：在美国的以下区域俄勒冈、爱荷华、南卡罗来纳；
- 磁盘限制：30 GB 标准永久性磁盘
- 流量限制：每月 1 GB 网络出站流量（不包括中国和澳大利亚）

1 GB 够干啥？送了等于没送啊~ 不过，好消息是谷歌云在 2023 年 9 月官方博客宣布：“每月 200 GB 免费标准层互联网数据传输”。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f2f8d24434797084f63051b3b17d4f6e.png)

特别注意：这 200GB 限制标准层的互联网数据。当你创建实例的时候，其中网络设置默认选择的是~~高级网络~~。如果你要用这个每月 200GB，一定要注意将网络改变**标准层级**。

接下来，带着大家来实操一番。

# 2.服务器创建

首先你需要注册一个谷歌云账号，然后进入控制台：
> 传送门：[https://console.cloud.google.com/](https://console.cloud.google.com/)

在控制台首页：创建虚拟机：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b02eb27c6a79c622f51841e82a7cae28.png)

1. 地区选择：选择美国的以下区域（俄勒冈、爱荷华、南卡罗来纳），任一均可

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/281283d2e28936bdce268565f91738cb.png)

2. 机器配置：选择 通用-E2-e2-micro

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/33fd47f62abe30cb26484c31fcc6e8b0.png)

3. 启动磁盘：更改为标准永久性磁盘，30GB，这是谷歌给你的免费额度；操作系统默认是是 Debian，可根据需要进行更换。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6dc6c5dfed384ea1490d40e944333b90.png)

4. 网络设置：依次找到：高级选项->网络->网络接口，点击 default 接口下拉菜单，将网络服务层级从**高级**改为**标准**，可看到提示：每个区域每月可免费传输 200 GB 数据。


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/00fd6a257e09206949a6f9b38fa0de78.png)

5. 确认上述信息没问题后，点击底部`创建`，稍等片刻，你的专属永久免费云服务器就部署成功了。


# 3.服务器配置

接下来，我们介绍一些常见配置，方便日常使用。

## 3.1 如何查看账单

对于`将白嫖进行到底`的你来说，首次创建实例，最重要的当然是`账单`了。

在创建的实例首页-查看结算报告：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/5eaba94919479648a695acca145e408e.png)

当然也可以在控制台左上角，点击`结算`：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/4887888a4ef5fd9cc7c12913e1ce985c.png)

如果是首次创建实例，费用需要等到第二天才能显示。账单中正数代笔实际消费金额，负数为赠送的金额，如果总费用是负数，就不用担心了。

如果你还是不放心你的账单，可以设置预算报警通知，以便及时止损。在结算页面中，找到预算和提醒，创建预算。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a4dd82baea7e2787e02af76e0af643eb.png)

填写预算名称后，这里金额填入 0 即可。也就是达到 0 金额就发送报警通知到你的邮箱。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/0a2814ebb614e9eb62cfef15089f343c.png)

## 3.2 如何设置防火墙
在你的实例首页下面，可以看到`设置防火墙规则`，点击进去。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/7f2de97284f2ef7547a6fd89b7cce866.png)

然后，创建防火墙规则：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e465669e92ff10f87001e536d7b5dbfb.png)

参考如下填写防火墙规则：其中协议和端口，可以选择全部，也可以根据需要放行的端口进行设置。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c477998a9b3eda9c7897f6edcf2eaaa1.png)

接下来，我们一起连接到服务器实例，干点有意思的~ 🤫

# 4.服务器登录

谷歌云实例，支持在浏览器采用 ssh 远程连接：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e1d0e13fb518f879c3f1154b16399c8d.png)


唯一的缺陷是打开时间比较长，如果你的网络不稳定，很容易掉线，需要重新登录。

有没有一劳永逸的登录方法？

答：本地电脑终端 ssh 登录。

**方式一：密钥登陆**

首先，需要**生成 SSH 密钥**(如果已有，可忽略)。不知道如何生成的小伙伴可以参考：[【保姆级教程】Windows 远程登陆 Linux 服务器的两种方式：SSH + VS Code，开发必备](https://blog.csdn.net/u010522887/article/details/138187926)

生成的密钥文件 .ssh 文件夹一般保存在 C 盘，比如我的是 `C:\Users\12243\.ssh`，文件夹下 id_rsa 是私钥，id_rsa.pub 是公钥。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/956f6482546f3d99ba2de6c9f25b5857.png)


然后，将 ssh 公钥复制到你的根目录下 `.ssh/authorized_keys` 中。

此外，还需要在 ssh 配置文件中，将公钥进行身份验证的选项打开。配置文件通常是`/etc/ssh/sshd_config`，

```
PubkeyAuthentication yes
PasswordAuthentication yes
KbdInteractiveAuthentication yes
```

修改后，记得重启 ssh 服务：

```
sudo systemctl restart sshd
```

接下来，再尝试下在你的本地终端 ssh 连接！

当然，也可以选择将你的公钥上传到：元数据 - SSH 密钥中。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/4400129231124ea5a6628748899cc4e6.png)

**方式二：密码登陆**

打开浏览器终端后，默认是有 root 权限的，可以修改你的账号密码：

```
sudo passwd your_name
```
然后再采用 ssh 登陆时，输入密码即可。

# 5.常用软件安装

## 5.1 安装宝塔面板
我们先给这台服务器，安装上宝塔面板，方便后续使用和运维。

以我们默认安装的 Debian 系统为例，安装脚本如下：

```
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```


如果遇到以下报错：

```
当前主机名hostname为空无法安装宝塔面板，请咨询服务器运营商设置好hostname后再重新安装
```
说明找不到主机名，此时去实例主页中找到外部 IP 地址：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c543a85da979526a658e95411538aaaa.png)

然后，在终端中设置主机名为外部 IP 地址：
```
sudo hostnamectl set-hostname <your_ip>
```

再重新执行安装命令，安装成功后，提示如下：

```
=============注意：首次打开面板浏览器将提示不安全=================

 请选择以下其中一种方式解决不安全提醒
 1、下载证书，地址：https://dg2.bt.cn/ssl/baota_root.pfx，双击安装,密码【www.bt.cn】
 2、点击【高级】-【继续访问】或【接受风险并继续】访问
 教程：https://www.bt.cn/bbs/thread-117246-1-1.html
 mac用户请下载使用此证书：https://dg2.bt.cn/ssl/mac.crt

========================面板账户登录信息==========================

 【云服务器】请在安全组放行 38665 端口
 外网面板地址: https://35.xxx.xxx.6:38665/9d5eec02
 内网面板地址: https://10.138.0.2:38665/9d5eec02
 username: nh9aneyp
 password: xxx

 浏览器访问以下链接，添加宝塔客服
 https://www.bt.cn/new/wechat_customer
==================================================================
```


确认防火墙中端口已经放开，即可访问宝塔面板:

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/aae786e0d6ef717c5e477b490ae455a5.png)

可以看到你的机器基本信息。


## 5.2 安装 docker
有了宝塔面板，顺手装个 docker：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f42676136185dc8117718029316f5af7.png)

安装成功后，在终端进行检查，返回版本号说明安装成功。

有了 docker 这款利器，你可以玩的就可多了，比如：
- [OneAPI-接口管理和分发神器：所有大模型一键封装成OpenAI协议](https://zhuanlan.zhihu.com/p/707769192)
- [【保姆级教程】免费内网穿透，手把手搭建，三步搞定](https://blog.csdn.net/u010522887/article/details/140761164)

感兴趣的小伙伴赶紧去试试吧~

# 写在最后
**切记**：免费 200GB 流量只能用于标准层互联网数据传输，也就意味着不要走 Cloudflare 等 cdn 服务，这个是需要收费的。

同时，也要关注谷歌云公布的消息，官方可没给出永久免费承诺啊，本号也将持续关注并同步给大家。

如果本文对你有帮助，欢迎**点赞收藏**备用！

