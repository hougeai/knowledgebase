
前两天，想导出微信聊天记录，发现很多都要收费，我想着「这破功能还得收费？」，于是决定自己搞一个。

感兴趣的小伙伴，可以回看：

- [微信聊天记录导出为电脑文件实操教程（附代码）]()

- [自制神器！一键获取所有微信聊天记录]()

拿到这些数据都有什么用？

今天突发奇想，把我和老婆近一年的聊天记录发给 AI 大模型 - Kimi，看看它能分析出个啥。。。
# 1. 为啥选择 Kimi
在众多AI大模型中，Kimi 这款大模型有两大最明显的优势：

**长文本处理能力**：Kimi 号称能够阅读并理解长达200万字甚至1000万字的长文本（不过我实际测下来并没有啊）。

**文件处理能力**：Kimi可以处理多种格式的文件，包括TXT、PDF、Word文档、PPT幻灯片和Excel电子表格等。

# 2. 聊天记录怎么获取
上一篇: [自制神器！一键获取所有微信聊天记录]()，自制了一个 `微信信息提取` 的小工具，就拿它来提取出我们之间这一年的聊天记录。

我们平时主要还是语音聊的比较多，文字信息发的少一些。

Kimi 尽管具备长文本处理能力，不过我发现，如果不过滤掉超链接等一些无效文本，直接把整个聊天记录发给它，Kimi 表示超出了它的理解能力？
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/611a41aea5ad460da2a48c8486d6633c.png)

于是，通过设置如下规则，只保留文本数据：

```python
def filter_chat_info(chat_file='output/chat.json'):
    data = json.load(open(chat_file, 'r', encoding='utf-8'))
    res = []
    times = set()
    for time, name, content in data:
        if time in times:
            continue
        times.add(time)
        if content in ['[图片]', '[语音]', '[视频]', '[表情包]', '[文件]', '[分享卡片]', '[音乐与音频]']:
            continue
        if '[链接]' in content:
            continue
        res.append((time, name, content))
    with open('output/chat_new.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
```

过滤完成后，共 1700 多条，在 Kimi 能接受的文本长度范围之内，接下来发给它，看看能问出个啥来！
# 3. 和 Kimi 的对话
直接把生成的 json 文件发给它，初始化提示词设定为：*这是我和我老婆近一年的聊天记录，我需要你帮我仔细分析后，回答我一些问题。*

一年的聊天记录，不到 2s  给你分析的妥妥的，且看下面 Kimi 的答复，着实给我感动了一把。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/294ef0b23fbb4a4bbb10b729b57afa79.png)
“你们聊天语气比较平和，很少有争吵。”  想想确实也是，谁也不至于闲到用文字聊天吵架吧。

遗憾的是，语音聊天的记录没法保存下来，丢失了一大部分宝贵的聊天语料，否则在未来的某一天，让 AI 帮忙写一本回忆录，妥妥没问题！

接着来考验它的信息抽取能力：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/bf02f9fa8d1b49a8a5684e72126ed9a0.png)

你看看这回答，有模有样，共提取到了6次有效数据，时间和聊天记录也都能对应上。

总的来说， Kimi 的回答还是挺有温度的。目前还没有拿其他 AI 大模型测过，感兴趣的小伙伴可以去试试看~
# 写在最后

我相信，真正有价值的并非是聊天记录本身，而是那些在聊天窗口背后默默展开的深刻故事。

AI 已来，而我们的数据将是 AI 了解我们过往记忆的宝贵财富。

如何善用并用好这些数据，是我们每个人绕不开的话题。进一步，如何将这些数据和  AI 结合，做出更有价值、更有创意的应用，是值得每一个 AI 开发者思考的话题。

AI 已来，这将是一场关于真挚情感的革命，一场让技术更加贴近人心的探索。

我是猴哥，一直在做 AI 领域的研发和探索，会陆续跟大家分享路上的思考和心得。

如果本文对你有帮助，欢迎点赞收藏备用！




