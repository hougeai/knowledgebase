上一篇，带大家分享了：[如何薅一台腾讯云服务器](https://blog.csdn.net/u010522887/article/details/140091900)。

不过，只有一个月免费额度，到期后需要付费使用。

相对而言，海外云厂商更加慷慨一些，比如微软Azure、甲骨文、亚马逊AWS等。

甲骨文2019年9月就推出了永久免费服务，“永久免费”的噱头一经打出，立即引来了不少流量。不过随着国内薅羊毛大军的进驻，注册账号的门槛越来越高。

这两天猴哥又走了一遍注册流程，成功跑通，亲测有效，趁热乎赶紧分享给大家~

本次分享，手把手带领大家在`甲骨文云`上，跑通账号注册流程，申请一台虚拟机实例，完成服务器配置，希望能够帮助大家成功白嫖甲骨文的永久免费云服务。

# 1. 真假‘永久免费’
所谓的永久免费，其实是有很多限制的，**而且你不一定能抢得到哦**。

且看官方是这样描述的：
> Oracle 云免费套餐只需注册 Oracle 云帐户即可获取，不仅包含丰富的 Always Free 云服务，还提供 300 美元的免费试用储值，让您可以在 30 天内免费使用所有适用的 Oracle 云基础设施服务。其中，Always Free 云服务无时长限制，免费试用仅 300 美元免费储值用尽或 30 天到期（以先到者为准）前有效。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a8c8938d6de57ead2f51f2d6a7a6f660.png)

虚拟机资源方面，单个账号可以拥有：
- 2 个基于 AMD 的虚拟机，每个虚拟机配备 1/8 OCPU 和 1 GB 内存
- 基于 Arm 的 Ampere A1 内核和 24 GB 内存，可作为 1 个虚拟机或最多 4 个虚拟机使用，每月有 3000 个 OCPU 小时和 18000 GB 小时。（每个月 24*30 = 720 小时，**意味着你的 4C24G 的 ARM 服务器可以全天候免费在线**）


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d30b4d24aa6c374c1f4613ee67d04c08.png)

存储方面，有 200G 的免费块存储，不得不说甲骨文还是蛮慷慨的~
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c80dfdb6840ae2eccc501cc556c33a30.png)

为了实现最大化利用免费实例，猴哥认为可以采取如下配置：
- 单台 ARM 4C/24GB/200G（性能存储带宽最大化）
- 单台 ARM 4C/24GB/100G + 两台 X86 1C/1G/50G（性能和数量均衡选择）

要使用这些免费资源，首先你得注册一个账号，为了阻止大家薅羊毛，甲骨文设置了重重障碍，很多小伙伴倒在了账号注册的路上。

# 2. Oracle Cloud 账号注册

## 2.1 前置准备
申请 Oracle Cloud 账号的第一道门槛就是如下条件，缺一不可：
- 一个邮箱，有网友提到需要 Gmail 或 hotmail 之类的国外邮箱，不过猴哥亲测 QQ 邮箱也没问题；
- 一个手机号，中国的就行
- 一张支持 Master、VISA 等的外币信用卡
- 魔法上网环境（登录需要）
## 2.2 开始注册
> 注册地址：[https://www.oracle.com/cn/cloud/free/](https://www.oracle.com/cn/cloud/free/)

上述地址，点击立即免费试用，第一个国家/地区下选择中国就行，后面手机号/家庭住址/信用卡都采用国内的地址，名字/姓氏确保和你的信用卡保持一致：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/87e25c053c074f9b2a16e8b05a76f07d.png)

邮箱收到验证邮件后，点击进入注册页面。这里有两点比较重要：
- 密码需要设置的尽可能复杂，因为要命中它的所有规则，否则不容易通过
- 归属区域，注册成功后，以后所有的IP都是在该区且不可更改（**我选择的 Singapore 目前抢不到免费计算资源，大家慎重**）。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e1c0b91b16c23bdee56973d8e20fa828.png)

接下来，填写个人住址，我是采取全英文填写，不知道中文是否影响注册成功：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/96849dd3abef68ce87a7a03d26cb0db5.png)

点击继续后，会让你添加付款验证方式，此时需要填写你的信用卡信息，确保信息和之前的个人信息一致，然后你的信用卡会受到扣款信息，不用担心，后续会撤销的~

一切都搞定后，你会受到注册成功的邮件（**有你的账号信息**），恭喜你，**拿到 Oracle Cloud 永久免费资源的入场券**！

# 3. 计算资源申领

## 3.1 账号登录
> 登录地址：[https://www.oracle.com/cn/cloud/sign-in.html](https://www.oracle.com/cn/cloud/sign-in.html)

输入你的 Cloud 账号名称，点击 下一步，然后输入注册邮箱和密码后，你会看到如下界面，需要你进行验证：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/9122bbc3010b730109f48724a4220736.png)

而这个验证还比较麻烦，需要你下载移动端 APP，名为 Oracle Mobile Authenticator，你会发现国内各大应用商店都找不到。需要到 Google Play 安装，我这里已经把安装包下载好了，在Android手机上直接安装即可。（**需要的小伙伴文末自取**）

## 3.2 虚拟机申请

登录成功后，会提示你有 400 元的免费额度，有效期 30 天，可使用丰富的 OCI 服务，包括 Oracle Database、Analytics、Compute 和 Container Engine for Kubernetes。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/dc45c4728d273f9347d553d996760c83.png)

右上角可以切换语言为中文，在这里我们先创建一台虚拟机实例试试：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e5b0dcc1c4db51244336c8e679df01c7.png)

进来后，默认配置就是永久免费的，右侧点击 `配置` 可以进行手动更改，我们先用默认的申请了试试。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/7ae3b5f838b6dd65a846f955bf8cf6da.png)

接下来，需要 **添加 SSH 密钥**(如果已有，可忽略)。对不了解 SSH 的小伙伴稍有点麻烦，首先，Windows 本地生成SSH密钥对。下载并安装Git for Windows，在Git Bash终端中执行命令 `ssh-keygen` ，这时会在本地 .ssh 文件夹中生成了密钥文件，.ssh 文件夹一般保存在 C 盘，比如我的是` C:\Users\12243\.ssh`，文件夹下 id_rsa 是私钥，id_rsa.pub 是公钥。

当然，你也可以直接在下图的页面中选择 `为我生成密钥对`。

然后把 id_rsa.pub 上传到下图中位置：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/630c88b54fe8b1bed7c3def79b7c3c0e.png)

最后，点击 `创建`，如果出现下图的警示，说明 免费资源 暂时你是薅不到了！（*PS：如果有小伙伴申请到了，欢迎留言告诉我你选择的主区域啊*）

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/95dc62ca3f5ce7b929f7637daf5d390b.png)

羊毛薅不到，那就修改配置，注册一台付费的试试吧，毕竟也给了你 400 元的免费额度，够用一个月了~

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/4983e81aa0ed94cc910461b23662c767.png)

在上述 映像和配置 中进行选择，我这里先搞了一台 1C16G 的，瞬间就分配到了。

# 4. 服务器配置

## 4.1 服务器基本信息

进来后，状态变成正在运行，就可以登陆了。下图红色箭头处是你这台虚拟机的公网 IP，用户名默认为：opc。


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/92e052c9e0a502de2602e6e029c844a1.png)

## 4.2 远程登录

因为我们在新建实例时，已经上传了 SSH 密钥，所以可以直接采用 SSH 登陆。如果选择在 IDE 中远程登录，以 VS Code 为例，远程登录的方式可以参考猴哥之前的这篇教程：

[【保姆级教程】Windows 远程登陆 Linux 服务器的两种方式：SSH + VS Code，开发必备](https://blog.csdn.net/u010522887/article/details/138187926)

这台服务器的 Host 配置为：
```
Host tx
  HostName 129.150.63.184
  Port 22
  User opc
```

成功登陆后，默认是在 `/home/opc` 目录：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e249e924ff3f93429638c9277552c085.png)


## 4.3 常用软件安装

### 4.3.1 安装宝塔面板

先给这台服务器，安装上宝塔面板，方便后续各种操作，极大提升服务器使用和运维效率。

在上一篇，我们申请腾讯云服务器时，新建实例时选择了自带宝塔面板的系统镜像，而 Oracle cloud 上的系统镜像是一个裸的 Linux 镜像，所以我们需要采用如下命令手动安装宝塔面板。
> 安装指南参考：[https://www.kancloud.cn/chudong/bt2017/431320](https://www.kancloud.cn/chudong/bt2017/431320) 
> 
> 安装脚本参考：[https://www.bt.cn/new/btcode.html](https://www.bt.cn/new/btcode.html)

以我默认的 Linux 系统为例，安装脚本如下：
```
wget -O install.sh http://download.bt.cn/install/install-ubuntu_6.0.sh && sudo bash install.sh
```

安装成功后，终端会输入如下信息：

```
Congratulations! Installed successfully!
=============注意：首次打开面板浏览器将提示不安全=================

 请选择以下其中一种方式解决不安全提醒
 1、下载证书，地址：https://dg2.bt.cn/ssl/baota_root.pfx，双击安装,密码【www.bt.cn】
 2、点击【高级】-【继续访问】或【接受风险并继续】访问
 教程：https://www.bt.cn/bbs/thread-117246-1-1.html

========================面板账户登录信息==========================

 【云服务器】请在安全组放行 27153 端口
 外网面板地址: https://129.150.63.184:27153/ac4e837c
 内网面板地址: https://10.0.2.147:27153/ac4e837c
 username: vdgxzlsc
 password: xxx

 浏览器访问以下链接，添加宝塔客服
 https://www.bt.cn/new/wechat_customer
==================================================================
Time consumed: 7 Minute!
```

注意，此时你打开上面的 `外网面板地址` 是无法访问的，还需要放开 27153 端口的入站限制：
点击下图方框处进入子网：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/92e052c9e0a502de2602e6e029c844a1.png)

安全列表第一个点击进去，添加入站规则。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3b937dca6594c9c9a071a57a41ade105.png)

比如我这里要放开宝塔面板的端口号，就可以参考下图填写：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6c3a4e95e5c78fc4671437a32fb873af.png)

解除端口限制后，就可以在浏览器中打开上面的 `外网面板地址` ，输入 `username` 和 `password`。

注意：首次登陆需要绑定下宝塔面板账号，没有的话免费注册一个即可~

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3c4ac45987e37798cb5f8bb840b837c0.png)

登陆成功，首次进入宝塔页面，会有一个插件推荐安装，如果不装，后续也可以在左侧菜单栏的软件商店进行安装：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/60b331a8c2572e864c6b2d0493910814.png)


### 4.3.2 安装 docker
有了宝塔面板，安装 docker 就很方便了。


点击宝塔面板左侧菜单栏的 Docker，首次进入需要安装docker 和 docker-compose。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f7696fc483d13bd392d8b7aeec947c01.png)

注意：为了加快安装速度，安装方式建议选择自定义，然后采用阿里云镜像：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/9408007e6396363a6e0fc9c6120c7929.png)

安装成功后，在终端进行检查，返回版本号说明安装成功：
```
[opc@instance-20240702-1632 ~]$ docker -v
Docker version 26.1.4, build 5650f9b
[opc@instance-20240702-1632 ~]$ docker-compose -v
Docker Compose version v2.27.1
```

### 4.3.3 安装 Node
点击宝塔面板左侧菜单栏`网站`，在 Node 项目中选择 Node版本管理器。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ab7ccd783e81f39052170880e373d546.png)

选择最新的 LTS 版本进行安装，成功后可以看到软件安装位置：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/4d7b4e35f731ca356519801ace2e3dea.png)

我们也可以在终端中进行测试，返回版本号代表成功：
```
[opc@instance-20240702-1632 ~]$ /www/server/nodejs/v20.15.0/bin/node -v
v20.15.0
```
为了更快捷使用 node 以及 npm 等命令，需要把上述地址放到系统环境变量中，然后再执行 `node -v` 就 OK 了，命令如下：

```
[opc@instance-20240702-1632 ~]$ echo "export PATH=$PATH:/www/server/nodejs/v20.15.0/bin/" >> ~/.bashrc
[opc@instance-20240702-1632 ~]$ source ~/.bashrc
[opc@instance-20240702-1632 ~]$ node -v
v20.15.0
```

### 4.3.4 安装更多...

有了宝塔面板，你想安装啥，都可以在 `软件商店` 中找到，感兴趣的小伙伴赶紧去试试吧~

# 写在最后

至此，我们一起走完了“Oracle Cloud服务器注册及配置”的完整流程。

祝各位都能成功开启你的 Oracle 白嫖之旅！

同时请注意薅羊毛不要有骚操作，避免账户被封号。

如果本文对你有帮助，欢迎**点赞收藏**备用！

猴哥一直在做 AI 领域的研发和探索，会陆续跟大家分享路上的思考和心得，以及干货教程。

有需要 Oracle 移动端验证 APP的，可以在 **“猴哥的AI知识库”** 公众号后台回复 **“oracle”** 自取。

新朋友欢迎关注，下次更新不迷路👇。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/8ca1f7b4e5ce4a8c87e1023e0c9595f2.png)






