最近，很多朋友发现 Docker 镜像拉取不下来了~
> PS：还不了解 Docker 的小伙伴，可以看这篇：[【保姆级教程】Linux系统如何玩转Docker](https://blog.csdn.net/u010522887/article/details/137206719)

罪魁祸首是：国内的大部分镜像站都停止服务了，包括：sjtu、ustc、百度、腾讯。。。

不过还好，阿里云的镜像还不受影响。

怎么搞？

**第 1 步： 阿里云注册账号**
> 传送门：[https://www.aliyun.com/](https://www.aliyun.com/)

支付宝扫码即可登录。

**第 2 步： 搜索容器镜像服务**

点击立即开通。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311736135.png)

**第 3 步： 找到镜像加速器**

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/202407311736257.png)

**第 4 步： 配置镜像加速器**

参考不同操作系统的配置文档，比如在我的 Linux 服务器上：

通过修改 daemon 配置文件，就可以使用加速器。

首先，新建文件夹：
```
sudo mkdir -p /etc/docker
```
然后，写入第 3 步的加速器地址：

```
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://xxx.mirror.aliyuncs.com"]
}
EOF
```

最后，重启 docker：

```
sudo systemctl daemon-reload
sudo systemctl restart docker
```

快去试试，镜像下载，有没有快到飞起~

如果本文对你有帮助，欢迎**点赞收藏**备用。









