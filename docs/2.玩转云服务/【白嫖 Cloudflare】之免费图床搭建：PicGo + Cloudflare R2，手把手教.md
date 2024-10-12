
前段时间，和大家分享过一个`免费图床方案`：
[从0搭建你的免费图床（PicGo + Oracle cloud 甲骨文云对象存储）](https://blog.csdn.net/u010522887/article/details/141101468)

后来发现，Oracle cloud 对象存储在国内访问速度受限，存在部分图片无法加载的问题！

今天，继续分享一个平替方案：`PicGo + Cloudflare R2`。

最近一直在摸索 `Cloudflare` 家的产品，而 `Cloudflare R2` 正是它推出的对象存储服务，10G 免费额度。

本文将手把手带你用 `Cloudflare R2` 搭建免费图床，供小伙伴们尽情白嫖。

## 1. Cloudflare R2 简介

R2 是 Cloudflare 在`对象存储`部分的又一项免费服务，

注册登录后，点击左侧边栏的 R2 访问服务。

![](https://img-blog.csdnimg.cn/img_convert/d0be87f6a557912155ea10e5aa5fff81.png)

进来后，可以看到免费额度。相比 Oracle cloud 的对象存储：
- 存储空间：Oracle cloud 有 20 G，Cloudflare 只有 10 G； 
- API 调用：Oracle cloud 每月限制 5 万次，Cloudflare **100 万次**！

大家可根据自己需求进行选择，不过我的建议：全都要！

![](https://img-blog.csdnimg.cn/img_convert/ffebc93925bccb6adff15663640a9b9a.png)

上图中的 A 类代表`上传`等操作，B 类代表`下载、访问`等操作。

和免费 DNS 服务不同的是，开通 R2 服务需要绑定一张信用卡，一来为了验证用户身份，二来怕你用超了，跑路~ 

免费额度内使用，不用担心扣费。

## 2. 创建存储桶

信用卡绑定成功后，左侧才会出现`创建存储桶`的选项。

![](https://img-blog.csdnimg.cn/img_convert/cc6e407678394d456885c160434ef2b1.png)

如果数据一般都是在国内访问的话，可以把桶放在亚太地区。下方点击「创建存储桶」。

![](https://img-blog.csdnimg.cn/img_convert/0eb60e166ddd8f562702f3b761cd2ed9.png)

桶创建成功后，可以直接从本地拖拽上传，至此，你完全可以把它当成一个网盘使用！

![](https://img-blog.csdnimg.cn/img_convert/e6d9c14be28650f572aaab6d3d4bee24.png)

## 3. 获取公网访问地址
如何获取图片的公网访问地址呢？

首先，在桶的主页，`配置`Tab页找到`公开访问`：

![](https://img-blog.csdnimg.cn/img_convert/8b415bca1313bde33ca6cb77e9359940.png)

为了获得突破的公网地址，需要打开「R2.dev 子域」，点击「允许访问」，输入 `allow`。

他会返回给你一个以 r2.dev 结尾的公网网址，即后续访问图片的网址。

![](https://img-blog.csdnimg.cn/img_convert/2fa52ff87622e0de72dc380070773a65.png)

当然，如果你有自己的域名且在 Cloudflare 完成了域名解析，也可以通过「自定义域」来绑定专属域名，点击「连接域」即可。

此外，对于开发者而言，一定还需要批量操作的 API。

接下来，我们看看如何通过 S3 API 进行上传下载等操作！毕竟搭建图床的 PicGo 客户端，需要依赖这种方式！

## 4. S3 API 调用

S3 API 是啥？

Amazon Simple Storage Service (S3)，是 Amazon 提供的对象存储服务，S3 API 支持使用 RESTful API 直接通过 HTTP 请求访问 Amazon S3，所以在业界使用非常广泛，**当然 Cloudflare R2 也提供了对 S3 的支持**。

要使用 S3 API，首先需要获取用于身份验证的 AccessKeyId 和 SecretAccessKey。

这个在 Cloudflare R2 哪里获取？

在主页右侧，点击「创建 API 令牌」
![](https://img-blog.csdnimg.cn/img_convert/299cfce5e844641fafec798dddaea9cc.png)

输入令牌名称，「权限」这里：`对象读和写`适用于特定的桶，而第一个权限的最大。

![](https://img-blog.csdnimg.cn/img_convert/12676a7b8eca85b074fc6b0f227ab1cd.png)

R2 Token 成功创建后，这里有所有 S3 API 需要的所有信息:

![](https://img-blog.csdnimg.cn/img_convert/9187d4b2f3aa764c0f5802af51127513.png)

搞定各种 key 后，如何调用？

和 [Oracle cloud 对象存储搭建图床](https://blog.csdn.net/u010522887/article/details/141101468) 一样，我们依然采用`boto3` SDK。

首先创建一个 client:

```
import os
import boto3
from botocore.client import Config

def init_s3(end_point, access_key, secret_key, region_name='auto'):
    return boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    use_ssl=True,
    region_name=region_name,
    endpoint_url=end_point,
    config=Config(s3={"addressing_style": "path"})
    )
    
s3_endpoint = "https://xx.r2.cloudflarestorage.com" # 换成你自己的
s3_access_key = "xx" # 换成你自己的
s3_secret_key = "xx" # 换成你自己的
region_name = "auto"
s3 = init_s3(s3_endpoint, s3_access_key, s3_secret_key, region_name)
```
对 Cloudflare R2 而言，这里的 region_name 要设置为："auto"。

然后，调用这个 client 列出所有 bucket:

```
buckets = s3.list_buckets()['Buckets']
print(buckets)
# 输出
[{'Name': 'houge', 'CreationDate': datetime.datetime(2024, 8, 23, 8, 37, 30, 977000, tzinfo=tzutc())}]
```

上传一张图片试试吧：

```
file_name = "xx.png"
response = s3.put_object(Bucket='houge', Key=os.path.basename(file_name), Body=open(file_name, 'rb'))
if response['ResponseMetadata']['HTTPStatusCode'] == 200:
    print("Upload file successfully!")
```


上传成功后，在桶主页可以看到图片详细信息，下面是公网可访问的地址，无防盗链，支持嵌入到任意前端页面！

![](https://img-blog.csdnimg.cn/img_convert/b76899f4f8c8ee224c9d6f0d1553c619.png)


## 5. PicGo 图床配置
PicGo 是一个用于快速上传并获取图片 URL 的工具软件。

如果你在 [Oracle cloud 对象存储搭建图床](https://blog.csdn.net/u010522887/article/details/141101468) 这一篇中安装好了 s3 插件，在图床设置中就可以看到 Amazon S3 的图床，设置参考下图，把上面 API 中的信息填入即可：

![](https://img-blog.csdnimg.cn/img_convert/d8f9422dee2730043a5cc54a4f2a655f.png)

完成配置后，可以在「上传区」直接拖入文件测试下，上传无误则配置成功，生成的链接会自动在系统剪贴板中。

## 写在最后

江湖人称`赛博菩萨`的 `Cloudflare`，还有很多面向开发者的免费服务，故打算做成一个系列，边探索边分享。

本文是`白嫖 Cloudflare 系列`教程之一，又一个免费又好用的图床搭建完毕：Cloudflare R2 + PicGo。

你学会了吗？有任何问题欢迎通过公众号找到我，一起打怪升级。

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

