# 0. 前言
很多情况下代码开发需要依赖 Linux 系统，远程连接 Linux 服务器进行开发和维护已成为一种常态。对于使用Windows系统的开发者来说，掌握如何通过 SSH 安全地连接到 Linux 服务器，并利用 VS Code 编辑器进行开发，是一项必备的技能。对于没有服务器的同学，可以参考笔者之前的文章 [Windows上安装Linux子系统，搞台虚拟机玩玩](https://blog.csdn.net/u010522887/article/details/137632509) 准备一个 Linux 环境。

本文将详细介绍两种在 Windows 下远程登陆 Linux 服务器的方法：SSH 命令行和 VS Code 远程开发。

# 1. 远程登陆的两种方式
## 1.1 SSH远程连接Linux服务器
SSH（Secure Shell）是一种网络协议，用于加密方式远程登录到服务器。以下是通过SSH连接Linux服务器的基本步骤：

1. **安装SSH客户端**：Windows 10及以上版本自带了OpenSSH客户端
2. **安装SSH服务端**：在服务器端安装 OpenSSH，需要在服务器终端进行。

	```bash
	# 安装 ssh
	sudo apt install openssh-server
	# 安装完成后一般会自动启动，通过如下命令检查 ssh 是否已经启动
	sudo systemctl status ssh
	# 如果没有启动，需要启动 ssh 服务
	sudo systemctl start ssh
	# 如果要停止 ssh 服务
	sudo systemctl stop ssh
	```
3. **通过SSH登陆服务器**：ssh 登陆服务器一般有两种方式：
- 使用密钥认证：参考笔者之前的文章 [Windows上安装Linux子系统，搞台虚拟机玩玩](https://blog.csdn.net/u010522887/article/details/137632509) 中对密钥认证步骤的分享，简言之，主要分为以下两步：
**首先，Windows 本地生成SSH密钥对**。下载并安装Git for Windows，然后打开Git Bash终端：在终端中执行命令 `ssh-keygen` ，这时会在本地 .ssh 文件夹中生成了密钥文件， .ssh 文件夹一般保存在 C 盘，比如我的是` C:\Users\12243\.ssh`，文件夹下 id_rsa 是私钥，id_rsa.pub 是公钥。
**然后，复制公钥到 Linux 服务器**。将id_rsa.pub中的内容复制到 Linux 的你的用户根目录 `~/.ssh/authorized_keys` 文件中。

	```bash
	mkdir ~/.ssh
	cd ~/.ssh
	echo xxx_in_your_id_rsa_pub >> authorized_keys
	```

- 使用密码认证：这种方式比较简单，唯一的缺点就是每次登陆都需要输入你的账号密码。
不管采用以上哪种方式，都可以参考如下命令在终端执行登陆，唯一的区别是第一种方式不需要输入密码：
	```bash
	ssh your_user_name@172.17.4.63
	```

## 1.2 使用VS Code进行远程开发
VS Code（Visual Studio Code）是一个功能强大的编辑器，支持远程开发。以下是使用VS Code连接Linux服务器的步骤：
### 1.2.1 安装VS Code
首先需要在本地 Windows 电脑上下载并安装最新版的 VS Code，下载地址见 [官网](https://code.visualstudio.com/)。安装流程可以参考笔者之前的文章[Windows 环境准备 - Conda 和 VS code 安装](https://blog.csdn.net/u010522887/article/details/136969406)
### 1.2.2 远程登陆
VS Code 访问服务器需要在本地进行一番配置后，然后执行 ssh 登陆，具体而言，可以分为以下几个步骤：
- **Step 1**: 安装 Remote-SSH 插件。第一次使用VS Code 需要在左侧插件栏搜索 Remote-SSH 并安装。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d60df712fe8e4ca1a57ec352310a62a5.png)
- **Step 2**: 左下角 Open a remote window 然后选择 Connect to Host。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/eb2f760d5c554584b2c59bcdc43f0855.png)
- **Step 3**: 执行 ssh 登陆。 如下图所示，这里有两种选择：
	![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/860be25c455e4657a842a080c3d2cb41.png)  	
	- Add New SSH Host，也就是新建一个 Host ：如果只是偶尔登陆这个 host ，可以选择这种方式
	- Configure SSH Hosts，也就是配置一个 Host：如果需要经常登陆，可以新建一个配置文件，这样每次登陆直接选择对应的 Host 名称就可以了，这里的配置文件一般在 C 盘用户目录下，比如我的就在 `C:\Users\12243\.ssh\config`。在config 文件中填入如下信息：Host 就是后续登陆使用的名称，HostName是服务器的 IP 地址，一般 SSH 对应的端口号 Port 是22 ，User 是你在服务器上注册的用户名。
		> Host 配置好后，再执行 SSH 登陆时，只需要终端输入Host 名称即可，比如我这里的就是`ssh cvlab` ，等同于之前的 `ssh your_user_name@172.17.4.63`。

		```bash
		Host cvlab
		  HostName 10.18.32.170 
		  Port 22
		  User xxx
		```

- **Step 3**: 配置好后再重新按照 Step 1 进行登陆，发现登陆名称中多了刚才新建的 cvlab ，点击进去，首先需要选择远程服务器的类型-Linux，然后输入你的账号密码。注：如果你之前应该采用了**密钥认证**，那么这一步就不需要输入密码了。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/60ba5ea88599499ebd7fd748415f5079.png)
- **Step 4**：首次登陆会自动在服务器端安装 VS Code server，如果账号密码都没问题的话，就可以登陆成功了，按 `Ctrl + ~ `键打开终端，可以发现现在已经进入服务器的环境了，接下来的操作就和你在本地机器上一样。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a7c8c47144f14531af6c2d4bf4056375.png)

## 1.3 方法对比
- **SSH命令行**：适合需要执行命令行操作的场景，对于脚本编写和快速命令执行非常有效。
- **VS Code远程开发**：适合需要图形界面和复杂编辑功能的场景，尤其是代码编辑、调试和版本控制。

## 结语
无论是通过SSH命令行还是VS Code，都能实现Windows系统下对Linux服务器的远程连接和开发。选择哪种方法取决于你的具体需求和偏好。至此，Windows 连接 Linux服务器的教程就结束了，实践是掌握技能的最好方式，不妨现在就开始尝试连接你的Linux服务器吧！

如果对你有帮助的话，不妨 **关注 点赞** 支持一下啊~ 带你了解更多 **Linux + AI** 开发的干货~
