上篇分享了：知识库工具-`WeKnora`

[微信开源 RAG：复杂文档秒变私有知识库，私有化部署](https://zhuanlan.zhihu.com/p/1950807564863382005)

本篇继续聊：

如何通过 MCP 的方式，把知识库接入 `小智AI` ？

思路很简单：既然`WeKnora`暴露了 API，只要在 MCP 服务中，调用 API 拿数据，不就 OK 了？

## 1. 搭建 MCP 服务器

正式接入之前，我们可以先搭建一个 MCP 服务器，用于从知识库中查询相关信息，并测试下服务的稳定性。

问题来了：如何快速启动一个 MCP 服务器?

强烈推荐你试试 `FastMCP`：一个构建 MCP 的 python 框架，同时支持服务器和客户端构建，比官方 SDK 好用多了。

### 1.1 FastMCP 拉起 MCP 服务

首先，安装依赖：

```
pip install fastmcp
```

然后，构建 MCP Server，只需简单三步：

**Step 1：** 注册服务：

```
# 注册 MCP 服务
mcp_server = FastMCP("weknora-server")
```

**Step 2：** 定义工具：

首先，我们定义一个`知识库搜索`的工具：
```
# 工具调用: hybrid_search
@mcp_server.tool
def hybrid_search(
    query: Annotated[str, Field(description="Search query")],
):
    """Perform hybrid search in knowledge base"""
    try:
        data = {
            "query_text": query,
            "vector_threshold": 0.5,
            "keyword_threshold": 0.3,
            "match_count": 3
        }
        response = requests.get(f'{base_url}/knowledge-bases/{kb_id}/hybrid-search', headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
```

再来一个工具：列出知识库文件，尽管这里无需任何输入，但也必须传参，否则报错:

```
# 工具调用: list_files
@mcp_server.tool      
def list_files(random_string: str = None):
    """List all files in knowledge base"""
    try:
        response = requests.get(f'{base_url}/knowledge-bases/{kb_id}/knowledge', headers=headers)
        response.raise_for_status()
        result = response.json()
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
```

**Step 3：** 启动服务：选择`sse`协议

```
if __name__ == "__main__":
    mcp_server.run(transport='sse', host="0.0.0.0", port=8001)
```

成功启动后，会出现如下日志，注意这里的 server 地址：后面有一个 sse：

![](https://i-blog.csdnimg.cn/img_convert/acbfc71f072763d56bc95772396534d0.png)

### 1.2 测试 MCP 服务

现在绝大部分 AI 编程工具，都支持接入 MCP。

我以在用的 VS Code 中的`通义灵码插件`为例：

![](https://i-blog.csdnimg.cn/img_convert/9700f18b1d95419993ac616b3e705569.png)


连接成功：

![](https://i-blog.csdnimg.cn/img_convert/c28ac9e7b8353877eefa01cd187d99dc.png)

可以看到，它读取到了刚定义的两个工具。

来测试一下：

![](https://i-blog.csdnimg.cn/img_convert/7d7988bfa772a10ec5b4c535c72b99b5.png)

成功调用！


## 2. 接入小智

小智 AI 接入 MCP 有两种方式：

1. 设备端新增 MCP tool；
2. 通过官方暴露的 MCP 接入点；

两种方式各有利弊：
- 前者需要重新制作固件，适合批量生产；
- 后者需要自己部署服务，适合测试；

不过只要能接入工具，交互逻辑是一样的，我们来看效果：

```
硅迹流动针对学生有哪些活动？
```

![](https://i-blog.csdnimg.cn/img_convert/50c96e22adbed576dc0959c5390a5131.png)

```
那针对企业有哪些活动？
```

![](https://i-blog.csdnimg.cn/img_convert/7b06e82fe07607a9535a87734563f503.png)

## 写在最后

本文分享了`如何快速把知识库工具搭建成一个 MCP 服务`，并接入了 `小智AI` 进行实测。

如果对你有帮助，不妨**点赞收藏**备用。

`小智AI + MCP`系列，将陆续分享更多实用、好玩的 MCP 工具。

敬请关注~
