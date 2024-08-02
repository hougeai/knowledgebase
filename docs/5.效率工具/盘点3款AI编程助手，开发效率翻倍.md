伴随着 AI 的大火，后台有小伙伴问我：AI 是否会淘汰程序员？

我的答案很明确：

AI 只会淘汰不会用 AI 的程序员。

也会你对 AI 的印象还停留在智能问答。

但，你不得不感叹，AI 已渗透到你职场的方方面面。

设计师用 AI 生成图像，运营人员用 AI 来优化文案，客服人员用 AI 来智能回复，程序员用 AI 来生成代码，据称百度内部 20% 的代码都是由 AI 生成的。

**虽然 AI 写代码已经很强了，但有多少同学能真正用好它呢？**

今日分享，就给大家展示下如何应用 AI 编程助手，提高开发效率。

# 1. 是什么 

AI 编程助手，说白了就是以 GPT 为代表的大语言模型，在编程这个垂直场景的应用。

其中的典型代表就是 GitHub 和 OpenAI 合作开发的 Copilot，目前国内也有了很多平替。

下面分别简单介绍一下它们。

## 1.1 GitHub Copilot
> 官网：[https://github.com/features/copilot/](https://github.com/features/copilot/)

不多说了，AI 编程助手工具领域的祖师爷，底层是 GPT-3.5，经过了大量代码片段的训练，因此非常擅长结构化的代码语法和语义。

体验非常出色，唯一的缺陷是需要付费使用，不过新注册用户可以免费体验一个月。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d5eaf99080f745d991e116c5af58f382.png)

接下来介绍的3款国产平替，对个人开发者都是免费的，个个能顶。

## 1.2 Comate
> [https://comate.baidu.com/zh](https://comate.baidu.com/zh)

百度开发的 AI 编程助手，底层是百度的文心大模型，训练数据包含了百度自己多年积累的代码大数据和优秀开源项目，在百度内部得到了广泛使用。


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b49790640df692f32584e36f874c4e34.png)


## 1.3 CodeGeex
> [https://codegeex.cn/](https://codegeex.cn/)

CodeGeex 是智谱团队开发的一款 AI 编程助手，底层是 GLM 大模型，同样经过了大量代码数据的训练。**完全免费**，生态活跃。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f2b63a3b9bfbf7ce68dcd9fedd10c73a.png)


## 1.4 FittenCode
> [https://code.fittentech.com/](https://code.fittentech.com/)

Fitten Code是由非十科技研发，底层由大模型驱动的AI编程助手，**完全免费**，速度超快。


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ccd080f1a59326ddbe36e915a3c42a44.png)

要问哪款更好用？

国产的 3 款 AI 编程助手，就目前的体验而言，都非常丝滑，都支持插件安装，而且使用方式也基本雷同。

所以，喜欢哪个用哪个~

# 2. 怎么用
下面就以我经常使用的 Fitten Code 为例，给大家展示下具体的使用案例。

## 2.1 插件安装

这些 AI 编程助手，都支持直接在 IDE 中作为插件使用，覆盖 VS Code、JetBrains 都主流 IDE ~

不知道大家常用的 IDE 都有哪些？这里以轻量编辑器 VS Code 给大家演示。

点击左侧的扩展页面，然后在搜索框中，输入 Fitten code （Comate、CodeGeex）都是类似的，右侧点击安装:

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/0a2b7bbd46ac50388f0eb2665da90dae.png)

然后在左侧侧边栏就会看到多了一个插件的图标：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c965719cdb5f798440763f0049c9503f.png)

接下来，给大家演示下猴哥最常用的几个功能。

## 2.2 代码解释

刚 clone 一份开源项目，代码看不懂怎么办？

没关系，选中你看不懂的部分，右键选择 “Fitten Code – 解释代码” 进行解释，左侧直接给出详细解释。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ec3320b4b6043055bd8f0ae69807dcab.png)

## 2.3 代码补全
这个功能可以说是最常用的。

那么多库，那么多函数名，记不住怎么办？

初始化一个类，需要自定义很多变量，实在是太繁琐！

没关系，现在你只需要一次 Tab 键！

打开代码文件，输入一段代码，Fitten Code 会根据上下文，为您自动补全代码，如果接受它的建议，按下 Tab 键，然后再调整到你的预期就好。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/558651b3c77701d612d0eb4ffed0cfbc.png)

## 2.4 注释生成代码
这个功能其实还是代码补全，不过日常经常用到，所以单独拎出来。

写一段注释，比如我说 `"编写冒泡排序算法"`，Fitten Code 会根据上下文，将你的注释意图补全，给出 `"编写冒泡排序算法，将 ADDRS 数组排序，使得修复版本号的地址在前面"`。

接下来，你只需要不断按下 Tab 键，接受它一步一步给你的建议。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a687376d19c73823dad9c56c51f38bde.png)

## 2.5 代码生成注释
相反，Fitten Code 还能够根据您的代码自动生成注释。

通过分析您的代码逻辑，为您的代码提供清晰易懂的解释，提高代码的可读性。

选中需要生成注释的代码段，然后右键选择 “Fitten Code – 生成注释”

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d7e3b20c968566645e06c648d68963d1.png)

```
def bubble_sort(arr):
    # 获取数组的长度
    n = len(arr)
    # 外层循环控制遍历的次数
    for i in range(n):
        # 内层循环进行相邻元素的比较和交换
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
```


## 2.6 Bug 修复

程序员最痛苦的事，莫过于修 Bug 。

开发 1 小时，bug 修 1 天。

莫名其妙的 Bug，现在有 AI 帮你搞定。

比如，上述冒泡排序算法中，我把索引搞错了，来看看 AI 怎么帮我解决：

选中对应代码段，然后右键选择 “Fitten Code查找Bug” ，如下图所示。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a1ea0ba0d16191fa30fe184e56750892.png)


## 2.7 对话问答
这个功能自由度最高，你可以随意问他你想要实现的功能：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e24983b296a32b59d72e7009317334ba.png)

当然，你也可以基于某一段代码中不理解的部分，向他提问：

选中代码部分，聊天框中输入你的问题，Fitten Code会自动引用用户所选中的代码段。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/1a00b646d2ddf9afc89cfd5aa4162ed8.png)

# 写在最后

怎么样？这样写代码的效率，是不是快了很多。

强烈建议大家用好这些 AI 工具，帮你节省时间，实现更多创意~

遇事不决，就问 AI。

如果本文对你有帮助，欢迎**点赞收藏**备用！
