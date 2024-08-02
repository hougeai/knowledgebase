# 前言

本次分享将带领大家从 0 到 1 完成一个基于 OCR 和 LLM 的视频字幕提取和智能视频问答项目，通过 OCR 实现视频字幕提取，采用 ErnieBot 完成对视频字幕内容的理解，并回答相关问题，最后采用 Gradio 搭建应用。本项目旨在帮助初学者快速搭建入门级 AI 应用，并分享开发过程中遇到的一些坑，希望对感兴趣的同学提供一点帮助。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d29f61f52756da97862757452596c963.png)

# 项目背景和目标

**背景：**

光学字符识别（Optical Character Recognition，简称 OCR）是一种将图像中的文字转换为机器编码文本的过程。通常一个 OCR 任务的处理流程如下图所示：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f0b50623a63d8f915d339d81114260db.png)
PP-OCR 是百度面向产业应用提供的 OCR 解决方案，底层采用的是两阶段 OCR 算法，即检测模型+识别模型的组成方式，其处理流程包括如下几个步骤：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a84fdcd2197e5f0022d04a15c2f41ec9.png)

而视频字幕提取就是对视频中的每帧图像提取出其中的字幕文字。

大语言模型（LLM，Large Language Model）是一种先进的自然语言处理技术，当前主流的 LLM 包括 GPTs、百度文心一言、阿里通义千问、字节豆包等，而 ErnieBot 正是基于百度文心一言的智能体框架。基于提取的视频字幕，借助 LLM 强大的语义理解能力，我们可以完成很多有意思的任务，比如让 LLM 帮我们提取视频的关键信息，甚至是基于视频回答我们的问题，减轻当前大模型常见的“幻觉”-胡说八道，比如下面这张图：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/adc2e4c5d7dec668defcf59db2922864.png)

**目标：**

- 掌握如何用 paddlepaddle 深度学习框架搭建一个文本识别模型；
- 掌握文本识别模型架构的设计原理以及构建流程；
- 掌握如何利用已有框架快速搭建应用，满足实际应用需求；

# 百度 AI Studio 平台

本次实验将采用 AI Studio 实训平台中的免费 GPU 资源，在平台注册账号后，点击创建项目-选择 NoteBook 任务，然后添加数据集，如下图所示，完成项目创建。启动环境可以自行选择 CPU 资源 or GPU 资源，创建任务每天有 8 点免费算力，推荐大家使用 GPU 资源进行模型训练，这样会大幅减少模型训练时长。

创建项目的方式有两种：

- 一是在 AI Studio 实训平台参考如下方式，新建项目。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/34dd553d540fe7e51f021b45945cf536.png)

- 二是直接 fork 一个平台上的已有项目，比如本次实验，可以选择[【飞桨 AI 实战】实验 6-基于 PP-OCR 和 ErnieBot 的智能视频问答](https://aistudio.baidu.com/projectdetail/7892508)的最新版本，然后点击 fork，成功后会在自己账户下新建一个项目副本，其中已经挂载了源项目自带的数据集和本次项目用到的核心代码。

**为了快速跑通项目流程，建议直接 fork 源项目。**

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e38638fc54caaaf1ba8ea85b9c0d0f24.png)

# 从零开始实战

## 1 基础：动手跑通 CRNN 文本识别任务

> 核心代码在：`core/` 文件夹下

背景：CRNN 是较早被提出也是目前工业界应用较多的文本识别方法。本节将详细介绍如何基于 PaddleOCR 完成 CRNN 文本识别模型的搭建、训练、评估和预测。数据集采用 CaptchaDataset 中文本识别部分的 9453 张图像，其中前 8453 张图像在本案例中作为训练集，后 1000 张则作为测试集。

### 1.1 数据准备

**step 1:解压缩数据**

```
# 打开终端
# 解压子集  -d 指定解压缩的路径，会在data0文件夹下生成
unzip data/data57285/OCR_Dataset.zip -d data0/
# 查看文件夹中文件数量
ls data0/OCR_Dataset/|wc -l
```

**step 2: 准备数据部分代码**

```
# 数据读取类在 reader.py, 可以执行如下脚本查看训练数据
python reader.py
```

可视化结果如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c6a7a340d0a05c5641e626f62397738e.png)

### 1.2 模型构建

本次实验我们将采用最简单的网络架构来搭建 CRNN 网络 并构建损失函数 CTCLoss

**step 1: 搭建 CRNN 网络**

```
# 定义模型类
net.py
```

**step 2: 定义损失函数 CTCLoss**

```
# 定义 loss, 位于 net.py
class CTCLoss(paddle.nn.Layer):
    def __init__(self, batch_size):
        """
        定义CTCLoss
        """
        super().__init__()
        self.batch_size = batch_size

    def forward(self, ipt, label):
        input_lengths = paddle.full(shape=[self.batch_size],fill_value=LABEL_MAX_LEN + 4,dtype= "int64")
        label_lengths = paddle.full(shape=[self.batch_size],fill_value=LABEL_MAX_LEN,dtype= "int64")
        # 按文档要求进行转换dim顺序
        ipt = paddle.tensor.transpose(ipt, [1, 0, 2])
        # 计算loss
        loss = paddle.nn.functional.ctc_loss(ipt, label, input_lengths, label_lengths, blank=10)
        return loss
```

### 1.3 模型训练

编写训练脚本 `train.py` 如下，主要是定义好数据集、模型，配置训练相关参数：

```
# 运行训练脚本
python train.py
```

训练过程如下图所示：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/05a736b034194fd96c986500bf7b4059.png)

### 1.4 模型预测

编写预测脚本 `predict.py`

```
# 运行预测脚本
python predict.py
```

调用模型预测函数：得到生成图像的可视化结果

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3c7c7cf98e99e195d6c1ef0a70e67623.png)

## 2 进阶：基于[PP-OCR](https://github.com/PaddlePaddle/PaddleOCR)和[ErnieBot](https://github.com/PaddlePaddle/ERNIE-SDK)搭建应用

> 核心代码在：`ocr-bot/` 文件夹下

### 2.1 环境准备

本项目主要用到了以下安装包，可以采用 `pip install -r requirements.txt` 一键安装。

```
paddlepaddle
paddleocr==2.7.0
erniebot
moviepy
gradio
```

### 2.2 需求分析
本项目主要需要完成两个功能：`视频字幕提取` 和 `智能视频问答`。

`视频字幕提取`：
- 中文视频能提取出其中的字幕
- 英文视频能自动生成中文字幕
- 生成 SRT 格式的字幕文件
- 将字幕文件内嵌到视频中去

`智能视频问答`：
- 提取视频中的关键信息，完成视频摘要
- 根据字幕信息，回答用户针对视频的提问
- 根据字幕信息，定位关键信息对应的时间片段

### 2.2 核心功能实现
#### 2.2.1 基于 PP-OCR 完成字幕提取
采用 opencv 读取视频中的图片，引入 paddleocr 包实现图片中的字幕提取，同时记录时间信息，为了快速完成 demo 展示，这里采用每秒抽取一帧图像，且只用图像底部包含字幕的部分进行文字识别，核心代码如下：

```
def get_video_ocr(vid_path='/home/aistudio/demo/trim.mp4'):
    ocr = PaddleOCR(use_angle_cls=True, debug=False)
    src_video = cv2.VideoCapture(vid_path)
    fps = int(src_video.get(cv2.CAP_PROP_FPS))
    total_frame = int(src_video.get(cv2.CAP_PROP_FRAME_COUNT)) # 计算视频总帧数
    save_text = []
    for i in tqdm(range(total_frame)):    
        success, frame = src_video.read()
        if i % (fps) == 0 and success:
            result = ocr.ocr(frame[-120:-30, :], cls=True)[0] # 只抽取下半部分图片
            if len(result)> 0: 
                res = result[0][1][0]
                start_time = i//fps
                save_text.append([start_time, res])
    # 将数据转换为字典，合并重复的字幕
    subtitles = {}
    for (time, text) in save_text:
        if text in subtitles:
            subtitles[text].append(time)
        else:
            subtitles[text] = [time]
    subtitle_path = vid_path.replace('.mp4', '.json')
    print(f"字幕提取完成，结果已保存至{subtitle_path}")
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        json.dump(subtitles, f, ensure_ascii=False)
    return '\n'.join(list(subtitles.keys())), subtitle_path
```

#### 2.2.2 基于 百度翻译API 完成字幕翻译
为了帮助大家对原版英文视频的理解，可以将原始的英文字幕翻译成中文，这里选择直接调用 百度翻译API，开发者每个月都有一定的免费额度。注意将其中的 `API_KEY 和 SECRET_KEY` 换成你自己的。

```
def get_access_token():
    API_KEY = "j5HodGgjG2iQ87MenXrw2hot"
    SECRET_KEY = "Ea1AYc1kjzv2MNExEZeMAEwzanDDlsdK"
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def translation(content, from_lang="en", to_lang="zh"):
    url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=" + get_access_token()
    payload = json.dumps({
        "from": from_lang,
        "to": to_lang,
        "q": content
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    i = response.text.find("dst")+6
    j = response.text.find("src")-3
    return response.text[i:j]
    
def translate_subtitles(subtitle_path, from_lang="en", to_lang="zh"):
    new_subtitles = {}
    subtitles = json.load(open(subtitle_path, 'r'))
    for text, value in subtitles.items():
        trans_text = translation(text, from_lang, to_lang)
        new_subtitles[trans_text] = value
    subtitle_path = subtitle_path.replace('.json', f'_{to_lang}.json')
    print(f"字幕翻译完成，结果已保存至{subtitle_path}")
    with open(subtitle_path, 'w', encoding='utf-8') as f:
        json.dump(new_subtitles, f, ensure_ascii=False)
    return '\n'.join(list(new_subtitles.keys())), subtitle_path
```

#### 2.2.3 生成 SRT 格式的字幕文件
视频文件中最简单、最常见的外挂字幕格式是SRT（SubRip Text）。SRT字幕通常以srt作为后缀，作为外挂字幕，多数主流播放器都支持直接加载并显示SRT字幕。通常每个字幕段有四部分构成：
- 字幕序号：从 1 开始（而不是 0）
- 字幕显示的起始时间
  - 格式为`hour:minute:second,millisecond --> hour:minute:second,millisecond`
- 字幕内容（可多行）
- 空白行（表示本字幕段的结束）

一个简单的例子如下：
```
1
0:00:00,000 --> 0:00:02,000
可能没有意识到。

2
0:00:02,000 --> 0:00:03,000
他们怎么会知道我们总有一天
```
让我们编写代码将提取的字幕改写成 SRT 格式的字幕文件：

```
def generate_subtitles(subtitle_path, save_path='./subtitles.srt'):
    srt_content = ''
    subtitles = json.load(open(subtitle_path, 'r'))
    for index, (text, times) in enumerate(subtitles.items()):
        # SRT文件的索引从1开始
        srt_index = index + 1
        # 格式化时间戳
        start_time = "%s,%03d" % (timedelta(seconds=times[0]), 0 * 100)
        end_time = "%s,%03d" % (timedelta(seconds=times[-1]+1), 0 * 100)
        time_str = f"{start_time} --> {end_time}"
        # 将字幕合并为一个字符串，并用逗号分隔
        # 构建SRT条目
        srt_entry = f"{srt_index}\n{time_str}\n{text}\n"
        srt_content += srt_entry
    # 写入SRT文件
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(srt_content)
    return srt_content
```


#### 2.2.4 基于 moviepy 实现视频拼接
注意 moviepy 实现视频拼接需要安装 imagemagick。在 AIStudio 的 Linux 环境中没有 sudo 权限，因此无法安装 imagemagick，如果要实现视频拼接，需要大家移步到自己本地电脑运行。Linux 下一键安装 imagemagick：
```
sudo apt-get install imagemagick
```

如果 imagemagick 安装没问题，那么就可以实现将翻译后的中文字幕添加到视频中。这里给出示例代码实现：

```
def add_subtitles(video_path, subtitle_path, output_path='./video_with_subtitles.mp4'):
    # 加载视频文件
    video = VideoFileClip(video_path)
    width, height = video.w, video.h
    subtitles = json.load(open(subtitle_path, 'r'))
    trans_text = []
    for text, dura in subtitles.items():
        start_time = float(dura[0])
        end_time = float(dura[-1]+1)
        duration = end_time - start_time
        text = TextClip(text, fontsize=20, size=(width-20, 25),
                        align='center', color='white').set_position((10,height-40)).set_duration(duration).set_start(start_time)
        trans_text.append(text)
    video = CompositeVideoClip([video, *trans_text])
    video.write_videofile(output_path)
```


#### 2.2.5 基于 ErnieBot 实现视频问答
ERNIE Bot 为开发者提供了便捷接口，可以轻松调用文心大模型的文本创作、通用对话、语义向量及AI作图等基础功能。

这里仅使用通用对话接口，你只需要将`字幕文件(srt_content)`、`提示词(prompt_content)`和`你的问题(user_content)`准备就可以了，示例代码如下：

```
import erniebot
erniebot.api_type = 'aistudio'
erniebot.access_token = '7d8bcc8494fb95e9059bae34856c3a40daaf8671' # 注意替换成自己的

def chat_with_bot(srt_content, prompt_content, user_content):
    if not srt_content:
        return "请先点击👂生成srt格式字幕"
    messages =[{'role': 'user', 'content': f'{srt_content} {prompt_content} {user_content}'}]
    response = erniebot.ChatCompletion.create(
        model='ernie-3.5',
        messages=messages,
    )
    res = response.get_result()
    # print(res)
    return res
```
注意这里的`erniebot.access_token`可以在 AIStudio 的个人中心获取（如下图所示），每个新用户都有免费额度。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a9ba6e9e6f6cbcc376e275d1826e5052.png)


### 2.3 Gradio前端界面实现
本次实验同样还是基于 Gradio 搭建一个简单的前端应用，将上述实现的功能集成进来。具体界面逻辑如下：

```
def launch():
    theme = gr.Theme.load("theme.json")
    with gr.Blocks(theme=theme) as demo:
        gr.Markdown(top_md)
        with gr.Row():
            with gr.Column():
                video_input = gr.Video(label="视频输入 | Video Input")
                with gr.Row():
                    gr.Examples(['zh.mp4'],
                                [video_input],
                                label='中文示例视频 | Chinese Demo Video')
                    gr.Examples(['en.mp4'],
                                [video_input],
                                label='英文示例视频 | English Demo Video')
                with gr.Row():
                    recog_button = gr.Button("👂 识别字幕", variant="primary")
                    recog_button2 = gr.Button("👂英文->中文")
                srt_button = gr.Button("👂生成srt格式字幕", variant="primary")
            with gr.Column():
                with gr.Tab("🤖 PP-OCR视频字幕"):
                    
                    with gr.Row():
                        video_text_ori = gr.Textbox(label="📖 原始字幕内容", lines=8)
                        video_text_tra = gr.Textbox(label="📖 翻译字幕内容", lines=8)
                    video_text_path = gr.Textbox(label="字幕地址", visible=False)
                    video_text_srt = gr.Textbox(label="✏️ SRT字幕内容", lines=8)
                with gr.Tab("🧠 ErnieBot视频智能问答"):
                    with gr.Column():
                        prompt_head = gr.Textbox(label="Prompt", value=("你是一个视频分析助手，基于输入视频的srt字幕，回答我的问题"))
                        prompt_user = gr.Textbox(label="User", value=("我的问题是："))
                        llm_button =  gr.Button("Enrie bot推理", variant="primary")
                        llm_result = gr.Textbox(label="Enrie bot 回答", lines=8)
            recog_button.click(get_video_ocr,
                            inputs=video_input,
                            outputs=[video_text_ori, video_text_path])
            recog_button2.click(translate_subtitles,
                                inputs=video_text_path,
                                outputs=[video_text_tra, video_text_path])
            srt_button.click(generate_subtitles,
                            inputs=video_text_path,
                            outputs=video_text_srt)
            llm_button.click(chat_with_bot,
                            inputs=[video_text_srt, prompt_head, prompt_user],
                            outputs=llm_result)
    demo.launch(server_name='0.0.0.0', server_port=8080)
```
在 AIStudio 的云环境中启动应用：

```
python demo.py
```
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/dba34c6f44b474965eaf7f14bc71f574.png)
如果你是在 AIStudio 的 CodeLab 中启动应用的话，本地浏览器中是无法访问这个地址的，那么如何访问这个应用呢？

下面介绍两种方式：

**方式一：**

参考 AIStudio 的[项目服务部署](https://ai.baidu.com/ai-doc/AISTUDIO/Blopive5g)官方文档，采用url拼接的方式：`Codelab项目链接/api_serving/<user_port>/`。

举个例子：比如我的Codelab地址是：

`https://aistudio.baidu.com/bd-cpu-01/user/226606/7892508/home#vscode`

那么在浏览器中打开如下链接即可访问你启动的 Gradio 应用：

`https://aistudio.baidu.com/bd-cpu-01/user/226606/7892508/api_serving/8080/`

如果你打开后的界面如下图所示，和本文前面展示的界面相比，不符合预期。什么原因？ F12 打开 Chrome 开发者工具，发现是因为加载本地文件失败了（比如这里的前端样式和示例视频），目前还没找到很好的解决方案。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/5213d2d5fd6748170bcd5b7308859395.png)

**方式二：**

为此，我们选择在 Codelab 的 Notebook 界面中进行前端展示。在Notebook 界面中进行前端展示，需要`xx.gradio.py`格式的文件，为此可以将`demo.py`复制一份命名为`demo.gradio.py`，如下图所示：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/bd0e895470ff7abbdf9edcd034787cc6.png)

这里有几点坑，大家注意避开：
- 在 demo.launch()中不要指定 8080 端口
- 如果依然出现上述 css 文件加载不出来，导致界面显示有问题，换一台开发机试试吧，笔者亲测有效。
- 需要在初始 python 环境中安装项目依赖包：`pip install -r requirements.txt`，因为`xx.gradio.py`是在下面这个python环境中启动的：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c10355f51d13c97e60c5ecccfa0a7369.png)


此外，还可以选择在本地 Linux 环境中运行项目，完美避开上述各种坑。


# 总结

至此，我们共同走完了一个完整的视频问答项目，从基础的动手跑通 CRNN 文本识别任务，再到应用开发和部署，旨在帮助初学者快速入门 OCR 相关技术并搭建一个简单的应用。

本系列的后续文章将沿袭这一思路，继续分享更多采用 Paddle 深度学习框架服务更多产业应用的案例。如果对你有帮助，欢迎 **关注 收藏** 支持~

