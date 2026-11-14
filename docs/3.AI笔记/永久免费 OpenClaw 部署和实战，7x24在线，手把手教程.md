
最近 OpenClaw 爆火，不只是在自媒体上！

很多朋友被各种配置劝退，被高额Token费劝退！

今日分享，写给想体验 `OpenClaw` 的朋友：

一份`OpenClaw 从配置、部署到实战`的完整指南，**全程免费**，放心食用！

全文三部分：

- 申领 Nvidia NIM API
- HuggingFace Space部署
- OpenClaw 实战

## 1. Nvidia 免费模型
> 地址：[https://build.nvidia.com/](https://build.nvidia.com/)

浏览器中打开上面的地址，国内直达，注册一个`Nvidia`账号，注册完成后右上角创建`APIKEY`。

为啥选 `Nvidia NIM`？

因为这里部署了 SOTA 的开源模型，兼容 `OpenAI`，免费调用（最新`GLM 5`也上了）：

![](https://i-blog.csdnimg.cn/img_convert/1159a734d58fc71c9436bded20d70468.jpeg)

## 2. HuggingFace Space部署

为啥选这个？

`HuggingFace` 提供免费的 CPU Basic 实例，`2c16g` 这个配置足以玩转`OpenClaw` 。

**注：免费 Space 实例有以下约束：**

- 计算资源：固定为 2 vCPU 和 16 GB RAM。

- 存储空间：默认提供 50GB 临时磁盘空间。重启后，文件会丢失。

- Repo 大小：Space 自身的代码仓库（Git/LFS）限制在 1GB 以内。

所以，我们通过 `HuggingFace Dataset` 持久化保存历史对话记录，确保`OpenClaw`状态永久在线。

### 2.1 新建 HuggingFace Space

具体步骤：
- 进入 HuggingFace Spaces 页面：[https://huggingface.co/spaces](https://huggingface.co/spaces)
- 点击 `+ New Space`
- SDK: 选择 Docker。
- Template: 选择 Blank。
- Privacy: 选择 Private。

### 2.2 新建 HuggingFace Dataset

从个人头像页面，点击 `+ New Dataset`：

![](https://i-blog.csdnimg.cn/img_convert/2fdcccf9bb909a76fabdc8fc7862474a.png)

Privacy: 还是选择 Private，因为这里保存的是你个人数据。

**注**：新建的 space 和 dataset 都在个人页面 Profile 找到。

### 2.3 新建 Access Token

从个人头像页面，点击 `Access Tokens`。

`Token Type` 选择 Write（因为要写入）：

![](https://i-blog.csdnimg.cn/img_convert/c43ddc18f02ab8029033f267ac9dcbd8.png)

复制保存，下面要用。

### 2.4 配置 HuggingFace Space

回到刚刚创建的 Space，右上角点击 `Settings`，拉到最下面找到 `Variables and Secrets`：

![](https://i-blog.csdnimg.cn/img_convert/0f9140dc6c3ff77bbcdd02f823ca2f79.png)

参考上图，完成上述字段配置，不同字段说明如下：

**变量：**
- `OPENAI_API_BASE`：如果是用的 `Nvidia NIM`，那就是`https://integrate.api.nvidia.com/v1`;
- `MODEL`：模型ID，比如`z-ai/glm4.7`；
- `HF_DATASET`：刚刚新建的数据集，命名格式为 `用户名/数据集名`

**密钥：**
- `OPENAI_API_KEY`：对应上面`OPENAI_API_BASE`的密钥；
- `HF_TOKEN`：2.3 部分创建的`Access Tokens`
- `OPENCLAW_GATEWAY_PASSWORD`：连接 `OpenClaw UI` 的密码，自己设置，后面会用到。

### 2.5 三步完成部署

回到刚刚创建的 Space，如下图新建三个文件：

![](https://i-blog.csdnimg.cn/direct/b84631b611244e1186c21550674e92f7.png)

三个文件的完整代码和功能介绍如下：

- `sync.py`：负责和 Dataset 同步数据，实现配置文件持久化

```
import os
import sys
import tarfile
from huggingface_hub import HfApi, hf_hub_download

api = HfApi()
repo_id = os.getenv("HF_DATASET")
token = os.getenv("HF_TOKEN")
FILENAME = "latest_backup.tar.gz"

def restore():
    try:
        if not repo_id or not token:
            print("Skip Restore: HF_DATASET or HF_TOKEN not set")
            return
        
        # 直接下载最新文件
        print(f"Downloading {FILENAME} from {repo_id}...")
        path = hf_hub_download(repo_id=repo_id, filename=FILENAME, repo_type="dataset", token=token)
        
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(path="/root/.openclaw/")
        print(f"Success: Restored from {FILENAME}")
        return True
    except Exception as e:
        # 如果是第一次运行，仓库里没文件，报错是正常的
        print(f"Restore Note: No existing backup found or error: {e}")

def backup():
    try:
        if not repo_id or not token:
            print("Skip Backup: HF_DATASET or HF_TOKEN not set")
            return

        with tarfile.open(FILENAME, "w:gz") as tar:
            # 备份关键数据
            paths_to_backup = [
                "/root/.openclaw/sessions",
                "/root/.openclaw/agents/main/sessions",
                "/root/.openclaw/openclaw.json"
            ]
            for p in paths_to_backup:
                if os.path.exists(p):
                    arcname = p.replace("/root/.openclaw/", "")
                    tar.add(p, arcname=arcname)
        
        # 上传并覆盖
        api.upload_file(
            path_or_fileobj=FILENAME,
            path_in_repo=FILENAME,
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
        print(f"Backup {FILENAME} Success (Overwritten).")
    except Exception as e:
        print(f"Backup Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "backup":
        backup()
    else:
        restore()
```

- `start-openclaw.sh`：启动和运行 `openclaw`

```
#!/bin/bash
set -e

# 1. 补全目录
mkdir -p /root/.openclaw/agents/main/sessions
mkdir -p /root/.openclaw/credentials
mkdir -p /root/.openclaw/sessions

# 2. 执行恢复
python3 /app/sync.py restore

# 3. 处理 API 地址
CLEAN_BASE=$(echo "$OPENAI_API_BASE" | sed "s|/chat/completions||g" | sed "s|/v1/|/v1|g" | sed "s|/v1$|/v1|g")

# 4. 生成配置文件
cat > /root/.openclaw/openclaw.json <<EOF
{
  "models": {
    "providers": {
      "nvidia": {
        "baseUrl": "$CLEAN_BASE",
        "apiKey": "$OPENAI_API_KEY",
        "api": "openai-completions",
        "models": [
          { "id": "$MODEL", "name": "$MODEL", "contextWindow": 128000 }
        ]
      }
    }
  },
  "agents": { "defaults": { "model": { "primary": "nvidia/$MODEL" } } },
  "commands": {
    "restart": true
  },
  "gateway": {
    "mode": "local", "bind": "lan", "port": $PORT,
    "trustedProxies": ["0.0.0.0/0"],
    "auth": { "mode": "token", "token": "$OPENCLAW_GATEWAY_PASSWORD" },
    "controlUi": { "allowInsecureAuth": true }
  }
}
EOF

# 5. 启动定时备份 (每 1 小时)
(while true; do sleep 3600; python3 /app/sync.py backup; done) &

# 6. 运行
openclaw doctor --fix
exec openclaw gateway run --port $PORT
```

- `Dockerfile`：容器化环境配置

```
FROM node:22-slim

# 1. 基础依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git openssh-client build-essential python3 python3-pip \
    g++ make ca-certificates && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir huggingface_hub --break-system-packages

# 2. 安装 OpenClaw
RUN npm install -g openclaw@latest --unsafe-perm

# 3. 设置工作目录并拷贝脚本
WORKDIR /app
COPY sync.py .
COPY start-openclaw.sh .
RUN chmod +x start-openclaw.sh

# 4. 环境变量
ENV PORT=7860 HOME=/root

EXPOSE 7860
CMD ["./start-openclaw.sh"]
```

创建好三个文件，打好 `commit`，space 会自动触发构建，执行代码。
> 注：每次`commit`都会触发自动构建，所以要谨慎`commit`。

当然，熟悉`git`操作的朋友，也可以在本地建好文件 push 上去。

运行成功后，在 space 点击 `logs` 可查看运行状态：

```
◇  Gateway connection ─────────────────────╮
│                                          │
│  Gateway target: ws://10.108.65.42:7860  │
│  Source: local lan 10.108.65.42          │
│  Config: /root/.openclaw/openclaw.json   │
│  Bind: lan                               │
│                                          │
├──────────────────────────────────────────╯
2026-02-13T03:09:42.149Z [canvas] host mounted at http://0.0.0.0:7860/__openclaw__/canvas/ (root /root/.openclaw/canvas)
2026-02-13T03:09:42.210Z [heartbeat] started
```

看到上方日志，恭喜你，你的`openclaw`已成功启动！

打开你的 Space 地址看看吧：

格式为 `https://{user}-{space}.hf.space/`

### 2.6 UptimeRobot 定期保活

因为 HuggingFace 默认会关闭48小时内无访问的 space，其判断依据是：
- 是否有外部请求 `https://xxx.hf.space`；
- 是否维持有效`wss`连接；
- 内部定时任务不计入活跃;

所以，我们需要执行cron计划，定时访问你的 space。

怎么搞？

前往 [https://dashboard.uptimerobot.com/](https://dashboard.uptimerobot.com/) 注册一个免费账号。

点击 "Add New Monitor"（添加新监控）：
- `Monitor Type`: 选择 HTTP(s)
- `URL`: 你的 Space 公网地址
- `Monitoring Interval`: 免费版最低支持每 5 分钟访问一次。



## 3. OpenClaw 实战

打开你的前端UI控制台：`https://{user}-{space}.hf.space/`

首次登录是未连接状态。

参考下图，填入刚才你设置的登录密码，状态变成 `Connected` 即可：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0a35f589d1b54994beeb8ffa5572b0ae.png)

终于，在最上方的 `chat` 可以和它愉快聊天了~

不过，在这之前，还需要给它一个人设，让它**说人话**！

### 3.1 人设设定

左侧找到 Agent，这里重点关注两个文件：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bb298e77bfe1441e8b4b1fae05e29233.png)

- `SOUL.md`: 是AI的人设，让AI知道它是谁；

- `user.md`：是你的人设，是AI眼中的你；

以下是笔者的人设，供各位参考：
- `SOUL.md`:
```
_你不是聊天机器人。你是个靠谱的助手。_
##核心原则
尽量用中文和我对话
**认真做事,别敷衍。**少说"好的!马上帮您处理!",直接动手。
**有自己的想法。**
可以不同意,可以有偏好,可以觉得有些东西不太行。
**先自己想办法。**翻文件、看上下文、搜一搜。实在搞不定再问。目标是带答案
回来,不是带问题回来。
**用能力赢信任。**
用户给了你权限,别搞砸。对外的事(发邮件、发推)要谨慎真。对内的事(读文件、
整理资料)可以大胆。
**记住你是客人。**你能看到别人的消息、文件、日程,甚至家里的设备。
## 边界
-不确定的对外操作,先问。
-别发半成品消息到聊天软件。
## 风格
该简洁时简洁,该详细时详细。
像个靠谱同事。可以直接,可以有态度,可以指出问题
不拍马屁。不当应声虫。就做个靠谱的。
##记忆
每次对话你都是新的。这些文件就是你的记忆。读它们,更新它们。
```
- `user.md`：

```
**Name:**
猴哥
**What to call them:**
猴哥
- **Timezone:** Asia/Shanghai
-**Notes:**晚上10点后别打扰
## Context
###工作相关
-做AI应用、小程序、写公众号
-讨厌啰嗦，喜欢直接给结果
### 偏好
-说话直接,别拐弯抹角
```


有了这两个文件，

AI 会懂你，会陪你，还能自我进化。

接下来，你只需要在 `chat` 中和它说人话，让它帮你干活就 Ok 了。

比如你可以。。。

接着往下看👇

### 3.2 添加模型

让它查查现在的模型配置：

![](https://i-blog.csdnimg.cn/img_convert/9717534d33bbe59642d0457e4513851c.png)

看看，贴心给出了三种方法：

![](https://i-blog.csdnimg.cn/img_convert/e1a5a8f392de432dafc478170475bd6f.png)

让它继续帮忙加模型：

![](https://i-blog.csdnimg.cn/img_convert/545c8ef70e6f03c3ff5158bee888a65f.png)

模型加好了：

![](https://i-blog.csdnimg.cn/img_convert/c74f96decd19ed7fdca0987302e9e1b3.png)

我让它帮我自动重启，完成之后，怎么验证？

控制台左侧`config`查看配置文件:

![](https://i-blog.csdnimg.cn/img_convert/600007abad209ecfa0169c9ae8a9c7d2.png)

所以，不懂配置没关系，它懂就行。

### 3.3 添加飞书

默认插件中不支持飞书，我来问问他：

![](https://i-blog.csdnimg.cn/img_convert/0ad34060152bf605dccc29e01812a22a.png)

看它教你具体步骤：

![](https://i-blog.csdnimg.cn/img_convert/902f8ee8fa8b9fadaed2ee4a11169a6c.png)


让它帮我安装插件并完成配置：


![](https://i-blog.csdnimg.cn/img_convert/4dcda0224e5c26c029497da2f9631c7b.png)

这时，只需按照它给的步骤去飞书开放平台创建一个bot，拿到上面两个值，发给它即可。

回到配置文件中看看，发现已经帮我配置好了：

![](https://i-blog.csdnimg.cn/img_convert/f9abb3766fb28a534b77a0cae866f911.png)

再问它，怎么给飞书发消息：

![](https://i-blog.csdnimg.cn/img_convert/2dddec345ec9f12c9e7fd0d069f2afd0.png)

根据它的指令，需要去飞书配置事件：

![](https://i-blog.csdnimg.cn/img_convert/ef64a45dee6080ff5a96421db9502936.png)


配置成功后，去飞书给它发条消息试试吧：

![](https://i-blog.csdnimg.cn/img_convert/b370b690cc568665eb27ec69f3998b07.png)

搞定！

接下来，可以直接在飞书中指挥它干活了~

尽情发挥你的想象力!


## 写在最后

本文分享了`OpenClaw 部署和实战`的全程免费版。

如果对你有帮助，不妨**点赞收藏**备用。

看到这里的你，如果对 `OpenClaw` 还有一丝好奇或期待，强烈推荐你去试试。

也许，你也会发现：

**以前**：AI 是工具，冰冷。

**现在**：AI 是伙伴，温暖。
