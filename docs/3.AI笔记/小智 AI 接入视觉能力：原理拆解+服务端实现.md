
前文，分享了`小智AI如何通过 MCP 控制IoT设备`：

[小智AI MCP 控制IoT设备：原理+流程拆解](https://zhuanlan.zhihu.com/p/1921139871113781343)

不得不说，接入了 MCP，可玩性越来越高了。

本文，就来聊聊`小智AI如何通过 MCP 接入视觉能力`。

## 1. 交互逻辑

视觉能力，是通过接入摄像头搞定的。

上篇已经实现了`MCP 控制IoT设备`，设备端的`摄像头`也是一种`IoT设备`。

当用户有`图片识别需求`时，服务端识别到这种意图，会通过 MCP 向客户端发请求。

客户端，调用摄像头拍照，然后请求`视觉识别模型`，获得当前图片的描述。

客户端通过 MCP 把`当前看到的`发给服务端，由服务端 LLM 进行总结后回答用户。

交互逻辑，用流程图描述如下：

![](https://i-blog.csdnimg.cn/img_convert/b21e5c531babcdf1bc26c4d48c5657f9.png)

我们来看日志，会更直观一些：

![](https://i-blog.csdnimg.cn/img_convert/6b6a7f004365ba57990857233b1ccf4b.png)

整个流程，基于上篇分享的 `MQTT + UDP` 协议框架，实现并不复杂。

下面重点看：如何自建`视觉识别模型`。


## 2. 视觉识别模型

对于简单的`图片描述生成`，其实只要接入一个`多模态大模型`就够了，比如`Qwen 2.5-VL`。

无论是本地部署，还是调用云端API，最终都给封装成 `OpenAI` 兼容格式。 

```
openaiClient = OpenAI(api_key=settings.VISION_KEY, base_url=settings.VISION_URL)

def process_image_with_ai(image_data: bytes, question: str) -> str:
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    response = openaiClient.chat.completions.create(
        model=settings.VISION_MODEL,
        messages=[{"role": "user","content": [
            {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
            {"type": "text", "text": question},
        ]}]
    )
    return response.choices[0].message.content
```

以阿里云的`qwen-vl-plus`，单张图像推理需要 `1.5-2s` 左右。


```
# 1.68 s
{'success': True, 'result': '图片中有一只卡通风格的猴子。猴子的毛色是棕色的，脸上有彩虹色的装饰，显得非常可爱。它手里拿着一块牌子，牌子上用红色字母写着“AI”。背景是浅绿色的，整体画面色彩鲜艳，给人一种愉快和积极的感觉。'}
```


所以，对延时要求较高的朋友，可选择部署端侧模型，对于`图片描述`这种简单任务，完全足够了。

最后，再把上述结果，封装到一个`/mcp/vision/explain`接口中，对外提供服务即可，这里给出接口示例：


```
@app.post("/mcp/vision")
async def analyze_image(
    request: Request,
    file: UploadFile = File(..., description="JPEG 图像文件"),
    question: str = Form(...),
):
    """
    接收 JPEG 图像文件和问题，进行 AI 分析并返回结果。
    - **file**: JPEG 格式的图像文件
    - **question**: 关于图像的问题
    - **headers**:
        - Device-Id (required)
        - Client-Id (optional)
        - Authorization (Bearer token, optional)
    返回:
    - 成功时返回 AI 分析结果
    - 失败时返回错误信息
    """
    # 1. 提取 headers
    # 2. 调用 AI 模型分析
    try:
        image_data = await file.read()
        result = process_image_with_ai(image_data, question)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI 分析失败")

```


如果有类似`人脸识别`等需求，那就再接入一个`人脸识别`的服务不就 OK 了。

反正有了 MCP，想干点啥不行啊。


## 写在最后


本文分享了 `小智AI 接入视觉能力` 的原理，和服务端实现方案。

如果对你有帮助，欢迎**点赞收藏**备用。

下篇继续聊：

- 如何低成本 DIY 一套接入视觉能力的`小智AI`。

---

为方便大家交流，新建了一个 `AI 交流群`，公众号后台「联系我」，拉你进群。


