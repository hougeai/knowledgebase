前不久，OpenAI 宣布终止对中国提供 API 服务，国内开发者想访问 GPT 实在是太难了。

于是猴哥立马输出了一篇教程，推荐大家用国内的 SiliconCloud，免费用各大国产大模型，见：[国产大模型All In One，API免费用，开发者的福音](https://zhuanlan.zhihu.com/p/705681762)

有小伙伴说：某些场景下，没有 GPT 还真不行~

今天就来分享一个不会被封，还能免费用GPT等各大厂商 LLM 的 API 制作方法。

方法很简单，分为两个部分：

- 1. Coze Bot 发布
- 2. Coze2OpenAI

话不多说，赶紧实操。

# 1. Coze Bot 发布
## 1.1 什么是 Coze
Coze 是由抖音母公司-字节跳动推出的 AI 聊天机器人开发平台。Coze 和 扣子 分别对应国际版和国内版。

> 国内版 扣子 ：[https://www.coze.cn/](https://www.coze.cn/) (国内直连)
>
> 国际版 Coze ：[https://www.coze.com/](https://www.coze.com/) (需要魔法)

二者最大的区别在于支持的底层大模型不一样：

- 国内版使用的是国内厂商开发的大模型，如 Kimi/Qwen；
- 国际版支持 GPT-4o/GPT-4 等模型。

这就给了我们**白嫖 GPT-4/Kimi** 的机会~

下面，我们一起看下：如何把 Coze 打造成一个可供调用的 API。

注意：国内版和国际版的使用方法和流程基本是一致的，下面以国内版为例进行介绍。

## 1.2 制作并发布 Bot
第一步，打开[https://www.coze.cn/](https://www.coze.cn/) ，注册账号后，点击左上角的`创建 Bot`。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-a43c355e5e41a05992a905b5fa6f55c8_1440w.webp)

第二步，模型设置 这里，可以选择 Kimi 支持 128k 输入的大模型，其他地方可以不用动，直接点击右上角的发布。（**注：如果是国际版的，模型设置 可以选择 GPT4**）

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-f8a565a7c46586437c8b020ae9af1986_1440w.webp)

最后，如下图所示，勾选上 “Bot as API” ，然后再点击右上角的 '发布'。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-e8ca7ea298504fa59a7ea4e91dbf4913_1440w.webp)

稍等片刻，等待发布成功。

## 1.3 获取 API
回到 Coze 首页，点击左下角的 “Coze API”。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-66fa14abb48a6c5f101fbb61b5c63a4a_1440w.webp)

在 “API 令牌” 页面添加一个新令牌，并保存下来。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-37da249ce4427fc18411f174e89fc4b9_1440w.webp)

这时你就有了一个可以免费调用的 LLM API。

接下来，一起来测试了看看。

## 1.4 API 测试
> **API 接口文档：**
> 
> 国内版：[https://www.coze.cn/docs/developer_guides/coze_api_overview](https://www.coze.cn/docs/developer_guides/coze_api_overview)
>
> 国际版：[https://www.coze.com/docs/developer_guides/chat?_lang=zh](https://www.coze.com/docs/developer_guides/chat?_lang=zh)

一个 API 请求，需要准备两个内容：
- Personal_Access_Token：也就是你刚刚保存的 API 令牌
- Bot_Id：进入你发布的 Bot 页面，URL 中 bot 参数后的数字就是 Bot ID。例如https://www.coze.cn/space/73428668341/bot/123，Bot ID 就是 123。

编写如下 python 代码进行测试：

```
import requests

# 替换以下变量的值为你的实际值
personal_access_token = '你的Personal_Access_Token'
bot_id = '你的Bot_Id'
conversation_id = '123'
user = 'CustomizedString123'
query = '你是谁'

url = 'https://api.coze.cn/open_api/v2/chat'

headers = {
    'Authorization': f'Bearer {personal_access_token}',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': 'api.coze.cn',
    'Connection': 'keep-alive'
}

data = {
    "conversation_id": conversation_id,
    "bot_id": bot_id,
    "user": user,
    "query": query,
    "stream": False
}

response = requests.post(url, headers=headers, json=data)

print(response.text)
```

正常返回，测试成功：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-5e459705c3fe26b96d6d296ed62e7b13_1440w.webp)

## 1.5 使用限制
国内版：当前扣子 API 免费供开发者使用，每个空间的 API 请求限额如下：
- QPS (每秒发送的请求数)：2
- QPM (每分钟发送的请求数)：60
- QPD (每天发送的请求数)：3000

国际版：每个注册用户每天100次调用

目前来看，国内版还是相对友好一些。

# 2. Coze2OpenAI
细心的小伙伴已经发现了，Coze 提供的 API 不兼容 OpenAI 格式。

如果要适配应用中 OpenAI 的 API 格式，怎么搞？

GitHub 上早已有大佬搞定了！
> 传送门: [https://github.com/fatwang2/coze2openai](https://github.com/fatwang2/coze2openai)

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-dfcf4e4260d1ee10eed9e1b960b27411_1440w.webp)

下面介绍两种部署方式：
## 2.1 部署到自己的服务器

上一篇，我们已经薅了一台拥有公网 IP 的腾讯云服务器：[手把手带你薅一台云服务器](https://zhuanlan.zhihu.com/p/706326769)。

所以，首先带大家动手把项目部署到这台腾讯云服务器上。

### 2.1.1 项目准备

第一步，先打开终端，把项目代码 clone 下来：

```
git clone https://github.com/fatwang2/coze2openai
```
第二步，复制一份环境变量的配置文件:

```
cp .env.template .env
```

第三步，在 .env 文件中修改环境变量：

```
PORT=3002
BOT_ID="your_bot_id"
BOT_CONFIG={"model_name_1": "bot_id_1", "model_name_2": "bot_id_2", "model_name_3": "bot_id_3"}
COZE_API_BASE=api.coze.cn
```
其中：
- PORT 是服务启动后的端口号，如果端口已被占用，记得换用其他端口号
- BOT_ID 是默认采用的机器人的ID，也就是刚才 API 请求中的 Bot_ID
- BOT_CONFIG **非必填**，如果你有多个机器人，用于区分不同的机器人，实现切换模型来调用不同的机器人。如果调用不在配置文件的模型，则走默认的 BOT_ID
- COZE_API_BASE 根据国内版和国际版，选择 coze.cn 或者 coze.ccm

### 2.1.2 安装依赖
因为该项目是一个JavaScript项目，所以需要服务器安装好 Node.js。
> 基本概念科普：Node.js 是一个 JavaScript 运行时环境；npm 是 Node.js 的包管理工具，方便管理Node.js项目中的依赖项；pnpm 也是包管理器，和 npm 类似。

查看是否安装 Node.js：打开终端，输入：

```
node -v
```
如果没有返回版本号，则需要自己安装：

方式一：源码安装（容易失败）

首先，访问 [Node.js 官网](https://nodejs.org/zh-cn)。下载适用于你Linux发行版的最新源码包。
```
wget https://nodejs.org/dist/v20.15.0/node-v20.15.0.tar.gz
cd node-v20.15.0
# 配置环境
./configure
# 编译并安装
sudo make
sudo make install
```
如果编译失败，直接采用下面的方式二：选择阿里云上已经编译好的安装包，无需编译安装。

方式二：

首先，访问[镜像网站](https://registry.npmmirror.com/binary.html)，然后找到对应版本的 node 包并下载。

```
wget https://registry.npmmirror.com/-/binary/node/latest-v20.x/node-v20.15.0-linux-x64.tar.gz
# 解压
tar -xf node-v20.15.0-linux-x64.tar.gz
cd node-v20.15.0-linux-x64/
./bin/node -v # 输出node 版本
```
可以发现解压文件的 bin 目录下，包含了 node、npm 等命令，因此可以将整个目录放到环境变量中：
```
export PATH=$PATH:/home/lighthouse/node-v20.15.0-linux-x64/bin/
```
再执行：`node -v` 就 OK 了。

当然为了一劳永逸解决问题，最好是放到系统全局配置中，命令如下：

```
echo "export PATH=$PATH:/home/lighthouse/node-v20.15.0-linux-x64/bin/" >> ~/.bashrc
# 让更改立即生效
source ~/.bashrc
```

node.js 安装好之后，我们再来安装 pnpm：

```
npm install -g pnpm
```

上述没问题后，安装本项目的依赖项：

```
cd ../coze2openai/
pnpm install
```

### 2.1.3 启动服务
最后，一键运行项目：
```
pnpm start
```

终端输出下面这个 url, 说明服务启动成功：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-e2aea3cef9c5192c954baa804c530493_1440w.webp)

当然，也可以采用 nohup 将命令放到后台运行，并将输出重定向到 nohup.out 文件中。
```
nohup pnpm start &
```

浏览器中访问腾讯云服务器的控制台，在防火墙中把3002端口打开，然后找到你的公网 IP，替换上面的 localhost，也是可以访问的。

返回如下界面，说明成功搞定！

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-ef5f09a14dc09f5907ef5d32303a4370_1440w.webp)

### 2.1.4 测试服务

接下来我们编写代码，来测试一下刚启动的 OpenAI API：

```
from openai import OpenAI

model_dict = {
    'coze': {
        'api_key': 'pat_xxx',
        'base_url': 'http://101.33.210.166:3002/v1',
        'model_name': 'coze-1'
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

上述代码中：
- 'api_key' 就是你之前保存的 API 令牌，以 pat_ 开头
- 'base_url' 的拼接方式为：'http://your_ip:port/v1'


## 2.2 部署到 Zeabur
> 传送门：[https://zeabur.com](https://zeabur.com)

如果你没有云服务器，或者嫌自己部署太麻烦，可以考虑采用 Zeabur 部署试试。

### 2.2.1 什么是 Zeabur
Zeabur 是一个国内团队开发的，可以帮助您部署服务的平台，和 Vercel、Railway、Netlify、Render 类似，不过国内使用更加方便，每个月有 5 元的免费额度，用完即停止服务。



### 2.2.2 项目部署
首先进入项目模板页：[https://zeabur.com/templates/BZ515Z](https://zeabur.com/templates/BZ515Z)

点击 Deploy，选择区域后，确认进入部署页面：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-897818256f194ca0638505c92873096e_1440w.webp)

然后，拉到下方'环境变量'部分，根据 2.1.1 部分的环境变量配置，逐一添加进来，然后点击 “重新部署”：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-8884a32f5d23cf87364ea14aaaab81ee_1440w.webp)

最后，在下方‘网络’部分，创建一个自定义域名：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-50b97b809b5c1c40306d92b4a3653855_1440w.webp)

这样，你就可以通过这个域名访问你的OpenAI API 服务了。

举个例子，我自定义的域名是：https://coze2openaitest.zeabur.app/

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-a0867ecb00de14b8e3565accd40d9387_1440w.webp)

看到上述页面，说明已经部署成功，接下来我们测试一下 API。

### 2.2.3 服务测试
依然采用 2.1.4 部分的代码，唯一的区别就是把代码中的 'base_url' 改成上面的域名。**（注意要用 https 而非 http）**

```
'base_url': 'https://coze2openaitest.zeabur.app/v1',
```
# 写在最后

至此，我们一起走完了 “部署一个 OpenAI API 服务” 的完整流程。底层采用 Coze 提供的各类大模型（包括GPT/Kimi等），后端采用 coze2openai 开源项目提供的封装。

最后提供了两种部署方式，方便大家按需取用！

祝大家借助这些免费的 API 玩转大模型，开发出更多 AI 创意应用。

如果本文对你有帮助，欢迎**点赞收藏**备用！











