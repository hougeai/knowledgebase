最近，Linux 服务器自带的固态硬盘，空间告警，急需加上一块新的硬盘来救急。

今日分享，系统梳理下 Linux 下挂载磁盘的详细步骤和注意事项，希望给有类似需求的小伙伴一点帮助。

## 1. SSD（固态硬盘）和 HDD（机械硬盘）

**有啥区别？**
- HDD（机械硬盘）：HDD 由旋转磁盘组成，数据通过磁头在磁盘上写入或读取。因此，数据存取速度受限于磁盘转速和机械结构。

- SSD（固态硬盘）：SSD 由闪存芯片组成，无需任何机械部件。数据可以直接在芯片中读取或写入，速度更快且更加稳定。

**速度咋样？**

SSD 的读写速度比 HDD 快数倍甚至几十倍。通常，普通 SSD 的读写速度在 500 MB/s 左右，而 HDD 在 100 MB/s 左右。

**价格咋样？**

HDD 相对价格更便宜，适用于存储大量数据但访问频率不高的场景，比如备份、冷数据存储。

**怎么选？**

对于 Linux 服务器来说：

- 操作系统和数据库：选择 SSD 提高性能。
- 数据备份或冷数据：选择 HDD 节省成本。

**因此，我打算新增一块 HDD，把不常用的数据挪过去，为 SSD 腾出更多空间。**


## 2. HDD 类型和接口

市面上的各大厂商的 HDD 类型可太多了，怎么选？

不同类型和接口的 HDD 会影响到硬盘的性能、适用场景和兼容性。

## 2.1 HDD 类型选择

从类型上来看：

- **3.5 英寸 HDD**：桌面电脑和服务器中最常见的类型。适合存储大量数据，转速一般在 5400 RPM 到 7200 RPM**（推荐）**。

- **2.5 英寸 HDD**：这种硬盘通常用于笔记本电脑，容量和转速一般低于 3.5 英寸的 HDD。某些小型服务器和 NAS 设备也会使用这种硬盘。

- **企业级 HDD**：企业级 HDD 比消费级的更耐用，设计寿命更长，支持 24/7 不间断运行，通常用于数据中心、服务器或存储阵列。

**服务器上预留的插槽，一般会兼容 3.5 英寸和 2.5 英寸，不过还是留意一下比较好。**

## 2.2 HDD 接口分类
HDD 中常用接口主要有两个：

**SATA（Serial ATA）：**

特点：广泛应用于消费级和企业级硬盘。

版本：目前主流的是 SATA 3.0，最大理论带宽为 6 Gbps。

**SAS（Serial Attached SCSI）：**

特点：主要用于企业级硬盘，常见于服务器和数据中心。

版本：SAS 2.0 支持 6 Gbps，SAS 3.0 支持 12 Gbps。

**所以，购买时需要注意硬盘的接口类型，以免接口不匹配的问题。**

## 3. 硬盘挂载

新买的硬盘拆封后，放进插槽后，需要根据不同尺寸，用螺丝固定住对应位置。

**记得一定要看到硬盘灯亮**，才意味着安装成功！


### 3.1 查看盘符

终端执行 `lsblk`：

![](https://img-blog.csdnimg.cn/img_convert/ce022bb2d666b454c60d02718503fd45.png)


如果能看到新增的硬盘，比如我这里的`sda`（机械硬盘一般以sda开头），说明系统已经成功识别到。

通常，服务器支持硬盘的热插拔，如果没识别到，且硬盘灯是亮的，可以重启机器试试。


### 3.2 开始分区
分区有两种方式：

**方式一：fdisk**

终端执行：

```
sudo fdisk -l
```

可以看到新增的盘符`/dev/sda`，接下来开始对它进行分区：

```
sudo fdisk /dev/sda 
```

如果你的硬盘大于 2 T，会看到提示如下：

```
The size of this disk is 7.3 TiB (8001563222016 bytes). 
DOS partition table format cannot be used on drives for volumes larger than 2199023255040 bytes for 512-byte sectors. 
Use GUID partition table format (GPT).
```

这是提示你要改用 GPT 分区，因为当前 MBR 分区方式，最高只支持 2.2T。

如果继续执行下去，你将会得到一个 2T 的分区。

```
# 按 n 开始
# 选择 p 为主要分区
# 剩下的默认回车
# 结尾输入 w 来保存
```

这时，如果还只希望得到一个分区，怎么搞？

需要先删除刚才新建的分区：
```
sudo fdisk /dev/sda
Command (m for help): d
Partition number (1-4): 1
Command (m for help): w
```

接下来，我们采用方式二来创建 GPT 分区表。

**方式二：gdisk**

使用 gdisk 工具创建GPT分区表，命令如下：

```
sudo gdisk /dev/sda

Command (? for help): o
Command (? for help): n
Partition index (1-128): 1
First sector (34-15628053167, default = 2048) or {+-}size{KMGTP}: 

# 下面这行代表你要用多大空间，这里以分 500G 举例，不写就是全用上
Last sector (2048-15628053167, default = 15628053167) or {+-}size{KMGTP}: +500G
Hex code or GUID (L to show codes, Enter = 8300): 8300
Command (? for help): w
```

再次执行`sudo fdisk -l`看看呢？

```
Device     Start         End     Sectors  Size Type
/dev/sda1   2048 15628053134 15628051087  7.3T Linux filesystem
```

搞定，一个 7.3 T 的分区 `/dev/sda1` 出来了！

### 3.3 格式化分区

创建分区后，首先需要格式化。

假设新分区是sda1，可以使用以下命令：

```
sudo mkfs.ext4 /dev/sda1
# 输出如下信息
Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (262144 blocks): done
Writing superblocks and filesystem accounting information: done
```

### 3.4 挂载新分区

在迁移数据之前，需要挂载新分区到一个临时目录：

```
sudo mkdir /mnt/sda1
sudo mount /dev/sda1 /mnt/sda1
```

注：这里最好新建一个空目录。

最后，把之前存放在 SSD 中的 `/home/xxx/data`，挪过来吧。

```
mv /home/xxx/data /mnt/sda1
```

再创建一个软链接，无缝衔接：

```
ln -s /mnt/sda1/data /home/xxx/data
```
### 3.5 重启自动挂载
为了让系统在重启时，自动挂载新分区，还需要更新/etc/fstab文件。

首先，找出sda1的UUID：

```
sudo blkid
```

然后，编辑/etc/fstab文件：

```
sudo vim /etc/fstab
# 添加一行，然后保存
UUID=ae03686c-xxx /mnt/sda1 ext4 defaults 0 2
```

上述参数说明如下：

- UUID：每个分区都有一个UUID，通过blkid命令查询得到。UUID不会因为分区的重新排序或系统重启而改变。
- /mnt/sda1：这是挂载点，即文件系统挂载到的目录路径。
- ext4：这是文件系统的类型，表明这个分区使用的是ext4文件系统。
- defaults：这是挂载选项，defaults表示使用默认的挂载选项，包括权限、是否同步等。
- 0：这是dump的备份操作设置，0表示不需要备份。
- 2：这是fsck磁盘检查的顺序设置，2表示在启动时检查文件系统的顺序。1是根文件系统，2是其他文件系统，0表示不检查。

## 写在最后

本文梳理了 Linux 下挂载磁盘的详细步骤和注意事项。不到之处，欢迎评论区留言，我来更新。

如果对你有帮助，欢迎**点赞收藏**备用。
