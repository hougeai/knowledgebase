前文，分享了【小智Pro】系列文章：

[30天，AI 陪我写了3万行代码，上线一款应用，3点血泪教训](https://zhuanlan.zhihu.com/p/1970051780579660673)

[小智Pro：智能闹钟提醒 + 云端同步，端云协同方案](https://zhuanlan.zhihu.com/p/1970446275288741797)

[小智Pro：在线点歌+歌词同步，支持打断和搜索，端云协同方案](https://zhuanlan.zhihu.com/p/1971130142131730137)

[小智Pro：给小智装上"知识外挂"，从此告别一问三不知](https://zhuanlan.zhihu.com/p/1972219653188194715)


知识库搭建是个苦累活，为了进一步降低大家的使用门槛，除了 `平台自研知识库`，`小智Pro` 还支持接入`Dify知识库`。

后端已经做了大量封装，你只需根据以下流程，

三步走，即可把你在`Dify`上辛苦搭建好的知识库，接入小智。

下面上实操：

## 1. Dify 知识库

体验 小智Pro ，请戳👇：
> https://mkwyqeoebedx.sealosbja.site

### 1.1 创建知识库

点击左上角`创建知识库`，选择`Dify知识库`：

![](https://i-blog.csdnimg.cn/img_convert/ea8812fc7e348501cf8973719a442be1.png)


### 1.2 测试连接

如果是自部署的 `Dify`，需要确保你的应用公网可访问。

在 `Dify` 平台找到后端服务 API，和密钥：

![](https://i-blog.csdnimg.cn/img_convert/ce0056fe98b5c064ceb5fec4da5bbc9a.png)

填入上方文本框，点击`测试连接`，自动抓取你在 `Dify` 平台上构建的所有知识库：

![](https://i-blog.csdnimg.cn/img_convert/49724b5ed4532dcc1bf62100bd769761.png)


### 1.3 接入知识库


选择一个知识库后，后端会拉取当前知识库下的文件列表：

![](https://i-blog.csdnimg.cn/img_convert/3cf5942600b71e5e1405fa6396df5b75.jpeg)

### 1.4 检索测试

在设备端使用之前，可以在前端先测试一下：

![](https://i-blog.csdnimg.cn/img_convert/a27f31f08bee892c9fab5c214dfed739.jpeg)


### 1.5 设置为设备端知识库

当前，设备端只支持调用一个知识库，可以点击如下按钮，进行设置：

![](https://i-blog.csdnimg.cn/img_convert/7f6de6b567569654366e090545ddcea4.png)

设置成功后，选择的`Dify知识库`上方会新增`设备`标签：

![](https://i-blog.csdnimg.cn/img_convert/f12d77a0edebdc67d3ec6719a65d0b08.png)


### 1.6 设备端测试

前端检索没问题后，设备端`小智`即可通过 MCP 调用这里的知识库，获取相关上下文来回答你的问题了:

![](https://i-blog.csdnimg.cn/img_convert/60a34368e87de1e5388f998a66cbb25e.png)

> 注：小智 MCP 工具调用，有延时限制，如果`Dify知识库`返回超时，将调用失败。

## 写在最后

本文分享了`小智Pro: Dify 知识库接入+设备端检索`的完整流程。

如果对你有帮助，不妨**点赞收藏**备用。

欢迎体验 `小智Pro` 更多功能，请戳👇：

> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

有任何问题，欢迎进群交流：

![](https://i-blog.csdnimg.cn/img_convert/b34a60432b08eba6ba481b86a916a143.png)

