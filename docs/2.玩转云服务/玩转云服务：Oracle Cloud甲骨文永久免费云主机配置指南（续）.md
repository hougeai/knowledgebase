

前段时间，和大家分享了白嫖`Oracle Cloud`的云服务器：
[玩转云服务：Oracle Cloud甲骨文永久免费云服务器注册及配置指南](https://blog.csdn.net/u010522887/article/details/140223094)。

新注册的小伙伴，可以在 30 天内，利用 300 美元免费储值，任性使用所有 `Oracle Cloud` 基础设施服务。

30 天后呢？

你仍然可以畅享 Always Free 免费套餐中的云服务！

## 1. 永久免费套餐

Always Free 免费套餐包含哪些内容？

![](https://img-blog.csdnimg.cn/img_convert/6b69bd5fb5c0451d2419ded3b676d07a.png)

总结而言：

计算资源方面：

- 2 个基于 AMD 的 x86 虚拟机，每个虚拟机配备 1核 和 1 GB 内存
- 基于 Ampere A1 内核的 Arm 虚拟机，最高 4核 和 24 GB 内存，可作为 1 个虚拟机或最多 4 个虚拟机使用。
- 所有虚拟机均拥有公网 IP。

存储资源方面：
- 200G 的块存储，相当于挂载在虚拟机上的硬盘；
- 20G 的对象存储，相当于网盘，用来搭建图床妥妥够了。使用教程👉[从0搭建你的免费图床（PicGo + Oracle cloud 甲骨文云对象存储）]https://blog.csdn.net/u010522887/article/details/141101468)

问题来了：计算资源和存储资源，如何搭配使用，才能价值最大化？

本文是[甲骨文永久免费云服务器注册及配置指南](https://zhuanlan.zhihu.com/p/707330156)的续篇，带大家用好免费的`块存储`资源。

## 2. 计算实例申请

目前 Singapore 区域放出了一波 x86 虚拟机，而 Arm 依然配额不足，大家可以先去抢两台 x86 试试！

不了解如何申请实例的可以参看上篇，这里需要注意的有两点，其他采用默认配置即可。

**一是操作系统：**

默认选用的是 Oracle Linux 8 镜像，这个镜像的底层是小众的 Fedora 系统，软件安装指令是`sudo dnf install xxx`，熟悉 Debian|Ubuntu 等系统的小伙伴可能不太习惯。右侧点击`更改镜像`选择你熟悉的系统镜像就行。 

![](https://img-blog.csdnimg.cn/img_convert/ebb80c835709d7aa71462800778c8a9a.png)

这里给大家展示下，两个系统的内存和磁盘占用情况：

Oracle Linux 8 镜像：

```
$ free -m
              total        used        free      shared  buff/cache   available
Mem:          948Mi       277Mi        67Mi       1.0Mi       603Mi       514Mi
Swap:         1.9Gi       111Mi       1.7Gi
$ df -h
Filesystem                  Size  Used Avail Use% Mounted on
devtmpfs                    428M     0  428M   0% /dev
tmpfs                       475M     0  475M   0% /dev/shm
tmpfs                       475M  6.6M  468M   2% /run
tmpfs                       475M     0  475M   0% /sys/fs/cgroup
/dev/mapper/ocivolume-root   36G  7.2G   29G  21% /
/dev/mapper/ocivolume-oled   10G  161M  9.9G   2% /var/oled
/dev/sda2                  1014M  329M  686M  33% /boot
/dev/sda1                   100M  6.0M   94M   6% /boot/efi
tmpfs                        95M     0   95M   0% /run/user/986
tmpfs                        95M     0   95M   0% /run/user/1000
```

Ubuntu 22.04 Minimal 镜像：

```
               total        used        free      shared  buff/cache   available
Mem:           947Mi       153Mi       367Mi       1.0Mi       427Mi       642Mi
Swap:             0B          0B          0B

Filesystem      Size  Used Avail Use% Mounted on
tmpfs            95M  1.1M   94M   2% /run
efivarfs        256K   17K  235K   7% /sys/firmware/efi/efivars
/dev/sda1        45G  1.7G   44G   4% /
tmpfs           474M     0  474M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/sda15      105M  6.1M   99M   6% /boot/efi
tmpfs            95M  4.0K   95M   1% /run/user/1001
```

可以发现，后者占用的内存和磁盘空间更低，故更推荐使用。



**二是：添加 SSH 密钥**

![](https://img-blog.csdnimg.cn/img_convert/7ff0d9790638fd3095b1aca3351480d8.png)

记得一定要添加 SSH 密钥，否则后续远程登录服务器，会非常麻烦！

## 3. 配置虚拟内存

免费虚拟机只有 1G 的内存，稍微复杂一点的应用都会带不动！

这时，你需要手动配置一下虚拟内存：用磁盘空间来扩展物理内存的能力。

因为 Ubuntu 22.04 Minimal 镜像默认没有配置虚拟内存。

怎么搞？

配置虚拟内存的交换空间，一般为物理内存的1-2倍，具体步骤如下：

```
1. 首先创建交换文件，使用 fallocate 创建一个交换文件。
sudo fallocate -l 2G /swapfile
2. 设置权限确保只有 root 用户可以读取和写入交换文件：
sudo chmod 600 /swapfile
3. 设置交换区域将文件格式化为交换空间：
sudo mkswap /swapfile
4. 启用交换文件启用交换文件以开始使用：
sudo swapon /swapfile
5. 验证：检查交换空间是否已启用：
sudo swapon --show
6. 开机自动挂载：系统启动时自动启用交换文件：
打开 /etc/fstab 
最后一行添加 /swapfile none swap sw 0 0

再次执行 free -h 就可以看到 swap 了。
               total        used        free      shared  buff/cache   available
Mem:           947Mi       151Mi       216Mi       1.0Mi       579Mi       638Mi
Swap:          2.0Gi          0B       2.0Gi
```


## 4. 块存储挂载
块存储：分为`块存储卷`和`引导卷`，二者有什么区别？

- `引导卷`：是实例的系统启动盘，就像你本地电脑的 C 盘。在实例创建时，默认是 46.6 G，后面如果需要扩容也是支持的。
- `块存储卷`：一个新磁盘，就像你本地电脑的 D 盘。需要在服务器上进行分区，格式化，挂载才能使用，用来存储数据。

不过，`块存储卷`和`引导卷`共享 200G 免费块存储资源，所以需要进行合理分配。

### 4.1 新增块存储卷
如何为新建的实例，新增一块块存储？

进入实例主页，在右侧可以看到：附加的块存储卷，点击附加:

![](https://img-blog.csdnimg.cn/img_convert/563f429f10879740f7b5a04004d0f4f3.png)

创建成功后，点击右侧的三个小点，找到 ISCSI 命令和信息。

然后远程登陆实例，复制附加命令到终端。

接下来，执行 `fdisk -l` 试试吧，你应该看到多了一块`/dev/sdb`的新磁盘。

继续执行如下命令对新磁盘分区：

```
fdisk /dev/sdb
n
# 按 n 开始
p
# 选择 p 为主要分区
# 剩下的默认回车
w
# 结尾输入 w 来保存
```

再次执行`fdisk -l`就可以看到已经分区为 `/dev/sdb1`。

接下来，需要对磁盘进行格式化（**必须**）：
```
mkfs.ext4 /dev/sdb1
```

然后，创建一个新目录，或选择已有空目录，实现磁盘挂载：

```
mount /dev/sdb1 /backup # 挂载磁盘到 /backup
```

最后，来设置一下开机自动挂载吧，确保主机重启也能自动挂载该目录。

```
vim /etc/fstab
# 在最后一行添加
/dev/sdb1 /backup ext4 defaults 0 0
```

如果想删除挂载的盘，怎么办？

很简单：删除所有文件后，`sudo umount /backup`

### 4.2 扩展引导卷

系统盘不够用了，咋办？

进入实例主页，在右侧找到引导卷，点进去。

![](https://img-blog.csdnimg.cn/img_convert/4ac4d3ab6ba82c1b68756d11e2d180e9.png)

首先将实例的引导卷扩展到 100G，下方保存更改：

![](https://img-blog.csdnimg.cn/img_convert/8a2d4bd56a7f4bae45ca5b6fe85d9d93.png)

远程登陆实例，终端执行 `lsblk` 可以看到整个系统盘，也就是引导卷为 46.6G，其中 sda3 就是系统根目录的容量。

执行复制的扫描命令，再次执行 `lsblk` ，可以发现整个引导卷 sda 已经变为 100G了，但为啥 sda3 根目录还是以前的容量？

继续执行以下命令将其扩容，提示 Confirm 时输入 Y.

```
LANG=en_US.UTF-8
sudo /usr/libexec/oci-growfs
```
再看看 sda3 呢？

是不是已经加满了。

## 写在最后

`Oracle Cloud`的免费服务还有很多，和对面的 `Cloudflare` 有的一拼，更多甲骨文云教程及使用，我打算边探索边分享。

有任何问题欢迎通过公众号找到我哦，一起打怪升级。

祝各位成功开启 Oracle 白嫖之旅！

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。
