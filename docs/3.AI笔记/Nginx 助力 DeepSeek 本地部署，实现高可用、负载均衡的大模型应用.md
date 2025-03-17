最近被 DeepSeek 官网平替的各种文章刷屏，原因无它：太火了！

```
服务器繁忙，请稍后再试。
```

为此，也催生了大量 DeepSeek 本地部署的需求。

尽管本地部署对资源要求较高，但优势也非常显著：
- 敏感数据不出内网；
- 无公网传输延迟；
- 无调用限制。

前几篇和大家分享了如何采用 Ollama 本地部署 DeepSeek-R1。

如果只是自己玩玩，当然没问题。

如果要嵌入到自己的AI应用中，一旦并发量上来，就得考虑高可用性。

怎么搞？

今天分享，将采用以下**三步走**策略，演示如何实现**高可用**的大模型应用：
- **Ollama** 部署多个 DeepSeek 实例（生产环境推荐 vLLM）；
- **Nginx** 实现负载均衡；
- **Locust** 实现压力测试。

## 1. 写在前面
### 1.1 选多大的模型？

显卡、显存，决定了能跑多大的模型。

尽管 DeepSeek 已经完成了多国产 GPU 的适配，不过当前来看，普适性最高的还得是 Nvidia 家的显卡，简称 N 卡。

不同参数量模型对显存的需求，可参考下表（*建议收藏*）：

| 显卡型号 | 显存 | 0.5B | 1B | 3B | 7B | 13B | 32B | 70B |
|---------|------|------|----|----|----|----|-----|-----|
| RTX 5090 | 32GB | FP16 2GB | FP16 3GB | FP16 8GB | FP16 19GB | INT8 17GB | INT4 21GB | ❎ |
| RTX 4090 | 24GB | FP16 2GB | FP16 3GB | FP16 8GB | FP16 19GB | INT8 17GB | INT4 21GB | ❎ |
| RTX 4080 | 16GB | FP16 2GB | FP16 3GB | FP16 8GB | INT8 10GB | INT4 9GB | ❎ | ❎ |
| RTX 3080 | 12GB | FP16 2GB | FP16 3GB | FP16 8GB | INT8 10GB | INT4 9GB | ❎ | ❎ |
| RTX 2080 | 8GB | FP16 2GB | FP16 3GB | FP16 8GB | INT4 5GB | ❎ | ❎ | ❎ |
| RTX 2060 | 6GB | FP16 2GB | FP16 3GB | INT8 4GB | INT4 5GB | ❎ | ❎ | ❎ |

### 1.2 为什么选 Ollama

相比 vLLM / SGLang 等部署方案，Ollama 的门槛最低，几乎人人均可上手。

模型默认采用 INT 4 量化，同等显存下可以跑更大的模型。

在单张显卡显存不足的情况下，支持自动将模型切分到多张显卡进行推理。

支持自动模型加载与卸载，推理时按需动态分配，闲置时降低显存占用，极大提高了资源利用率。


### 1.3 为什么是 DeepSeek-R1

简单梳理下 DeepSeek-R1 的前世今生。

所谓**满血 DeepSeek-R1**，即 **DeepSeek-R1-671B**，它基于 DeepSeek-V3-Base进行训练，并全面超越了 DeepSeek-V3。区别在于 R1 具备深度推理能力，而 V3 没有。

但 671B 的模型显然不是我等大众能玩的，所以 DeepSeek 团队又用 DeepSeek-R1 蒸馏得到了 6 个小模型，这就是你在 Ollama Library 中看到的:

![](https://i-blog.csdnimg.cn/img_convert/3eb59e67daee6898f138287b74ec2d5d.png)

从 1.5b 到 70b，分别来自开源的 Llama 和 Qwen 架构。比如 `DeepSeek-R1-32b` 就是来自 qwen2，你要知道这个开源模型，竟然击败了 `GPT-4o`、`Claude-3.5-Sonnet`、`o1-mini` 这三个闭源模型。

![](https://i-blog.csdnimg.cn/img_convert/26643e0fd8ce89515a856c6de39dce85.png)


**所以，在资源允许条件下，推荐选用 `32b` 模型，真的很强！**
- 一张 4090 能跑；
- 两张 4080 也行。


## 2. Ollama 部署 DeepSeek 实例
关于 Ollama 的使用，可以翻看之前教程：[本地部署大模型？Ollama 部署和实战，看这篇就够了](https://blog.csdn.net/u010522887/article/details/140651584)

这里我们采用 docker 容器进行部署，方便动态扩缩容。

- 根据自己的显存容量，指定显卡设备号：
```
# GPU 单卡
sudo docker run -d --gpus "device=1" -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama ollama/ollama
# GPU 多卡
sudo docker run -d --gpus '"device=1,2"' -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama ollama/ollama
```

假设要起两个 DeepSeek 实例，只需映射两个端口出来，并指定不同的实例名称：
- 实例1：3001 端口
```
sudo docker run -d --gpus "device=0" -v ollama:/root/.ollama -p 3001:11434 --restart unless-stopped --name ollama1 ollama/ollama
```

- 实例2：3002 端口
```
sudo docker run -d --gpus "device=1" -v ollama:/root/.ollama -p 3002:11434 --restart unless-stopped --name ollama2 ollama/ollama
```

然后，分别进入容器，拉起 DeepSeek 模型，根据显存拉对应参数量的模型:

```
sudo docker exec -it ollama1 /bin/bash
ollama run deepseek-r1:32b
```


## 3. Nginx 负载均衡

### 3.1 Nginx 安装

Linux 下推荐编译安装最新稳定版：
```
wget https://nginx.org/download/nginx-1.26.3.tar.gz
tar -xf nginx-1.26.3.tar.gz
cd nginx-1.26.3
./configure
make -j 4
sudo make install
```
默认安装位置：/usr/local/nginx/sbin/nginx

如果环境变量中找不到，需建立软连接：

```
sudo ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx
```

执行：nginx -v 返回版本号，说明安装成功。

nginx 服务启动 & 停止 & 重启命令如下：

```
nginx # 启动
nginx -s stop # 关闭
nginx -s reload # 重启
nginx -t # 测试配置文件
```

Nginx 依赖配置文件运行，因此在启动 nginx 服务之前，还需一番配置。

### 3.2 Nginx 配置

默认配置文件在哪？

```
sudo nginx -t
nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful
```

不过，为了方便后续启用多个 nginx 服务，可以新建 deepseek 的配置文件，内容如下：

```
upstream deepseek_api {
    random;  # 负载均衡策略：随机选择一个服务器
    server 127.0.0.1:3002;
    server 127.0.0.1:3004;
}

server {
    listen 3008; # 当前nginx服务监听端口
    server_name _;  # 允许任何域名访问
    charset utf-8;
    access_log /var/log/nginx/deepseek.log; # 日志文件名称
    error_log /var/log/nginx/deepseek.error warn;  # 错误日志文件名称 warn级别 
    
    location / {
        proxy_pass http://deepseek_api;
    }
}

```

然后在默认的 nginx.conf 中用 include 指令引入这些配置文件。

![](https://i-blog.csdnimg.cn/img_convert/38a3898bcbbff3cef10b117e2ee23efc.png)

再次检查配置文件是否有问题：

```
sudo nginx -t
```

最后，启动 nginx 服务：

```
sudo nginx
```

打开上方指定的 nginx 服务的端口号：http://localhost:3008/，出现下图，代表成功路由到了 ollama 实例。

![](https://i-blog.csdnimg.cn/img_convert/54f814e1f26828c5feb61b7d5644c7bc.png)


## 4. Locust 压力测试

为了验证` 负载均衡`后，能抗住多大并发量，还需要进行压力测试。

这里采用`Locust`这款开源工具，pip 一键安装：

```
pip install locust
```


### 4.1 编成测试脚本
新建 ollama.py，脚本如下：
```
from locust import HttpUser, task, between

# 模拟 http 请求的用户
class OllamaUser(HttpUser):
    wait_time = between(0, 2)  # 每个请求的间隔时间
    @task
    def generate_text(self):
        headers = {"Content-Type":"application/json"}
        data = {
            "model": "deepseek-r1:1.5b",
            "prompt": "仿照苏轼写一首宋词",
            "stream": True
        }
        self.client.post("/api/generate", headers=headers, json=data, timeout=60)
```


### 4.2 启动 Web 界面

```
$ locust -f ollama.py
[2025-02-15 20:34:42,926] ps/INFO/locust.main: Starting Locust 2.32.9
[2025-02-15 20:34:42,927] ps/INFO/locust.main: Starting web interface at http://0.0.0.0:8089
```

默认端口号 8089，打开后进行模拟测试，填入刚才 Nginx 的服务地址：

![](https://i-blog.csdnimg.cn/img_convert/3fffa94a4f0db7d9acf4f72a5fb6b3b7.png)

### 4.3 开启测试

点击 start 即可，我这里模拟压测了 10 分钟，两个模型实例，峰值时 10 个用户并发，测试结果如下：

![](https://i-blog.csdnimg.cn/img_convert/885f4a45c4ba4fb223368f2bf19d05b5.png)

![](https://i-blog.csdnimg.cn/img_convert/18aa40504a2c556e76aed89848664272.png)

大家可以根据`Failures`情况，进行扩缩容。

## 写在最后
本文带大家采用 **Ollama** + **Nginx** 实现了**高可用**的大模型应用，并采用**Locust** 进行模拟压力测试，为应用上线做好准备。

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。


