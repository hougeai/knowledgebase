前端时间，搭了个个人知识库，并部署到 GitHub Pages 上：
[一天时间，搭了个专属知识库，部署上线了，手把手教，不信你学不会](https://blog.csdn.net/u010522887/article/details/140919939)

免费使用的 GitHub Pages 优势非常明显，唯一的缺点是：
- 对于大型网站或高流量网站可能存在访问速度较慢的问题。

本文将再介绍一款静态网站托管工具：`Cloudflare Pages` ，由 Cloudflare 提供，利用 Cloudflare 的全球性 CDN 进行加速，而且功能更加丰富：
- 支持主流的前端构建工具和框架，如 React、Vue 等；
- 提供更丰富的缓存策略和性能优化选项；
- 支持 Github/GitLab 仓库，和 Github Pages 类似。

之前我们网站的域名解析也是用的 Cloudflare 家的服务，感兴趣的小伙伴可参考：[【保姆级教程】免费域名注册 & Cloudflare 域名解析 & Ngnix端口转发](https://blog.csdn.net/u010522887/article/details/140786338)。

下面我们开始实操演示：如何利用 `Cloudflare Pages` 部署一个网站。

## 1. 网站部署

注册登录后，进入 Cloudflare 控制台，点击按图示进入 `Workers 和 Pages` 面板，选择 Pages。
> 多一嘴：区别于 Pages，Workers 是一个可以运行 Javascript 的无服务器平台。

![](https://img-blog.csdnimg.cn/img_convert/043babd39946be91f01b6c0f377b752c.png)


`Cloudflare Pages` 支持 Github/GitLab 仓库，这一点和 `Netlify` 是一致的。

![](https://img-blog.csdnimg.cn/img_convert/083adc814591cfeb6b9f751c62fbdd9f.png)


选择 Github 账号授权后，你可以选择授权所有项目给 Cloudflare，或者选择授权指定的项目仓库。

我这里选择全部授权，授权之后，选择一个你要部署的项目，点击 “开始设置”。

静态页面，一般设置部署分支、构建命令、构建输出目录就可以。点击“保存并部署”，等待几分钟即可部署完成。

![](https://img-blog.csdnimg.cn/img_convert/31ebe883bc22faebdcefd7959ee7d356.png)


部署完成后可看到 Cloudflare 给我们的域名 `xx.pages.dev`，刚部署完成，需要稍等 2 分钟，点击即可直接公网访问。

![](https://img-blog.csdnimg.cn/img_convert/4a4413a2361efba151837ea1ae8b52cd.png)


如果你有自己的域名，并在 Cloudflare 上进行了域名解析，也可以进入项目主页，选择自定义域。

## 2. 自定义域名
进入项目，点击 “自定义域”。

注：这里填入的域名一定要在 Cloudflare 上进行了域名解析。

![](https://img-blog.csdnimg.cn/img_convert/34ddd9fcdbc7ebd46e80da4b09944e38.png)

接入完成之后，Cloudflare 会自动帮你更新 DNS 记录。比如，我这里会自动将原来 github pages 上面的 IP 替换为 `Cloudflare Pages` 上的域名。点击“激活域”，完成更新。

![](https://img-blog.csdnimg.cn/img_convert/fd4448336c6b59910e1ba65fc5e32212.png)


![](https://img-blog.csdnimg.cn/img_convert/f3cc0d2690023c4d2a5b29dbe4a78105.png)

![](https://img-blog.csdnimg.cn/img_convert/b4a9a09b6609344287e9348614233427.png)

域名验证成功后，你的网站就可以通过自定义域名正式上线了！

## 3. 更多部署方案？

相信看到这里的你，一定有个疑问：除了 `Cloudflare Pages`，还有哪些平替？

今天，趁机给大家做一个盘点~

静态网站部署，大致可以分为以下两类：

### 3.1 云部署平台
和 `Cloudflare Pages` 类似的云部署平台还有：

- Vercel：和全栈开发框架 next.js 同属一家公司，生态非常完善，缺点就是太贵。
- Netlify：Vercel的直接竞争对手，每月 100 GB 免费访问流量。
- Railway：优势是支持 Docker 容器，包括 Dockerfile 和公开的 docker 镜像进行部署，但不支持docker-compose。
- Zeabur：国内公司开发，直接对标 Railway，也支持 Docker 容器。
- Render：另一个流行的云部署平台，和 Vercel 类似。
- Firebase：Google 提供的一个平台，可用于部署和托管 web 应用。

### 3.2 开源的部署方案
社区也有很多开源项目，旨在成为 Vercel 和 Netlify 等云平台的自托管替代方案，可以部署在自己的服务器上：

- [Coolify](https://github.com/coollabsio/coolify)(27.8k star)
- [Dokku](https://github.com/dokku/dokku)(26.5k star)：一个轻量级的开源 PaaS（平台即服务）。
- [SST](https://github.com/sst/sst)(21.2k star)：专注于无服务器架构和AWS生态系统。
- [Dokploy](https://github.com/Dokploy/dokploy)(5.3k star)：直接叫板 Vercel, Netlify and Heroku 的开源替代方案。

我还没尝试过，有机会实操后再来跟大家分享。


## 写在最后
本文通过一个简单的例子，带大家完成在 `Cloudflare Pages` 上部署网站，其生成的域名，亲测在国内可以直接访问~

对于免费账户而言，每天限制访问 10W 次。对于个人网站而言，完全足够。

江湖人称`赛博菩萨`的 `Cloudflare`，还有很多常用的网站管理服务，绝大部分都有免费额度。

我还没探索完，等用到了再陆续给大家分享。

如果本文有帮助，不妨点个**免费的赞**和**收藏**备用。



