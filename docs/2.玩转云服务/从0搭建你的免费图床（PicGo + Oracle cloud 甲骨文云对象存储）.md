上一篇，给大家分享了：

[一天时间，搭了个专属知识库，终于上线了](https://blog.csdn.net/u010522887/article/details/140919939)


全文较长，涉及到的技术点和工具比较多，有个问题没说清楚：
既然选择了甲骨文云的对象存储作为图床，如何配合 PicGO 使用呢？

本文作为上一篇的补充，继续和大家分享一个**免费图床**的实现方式：PicGo + Oracle cloud 对象存储。

全程依然干货满满，希望给有类似需求的小伙伴一点帮助~

# 1. Oracle cloud 对象存储

## 1.1 存储桶申请

Oracle cloud 对象存储的免费空间有 20 G，每月限制 50000次 API 调用，对于个人开发者足够使用了。

接下来手把手带大家申请一块 `存储桶`。

在控制台左上角的导航菜单中，找到`存储`，然后选择对象存储。

![](https://img-blog.csdnimg.cn/img_convert/877ff116f4b797b8b0e9919aa2941378.png)

进来后，点击`创建存储桶`，名称默认以时间命名，你可以换一个方便自己记忆的，莫瑞诺存储层选标准就行，因为 标准 和 归档 共同组成你的 20G 免费空间。

![](https://img-blog.csdnimg.cn/img_convert/89df12e7e58f8a5459d973cad4bc97ce.png)

进来后，在`编辑可见性`这里，**需要把桶设置为公共的**，这样你上传的图像才可以被访问。

![](https://img-blog.csdnimg.cn/img_convert/2342cc26f963ef9c135daedc33b60d5c.png)


## 1.2 客户端上传下载

下面就是在 web 端手动操作上传、下载等功能，上传速度非常快，而且同名文件会自动替换。就这一点，比 GitHub 图床可强太多了。

![](https://img-blog.csdnimg.cn/img_convert/d239b87c082832f6380353cfd549aeed.png)

每张图片的后面三个点，点击即可查看图片详细信息，包括 url 等。国内访问速度也还 OK 的，部分有延时。

客户端手动操作，对于开发者来说，显然是不能接受的，有没有 API 可调用？

接着往下看👇

## 1.3 Amazon s3 API

甲骨文云官方提供了 Object Storage API，不过这个 API 用起来特别麻烦，而且我们接下来还需要和 PicGo 配合，实现自动上传。

这时，我们需要用到 Amazon s3 API，甲骨文云官方贴心地为 Amazon s3 API 提供了兼容。详情可参考官方文档：[Object Storage Amazon S3 Compatibility API](https://docs.oracle.com/en-us/iaas/Content/Object/Tasks/s3compatibleapi.htm#notableDifferences)。

Amazon S3 API 是啥？ 

Amazon Simple Storage Service (S3) 是 Amazon 提供的对象存储服务，Amazon S3 API 就是和 S3 交互的 API。因为它支持使用 RESTful API直接通过 HTTP 请求访问 Amazon S3，所以在业界使用比较广泛。

而要使用 Amazon S3 API，首先需要获取到用于身份验证的 AccessKeyId 和 SecretAccessKey。

这个在 Oracle cloud 哪里获取？

### 1.3.1 Oracle cloud 密钥获取
登录Oracle Cloud后，点击右上角头像，依次点击 我的概要信息-客户密钥-生成密钥。

![](https://img-blog.csdnimg.cn/img_convert/c52b096c771050a21d936049fa58d9ca.png)

点击生成密钥，记得立即复制出来，这个就是 `SecretAccessKey`，否则后续就拿不到了。然后点击访问密钥下方的字符串，这个就是 `AccessKeyId`。

这两个东西是用于后续身份验证的，一定要保存好。

### 1.3.2 对象存储基本信息获取

回到你的对象存储页面，上面就是你的`桶名称`，名称空间需要保存下来，记作 `{object-storage-namespace}`。

![](https://img-blog.csdnimg.cn/img_convert/7d7089263ff4cb6aa6fca7bd833ad942.png)

接下来通过如下拼接方式，得到请求的节点`Endpoint`：

```
https://{object-storage-namespace}.compat.objectstorage.{region}.oraclecloud.com
```
`{region}`是你的主区域代码，怎么获取？

点击一张你上传图像的详细信息，在 url 中可以看到，比如我的就是 `ap-singapore-1`。

![](https://img-blog.csdnimg.cn/img_convert/a0767bcf7eb3e189a91f63cea74e0b8c.png)

有了这些东西后，我们就可以前往 PicoGo 配置 S3 插件了。

不过在此之前，我还有一个需求：能否在应用中批量化处理所有本地图片？

接下来，我们一起去探索下如何实现 s3 API 的本地调用。

### 1.3.3 s3 API 调用

因为 s3 API支持 RESTful API，自然可以用 Python 调用，看了一圈它的鉴权方式，直接把我劝退了，不同请求类型的 Authorization 都不一样，感兴趣的可以从这篇博客了解更多：[Amazon S3 REST API 详解](https://blog.csdn.net/zhangxin09/article/details/124522934).

好在已经有 SDK 把上述过程封装好了，这个宝藏 SDK 叫 `boto3`，你只需要一键安装：

```
pip install boto3
```

使用也非常简单，我把常见的功能给大家梳理下。

首先，需要初始化一个 client:

```
import os
import boto3
from botocore.client import Config

def init_s3(end_point, access_key, secret_key, region_name='ap-singapore-1'):
	return boto3.client(
		's3',
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key,
		use_ssl=True,
		region_name=region_name,
		endpoint_url=end_point,
		config=Config(s3={"addressing_style": "path"})
	)
```

然后，直接调用这个 client 做任何想做的：

```
s3_endpoint = "https://{object-storage-namespace}.compat.objectstorage.{region}.oraclecloud.com" # 换成你自己的
    s3_access_key = "xxx" # 换成你自己的
    s3_secret_key = "xxx" # 换成你自己的
    region_name = 'ap-singapore-1' # 换成你自己的
    s3 = init_s3(s3_endpoint, s3_access_key, s3_secret_key, region_name)
    
    # 列出所有bucket
    buckets = s3.list_buckets()['Buckets']
    
    bucket_name = 'bucket-xxx'
    # 列出所有文件
    objects = s3.list_objects(Bucket=bucket_name)['Contents']
    for obj in objects[:3]:
        print(obj['Key'])
    
    # 下载文件
    response = s3.get_object(Bucket=bucket_name, Key='xxx.png')
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        response_content = response['Body'].read()
        with open('test.png', 'wb') as f:
            f.write(response_content)
    
    # 上传文件
    file_name = r"D:\data\xx.png"
    response = s3.put_object(Bucket=bucket_name, Key=os.path.basename(file_name), Body=open(file_name, 'rb'))
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Upload file successfully!")
```

# 2. PicGo 插件安装和使用
## 2.1 S3 插件
参考[上篇教程](https://blog.csdn.net/u010522887/article/details/140919939)，相信你已经完成了 PicGo 的安装。接下来我们在插件设置，搜索框中输入 s3，下图中装第一个就行：

![](https://img-blog.csdnimg.cn/img_convert/6e154cc978d772633f36b6272ca021f0.png)

安装成功后，在图床设置中就可以看到 Amazon S3 的图床，设置参考下图：

![](https://img-blog.csdnimg.cn/img_convert/d9717a62f1d2c502d42afcf5cd5d440e.png)

具体的字段说明如下：
- 应用密钥ID：就是上面获取的 `AccessKeyId`
- 应用密钥：就是上面获取的 `SecretAccessKey`
- 桶名：你创建的`桶名称`
- 文件路径：你怎么定义存储桶中的上传路径，下面详细说明
- 地区：就是上面获取的 `{region}`
- 自定义节点：就是上面拼接得到的节点 `Endpoint` 

`文件路径`支持的 payload与描述如下，可按需配置，因为我希望同名文件直接覆盖，所以选用了 `{fullName}`：

![](https://img-blog.csdnimg.cn/img_convert/10b32d80b13e3caf57925491b409a633.png)

**！注意**：`ForcePathStyle` 必须设置为 yes，否则上传时使用的自定义节点会在输入的节点前自动加上桶名，导致上传失败。

至此，Amazon S3 的图床的配置就基本完成了，快去上传区上传一张图片试试吧~

![](https://img-blog.csdnimg.cn/img_convert/aae8c506eb804fb3bc586185695382c0.png)

上传成功后，得到的 url 格式如下：

```
https://{object-storage-namespace}.compat.objectstorage.{region}.oraclecloud.com/{bucket}/{img_name}.png 
```


## 2.2 squoosh 图片压缩插件
贴心提示：如果你每次都是截图上传图片，由于现在的截图软件默认保存的都是 png 图片，导致图片占用存储空间不小，而且图片太大的话也会影响网络加载速度。

所以，如果你不想 20G 免费空间很快爆满的话，最好安装一个图片压缩插件。


操作也很简单，在插件设置，搜索框中输入 squoosh，装上就行~

初次使用，需要进行配置：


![](https://img-blog.csdnimg.cn/img_convert/b82238eba3c788775cc06c23ea93fcb4.png)

我这里并不打算采用 md5 重命名，所以只把下面相应扩展名的图片压缩打开了。

![](https://img-blog.csdnimg.cn/img_convert/7e833d1b71a5e624e241e25ff5145515.png)

记得点击下方的 确定 进行保存哦，否则配置不会生效的。


# 写在最后
至此，一个免费又好用的图床就搭建好了，本文的所有图片上传也是 PicGo + Oracle cloud 对象存储 + S3 API实现的。

有了这个图床，以后写文章方便多了!

整个过程虽然略显复杂，但跟着文章一步步实操，相信你也能轻松搞定！有什么问题欢迎留言哦~

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。你的支持是我创作的最大动力。