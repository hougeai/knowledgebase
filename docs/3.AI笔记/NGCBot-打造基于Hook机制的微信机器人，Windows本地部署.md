前两篇，带大家手把手搭建了基于云服务器的微信机器人：
- [手把手搭建微信机器人，帮你雇一个24小时在线的个人 AI 助理（上）](https://zhuanlan.zhihu.com/p/707507951)
- [手把手搭建微信机器人，帮你雇一个24小时在线的个人 AI 助理（下）](https://zhuanlan.zhihu.com/p/708378105)

过程略显复杂，对没有云服务器的小伙伴，不是特别友好。

今天分享的这个开源项目，带大家在本地搭建一款微信机器人，调用的是 Windows 电脑端的微信，无需云服务器，无需部署，更安全可靠。

# 1. 项目简介
> 传送门：[https://github.com/ngc660sec/NGCBot](https://github.com/ngc660sec/NGCBot)

一个基于HOOK机制的微信机器人：
- 支持自动拉人，自动群发，自动回复等，解放你的双手
- 支持各种免费的API接口，查天气，查日历等
- 支持 AI 回复，只需传入大模型的 key

所谓 "Hook"机制，是计算机编程中常用的一种技术，它允许开发者拦截系统或应用程序的某些事件、消息。比如在微信机器人中，应用会拦截用户发送的消息，然后根据消息进行判断，进而调用不同的API，把调用结果回复给对方用户，从而代替人工回复信息。

总的来说，自定义程度高，操作简单，小白可轻松上手！

# 2. 前置准备

除了自己常用的微信账号以外，还需要准备一个微信小号。最终我们会把这个小号改造成一个机器人，然后用你的大号对它发号施令。

本项目只能在 Windows 系统中运行，且目前依赖指定微信版本。贴心的是，作者已经把微信安装包准备好了：从仓库主页，找到 Releases 点击进去，

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ceeb63f6390cd8053ad1ba114bbe80c7.png)

在Assets中找到微信安装包并下载：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6152cb44eb5467cd8ef5a6044f26f1a6.png)


# 3. 项目安装
## 3.1 环境准备
下载并安装依赖包：

```
git clone https://github.com/ngc660sec/NGCBot.git
cd NGCBot
pip install pymem
pip install -r requirements.txt
```

此外，因为目前只能使用 3.9.2 版的微信安装包，在扫码登录时会遇到版本过低的问题：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/50519601ce3b16b451fe78cf083ba943.png)

目前作者也提供了解决方案：在项目文件夹下新建 `xiufu.py`，然后填入如下代码：

```
from pymem import Pymem

ADDRS = [0x2FFEAF8, 0x3020E1C, 0x3021AEC, 0x303C4D8, 0x303FEF4, 0x3040FA4, 0x30416EC]

def fix_version(pm: Pymem):
    WeChatWindll_base = 0
    for m in list(pm.list_modules()):
        path = m.filename
        if path.endswith("WeChatWin.dll"):
            WeChatWindll_base = m.lpBaseOfDll
            break
    for offset in ADDRS:
        addr = WeChatWindll_base + offset
        v = pm.read_uint(addr)
        if v == 0x63090A13:  # 已经修复过了
            continue
        elif v != 0x63090217:  # 不是 3.9.2.23 修复也没用
            raise Exception("别修了，版本不对，修了也没啥用。")
        pm.write_uint(addr, 0x63090A13)
    print("好了，可以扫码登录了")

if __name__ == "__main__":
    try:
        pm = Pymem("WeChat.exe")
        fix_version(pm)
    except Exception as e:
        print(f"{e}，请确认微信程序已经打开！")
```


## 3.2 修改配置文件
项目配置文件在 `Config/config.yaml`，用任意一款编辑器打开它。

配置文件的开始进行超级管理员的配置，填入你大号的微信号，用于向小号发号施令。
```
## 超级管理员配置
Administrators:
  - 'wxid_xxx'
```

你的微信号怎么找？任意聊天窗口中，点击你的微信头像即可找到~

如果需要使用 AI 回复功能，还需要配置大模型的应用接口，目前该项目只支持：讯飞星火大模型，OpenAI，百度千帆大模型，填写任意一个即可。

以星火大模型为例，需要在下方配置处填入 ApiSecret ApiKey 等信息。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/0beaae644044ce198a4c07fb0df59d29.png)

目前**讯飞星火 spark lite 模型完全免费**，不知道如何获取这些 key 的同学，可参考猴哥的这篇总结：[拒绝Token焦虑，盘点可白嫖的6款LLM大语言模型API~](https://zhuanlan.zhihu.com/p/703523223)

## 3.3 项目启动 
首先打开电脑端微信，执行修复脚本，解决版本过低而不能登录的问题：
```
(ngcbot) PS D:\projects\NGCBot> python .\xiufu.py
别修了，版本不对，修了也没啥用。，请确认微信程序已经打开！
```

然后执行 python main.py，扫码登录，看到如下信息，说明已经启动成功：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/36426b502c676bb04224f56b87407c72.png)

如果遇到如下报错，把微信从任务管理器中关掉后重启，再重新登录一下就好了。
```
连接失败: Connection refused
```


登录成功后，用你的大号给小号发一条消息，第一个红色箭头处可以看到你大号的微信号，第二个红色箭头是小号：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/59704cac9b22309401f2ed51ebddd223.png)


如果看到红色报错，说明你的 AI 对话模型配置失败，需要查看配置文件进行排查：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/bd50151b8095c4e03922f2e289fd8fc3.png)

只要一个 AI 对话模型配置成功，就可以成功调用，如下是我配置的星火大模型返回的结果：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/cd226aa8e8870a1351eaee939c50de36.png)


启动成功后，把小号拉到一个群聊中，对他发号施令吧~

更多功能使用，参考官方仓库👉[https://github.com/ngc660sec/NGCBot](https://github.com/ngc660sec/NGCBot)

这里展示几张示例：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/23c90c1bdc5ecdbf4577880ffd6e1e30.png)

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a45a697c7bd650c8d4edd4d83e24a098.png)

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/bf5c0b0e54a4506d6d498ee087e24c73.png)

不过猴哥亲测了下，有部分接口已经失效了，看来很有必要进行二次开发~

# 写在最后

至此，一个本地的微信机器人就搭建好了，感兴趣的小伙伴赶紧去试玩~

项目支持二开，有一定开发能力的同学可以基于此添加更多接口和功能。

如果本文对你有帮助，欢迎**点赞收藏**备用！
