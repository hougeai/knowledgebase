# 写在前面

最近的各大厂商的 LLM 大模型，可谓百花齐放，想都尝试下，但每家的 API 协议都不尽相同~

注册了各家的 LLM API 帐号，如何统一管理？

甚至，想乘这阵 LLM 之风赚一波...

别急，今天介绍的这个 GitHub 开源项目满足你所有幻想：OneAPI，一款接口管理和分发神器，将所有大模型一键封装成OpenAI协议。
> 传送门：[https://github.com/songquanpeng/one-api](https://github.com/songquanpeng/one-api)

话不多说，上实操！

# 1. 服务部署

作者了提供了源码部署和 Docker 部署两种方式，其中源码部署需要分别构建前端和后端，相对麻烦一点。

前两篇，我们分别搞了一台本地 Linux 虚拟机和一台云服务器：
- [Windows上安装Linux子系统，搞台虚拟机玩玩](https://blog.csdn.net/u010522887/article/details/137632509)
- [玩转云服务：手把手带你薅一台腾讯云服务器，公网 IP](https://blog.csdn.net/u010522887/article/details/140091900)。

接下来，就把 OneAPI 部署在这台云服务器上，如果你用本地 Linux 虚拟机当然也没问。

因为本项目还依赖数据库的服务，所以我们采用 docker-compose 的方式来进行部署，简单几步就能搞定，极大降低小白的部署门槛。

不了解 docker 的小伙伴可以看这里：[【保姆级教程】Linux系统如何玩转Docker](https://blog.csdn.net/u010522887/article/details/137206719)

## 1.1 创建 docker-compose 文件

打开一个终端：
```
mkdir oneapi
cd oneapi/
touch docker-compose.yml
```

把下述脚本复制到 docker-compose.yml 中：
```
version: '3.3'
services:
  mysql:
    # image: mysql:8.0.36
    image: registry.cn-hangzhou.aliyuncs.com/fastgpt/mysql:8.0.36 # 阿里云
    container_name: mysql
    restart: always
    ports:
      - 3306:3306
    command: --default-authentication-plugin=mysql_native_password
    environment:
      # 默认root密码，仅首次运行有效
      MYSQL_ROOT_PASSWORD: oneapimmysql
      MYSQL_DATABASE: oneapi
    volumes:
      - ./mysql:/var/lib/mysql
  oneapi:
    container_name: oneapi
    # image: ghcr.io/songquanpeng/one-api:latest
    image: registry.cn-hangzhou.aliyuncs.com/fastgpt/one-api:v0.6.6 # 阿里云
    ports:
      - 3001:3000
    depends_on:
      - mysql
    restart: always
    environment:
      - SQL_DSN=root:oneapimmysql@tcp(mysql:3306)/oneapi
      - SESSION_SECRET=oneapikey
      - MEMORY_CACHE_ENABLED=true
      - BATCH_UPDATE_ENABLED=true
      - BATCH_UPDATE_INTERVAL=10
      # 初始化的默认令牌
      - INITIAL_ROOT_TOKEN=fastgpt
    volumes:
      - ./oneapi:/data
```
简单介绍下上面几个参数：
- version: 指定了Compose文件格式的版本，用于确保配置文件与Docker Compose的版本兼容，最新版docker-compose已不需要这个字段；
- services: 定义了应用程序中的服务，每个服务运行在独立的容器中；
- image：镜像地址，国内服务器用阿里云的镜像会非常快，海外服务器不建议用阿里云的镜像；
- ports: 3001:3000 意味着容器内部的3000端口映射到宿主机的3001端口，用于防止宿主机端口冲突；
- volumes: ./mysql:/var/lib/mysql 意味着将本地的./mysql目录挂载到容器的/var/lib/mysql目录，用于数据持久化。

## 1.2 服务启动
配置好 docker-compose.yml 文件后，采取如下命令一键启动：

```
sudo docker-compose up -d
```

等待拉取镜像，终端出现如下提示，说明成功启动：
```
[+] Running 3/3
 ✔ Network oneapi_default  Created                   
 ✔ Container mysql         Started                   
 ✔ Container oneapi        Started
```

我们打开宝塔面板，可以看到服务已经在运行中了：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e044c1be189cf193be56fd8a9e40e6df.png)

# 2. 服务配置和管理
## 2.1 OneAPI 登录
还记得 OneAPI 的端口号不？3001！

因此，浏览器中的访问地址应该是：http://IP:Port，例如：http://129.150.63.xxx:3001

但这时，上述地址是打不开的，还需要到服务器中把 3001/3306 端口的防火墙打开。如果你用的也是腾讯云服务器，具体操作见：[玩转云服务：手把手带你薅一台腾讯云服务器，公网 IP](https://blog.csdn.net/u010522887/article/details/140091900)。

防火墙打开后，上述地址就可以访问了：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f37379f031506bf01cddbfa7164e423d.png)

首先需要登录，初始账号名 root，密码 123456，登录后立即修改密码。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/360fa8f3628aa7d0e99ed49aa3e5f796.png)

登录成功后，你会发现 Tab 页多了几个选项，这些只有超级管理员能看到：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/98ebee18564a1b8c2ef42d99f8bbd4e4.png)


接下来，我们一一了解下系统的几个模块。

## 2.2 用户
首先我们看下用户管理模块，左下角可以新增用户。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/eb0517f0ff4ba24964895da4003da8cd.png)

点击右侧编辑，可以发现用户分组有三个。分组有什么用？假如你在这个系统中代理 10 种大模型并商业化，可以设定 VIP 可以使用其中的 2 种模型，而 SVIP 可以使用全部。如果自己玩，那随意。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d894a6671b156b718bb290d24b0a5bfc.png)

## 2.2 渠道

渠道用来管理和添加各个大模型厂商的 LLM。只有超级管理员才能设置。

在渠道管理中，左下角点击添加新的渠道：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/63e21293bcddffb50df87ec7dde32af4.png)
### 2.3.1 渠道添加
我们以 Coze 为例进行介绍。

如何去 coze 申请一个bot，可以看这里：[coze2openai](https://zhuanlan.zhihu.com/p/707567256)

假设你已经申请到了一个bot，那么它的url应该是这样：https://www.coze.cn/space/**user_id**/bot/**bot_id**。

保存好**user_id** 和 **bot_id** ，下面渠道填写要用到：
- 类型：选择 Coze；
- 名称：渠道名称，随便填，方便自己使用即可；
- 模型：要用哪些模型，Coze 中以**bot_id**区分，红色方框里填入**bot_id**，最后点击填入；
- User ID：填写你的**user_id**；
- 密钥：填写你在 coze 中获取的令牌；
- 代理：如果是国内的coze，则是 https://api.coze.cn/；如果是国外的 coze，则对应 https://api.coze.com/。（**非常重要，否则调用不了**）

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/862e759b2e2604b4e7de396fffc02d45.png)

提交后，点击右侧测试，看看是否能够调用成功。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/80a672639c98c2e7c2e54eae07204d68.png)

再比如我们还要用智谱的GLM，添加则更加简单，只需要你准备好智谱的 API key 就好了：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c30be86612975348ed83c5ee123373d8.png)

### 2.3.2 渠道列表
其他厂商基本和上述一致，最后，给大家看下我的渠道列表：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/70f5c3d7f414a646530ed57aa14bc511.png)

## 2.3 令牌
这个模块用于创建令牌，供客户端或调用方使用，其作用跟 LLM的令牌（或密钥）的作用是一样的。点击复制后，会显示在上方搜索框。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3ba784079fe57bf2bea83f9706017dfc.png)

当然也可以选择添加新的令牌，如果仅仅是自用，可以设为无限额度，永不过期；如果是外发给其他人使用的，你可以给他设置一个限量:

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/28e4908e6dd06cee65d0c88a0b35ab16.png)

有了令牌，就可以采用 OpenAI 协议的 API 调用了。

## 2.4 兑换 & 充值
这两个模块是为了商业化准备的。

兑换模块，用于管理兑换码，类似话费充值卡。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ecebea57fc93f728016f4da9cfc7e1f9.png)

充值模块，用于给账户充值，与兑换配合使用。输入一个有效兑换码，就相当于给当前账户充值对应的额度，用于供令牌调用消耗。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/0b598a2d050acfac1e210bc558c84f41.png)


## 2.5 日志 & 设置
日志模块，用于展示用户充值和额度消耗记录。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/573528a7e0a07ec0405315972a28cdb3.png)


设置模板，包括个人设置、运营设置、系统设置和其他设置，整个系统的商业化功能还是挺完备的。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/227949efd487215bfd4a5735b9fee199.png)

# 3. 服务测试
最后，我们用获取到的令牌来测试一下。

其调用方式与 OpenAI API 一致，只需将: 
- OpenAI 的网址 'base_url'，改成你部署的 OneAPI 的网址，例：'http://129.150.63.xxx:3001/v1'；
- OpenAI 的令牌 'api_key'，改成你的令牌，在本文 2.3 部分得到。

我们在 2.2 渠道部分添加了两个模型，测试的示例代码如下：
```
from openai import OpenAI

model_dict = {
    'coze': {
        'api_key': 'sk-xxx',
        'base_url': 'http://129.150.63.184:3001/v1',
        'model_name': '7357494611763445771'
    },
    'glm': {
        'api_key': 'sk-xxx',
        'base_url': 'http://129.150.63.184:3001/v1',
        'model_name': 'glm-4'
    },
}

class LLM_API:
    def __init__(self, api_key, base_url, model):
        self.client =  OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model
    
    def __call__(self, messages, temperature=0.7):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return completion.choices[-1].message.content

if __name__ == '__main__':
    model = 'coze'
    llm = LLM_API(model_dict[model]['api_key'], model_dict[model]['base_url'], model_dict[model]['model_name'])
    user_question = "你是谁"
    messages = [{"role": "user", "content": user_question},]
    print(llm(messages))
```

# 写在最后

上篇分享的：，还只能将 Coze 的 LLM 转换为OpenAI API，而今天介绍的这款 OneAPI 则支持了更多的 LLM。本质上，OneAPI 相当于进行了中转操作：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6c15edbe4e3726cff7b8dc41deacadc5.png)

从此，你再也不用为用哪个 LLM 而纠结了，一个接口帮你测试所有 LLM！想调哪个你随意~

祝大家借助 OneAPI 玩转大模型，开发出更多 AI 创意应用。

下篇预告：*FastGPT - 给 GPT 插上知识库的翅膀！0基础搭建本地私有知识库*

如果本文对你有帮助，欢迎**点赞收藏**备用！





