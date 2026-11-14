上文分享了`小智AI自定义唤醒词+表情包+背景图`的基本原理：

[小智AI 如何自定义唤醒词+背景图：原理+流程拆解](https://zhuanlan.zhihu.com/p/1985997055970275872)

原理简言之：远程控制。

而`远程控制`的核心是：`MQTT + MCP`：

![](https://i-blog.csdnimg.cn/img_convert/dcdee56428403b6e7504cbdab50560b9.png)

今日分享，将尝试拆解`MQTT + MCP`实现远程控制的核心逻辑。

基于此，给出`小智Pro`远程控制的扩展方案。


## 1. 远程控制的基本原理

### 1.1 整体架构

小智设备端，MCP工具调用，涉及三个主要组件：

- **MQTT协议层**：对应`mqtt_protocol.cc`，负责与服务器通信
- **Application层**：对应`application.cc`，负责消息分发
- **MCP服务器**：对应`mcp_server.cc`，工具执行和响应处理

### 1.2 MQTT 通信架构

![](https://i-blog.csdnimg.cn/img_convert/6045cb817b664c3ac46c36e51c022dcb.png)


**step1. MQTT配置获取**

设备通过 OTA 接口获取MQTT配置信息：

```
{
  "mqtt": {
    "endpoint": "mqtt.xiaozhi.me", 
    "client_id": "GID_test@@@98_3d_ae_e6_83_d0@@@", 
    "username": "eyx", 
    "password": "6Yx", 
    "publish_topic": "device-server", 
    "subscribe_topic": "null"
  }
}
```

`publish_topic_` 是设备端给服务端发消息的 `topic`，`subscribe_topic` 会在 broker 端自动订阅。


**step2. MQTT连接建立**

在 `StartMqttClient` 方法中，`!mqtt_->Connect` 使用上述配置配置信息，连接到 MQTT 服务器。


**step3. 设备订阅主题**

设备监听服务端发来的请求，并上报结果：

```
mqtt_->OnMessage([this](const std::string& topic, const std::string& payload) {
    cJSON* root = cJSON_Parse(payload.c_str());
    if (root == nullptr) {
        ESP_LOGE(TAG, "Failed to parse json message %s", payload.c_str());
        return;
    }
    cJSON* type = cJSON_GetObjectItem(root, "type");
    // ... 处理不同类型的消息
});
```

### 1.3 完整通信流程

![](https://i-blog.csdnimg.cn/img_convert/0ba5b1436945ffdb100bbb3eb166be25.png)

**1. 服务器发起MCP请求**

当服务器要在设备上执行某些操作时，通过`MQTT协议`发送`mcp`类型的消息：

```
{
  "type": "mcp",
  "session_id": "xxx",
  "payload": {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 1,
    "params": {
      "name": "self.get_system_info",
      "arguments": {}
    }
  }
}
```

**2. MQTT消息接收与解析**

`MqttProtocol` 接收消息，在`OnMessage`回调中解析数据，识别为MCP请求。

**3. 消息分发到MCP服务器**

在主应用中，处理类型为"mcp"的消息：

```
if (strcmp(type->valuestring, "mcp") == 0) {
    auto payload = cJSON_GetObjectItem(root, "payload");
    if (cJSON_IsObject(payload)) {
        McpServer::GetInstance().ParseMessage(payload);
    }
}
```

**4. MCP消息处理**

MCP服务器（McpServer）接收到消息后，会执行以下步骤：

- 消息格式验证
- 方法路由
- 工具执行

**5. 响应返回**

工具执行完成后，将响应封装成 MQTT 消息发送回服务器：

```
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { /* 工具执行结果 */ }
}
```


## 2. `小智Pro` 远程控制方案

基于以上机制，`小智Pro` 实现了一套完整的远程控制解决方案，并开放 API 调用。

支持查看MCP工具列表、远程唤醒、重启、消息发送、获取设备信息、设备设置等功能。


### 2.1 获取 MCP 工具列表 

**基本信息：**

- **接口路径**: `/xiaozhi/tools/list`
- **请求方法**: POST
- **认证方式**: API Key

**请求参数：**

```json
{
  "device_id": "string",
  "common": "boolean"
}
```

**参数说明:**
- `device_id` (string, required): 设备 MAC 地址，例如：`00:11:22:33:44:55`
- `common` (boolean, optional):
  - `true`: 对应设备端 `mcp_server.cc` 中的 `CommonTools` 列表
  - `false`: 对应设备端 `mcp_server.cc` 中的 `UserOnlyTools` 列表

**响应示例：**

```json
{
  "code": 200,
  "msg": "OK",
  "data": {
    "tools": [
      "self.get_system_info",
      "self.reboot",
      "self.upgrade_firmware",
      "self.screen.get_info",
      "self.screen.snapshot",
      "self.screen.preview_image",
      "self.assets.set_download_url",
      "self.wake_up",
      "self.send_command",
    ]
  }
}
```

### 2.2 远程控制接口

用于调用设备端指定的工具。

**基本信息：**

- **接口路径**: `/xiaozhi/tools/call`
- **请求方法**: POST
- **认证方式**: API Key

**请求参数：**

```json
{
  "device_id": "string",
  "name": "string",
  "arguments": {}
}
```

### 2.3 远程控制接口示例

支持`MCP工具列表`返回的所有工具调用，调用示例可参考`API接口文档`：

![](https://i-blog.csdnimg.cn/img_convert/d75ed71d53f6b6418e13a40eeb12b8a4.png)



## 写在最后

本文分享了`小智AI: 远程控制的基本原理`，并给出了`小智Pro`的扩展方案。

如果对你有帮助，不妨**点赞收藏**备用。

此外，除了`远程控制接口`，平台将持续开放更多接口：

![](https://i-blog.csdnimg.cn/img_convert/1c51ba03f942dcf0f91e49e5b232ab94.png)


`One more thing`：设备端固件，已全面适配小智官方仓库收录的开发板型号：


![](https://i-blog.csdnimg.cn/img_convert/c8e457305c941a276468bf911ddb1044.png)


戳下方链接，免费体验👇：

> [https://mkwyqeoebedx.sealosbja.site](https://mkwyqeoebedx.sealosbja.site)

有任何问题，欢迎来聊。
