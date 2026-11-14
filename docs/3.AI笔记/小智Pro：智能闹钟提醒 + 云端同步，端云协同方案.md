前文，分享了【小智Pro】的开发过程：

[30天，AI 陪我写了3万行代码，上线一款应用，3点血泪教训](https://zhuanlan.zhihu.com/p/1970051780579660673)

这个项目，最初的出发点，就是为了解决在【小智终端设备】上实现【闹钟提醒】的痛点。

关于【闹钟提醒】的实现思路，可见前文分享：

[小智 AI + 闹钟提醒 + 定时任务，设备端MCP实现，想象空间巨大](https://zhuanlan.zhihu.com/p/1950126555238991207)

当初的实现，闹钟信息全部存储在设备端。

实际体验中，发现有两大硬伤：

- 一旦重新烧录固件，存储的闹钟信息就丢了；
- AI 识别不准，闹钟无法保证 100% 准确。

比如，语音识别错误：

你看下图，

![](https://i-blog.csdnimg.cn/img_convert/196ce94636c6c76215e86b79863861ac.png)

`午休提醒` 被 AI 识别成了 `王不休`，这能忍？

`闹钟提醒` 是一个刚需、高频、且对错误零容忍的功能，所以必须高优解决。

怎么解决？

端云同步！

## 1. 设备端

1. 设备初始化：从云端加载所有闹钟信息，并存储到本地 nvs；
2. 新增/修改/删除闹钟：更新本地nvs，并同步推送到云端；
3. 查询闹钟：从本地 nvs 获取闹钟信息；
4. 清空闹钟：从本地 nvs 清空，同步清空云端信息；

![](https://i-blog.csdnimg.cn/img_convert/b406c924e19119989f1ab5f13ab769a3.png)

## 2. 云端

设备端信息，会实时同步到云端，云端同样支持增删改查。

新增闹钟：

![](https://i-blog.csdnimg.cn/img_convert/3f3979739b2db08eb1b1ffd9319ebf90.png)

修改/删除闹钟：

![](https://i-blog.csdnimg.cn/img_convert/0eac1c7c32ad16a01856c250932110c8.png)


## 3. 端云同步

设备端和云端同步，逻辑上是这样的：

![](https://i-blog.csdnimg.cn/img_convert/a4d9ffb78b54d32d682258b3cd05282c.png)


这样做，完美解决前文的两个痛点：
- 闹钟信息不丢失：即使重刷固件，设备上电，即可自动从云端拉取数据；
- 闹钟信息100%准确：即使AI识别错误，也可在前端进行修改。

## 写在最后


本文分享了`小智Pro: 闹钟提醒 端云同步`的具体实现思路。

如果对你有帮助，不妨**点赞收藏**备用。

欢迎体验 `小智Pro` 更多功能，请戳👇：

> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

有任何问题，欢迎进群交流：

![](https://i-blog.csdnimg.cn/img_convert/574261a065449f619ced4253ce176e80.png)
