
# 写在前面
上一篇，我们部署了接口管理和分发神器-OneAPI，将所有大模型一键封装成OpenAI协议。见：[OneAPI)。

**基于此，本篇继续带领大家搭建一个基于本地知识库检索的问答系统。**

有同学说 Coze 不也可以实现同样功能么？

是的，不过在 Coze 上，你需要把知识库文件文件上传到 Coze 的服务器。如果对数据安全有要求，那么搭建本地私有的知识库就更有必要了。

而且，就目前的体验而言，相比下面介绍的 FastGPT，Coze 的知识库检索略逊色一些。

FastGPT，给 GPT 插上本地私有知识库的翅膀，让它可以利用你的领域知识回答问题。

有同学问：和 dify 有什么区别？ 

相比 dify，FastGPT 在知识库召回上更优，而 dify 产品功能更为丰富，适合 demo 搭建。
> 传送门：[https://github.com/labring/FastGPT](https://github.com/labring/FastGPT)

# 1. FastGPT 部署

前几天，我们分别搞了一台本地 Linux 虚拟机和一台云服务器：
- [Windows上安装Linux子系统，搞台虚拟机玩玩](https://blog.csdn.net/u010522887/article/details/137632509)
- [玩转云服务：手把手带你薅一台腾讯云服务器，公网 IP](https://blog.csdn.net/u010522887/article/details/140091900)。

接下来，就把 OneAPI 部署在这台云服务器上，如果你用本地 Linux 虚拟机也是没问题的。

因为本项目还依赖其他服务，所以我们采用 docker-compose 的方式来进行部署，简单几步就能搞定，大大降低小白的部署门槛。

不了解 docker 的小伙伴可以看这里：[【保姆级教程】Linux系统如何玩转Docker](https://blog.csdn.net/u010522887/article/details/137206719)

## 1.1 下载配置文件

打开一个终端：
```
mkdir fastgpt
cd fastgpt
curl -O https://raw.githubusercontent.com/labring/FastGPT/main/projects/app/data/config.json
curl -o docker-compose.yml https://raw.githubusercontent.com/labring/FastGPT/main/files/docker/docker-compose-pgvector.yml
```
从 docker-compose.yml 中可以看出：FastGPT 用到的大模型需要兼容 OpenAPI 格式。

没关系，因为上一篇我们已经完成了 OneAPI + MySQL 的部署，只需要把 OneAPI 的 base_url 和 API Key 填入 yml 文件如下位置：
```
fastgpt:
    container_name: fastgpt
    environment:
      - OPENAI_BASE_URL=http://101.33.210.166:3001/v1
      - CHAT_API_KEY=sk-xxx
```

如果没有部署OneAPI，也没关系，这个 docker-compose.yml 文件包含了 OneAPI 的部署，可以先进入下面的`1.3 服务启动`。

等 OneAPI 启动后，参考：[oneapi](https://zhuanlan.zhihu.com/p/707769192)，在 OneAPI 中手动复制令牌，填到上面 `CHAT_API_KEY` 的位置。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e1cc609ec528584c2db71cdf3690ffbc.png)

填写完成后，记得重启 FastGPT 容器：`docker restart fastapi`。 

## 1.2 模型配置
知识库的构建，需要使用向量模型将一段文本转换成向量。在 OneAPI 中我们加入的 GLM 渠道，是支持向量模型的。

为此，需要在 config.json 中将用到的对话模型和向量模型加入进来：
- 对话模型：采用 "glm-4"
```
"llmModels": [
    {
      "model": "glm-4",
      "name": "glm",
      "maxContext": 16000,
      "avatar": "/imgs/model/openai.svg",
      "maxResponse": 4000,
      "quoteMaxToken": 13000,
      "maxTemperature": 1.2,
      "charsPointsPrice": 0,
      "censor": false,
      "vision": false,
      "datasetProcess": true,
      "usedInClassify": true,
      "usedInExtractFields": true,
      "usedInToolCall": true,
      "usedInQueryExtension": true,
      "toolChoice": true,
      "functionCall": true,
      "customCQPrompt": "",
      "customExtractPrompt": "",
      "defaultSystemChatPrompt": "",
      "defaultConfig": {}
    },
  ]
```
- 向量模型：采用 “embedding-2”

```
"vectorModels": [
    {
      "model": "embedding-2", // 模型名（与OneAPI对应）
      "name": "Embedding-1", // 模型展示名
      "avatar": "/imgs/model/openai.svg", // logo
      "charsPointsPrice": 0, // n积分/1k token
      "defaultToken": 700, // 默认文本分割时候的 token
      "maxToken": 3000, // 最大 token
      "weight": 100, // 优先训练权重
      "defaultConfig": {}, // 自定义额外参数。例如，如果希望使用 embedding3-large 的话，可以传入 dimensions:1024，来返回1024维度的向量。（目前必须小于1536维度）
      "dbConfig": {}, // 存储时的额外参数（非对称向量模型时候需要用到）
      "queryConfig": {} // 参训时的额外参数
    }
  ]
```

## 1.3 服务启动
如果服务器是国内的 IP，建议将 docker-compose.yml 文件中的镜像都改为阿里云的镜像。

配置好 docker-compose.yml 文件后，采取如下命令一键启动：

```
sudo docker-compose up -d
```

看到下图，说明正在拉取镜像：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/5bd41cc590da1dbba002dda0dceaf57e.png)

打开宝塔面板，可以看到服务已经在运行中：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/68e0ab0e4c577dfcce13eadd6a0995cb.png)

## 1.4 启动失败解决

如果某个容器启动失败，可以采用如下命令重启：

```
docker restart oneapi
docker restart fastapi
```

如果还是不行，把 docker 重启试试：
```
sudo systemctl restart docker
```

可能有的小伙伴之前在服务器上安装过 MySQL，3306端口被占用，导致这里的 MySQL 容器启动失败。因此，可以终止已安装的 mysql 服务，再重新执行 `sudo docker-compose up -d`。

```
# 下面命令关闭服务是不行的，会自动重启。所以，进程依然存在，端口依然占用
systemctl status mysqld
systemctl stop mysqld
# 应采用如下命令：查看进程并关闭
pidof mysqld
kill pid
```

# 2. FastGPT 应用
## 2.1 登录 FastGPT

在 docker-compose.yml 配置文件中找到 FastGPT 的端口号：3000。

浏览器中打开：http://IP:Port，例如：http://101.33.210.xxx:3000/。

如果上述地址打不开，需要到服务器中把 3000/3001/3306 端口的防火墙打开。如果你用的是腾讯云服务器，具体操作见：[玩转云服务：手把手带你薅一台腾讯云服务器](https://zhuanlan.zhihu.com/p/706326769)。

防火墙打开后，上述地址就可以访问了，初始账号名 root，密码 1234：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f8da19110cbdb64b38113ca59aad602c.png)

## 2.2 新建知识库
我们需要先把知识库准备好，便于后续调用。

左侧菜单栏选择知识库，右上角新建：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/2ac5bb8603699beea32abbf52376a8a6.png)

进来后，点击下面的配置，将索引模型改为 **Embedding-1**，因为这个才是我们在`1.2 模型配置`部分加入的向量模型，而 Embedding-2 对应的是默认 GPT 的 "text-embedding-ada-002"模型。配置修改完成，记得保存。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/5ea969d9fd0a391303b0af0252b8cd7c.png)


然后上传文件，这里为了跑通测试流程，我选择了文本格式，并简单填写了一些内容：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/5c6a625fbfe3ab14ca0d8bc6b68b3cfc.png)

等待处理，最后文本状态是“已就绪”就是 OK 了。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6fc8e4eaff525b76808d82d5b121147f.png)

最后，我们来测试一下，看能否检索到对应内容：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ee1f8e1e8a260d8b60660e01a615a543.png)

Ok，知识库搭建完毕！


## 2.3 新建应用
登录 FastGPT 后，先新建一个简易应用：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/14f7ae2c1682d5d1b1a485330b5cbe26.png)

进入应用后，**AI 模型**：需要选择刚才放到 config.json 中的 glm 模型。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/69ac4521bc90badfb54fc72d85ee05e8.png)

然后，把刚刚建立的知识库，关联进来。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/89bab17ac2f992c5d320828f53f91526.png)

配置完成后，我们在右侧调试一下。比如我问他 “猴哥是谁”，他会先从知识库中检索到相关信息再回答我：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ff2e8aeeeb5db66081a06eba64eef681.png)

如果调试没问题了，再点击右上角 `发布`。成功后，你就拥有一个本地私有知识库增强的 LLM 了。

# 2.4. API 调用
为了在应用中能够调用刚发布的机器人，我们还需要一个兼容 OpenAI 格式的 API。

别急，FastGPT 也帮你搞定了！

如下图，在刚才发布的应用中间，点击 `发布渠道`-> `API 访问`，右侧点击新建，将密钥保存下来，这就是 api_key。

base_url 在哪？红色方框处自取👇

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/4c98543373cbfb13f73b58a87b65a02b.png)


有了 api_key 和 base_url，API 调用就很容易了，关注我的老朋友可能已经非常熟悉以下测试代码（记得 base_url 后面加上`/v1`）：

```
from openai import OpenAI

model_dict = {
    'fastgpt': {
        'api_key': 'fastgpt-xxx',
        'base_url': 'http://101.33.210.xxx:3000/api/v1',
        'model_name': 'glm-4'
    }
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
    model = 'fastgpt'
    llm = LLM_API(model_dict[model]['api_key'], model_dict[model]['base_url'], model_dict[model]['model_name'])
    user_question = "猴哥是谁"
    messages = [{"role": "user", "content": user_question},]
    print(llm(messages))
```

还记得么？上一篇中，我们采用 `chatgpt-on-wechat` 搭建了一个微信机器人。

如果把上述 api_key 和 base_url 放到 `chatgpt-on-wechat` 的配置文件 config.json 中，不就相当于让我们的微信机器人也拥有了基于私有知识库回答问题的能力？

感兴趣的小伙伴赶紧试试吧~

# 写在最后

如果说，OneAPI 帮你一键封装好所有 LLM 的调用接口，实现 **LLM 自由**~

那么，FastGPT 则为你的 LLM 插上了知识库的翅膀，实现**私有知识库自由**~

祝大家借助 OneAPI+FastAPI 玩转大模型，开发出更多 AI 创意应用。

如果本文对你有帮助，欢迎**点赞收藏**备用！


