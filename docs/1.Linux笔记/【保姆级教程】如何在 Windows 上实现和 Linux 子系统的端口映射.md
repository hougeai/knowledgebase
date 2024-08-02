# 写在前面
上次分享[【保姆级教程】Windows上安装Linux子系统，搞台虚拟机玩玩](https://zhuanlan.zhihu.com/p/689560472)，向大家介绍了什么是虚拟机以及如何在Windows上安装Linux虚拟机。对于开发同学而言，经常遇到的一个问题是：很多情况下代码开发需要依赖 Linux 系统，而在 Linux 子系统上搭建的服务，是无法通过 localhost 在本地浏览器打开的，这时就需要 `端口映射`了，将 Linux 子系统上的端口映射到本地 Windows 机器上。

本篇分享将手把手带领大家完成这一功能需求。整个流程需要分为如下几步：

 - 查看 IP
 - 查看端口
 - 端口映射

# 1 查看 IP
windows 和 linux 系统中查看 IP 地址的命令是不一样的，具体而言。
##  Windows 下查看 IP
直接打开一个终端，输入 `ipconfig`，可以看到本地的 IPv4 地址。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740270.png)
##  Linux 下查看 IP
Linux 下查看 IP 地址，有如下三种方式：

```bash
ifconfig # 需要 sudo apt install net-tools
hostname -I
ip addr show eth0
```
如果是通过 wsl 方式在 windows 上安装的虚拟机，还可以在windows的终端，通过如下命令查看 Linux 子系统的 IP：

```bash
wsl -- ifconfig eth0
```
# 2 查看端口
Linux 系统中如果服务启动后，可以通过如下命令查看都有哪些端口已经被占用了：
```bash
netstat -ntlp
```
如果发现有的端口已经被占用了，还可以根据进程号 kill 掉对应进程。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311740272.png)

在其中找到需要映射出来的端口号，进入下一步。
# 3 端口映射
Windows 下以管理员身份运行shell，然后运行如下命令实现端口映射：

```bash
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=172.17.0.37 # 注意这里是0.0.0.0而非127.0.0.1
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.17.0.37
```
其中 connectaddress 就是 Linux 子系统的 IP，注意如果你的服务中有两个端口，需要将两个端口都映射出来。

查看是否添加成功：

```bash
netsh interface portproxy show all
```
调试结束后，可以删除端口映射：

```bash
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
```



