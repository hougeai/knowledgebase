要列举 AI 绘画开源界的几个关键贡献，一定少不了 Stable Diffusion。

还记得前不久刚推出的 Stable Diffusion 3 么？

其背后的团队 Stability AI，真的是一波三折，其核心成员出走，成立了一个新公司：`Black Forest Labs` - 黑暗森林。

这不，刚刚开源了一款 AI 绘画模型，直接踢馆老东家，其生成效果，完全可以媲美闭源的 Midjourney。

今日分享，就带大家来体验一番，并在本地部署起来。

之前我的 AI 绘画，都是来自本地部署的 sd-webui。终于，我的 Stable Diffusion 2 该下线 - 光荣退休了？

No！No！No！

尽管 Flux.1 的表现可圈可点，不过要说能完全替代 sd，至少现阶段，还不至于。

我们先来实测体验一番~

## 1. Flux.1 简介

FLUX.1 AI 号称的优势有:

• 卓越的视觉质量: 生成具有出色细节和清晰度的图像。

• 精确的提示词遵循: 准确地将文本提示转化为图片，一次生成，无需抽卡。

• 多样化的风格: 支持广泛的艺术风格。

• 复杂场景生成: 创建精细详尽的场景。

真的有吹的那么神么？我们来实测体验一番

## 2. 在线体验

- 官网：[https://flux1ai.com/dev](https://link.zhihu.com/?target=https%3A//flux1ai.com/dev)
- modelscope: [https://www.modelscope.cn/studios/muse/flux_dev](https://link.zhihu.com/?target=https%3A//www.modelscope.cn/studios/muse/flux_dev)

我们以官网的地址为例，一起来体验一下。 使用非常简单，文本框输入你想要生成的内容，右侧一键 `Run`：

![img](https://pic3.zhimg.com/80/v2-e20e4d24158fe34a882c15d7a1a9c1d2_1440w.webp)

右侧提示框出现`分配到GPU`后，生成一张图像大概 30-50S 左右。

我用下面这个提示词实测了一下，第一次尝试在图片中生成中文，居然失败了！ 所以最好使用英文提示词。

```text
A Monkey holding up a sign with a rainbow in it, 
reading "猴哥 AI"
```

不过有一说一，这个 mokey 的毛发生成的还挺精细的~

![img](https://pic3.zhimg.com/80/v2-6f5942c859c69d48d8b9eb0873d59e4a_1440w.webp)

当然，下方还可以进行一番简单的设置，比如最基础的希望生成图像的宽和高：

![img](https://pic4.zhimg.com/80/v2-c186c69defa208400dab4fa69257712f_1440w.webp)

然后，我们把提示词修改一下，让它生成一只卡通猴子~

```text
A catoon monkey with smile holding up a sign with a rainbow in it, reading "AI".
```

哈哈，尽管并没完全按照指令生成。不过，个人感觉还是挺可爱的，用来做logo、做封面怎么样？

![img](https://pic3.zhimg.com/80/v2-c7f1668fcdd1ff89850a6ae17dbe6fc2_1440w.webp)

再来测试一个封面图，我让它写上 `Houge AI`：

```text
A round chocolate cake decorated with chocolate shavings, topped with the words Houge AI in white icing and garnished with red cherries. The cake is positioned on a white plate on a wooden table, with a coffee cup and saucer in the background.
```

![img](https://pic3.zhimg.com/80/v2-4ba66797326a13ca480b340d00dd5af2_1440w.webp)

接着，我们再从 AI 绘画社区中找一些垂类模型的提示词来实测一下：

```text
1girl,sweater,white background,
```

简单的提示词，默认是生成卡通类型的图像：

![img](https://pic2.zhimg.com/80/v2-165572785254b1279edcbee0435f074d_1440w.webp)

再给加点料：

```text
masterpiece,best quality,1girl,moyou,seductive smile,(Turtleneck_sweater_dress:1.5),(Thigh-high_boots:1.4),(Wide-brim_hat:1.3),(Autumn_foliage_background:1.3)
```

![img](https://pic4.zhimg.com/80/v2-1a802e812554d74db0b464965583605f_1440w.webp)

生成一张写实类的吧：

```text
official art,Best quality,masterpiece,ultra high res,((photorealistic:1.4)),((deep Focus)),raw photo,extremely delicate,intricate details,best shadow,1girl,upper body,beautiful,cool,smallface,detailed face,((detailed very long hair)),(pale skin),((brown eyes)),deep shadow,look away,film grain,low key,soft lighting,poised poise,dramatic angles,geometric shapes,contrasts of light and shadow,high-tech backdrop,crisp lines
```

![img](https://pic1.zhimg.com/80/v2-447c44a880bc02a25ed4afcaa13627dc_1440w.webp)

别的不说，细节绝对拉满。Asian girl 亚洲脸，能不能行？

![img](https://pic4.zhimg.com/80/v2-364d52749e87d0e9788a153eb0f6cf97_1440w.webp)

有一说一，Flux 在细节处理上已经足够逼真，不过写实类的还得是垂类大模型~

官方体验地址，因为 GPU 资源有限，高峰期容易排队失败~

但这是一个开源模型，我们完全可以本地跑起来，接着就带着大家实操一番~

## 3. 本地部署

Flux.1 根据模型大小，分为三个版本：

- Schnell：最快的模型。
- Dev：在速度和质量之间提供平衡，并支持更多定制选项。
- Flux.1 Pro：最强模型，模型不开源，只提供 API。

实测来看，开源最强，当之无愧！

**唯一的缺点，就是模型参数量太大了**，开源的两个版本都有 23.8G，就这一点，就拦住了不少玩家。

不过话说回来，模型参数量小，且还能打的，至少现阶段是不现实的。

## 3.1 模型下载地址

> 项目地址：[https://github.com/black-forest-labs/flux](https://link.zhihu.com/?target=https%3A//github.com/black-forest-labs/flux)

模型首发在 Huggingface 上，不过已经有同学迁移到了阿里的 modelscope 上。考虑到国内的小伙伴访问 Huggingface 比较困难，我们这次直接从 modelscope 下载。

两个初始模型有 23.8G：

![img](https://pic1.zhimg.com/80/v2-56f8c0b50df3a2ad8d092f45cfa71a5c_1440w.webp)

![img](https://pic4.zhimg.com/80/v2-3cc5f691dec2e47a2ede6d12894f305f_1440w.webp)

社区有小伙伴提供了量化版，体积小了一半，不过表现略差，不知道是不是我参数设置的原因，欢迎小伙伴们评论区交流。

![img](https://pic1.zhimg.com/80/v2-def71564320e828a17cea22f8e1674c4_1440w.webp)

附下载地址：

- schnell：[https://modelscope.cn/models/AI-ModelScope/FLUX.1-schnell/files](https://link.zhihu.com/?target=https%3A//modelscope.cn/models/AI-ModelScope/FLUX.1-schnell/files)
- dev：[https://modelscope.cn/models/AI-ModelScope/FLUX.1-dev/files](https://link.zhihu.com/?target=https%3A//modelscope.cn/models/AI-ModelScope/FLUX.1-dev/files)
- 量化版：[https://modelscope.cn/models/AI-ModelScope/flux-fp8/files](https://link.zhihu.com/?target=https%3A//modelscope.cn/models/AI-ModelScope/flux-fp8/files)

**！注意**：即便是量化后的 11.9G 模型，跑起来也至少需要 **16G** 显存的消费级显卡。

如果你的显存不足，可以接着往下看

## 3.2 ModelScope 实战

本地部署，我们这次采用阿里云的 GPU 服务器进行演示，如果你有本地 GPU 主机，当然下面是实操也是通用的。

首先，前往 modelscope 首页注册一个账号，新用户是有 GPU 免费使用额度的，选择下方的 `GPU 环境`，点击启动，你就可以拥有一台 24G 显存的云主机。

![img](https://pic4.zhimg.com/80/v2-8fd430f2492d4a246e1a71a0b90e0133_1440w.webp)

### Step1：下载 ComfyUI

实例启动后，打开一个终端，然后 git clone 下载 ComfyUI：

![img](https://pic1.zhimg.com/80/v2-df3518d1fb6b797d04eaf99629f1fbec_1440w.webp)

```text
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
```

### Step2：下载模型

实例镜像中默认安装好了 modelscope 下载命令，运行下方指令，下载我们所需的模型：

```text
# FLUX1-DEV
modelscope download --model=AI-ModelScope/FLUX.1-dev --local_dir ./models/unet/ flux1-dev.sft
modelscope download --model=AI-ModelScope/flux-fp8 --local_dir ./models/unet/ flux1-dev-fp8.safetensors

# text encoder model
modelscope download --model=AI-ModelScope/flux_text_encoders --local_dir ./models/clip/ t5xxl_fp16.safetensors
modelscope download --model=AI-ModelScope/flux_text_encoders --local_dir ./models/clip/ clip_l.safetensors
modelscope download --model=AI-ModelScope/flux_text_encoders --local_dir ./models/clip/ t5xxl_fp8_e4m3fn.safetensors

# vae
modelscope download --model=AI-ModelScope/FLUX.1-dev --local_dir ./models/vae/ ae.sft
```

给大家看下下载速度，300-400M/s，超快~

```text
Downloading:  82%|███████████████████████████████████████████████████████████████████████████████████████████████▍                     | 18.1G/22.2G [00:54<00:11, 374MB/s]
```

如果你是在其他云主机 or 本地服务器上，需要首先安装 modelscope download 工具：

```text
pip install modelscope
```

### Step3：启动 ComfyUI

ComfyUI 提供了一键启动脚本，运行下方指令，即可打开一个 web 客户端：

```text
python main.py
```

默认端口号是：`http://127.0.0.1:8188`。

不过，modelscope 上的云主机是没有公网 IP 的，你在本地浏览器当然是打不开的，怎么搞？

你需要一个内网穿透工具~

有没有最便捷的方式，实现内网穿透？

当然，强推 `cloudflared`

### Step4：cloudflared 安装和使用

> 仓库：[https://github.com/cloudflare/cloudflared](https://link.zhihu.com/?target=https%3A//github.com/cloudflare/cloudflared) **cloudflared 是啥？**

海外云厂商 Cloudflare 提供的一个命令行工具，用于创建安全的隧道，以便将本地服务暴露到互联网。

首先下载最新版的 cloudflared Debian 软件包（.deb 文件），并使用 dpkg 工具直接安装，无需编译。

```text
wget https://mirror.ghproxy.com/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

dpkg -i cloudflared-linux-amd64.deb
```

看到如下输出，则说明安装成功：

```text
(正在读取数据库 ... 系统当前共安装有 83567 个文件和目录。)
准备解压 cloudflared-linux-amd64.deb  ...
正在解压 cloudflared (2024.6.1) 并覆盖 (2024.6.1) ...
正在设置 cloudflared (2024.6.1) ...
```

此外，还可以查看下cloudflared版本：

```text
cloudflared -v
# 输出
cloudflared version 2024.6.1
```

由于 ComfyUI 的服务在 8188 端口上，所以我们用 cloudflared 开启一个监听隧道：

```text
cloudflared tunnel --url http://127.0.0.1:8188
```

监听成功后，找到下面这个临时的 url：

![img](https://pic3.zhimg.com/80/v2-9a8c62dde8ee7095c964df6f8ca91b1a_1440w.webp)

打开浏览器看看吧：

![img](https://pic2.zhimg.com/80/v2-d6a9b3590fe91c26f66972899bef258d_1440w.webp)

大功告成，开始 ComfyUI 之旅吧~

### Step5：愉快玩耍

首先，把 flux1-dev 模型的配置文件下载到本地：[https://modelscope.oss-cn-beijing.aliyuncs.com/resource/flux1-dev-test.json](https://link.zhihu.com/?target=https%3A//modelscope.oss-cn-beijing.aliyuncs.com/resource/flux1-dev-test.json)

然后，点击 `Load` 加载配置文件：

![img](https://pic3.zhimg.com/80/v2-154ddf3331dba6d491515079b2ad1a32_1440w.webp)

最后，输入你想要生成的提示词，以及图片大小设置。点击 `Queue Prompt` 开始生成，流程中的高亮模块，说明正在加载模型：

![img](https://pic1.zhimg.com/80/v2-79da7d0b1e5b16d1f5733a9292cfbc30_1440w.webp)

我这边实测，1360 x 768 大小的图像，量化版本的模型大约占用 14G 显存，所以一张消费级显卡完全够用。

有一说一：ModelScope 的云端 GPU 环境跑模型还是很爽的，尤其是下载 ModelScope 上的模型，速度直接拉满；唯一的缺陷是，模型权重文件等无法持久保存，一旦断掉后，还得重头再来一般。

## 写在最后

本文实测了地表最强开源 AI 绘画模型，手把手教你从在线体验到本地部署。就算你没有土豪级显卡，也可以用云端 GPU 来玩耍。

不得不说，这波 AI 绘画的更新迭代，看得人眼花缭乱、热血沸腾！

不知道下一个惊喜又会是谁呢？让我们拭目以待~

关于开源 AI 大模型的文章，我打算做成一个专栏，目前已收录：

- [CogVideo 实测，智谱「清影」AI视频生成，全民免费，连 API 都开放了！](https://zhuanlan.zhihu.com/p/711213593)
- [全网刷屏的 LLaMa3.1，2分钟带你尝个鲜](https://zhuanlan.zhihu.com/p/710991720)
- [SenseVoice 实测，阿里开源语音大模型，识别效果和效率优于 Whisper](https://zhuanlan.zhihu.com/p/710345380)
- [EasyAnimate-v3 实测，阿里开源视频生成模型，5 分钟带你部署体验，支持高分辨率超长视频](https://zhuanlan.zhihu.com/p/710131990)
- [开源的语音合成项目-EdgeTTS，无需部署无需Key](https://zhuanlan.zhihu.com/p/703686916)
- [一文梳理ChatTTS的进阶用法，手把手带你实现个性化配音](https://zhuanlan.zhihu.com/p/703678333)

后面会定期更新，感兴趣的小伙伴可以继续关注，或者留言告诉我想看什么大模型实测效果。