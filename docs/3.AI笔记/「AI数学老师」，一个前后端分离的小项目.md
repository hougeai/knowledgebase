前两天，给大家分享了`免费AI数学老师`的本地搭建：
- [最强OCR+数学模型Qwen-Math，本地搭建](https://blog.csdn.net/u010522887/article/details/142893400)

为了方便大家快速体验，我把`免费AI数学老师`接入了微信机器人`小爱`。

![](https://img-blog.csdnimg.cn/img_convert/f135233f459435b24c16e61f05ef314a.png)

实操后发现，**体验感非常不好**，主要问题有：
- 对于解复杂题目，Qwen 回复需要 100 秒以上，容易引发服务超时。
- matplotlib 只支持渲染部分 Latex 公式，导致生成图片中有不可识别字符，没法看。

**既然这么受欢迎，自然需要更好的前端展现。**

今日分享，就带大家实操一个简易的`AI数学老师`前端，通过调用上篇部署好的后端服务，展现`Qwen-Math`的实力。

## 1. Gradio 简介
**Gradio 是什么？**

一个用于构建交互式界面的 Python 库，主要用于展示各种 AI 模型。

**为何用 Gradio？**

你只需熟悉几个简单的组件，就可以快速搭建一个前端界面，无需编写繁琐的 HTML、CSS 和 JavaScript 代码。

**如何装 Gradio？**

安装Gradio非常简单，pip 一键安装：

```
pip install gradio
```

Gradio 依赖于 Flask 和 Werkzeug，这些库会在安装时自动安装。

**如何用 Gradio?**

下面是一个简单的Gradio应用示例，它创建了一个图像分类的界面：通过定义图像分类函数 `classify_image`，用户可以上传图像 `image`，进而获得分类结果 `label`。
```
import gradio as gr

def classify_image(img):
    # 这里是图像分类的逻辑
    pass

iface = gr.Interface(fn=classify_image, inputs="image", outputs="label")
iface.launch()
```


## 2. AI数学老师前端实现

如果理解了上面的`Hello-world`实现，那么用 Gradio 来搭建`AI数学老师`前端，就 so easy 了。

具体而言，我们可以采取三步走：

### 2.1 定义处理函数

假设你已参考上篇完成了后端服务部署：`http://localhost:3004/math`。

请求体包括两部分：
- `image`：包含问题的图片，可以为空；
- `text`：关于解题的文本描述。
```
data = {
        "image": image, 
        "text": text
    }
```

因此，处理函数可以定义如下：

```
def process(image, text):
    data = {
        "image": image, 
        "text": text
    }
    response = requests.post("http://localhost:3004/math", json=data)  # 修改为你的API地址
    return response.json()
```


### 2.2 创建界面组件

对于这个应用，最简单的可以分两栏进行展示：
- 问题输入区：包括图片输入和文本输入；
- 解答区：模型回答展示。

实现代码如下：
```
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            img_input = gr.Image(label="问题图片", type='pil')
            text_input = gr.Textbox(placeholder="输入问题")
            submit_button = gr.Button("提交", variant='primary')
        with gr.Column():
            with gr.Accordion("解答区", open=True):
                markdown_output = gr.Markdown()
    submit_button.click(fn=process, inputs=[img_input, text_input], outputs=markdown_output)
```

不得不赞的是，gradio 的 markdown 组件 `gr.Markdown`完美支持 Latex 渲染，完美！

### 2.3 演示和调试
搭建完成后，可以启动看看，不行再来调整呗。

```
# 启动应用
demo.launch(server_name="0.0.0.0", server_port=7860)
```

启动把`server_name`置为`0.0.0.0`，它表示“所有地址”，服务可以接受来自任何IP的连接请求。

## 3. 效果展示

一个简单的前端页面，它来了。。。

![](https://img-blog.csdnimg.cn/img_convert/1b78bb5d7a8931dadcb0844044c9e8a1.png)

图片输入这里，支持两种方式：
- 本地上传图片 or 复制粘贴；
- 调用电脑摄像头拍照；

![](https://img-blog.csdnimg.cn/img_convert/022083f8e3a6fd469c2835f46dbb6b9a.jpeg)

输入题目，点击提交，耐心等待大模型解答：

![](https://img-blog.csdnimg.cn/img_convert/a7492ed3d87bf849299608ba3faa05e4.png)

对于这种简单的题目，不到 10s 就能搞定： 

![](https://img-blog.csdnimg.cn/img_convert/20b0a198e31eec151027d32be6c4a551.png)

更多解题案例，可参见：[你的免费AI数学老师来了！](https://blog.csdn.net/u010522887/article/details/142893400)

*注：Qwen-Math 只支持文本输入，因此无法解答包含几何图形的题目。*

## 写在最后

本文通过引入 `Gradio`，带大家实操了`AI数学老师`的前端实现。

如果对你有帮助，不妨**点赞收藏**备用。

大家有更好的想法，欢迎来聊。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。
