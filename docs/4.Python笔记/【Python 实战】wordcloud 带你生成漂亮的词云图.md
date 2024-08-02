前两天写了一篇微信聊天记录导出教程：

[AI布道师：微信聊天记录导出为电脑文件实操教程（附代码）](https://zhuanlan.zhihu.com/p/704293254)

后台很多小伙伴对词云感兴趣：给一段文本，然后根据其中词语出现的频率，生成好看的词云，像下面这张图一样：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-3b4761ec369c0aedbaab5e13b23104cc_1440w.png)





添加图片注释，不超过 140 字（可选）

生成这个其实很简单，几行 Python 代码就能搞定，今天就来带大家实操一番。

## 1. 环境准备

配置好 Python 环境后，需要安装两个包：

- jieba：用于分词
- wordcloud：用于生成词云

```
pip install jieba
pip install wordcloud
```

## 2. 获取模板图片（可选）

wordcloud 中默认生成的是矩形图片。

如果希望生成的词云图片具有特定的样式，你需要准备一张 png 格式的含有透明图层的图片，像下面这样：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-93332c139b505d566b0dace2116fa61a_1440w.png)





添加图片注释，不超过 140 字（可选）

怎么获取 png 格式的图片？

打开：https://www.remove.bg/zh/upload

上传一张图片，然后点击下载即可：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-dc737ee76791ab41c7f44bc8975f6849_1440w.png)





添加图片注释，不超过 140 字（可选）

## 3. 获取字体文件

Windows 电脑中，字体默认保存在 C:\Windows\Fonts\，文件后缀为 .ttf。

找到想要想要生成的字体路径。

## 4. 获取文本信息

大家可以试试自己的微信聊天记录。

这里我们以《红楼梦》小说为例进行演示，输入的是 .txt 文本文件。

```
import jieba
def cut_words(text):
    # 使用 jieba 分词
    words = jieba.cut(text)
    return ' '.join(words)
with open('D:\Downloads\data\红楼梦.txt', 'r', encoding='utf-8') as f:
        text = f.read()
text = cut_words(text)
```

## 5. 生成词云图

最后，初始化一个 wordcloud 实例，把刚刚分词后的文本输入进来，生成最终的词云图片。

```
import wordcloud
def generate_wordcloud(text, stopwords=None, mask=None, max_words=50, img_name='1.jpg'):
    wordcloud = WordCloud(width=800, height=400, 
                        mask=mask,
                        background_color='white',
                        stopwords=stopwords,
                        font_path='C:\Windows\Fonts\simkai.ttf', # simkai.ttf STXINGKA.TTF
                        max_words=max_words,
                        ).generate(text)
    wordcloud.to_file(img_name)
```

- text：第 4 步分词后的文本；
- mask：第 2 步拿到的模板图片；
- stopwords: 停止词，对于你不想在词云中出现的词，你都可以添加到这个文件中过滤掉它；
- max_words：比如50，就是选择出现频率最高的50个词进行展示。

你可以换用不同的背景 mask 试试~

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-3912e6c5596f5ac1d3eca3a0863d6e99_1440w.png)





添加图片注释，不超过 140 字（可选）

## 写在最后

如果本文对你有帮助，欢迎**点赞收藏**备用！

我是猴哥，一直在做 AI 领域的研发和探索，会陆续跟大家分享路上的思考和心得，以及干货教程。

新朋友欢迎关注 “**猴哥的AI知识库**” 公众号，下次更新不迷路👇。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/v2-c44e3bede3365c259472d1957a423324_1440w.png)
