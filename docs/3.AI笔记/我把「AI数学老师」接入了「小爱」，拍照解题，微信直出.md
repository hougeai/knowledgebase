上篇给大家分享了`免费AI数学老师`的本地搭建：
- [最强OCR+数学模型Qwen-Math，本地搭建](https://blog.csdn.net/u010522887/article/details/142893400)

有朋友问：有什么方式可以体验一下么？

今天就来安排：把`免费AI数学老师`接入之前搭建的微信机器人`小爱`。

实操才发现，并非容易。因为`Qwen-Math`默认输出 Markdown 格式，且公式是 Latex 代码，如果直接文本输出，实在不忍直视。所以需要把 Latex 文本渲染成图片进行展示。

这里折腾了好久，实操过程分享给大家。

## 1. 新增意图识别
在[零风险！零付费！我把 AI 接入微信群，爸妈玩嗨了~附教程（下）](https://blog.csdn.net/u010522887/article/details/141882177)中，我把`意图识别`任务交给了大模型，因此，这里可以新增一个意图类别：`数学题解`，判断用户是否需要小爱调用`数学题解`服务。

至此，小爱可以识别的意图共有 9 个：

```
['天气', '步行规划', '骑行规划', '驾车规划', '公交规划', '地点推荐', '图片生成', '视频生成', '数学题解']
```

## 2. 核心思路实现

一旦触发`数学题解`意图，`小爱`需要根据用户输入的：图片+问题描述，去调用后端的`AI数学老师`大模型，并将模型回复渲染成图片，发送到微信端。

所以，核心实现逻辑包括以下几步：
- **意图识别**：根据用户聊天记录，进行意图识别，一旦判定为`数学题解`，则执行下一步；
- **图片输入**：从数据库中检索到用户发送的最近一张图片，作为`AI数学老师`的图片输入；
- **文本输入**：从用户输入中提取和问题相关的内容；
- **请求模型**：结合`图片输入`和`文本输入`，请求上篇部署的`AI数学老师`；
- **后处理**：由于`Qwen-Math`返回的是 Latex 文本，需要渲染成图片，答复用户；

## 3. Latex 文本转图片

`Qwen-Math`返回的是 Latex 文本示例如下：

```
要解二次方程 $(x^2 - 4x + 3 = 0)$，我们可以使用因式分解的方法。以下是步骤：

1. **识别二次方程**：给定的方程是 $(x^2 - 4x + 3 = 0)$。

2. **因式分解**：我们需要找到两个数，它们相乘等于常数项（3），并且相加等于线性项的系数（-4）。这两个数是 -1 和 -3，因为 $((-1) \times (-3) = 3)$ 和 $((-1) + (-3) = -4)$。

3. **重写二次方程**：使用这些数，我们可以将二次方程因式分解为 $((x - 1)(x - 3) = 0)$。

4. **解每个因子**：将每个因子等于零并解出 $(x)$。
   $[
   x - 1 = 0 \quad \text{或} \quad x - 3 = 0
   ]$
   $[
   x = 1 \quad \text{或} \quad x = 3
   ]$

5. **写出解**：方程 $(x^2 - 4x + 3 = 0)$ 的解是 $(x = 1)$ 和 $(x = 3)$。

因此，最终答案是 $(\boxed{1 \text{ 和 } 3})$。
```

*直接返回给用户，显然没法看。*

这里尝试了两种方案：
- markdown + imgkit
- matplotlib

其中第一种方案：首先采用 `markdown 库` 将文本渲染成 html 文件，然后再采用 `imgkit 库` 将 html 文件渲染成图片，尝试失败了。。。

下面主要介绍第二种方案，`matplotlib` 可以渲染最基本的 Latex 公式。


对于 Ubuntu/Debian，首先安装字体依赖包：
```
sudo apt-get install fonts-noto-cjk 
```

然后，下载字体文件，比如 `SIMKAI.TTF，SimHei.ttf`

依赖包引入：

```
import re
from matplotlib import pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'SimHei'  # 用来正常显示中文标签
rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
```

如果需要 `matplotlib` 支持所有 Latex 公式，可以加上下面这一行，不过需要先安装号 LaTeX，还比较麻烦。
```
rcParams['text.usetex'] = True
```

如果提示找不到字体文件，可以采用 `fm` 引入自定义字体：
```
import matplotlib.font_manager as fm

font_path = 'data/SIMKAI.TTF'
font_prop = fm.FontProperties(fname=font_path)

plt.figure()
plt.text(0.1, 0.5, markdown_text, fontproperties=font_prop, fontsize=14, va="center", ha="left")
plt.axis('off')  # 隐藏坐标轴
plt.savefig("output_image.png", bbox_inches='tight')
```
最后我们来看一张渲染结果：

![](https://img-blog.csdnimg.cn/img_convert/0c33991342d82888cd95226d1a92e33c.png)

当然，因为`matplotlib` 对 Latex 的支持有限，你会发现很多公式无法搞定，所以最好加上一些`正则表达式`的前置处理：

```
def markdown_to_img(markdown_text, image_path='output.png'):
    try:
        markdown_text = re.sub(r"\\boxed\{([^$]*)\}", r"\1", markdown_text)
        markdown_text = re.sub(r"\\text\{([^}]*)\}", r"\1", markdown_text)
        markdown_text = re.sub(r"(\$\[)(.*?)(\]\$)", lambda m: m.group(1) + re.sub(r"\s*\n\s*", " ", m.group(2)) + m.group(3), markdown_text, flags=re.DOTALL)
        markdown_text = markdown_text.replace(r"\quad", " ")
        markdown_text = markdown_text.replace("和", "&").replace("或", "|")
        plt.figure()
        plt.text(0.1, 0.5, markdown_text, fontproperties=font_prop, fontsize=14, va="center", ha="left")
        plt.axis('off')  # 隐藏坐标轴
        plt.savefig(image_path, bbox_inches='tight')
    except Exception as e:
        print(e)
```

最终效果展示如下：

![](https://img-blog.csdnimg.cn/img_convert/ca46e410a458a67c74f8f63d9990893b.png)

## 4. 效果展示

最后，我们接入微信机器人，看看测试效果吧：


![](https://img-blog.csdnimg.cn/img_convert/7e38ac1fd0e6c8a2ddf29651baa05aab.png)

默认会从数据库中检索用户最近上传的一张图片，如果没有，则完全基于文本输入进行回答。

![](https://img-blog.csdnimg.cn/img_convert/c3d35c51e035734a40d3f8acef897555.png)

## 写在最后

本文通过简单两步为`小爱`接入了 `AI数学题解` 的能力，你只需拍照上传图片，任性向他提问。

希望这款`免费AI老师`，能帮你省下一笔家教费~

如果对你有帮助，不妨**点赞收藏**备用。

大家有更好的想法，欢迎来聊。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。




