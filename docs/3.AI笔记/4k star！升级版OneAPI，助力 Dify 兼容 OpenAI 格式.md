最近用 dify 搭建了不少智能体，不过 dify 有一个缺陷。

相信用过的朋友会有同样的感受：**它的 API 和 Open AI 不兼容**！

这就导致一个应用中，用到 dify 的地方，还必须重新写一套 LLM 的调用逻辑。

很是麻烦，怎么搞？

前段时间，和大家分享过大模型分发和管理神器 OneAPI:

[所有大模型一键封装成OpenAI协议](https://zhuanlan.zhihu.com/p/707769192)

并接入了多款大模型 API：

[盘点 9 家免费且靠谱的AI大模型 API，统一封装，任性调用！](https://zhuanlan.zhihu.com/p/717498590)

实现一个接口聚合不同的大模型，再统一转换为 OpenAI 的 API，**遗憾的是不支持 Dify 接入**。

最近看到一款开源项目 **NewAPI**：对 OneAPI 进行了二次开发，实现了对 Dify 的支持。终于，Dify API 也可以通过 OpenAI 统一分发了！

话不多说，上实操！

## 1. 服务部署
> 项目：[https://github.com/Calcium-Ion/new-api](https://github.com/Calcium-Ion/new-api)

推荐使用 docker 部署：

**数据库使用 SQLite 的部署命令**：

```
docker run -d --name newapi --restart always -p 3007:3000 -e TZ=Asia/Shanghai -v ./data:/data calciumion/new-api:latest
```

当然，也支持 Docker Compose 的方式：

```
# 先下载项目到本地
git clone https://github.com/Calcium-Ion/new-api.git
# 然后修改 docker-compose.yml 文件
# 最后启动
docker-compose up -d
```

## 2. NewAPI 使用
### 2.1 登录
本地浏览器通过 IP + 端口的形式进行访问，初始账号密码：root 123456。

![](https://i-blog.csdnimg.cn/img_convert/ba5d0d07b3dfc58f8f39ddeebd236c2d.png)

### 2.2 渠道
相信用过 OneAPI 的朋友，应该不陌生：`渠道`用于添加不同厂商的大模型。

点击「控制台-渠道-添加渠道」，在支持的渠道里选择 Dify：

![](https://i-blog.csdnimg.cn/img_convert/d607321b30c92e627154d9d079cf7b77.png)


![](https://i-blog.csdnimg.cn/img_convert/7a17abd46a64849ae06c4b087b5c541a.png)

然后，在`代理`这里：需填入 dify 的 IP地址+端口号。

![](https://i-blog.csdnimg.cn/img_convert/8e295cbef85a73d7c633d00ec094a499.png)

注意：图中的`http://host.docker.internal:3006` 用于从Docker容器内部访问宿主机的网络，不过只能在Windows和Mac版本的 Docker 中使用。Linux 用户需要改为本机的 IP 地址（**同一局域网内即可，无需公网 IP**）。


清空下方所有模型，填入模型名称 dify：

![](https://i-blog.csdnimg.cn/img_convert/63741608e6f4f76b8e23f3afb728be70.png)

然后，在最下方填入 dify 应用中获取的密钥：

![](https://i-blog.csdnimg.cn/img_convert/d051b334633c11399be381dae17057e4.png)


最后，来测试一下吧，一般只要 IP+端口号没问题，这里都能通过：

![](https://i-blog.csdnimg.cn/img_convert/ee00f80203339c7c6363b29ea0125a77.png)

**此外，New API 完美兼容 OneAPI 的数据库，可直接迁移 OneAPI 的数据库（one-api.db），无需同时维护OneAPI 和 NewAPI 两个项目。**

### 2.3 PlayGround
相比 Dify，作者贴心地新增了 PlayGround，方便可视化模型效果。

模型选择我们之前在 Dify 上搭建的搜索引擎智能体：

![](https://i-blog.csdnimg.cn/img_convert/a1cf99b19960f890b7a723a17f043c8c.png)

### 2.4 令牌

要在本地客户端调用，还需一个 api_key。添加令牌：

![](https://i-blog.csdnimg.cn/img_convert/b6f68528a657a14d080d364eaecb88e5.png)

### 2.5 更多
此外，相比 OneAPI，NewAPI 这个项目还增加了更多实用功能，比如下方的调用量数据看板，同时也增加了支付接口，`新一代大模型网关与AI资产管理系统`，当之无愧！

![](https://i-blog.csdnimg.cn/img_convert/0374ac1e5984a4627c5bbaf24da6e3d9.png)


## 写在最后

本文介绍了大模型接口管理工具-NewAPI，除了 Dify 之外，还支持 Midjourney 绘图接口。有需要的朋友快去试试。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。
