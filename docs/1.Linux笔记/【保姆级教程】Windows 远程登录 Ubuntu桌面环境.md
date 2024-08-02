# 前言
在Windows下远程访问Linux服务器的桌面，有几种常见的方法：

- xrdp（X Remote Desktop Protocol）：xrdp允许Windows使用RDP（Remote Desktop Protocol）来连接到Linux服务器的桌面。这种方式相对简便，因为它使用Windows自带的远程桌面客户端。

- VNC（Virtual Network Computing）：VNC是一种基于图形界面的远程桌面协议，它允许用户远程访问Linux桌面。

- SSH（Secure Shell）：SSH是一种网络协议，用于加密方式远程登录到服务器。虽然SSH本身不提供图形界面访问，但可以通过X11转发功能在Windows上显示Linux的图形应用程序。

原本打算通过 VNC 实现远程连接，不过灰屏的问题一直无法解决，考虑到登陆远程桌面的需求并不多，主要是需要登陆浏览器实现校园网登陆，所以退而求其次采用 xrdp 来实现远程登陆。
# RDP连接Ubuntu桌面具体步骤
要通过远程桌面协议（RDP）连接运行Xfce4桌面环境的Ubuntu系统，大致可以按照以下步骤操作：
## 1. 安装 RDP 服务器：
在Ubuntu系统上，您需要安装一个RDP服务器，如xrdp。使用以下命令安装：

```bash
sudo apt-get update
sudo apt-get install xrdp
```

## 2. 配置 Xfce4 桌面：
xrdp默认使用Xfce4作为桌面环境。确保Xfce4已经安装在您的系统上。如果没有，您可以使用以下命令安装：

```bash
sudo apt-get install xfce4
```
xrdp 使用VNC 作为其显示协议，因此您还需要安装一个VNC服务器，不过 xrdp 安装过程中通常会同时安装 Xvnc。
## 3. 配置 xrdp
安装完成后，您可能需要配置xrdp以使用Xfce4。这通常涉及到编辑.xsession文件，确保它指向Xfce4。这里使用文本编辑器 Vim 编辑 ~/.xsession 文件，并添加以下行：

```bash
xfce4-session
```
## 4. 启动 xrdp 服务：
安装和配置完成后，启动 xrdp 服务：

```bash
sudo systemctl enable xrdp
sudo systemctl start xrdp
```
如果要退出 xrdp 服务：

```bash
sudo systemctl stop xrdp
```
## 5. 允许通过防火墙（可选）
这一步非必须，如果能连接到 RDP 服务器，则不需要执行这一步。否则，需要确保 RDP 端口 3389 在您的防火墙中是开放的。如果您使用的是ufw，可以使用以下命令：

```bash
sudo ufw allow 3389/tcp
```
## 6. 连接到RDP服务器
在Windows机器上，打开`远程桌面连接`应用程序，并输入Ubuntu服务器的IP地址。您应该会看到登录界面，输入Ubuntu的用户名和密码后，您就可以通过RDP访问Xfce4桌面了。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a1df694acdf644f7919e69f0c72395cb.png)

