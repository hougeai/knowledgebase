前文分享了`小智AI自定义唤醒词+表情包+背景图` 的基本原理：


[小智AI 如何自定义唤醒词+背景图：原理+流程拆解](https://zhuanlan.zhihu.com/p/1985997055970275872)

[远程控制+文字唤醒，小智Pro开放API调用，释放小智无限潜力](https://zhuanlan.zhihu.com/p/1988530667840111026)

有朋友好奇：

浏览器生成的`assets.bin`是如何发送给设备的？

今日分享，聊聊`前端-后端-设备端`的三方通信逻辑。

基于此，给出`小智Pro`的具体实现方案。

## 1. 架构设计

回到前文的问题：

**浏览器生成的`assets.bin`如何发送给设备端**？



> 参考：[https://github.com/78/xiaozhi-assets-generator](https://github.com/78/xiaozhi-assets-generator)

来看小智的实现思路：一个非常巧妙的三方通信架构：

- 前端 ↔️ 后端：WebSocket (控制通道)
- 设备 ↔️ 后端：HTTP (数据通道)
- 后端：作为中间协调者，连接两端

![](https://i-blog.csdnimg.cn/img_convert/881271370a63ffea91efbca7db0bcc0a.png)

简单画个流程图：

![](https://i-blog.csdnimg.cn/img_convert/52b4dd0759eacc690a9b569eebec90ba.png)


为啥要这么搞？

- **解耦设计**：前端不直接与设备通信
- **协议桥接**：WebSocket ↔ HTTP 的实时数据转发
- **状态同步**：通过事件机制实现三端状态一致
- **安全机制**：临时URL，防止未授权访问


## 2. 完整流程

了解了架构，我们来看完整流程：

![](https://i-blog.csdnimg.cn/img_convert/ce5ae29bd2e120f206ee9bbe10b089ce.png)

**阶段1-2：前端准备阶段**


前端通过WebSocket告诉后端："我要上传一个文件"

```
const createMessage = {
  type: 'create_file',
  fileName: 'assets.bin', 
  fileSize: blob.size
};
this.ws.send(JSON.stringify(createMessage));
```

**阶段3：后端生成URL**


后端创建临时文件会话并返回下载URL：

**阶段4：前端配置设备**


前端拿到URL后告诉设备去下载：
```
await callMcpTool('self.assets.set_download_url', {
  url: downloadUrl  // 这就是上面的download_url
})

```
**阶段5：设备端HTTP下载**

```
// 设备端直接HTTP GET请求
if (!http->Open("GET", url)) { 
    ESP_LOGE(TAG, "Failed to open HTTP connection");
    return false;
}
```

**阶段6：后端转发数据给设备**


当设备请求下载时，后端检测到这个请求对应某个`session`，不从文件系统读取，而是实时转发前端通过`WebSocket`发送的二进制数据：

**阶段7：后端通知前端传输开始**

当后端开始向设备提供HTTP数据时，发送`transfer_started`事件给前端：

```
case 'transfer_started':
  this.currentSession.transferStarted = true
  if (this.onTransferStarted) {
    this.onTransferStarted()  // 通知前端可以开始发送数据了
  }
```

**阶段8：前端传输完成 & 后端下载完成**

当前端传输的数据，被后端全部接收后，销毁 `session`，完结撒花！


## 3. 小智Pro 实现
> 免费体验👇：
>
> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

基于以上原理和流程，小智Pro 服务端，现已支持`自定义唤醒词+背景图`：


![](https://i-blog.csdnimg.cn/img_convert/cba2751fb23017cdf30048c15c379464.png)


![](https://i-blog.csdnimg.cn/img_convert/0083884d17fa02b7d5f487cb1fbc2f43.png)

注：需下载`小智Pro`-`v2.0.5.1`及以上版本固件体验：
> [https://github.com/hougeai/xiaozhiPro/releases](https://github.com/hougeai/xiaozhiPro/releases)

## 写在最后

本文分享了`小智AI实现固件更新`的`前端-后端-设备端`的三方通信逻辑。。

如果对你有帮助，不妨**点赞收藏**备用。

欢迎来聊。
