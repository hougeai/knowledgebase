
前段时间，和大家分享了一款免费的语音合成服务 EdgeTTS：

[EdgeTTS，支持粤语等各种方言，无需部署无需Key，完全免费](https://zhuanlan.zhihu.com/p/703686916)

后台有小伙伴反应，最近访问不了。。。

什么情况？实测发现，被qiang了，需要手动添加代理。

没有代理怎么办，有没有平替？

EdgeTTS 底层不就是使用微软的在线语音合成服务么，何不自己搞一个？

说干就干，本篇分享，带大家实操：**在微软 Azure 平台，注册一个语音服务，享用免费的 TTS 服务**。

## 1. 微软Azure平台介绍
> 官网：[https://azure.microsoft.com/](https://azure.microsoft.com/)

![](https://img-blog.csdnimg.cn/img_convert/98199fa0128485c75119f34e283fd00a.png)

微软 Azure 是微软提供的一系列**云计算服务**，包括计算、分析、存储和网络服务。

每个客户只能使用一个免费帐户，试用 30 天后，还有65项服务，每个月都有免费额度。

![](https://img-blog.csdnimg.cn/img_convert/3947872a58eda8f32c4034a85a7366a7.png)

> 注：Azure 的免费虚拟机，**如果开公网 IP 是需要付费的哦**，还没试用过的小伙伴注意。

## 2. 注册语音服务

成功登录 Azure 后，在控制台，选择创建一个 `语音服务`：

![](https://img-blog.csdnimg.cn/img_convert/4531760da93c01180a5090d9042a530d.png)

注意这里，国内用户选择 `East Asia` 节点，离你最近自然速度最快。

![](https://img-blog.csdnimg.cn/img_convert/c386a3e63cdc044ae4063b4740b3b2d0.png)

然后，在定价层选择 `Free F0`。

![](https://img-blog.csdnimg.cn/img_convert/e14b439c469012ba8f7362177d5ffdc8.png)

后面选择默认选项，创建即可。

创建成功后，在控制台资源列表中可以找到：

![](https://img-blog.csdnimg.cn/img_convert/bef9c877f2135db132ab7b34bc0616ab.png)

**免费额度如何？**

点进来，右侧查看定价层：

![](https://img-blog.csdnimg.cn/img_convert/26b687c09f8eaf6814c769d883b066e5.png)

**总结来说：**
- 语音识别：每月 5 小时；
- 语音合成：每月 50 万字符；

如果不是产品上线使用，个人测试，完成足够了吧。

## 3. TTS 调用

这里以 TTS 为例，介绍下如何使用它的语音服务。

资源主页，点击 `Speech Studio`，这里展示有平台的各种语音服务:

![](https://img-blog.csdnimg.cn/img_convert/d2406f574bdf8befbb6e9318285ce035.png)

选择`文本转语音`的`语音库`：

![](https://img-blog.csdnimg.cn/img_convert/e27a4e7ae98090150d7c311e269a56b9.png)


除了在浏览器端试听以外，如果进行后端调用，这里也提供了两种方式！

![](https://img-blog.csdnimg.cn/img_convert/0a10c017cb3595d118f621f3b0309bed.png)

一种是官方提供的 SDK，需安装后使用。

个人更推荐 REST API 调用，更简单直接！


### 3.1 REST API
> 参考文档：[https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech)


首先，在你的资源主页，查看密钥和 URL：

![](https://img-blog.csdnimg.cn/img_convert/d096041336bc61480fd75569042bf627.png)

有了这两，后端调用就很简单了。

比如，以Python为例，我想先看看中文音色有哪些：

```
def tts_azure_list():
    region = 'eastasia'
    url = f'https://{region}.tts.speech.microsoft.com/cognitiveservices/voices/list'
    headers = {"Ocp-Apim-Subscription-Key": azure_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    data = [item for item in data if item['Locale'] == 'zh-CN']
    for item in data:
        if item['Gender'] == 'Female':
            print(item['ShortName'])

```


进行语音合成，示例代码：

```
def tts_azure(text='', filename='data/audios/tts.pcm', voice='zh-CN-XiaoxiaoNeural'):
    region = 'eastasia'
    url = f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1'
    headers = {
        "Ocp-Apim-Subscription-Key": azure_key,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "User-Agent": "aiotbot/0.1.0"
    }
    data = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='{voice}'>{text}</voice></speak>"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        with open(filename, 'wb') as audio_file:
            audio_file.write(response.content)
    else:
        logger.error('azure tts请求失败，状态码：', response.status_code, response.text)
    return os.path.exists(filename)
```
需要注意的是：上述参数中的`X-Microsoft-OutputFormat`就是输出格式，非流式调用，输出只支持 `pcm` 格式的音频文件。

最后，在控制台-指标，可以查看调用量。50 万字符，放心大胆用吧：

![](https://img-blog.csdnimg.cn/img_convert/2d726593490d10f9d3ae913b6fc76642.png)

## 写在最后

本文分享了 EdgeTTS 的免费平替方案：微软 Azure 平台注册并调用语音服务。

如果对你有帮助，不妨**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近搭建的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。

