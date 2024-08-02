前段时间，带大家搞了两台云服务器：

- [玩转云服务：Oracle Cloud甲骨文永久免费云服务器注册及配置指南](https://zhuanlan.zhihu.com/p/707330156)
- [玩转云服务：手把手带你薅一台腾讯云服务器，公网 IP](https://zhuanlan.zhihu.com/p/707330156)

基于这两台云服务器，我们玩转了很多有趣的开源项目：

- [手把手带你搭建免费的人脸检测/识别系统](https://zhuanlan.zhihu.com/p/710781082)
- [本地部署大模型？Ollama 部署和实战，看这篇就够了](https://zhuanlan.zhihu.com/p/710560829)

不过上述这些应用都是通过 IP +端口号的方式访问的，非常不利于传播~

这时你需要的就是一个域名，以及把域名翻译成 IP 的服务。

通常各大云厂商都提供域名注册服务，不过域名注册是需要付费的。

如果你只是想搞个来玩玩，又不想花这个钱？

好在有一些二级域名可以白嫖~

**本文将带大家：注册一个免费域名，并通过 Cloudflare 实现免费的域名解析**，让小伙伴们通过域名就能访问你的网站！

## 1.免费域名注册

免费的域名网站有不少，不过随着大家*将白嫖进行到底*的精神，很多都不能用了。

最常见的就是 eu.org，由Paul Mockapetris 在1996年创建，是为了给没有资金买域名的个人或组织提供**永久免费**的域名。不过，状态一直处于审核中 == 没通过~

>  传送门：https://nic.eu.org/，感兴趣的小伙伴可以去试试，有成功的评论区告诉我哦~ 

接下来介绍的这个，亲测注册成功，带着大家走一遍流程。

>  传送门：https://nic.us.kg/ 

首先，测试一下你想要注册的域名，是否已被占用，然后点击下面的立即注册，用邮箱创建一个账号（国内邮箱即可）。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-7a1beeb13a83558537ccc415f285e9fe_1440w.png)





添加图片注释，不超过 140 字（可选）

账号注册有几种方式，我这里选择的是填写 github issue 申请，大概不到 1 小时就通过了，邮件标题为 GitHub KYC Approved，通过后即可前往申请域名。

注册成功后，点击域名注册。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-ae2ce04399de37c0525b3c7b6ec74c2e_1440w.png)





添加图片注释，不超过 140 字（可选）

如果没被注册过，它会提示你，你只需要180天后续订下一年，就可以一直使用下去。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-0ba0faa58b8c058a68a8cf1331af8df1_1440w.png)





添加图片注释，不超过 140 字（可选）

下面两个必填的 **Name Server** 是什么鬼？

这里是让你填：用于 域名解析 的域名服务器。

什么是域名解析：通过将域名映射到特定的IP地址，使得用户能够通过域名轻松访问你的网站 or 服务。而域名解析，需要由域名服务器来执行。

Cloudflare 是一个知名的云服务提供商，提供免费的域名解析服务，同时也提供域名注册服务，不过需要付费。

所以，我们就以 Cloudflare 为例，给大家展示如下如何拿到域名服务器。

## 2.免费域名解析

## 2.1 获取域名服务器

首先，前往 [https://www.cloudflare.com](https://www.cloudflare.com/) 注册一个账号。

然后，点击最上方的 添加站点。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-779c730a9de3c59774dde123c25f002a_1440w.png)





添加图片注释，不超过 140 字（可选）

输入你刚注册的域名，点击 继续。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-7fae7d347deff2481d062b21cd4a8b17_1440w.png)





添加图片注释，不超过 140 字（可选）

选择这里的 free 计划（付费的服务暂时还用不到），点击 快速扫描。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-1d775dc860e7dd8e19f07e2d2120a794_1440w.png)





添加图片注释，不超过 140 字（可选）

没有注册过的域名是没有任何解析记录的，如出现解析记录说明此域名已经被注册过了。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-c51b571f0c0c42a4a967d05426396699_1440w.png)





添加图片注释，不超过 140 字（可选）

最后，找到这里的名称服务器，复制到刚才的 **Name Server** 处。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-18890ee777c85e239c70f8ce25768ff2_1440w.png)





添加图片注释，不超过 140 字（可选）

比如我这里，最后点击 注册。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-70ff7e34edc614aa4d4762032db422ba_1440w.png)

添加图片注释，不超过 140 字（可选）

注册成功！这里提示您的域名已成功创建并提交到根 DNS。请允许最多 20 分钟或更长时间，以便域名解析记录和注册生效。 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-016f90c7cd188d70bb0a4da8029cce21_1440w.png)





添加图片注释，不超过 140 字（可选）

现在我们回到 Cloudflare，当 houge.us.kg 在 Cloudflare 上激活时，它会向您的注册邮箱发送电子邮件。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-46ad8f16f3a3f87b70ccb8b3ee1fdd13_1440w.png)





添加图片注释，不超过 140 字（可选）

大概不到 10 分钟就能收到 Cloudflare 的邮件。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-18d781c023a489398fb57d1f90e330ed_1440w.png)





添加图片注释，不超过 140 字（可选）

回到 Cloudflare，这里状态也变成了 活跃。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-9862fa338bb8a34d5101c6212296f217_1440w.png)





添加图片注释，不超过 140 字（可选）

## 2.2 添加 DNS 记录

接下来需要添加 DNS 记录，也就是 域名 和 IP 的一一映射关系。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-493454193d93d4a275f94a46be2f725a_1440w.png)





添加图片注释，不超过 140 字（可选）

**类型怎么填：**

- A：用于将域名映射到 IPv4 地址，大部分云服务器提供的都是 IPv4，所以选择默认的 A 即可。
- AAAA：用于将域名映射到 IPv6 地址。
- CNAME：用于将一个域名指向另一个域名（可以是另一个CNAME或者A记录）。

**名称怎么填：**

- 填入 @：直接指向你的根域名；
- 填入 www：指向www.xxx.com，比如对应这里：浏览器输入 www.houge.us.kg 也能指向你的 IP。

IP 地址填写你申请的云服务器地址，添加成功后，如下图所以：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-70447ff24e00dfd28f37abcde152a526_1440w.png)





添加图片注释，不超过 140 字（可选）

到这里，你的 域名 已经和 IP 绑定好了。

那么，在浏览器输入你的域名，就能访问你的网站了？

错，还差一步！

我们在浏览器中输入网址时，通常是发出 HTTP 请求，而 HTTP 请求的默认端口是 80，所以，你还需要确保服务器的 80 端口是开放和可用的。

这时，你得来了解下 Nginx 这款神器了。

## 2.3 Nginx 端口转发

Nginx 是啥？

一个高性能的开源 Web 服务器和反向代理服务器，同时也可以用作负载均衡器和 HTTP 缓存。主要有以下功能：

- Web 服务器：提供静态内容（如 HTML、CSS、图片等）。
- 反向代理：将客户端请求转发到后端服务器。
- 负载均衡：分配请求到多个服务器，提高性能和可用性。
- SSL/TLS 支持：处理 HTTPS 请求，确保数据安全。

上一篇：[Ollama 部署和实战](https://zhuanlan.zhihu.com/p/710560829)，我们把 Ollama 的 WebUI 部署在了 3000 端口上。

所以，我们这里就将 80 端口上的请求转发到 3000 端口的后端应用上，来给大家展示下如何使用 Nginx。

### 2.3.1 Nginx 安装

如果你的服务器上安装好了宝塔面板，可以直接在面板中安装，不过使用过程中并不是特别友好。

这里推荐大家直接在终端安装。

**方式一：** 如果是预装了 Debian/Ubuntu 的服务器，可以一键安装：

```
sudo apt install -y nginx
```

启动 & 关闭 & 重启命令：

```
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
```

设置开机自启动：

```
sudo systemctl enable nginx.service
```

查看 Nginx 状态：

```
sudo systemctl status nginx
```

**方式二：编译安装（推荐）**，前往官网找到指定版本

>  官网：https://nginx.org/en/download.html 

终端输入如下命令，进行下载并安装：

```
mkdir nginx 
cd nginx
wget https://nginx.org/download/nginx-1.26.1.tar.gz
tar -xf nginx-1.26.1.tar.gz
./configure
make
make install
```

默认安装在：/usr/local/nginx/sbin/nginx

此时环境变量中找不到，需要建立软连接：

```
ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/nginx
```

此时，再执行：nginx -v 

返回版本号，说明安装成功。

服务启动 & 停止 & 重启命令如下：

```
nginx # 启动
nginx -s stop # 关闭
nginx -s reload # 重启
nginx -t # 测试配置文件
```

### 2.3.2 Nginx 配置

Nginx 是依赖配置文件进行运行的，如果是按照上述方式二安装的，那么默认配置在：/usr/local/nginx/conf/nginx.conf

如何查看默认配置文件在哪？

```
sudo nginx -t
# 输出
nginx: the configuration file /www/server/nginx/conf/nginx.conf syntax is ok
nginx: configuration file /www/server/nginx/conf/nginx.conf test is successfuli
```

为了实现我们端口转发的需求：

**step 1:** 在默认配置文件中 http 的配置中添加一行：

```
http {
    include /usr/local/nginx/conf/server/*.conf;
}
```

**！！注意：修改后，记得保存，否则会无法生效。** 这样 Nignx 启动后，它就会自动匹配 /usr/local/nginx/conf/server/ 文件夹下所有后缀为 .conf 的文件。

**step 2:** 新建 /usr/local/nginx/conf/server/ 文件夹，然后在其中新建一个 .conf 的文件，其中填入：

```
server {
    listen 80;
    server_name houge.us.kg;
    location / {
        proxy_pass       http://127.0.0.1:3000;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   Host      $http_host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

上面的参数说明如下：

- listen 80，这时 http 默认的端口号，确保它没有被占用，否则需要换用其他端口号；如果有多个服务都在监听 80 端口，则 nginx 会按照配置中的顺序分配。
- server_name，当然就是你注册好的域名。
- proxy_pass，你要转发到的后端端口，我们这里是本地的 3000 端口。

修改配置文件后，记得一定要重启 Nginx，否则配置无法生效。

启动后，我们查看下进程号：

```
ps -aux | grep nginx
```

如果出现下面界面，说明 Nginx 服务已经成功启动，不过 80 端口出了问题，需要排查下： 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-9f68e67430faf742e77e716d14a0acea_1440w.png)





添加图片注释，不超过 140 字（可选）

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-fdcede5d048c80f67a9eef5a6da8e8be_1440w.png)





添加图片注释，不超过 140 字（可选）

成功搞定！ 

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-2d17e98cb656915de8f099ef389bf868_1440w.png)





添加图片注释，不超过 140 字（可选）

## 写在最后

至此，你也能让小伙伴们通过专属域名访问你的网站啦。

想要一个酷炫但不用花钱的域名？只需三步：

1. US.KG 注册免费二级域名
2. Cloudflare 实现免费域名解析
3. Nginx 实现端口转发

希望能够帮助更多的小伙伴搭建自己的在线网站，展示你的创意成果。快去试试吧！别忘了评论区展示你的成果~
