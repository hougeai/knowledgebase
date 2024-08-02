
话接上篇：
- [自动化处理 PDF 文档，完美实现 WPS 会员功能]()
- [如何优雅地实现 PDF 去水印？]()


后台有小伙伴们问：能否基于已有的内容（文本、图像等），一键生成 PDF 文档？

或者说，能否将其他格式的文档一键转换成 PDF ？

必须能！

今天带来的这款 Python 工具 - `reportlab`，可以完美实现上述功能，希望给有类似需求的小伙伴一点帮助~

话不多说，我们直接上实操。

## 0. 前置准备
首先需要在电脑上准备好 Python 环境，有不了解的小伙伴，送你一份保姆级教程：[【7天Python入门系列】Day1：环境准备之Conda和VS code安装](https://zhuanlan.zhihu.com/p/688627817)

生成 PDF 文档，需要用到 `reportlab` 这个工具包，打开终端，一键安装：

```
pip install reportlab
```

`reportlab` 这个库可以实现编辑文字、画图、绘表格等众多功能，最终输出为 PDF 文档，非常强大。




## 1. 引入必要模块

```
from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
from reportlab.lib import colors  # 颜色模块
from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
from reportlab.graphics.charts.legends import Legend  # 图例类
from reportlab.graphics.shapes import Drawing  # 绘图工具
from reportlab.lib.units import cm  # 单位：cm
```

然后，我们引入本地电脑支持的字体，注册注册一个字体：

```
pdfmetrics.registerFont(TTFont('simkai', 'C:\Windows\Fonts\simkai.ttf'))
```
Windows 电脑中，字体默认保存在 `C:\Windows\Fonts\`，文件后缀为 .ttf，在其中找到想要想要生成的字体路径，填入上述代码片段对应位置。

## 2. 实现不同功能
### 2.1 插入标题

下方的示例代码给出了一级标题的默认配置。
```
def draw_title(title, color=colors.black, title_style='Heading1', font_size=18):
    # 获取所有样式表
    style = getSampleStyleSheet()
    # 设置标题样式
    ct = style[title_style]
    # 单独设置样式相关属性
    ct.fontName = 'simkai'      # 字体名
    ct.fontSize = font_size     # 字体大小
    ct.leading = 50             # 行间距
    ct.textColor = color   # 字体颜色
    ct.alignment = 1    # 居中
    ct.bold = True
    # 创建标题对应的段落，并且返回
    return Paragraph(title, ct)
```
如果要插入二级标题，可以设置标题样式为 `style['Heading2']`，然后字体大小设置为 16。

当然，`getSampleStyleSheet()`已经设置好了默认配置，也可以直接使用，示例代码是为了给大家实现更多定制化，提供参考。
### 2.2 插入文本段落

```
def draw_text(text: str):
    # 获取所有样式表
    style = getSampleStyleSheet()
    # 获取普通样式
    ct = style['Normal']
    ct.fontName = 'simkai'
    ct.fontSize = 15
    ct.wordWrap = 'CJK'     # 设置自动换行
    ct.alignment = 0        # 左对齐
    ct.firstLineIndent = 24 # 第一行开头空格
    ct.leading = 25
    return Paragraph(text, ct)
```
和标题的设置基本一致，如果要设置首行缩进，需要修改 `ct.firstLineIndent`。

### 2.3 插入图片

```
def draw_img(path, width=10*cm, height=5*cm):
    img = Image(path)           # 读取指定路径下的图片
    img.drawWidth = width       # 设置图片的宽度
    img.drawHeight = height     # 设置图片的高度
    img.hAlign = 'CENTER'       # 设置图片的水平居中
    return img
```
可以自定义图像大小 以及 居中表示。

### 2.4 插入表格

```
def draw_table(*args):
    col_width = 120 # 列宽度
    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'simkai'),  # 字体
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # 第一行的字体大小
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # 第二行到最后一行的字体大小
        ('BACKGROUND', (0, 0), (-1, 0), '#d5dae6'),  # 设置第一行背景颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 第一行水平居中
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # 第二行到最后一行左右左对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 所有表格上下居中对齐
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.darkslategray),  # 设置表格内文字颜色
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为grey色，线宽为0.5
    ]
    table = Table(args, colWidths=col_width, style=style)
    return table
```
`style` 中设置表格样式，其中`(0, 0)`代表`列`和`行`的位置。`*args`传入表格内容。


## 3. 生成 PDF
接下来，采用上述函数，我们给出一个简单的生成 PDF 的示例。

```
content = []
# 添加标题
content.append(draw_title('猴哥的AI知识库'))
# 添加小标题
content.append(draw_title('By 猴哥', color=colors.darkslategray, title_style='Heading2', font_size=16))
# 添加段落文字
content.append(draw_text('你好！欢迎来到猴哥的AI知识库，这里汇集了猴哥在AI领域的一些经验和知识。'))
# 添加表格
data = [
    ('编程语言', '排名', '较上年增长'),
    ('Python', '1', '2.7%'),
    ('C++', '2', '-0.4%'),
    ('Java', '3', '-2.1%')
]
content.append(draw_table(*data))
content.append(draw_text(' '))
# 添加图片
content.append(draw_img('1.png'))
# 生成pdf文件
doc = SimpleDocTemplate('1.pdf', pagesize=letter)
doc.build(content)
```

最终合成的效果如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/902978ee-dfbe-46e3-82ec-8498a2dd8bfe.png)

上面仅是一个简单的示例，感兴趣的小伙伴可以结合自己的需求进行尝试。

## 写在最后

本文带大家采用 Python 和 reportlab 库，实现了一键生成 PDF 文档，旨在帮助大家提供办公效率。

如果本文对你有帮助，欢迎**点赞收藏**备用。

如果本文对你有帮助，不妨点个免费的“赞”和“在看”，随手“转发”支持一下。
