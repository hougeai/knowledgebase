数字化办公已成常态，文档管理和处理是很多小伙伴的日常工作。

PDF（Portable Document Format）文档因其跨平台兼容性和格式固定性而备受青睐。

然而，对于非WPS会员用户而言，一些高级功能如批量处理、格式转换、添加水印等常常受限。

即便是充了会员，有些文档的水印也无法完全去除。

本文旨在揭示如何通过 Python 和相关库，自动化处理 PDF 文档，从而完美实现类似WPS会员的高级功能，无需额外付费。

文章目录如下（按需取用）：
- **生成水印** —— 创建专属水印，保护你的文档版权。
- **添加水印** —— 将水印无缝融合到PDF文档中，增强文档的专业性和安全性。
- **提取文本内容** —— 从PDF中快速抽取文字，便于二次编辑和使用。
- **多个PDF合并** —— 将分散的PDF文件整合成一份，简化文档管理和阅读体验。
- **单个PDF分割** —— 按页或章节拆分大型PDF文档，便于分享和管理。
- **PDF转图片** —— 将PDF页面转换为图像格式，适用于各种展示场景。
- **图片转PDF** —— 反向操作，将多张图片合成为一份PDF文档，方便打印和分享。

## 0. 前置准备
首先需要在电脑上准备好 Python 环境，有不了解的小伙伴，送你一份保姆级教程：[【7天Python入门系列】Day1：环境准备之Conda和VS code安装](https://zhuanlan.zhihu.com/p/688627817)

PDF 文档处理，一般会用到下面三个库，打开终端，一键安装：

```
pip install PyPDF2
pip install PyMuPDF
pip install reportlab
```

## 1. 生成水印
采用 reportlab 的画布功能，先引入必要的模块：
```
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics   # 注册字体
from reportlab.pdfbase.ttfonts import TTFont # 字体类
from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
```

然后，我们引入本地电脑支持的字体，注册字体类：

```
pdfmetrics.registerFont(TTFont('simkai', 'C:\Windows\Fonts\simkai.ttf'))
```
Windows 电脑中，字体默认保存在 `C:\Windows\Fonts\`，文件后缀为 .ttf，在其中找到想要想要生成的字体路径，填入上述代码片段对应位置。


最后，给出函数实现：

```
def create_watermark(watermark_text='公众号：猴哥的AI知识库', font=15, pagesize=(30*cm, 30*cm)):
    watermark_canvas = canvas.Canvas("data/watermark.pdf", pagesize) # 指定存放位置和画布大小
    watermark_canvas.setFont("simkai", font) 
    watermark_canvas.setFillAlpha(0.1) # 设置透明度,1为不透明
    watermark_canvas.translate(10*cm, 5*cm)
    watermark_canvas.rotate(30) # 水印旋转角度
    for i in range(5):
        for j in range(10):
            a = 10*(i-1)
            b = 5*(j-2)
            watermark_canvas.drawString(a*cm, b*cm, watermark_text)
    watermark_canvas.save()
```

注意：画布大小可以作为一个参数传入，可根据 pdf 页面的大小进行设置。此外，你还可以任意修改水印的位置和字体。

如何获取 pdf 页面的大小，接着往下看。

我们先来看下生成的水印效果：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f46b9a1e-54c0-412c-bba2-6638c60387ee.png)


## 2. 添加水印

如何将上面生成的水印，添加到我们的 PDF 文档中？


首先，我们引入 PyPDF2 中的读写类，给定要插入水印的 PDF (`input_pdf`)和输出的 PDF (`output_pdf`)。

然后，根据输入的 PDF 首页大小创建水印文件。

```
page_size = (first_page.mediabox.width, first_page.mediabox.height)  # 获取页面大小
```


最后，调用 `.merge_page` 方法为每一页插入水印，当然也可以设置间隔几页插入，或者只插入特定页。

实现代码如下：
```
from tqdm import tqdm
from PyPDF2 import PdfReader, PdfWriter

def add_watermark(input_pdf, output_pdf, watermark_text='公众号：猴哥的AI知识库'):
    pdf_reader = PdfReader(input_pdf)  # 读取需要添加水印的文件
    first_page = pdf_reader.pages[0]
    page_size = (first_page.mediabox.width, first_page.mediabox.height)  # 获取页面大小
    create_watermark(watermark_text, pagesize=page_size)  # 创建水印PDF

    pdf_writer = PdfWriter()  # 创建PDF文件写入对象
    watermark_file = PdfReader("data/watermark.pdf")  # 读取水印PDF(假设水印页只有一页)

    for page_num in tqdm(range(len(pdf_reader.pages)), desc='add_watermark'):  # 遍历每一页PDF对象
        pdf_page = pdf_reader.pages[page_num]  # 获取PDF的当前页对象
        pdf_page.merge_page(watermark_file.pages[0])  # 将水印页合并到当前页中
        pdf_writer.add_page(pdf_page)  # 将合并后的PDF对象页添加到PDF写入对象中
    with open(output_pdf, 'wb') as output:  # 打开输出文件
        pdf_writer.write(output)  # 写入PDF内容到输出文件
```

最终效果，我们拿南瓜书来举个例子：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a8776213-95a0-44ac-8754-0450896e0d79.png)


## 3. 提取文本内容

手动复制 PDF 中的文本实在太麻烦了，能否一键提取所有内容？

不但能，而且还可以转存成 MarkDown 格式。

这里提供两种方式~

方式一：采用 PyPDF2：调用`.extract_text()`方法

```
def pypdf_to_txt(input_pdf, output_path='output.md'):
    pdf_reader = PdfReader(input_pdf)
    markdown_lines = []
    # 遍历PDF的每一页
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        markdown_lines.append(text)
        markdown_lines.append("\n\n")  # 分页
    # 将文本写入Markdown文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(markdown_lines)
```

方式二：采用 PyMuPDF
> 注：fitz 是 PyMuPDF 库的一个模块
```
import fitz
def pymupdf_to_txt(input_pdf, output_path='output.md'):
    pdf_document = fitz.open(input_pdf)
    markdown_lines = []
    # 遍历PDF的每一页
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")
        if not text:
            pm = page.get_pixmap()
            pm.save("temp.png")
            img = cv2.imread("temp.png")
            texts = img_ocr(img_data=img)
            # os.remove("temp.png")
            markdown_lines.append("\n".join(texts))
        else:
            markdown_lines.append(text+"\n\n")
    # 将文本写入Markdown文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(markdown_lines)
```
上述函数中，还加了一层判断，也即如果识别到当前 PDF 页是一张图片，没有文字，怎么办？

此时，我们可以调用 OCR 方法，识别出所有文字再进行拼接，市面上开源的 OCR 方案有很多，大家都在用哪款 OCR，欢迎评论区告诉我。

关于如何优雅地使用 OCR，如果感兴趣的小伙伴多的话，猴哥再单独出一篇分享。

## 4. 多个 PDF 合并
了解了上述操作以后，实现 PDF 合并就很简单了。

首先，新建一个 writer 用于写入新文件；

然后，每一个输入文件都对应一个 reader。

直接上代码：


```
def merge_pdf(input_pdfs, output_pdf):
    pdf_writer = PdfWriter()
    for input_pdf in input_pdfs:
        pdf_reader = PdfReader(input_pdf)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    with open(output_pdf, 'wb') as f:
        pdf_writer.write(f)
```


## 5. 单个 PDF 分割

如果想把一个大型 PDF 按需切割成多个文件，比如按页切割 或者 按章节切割，怎么处理？

假设我们每 10 页切割成一个 PDF，这里给一个示例代码：

```
def split_pdf(input_pdf, per_num=10):
    pdf_reader = PdfReader(input_pdf)
    total_pages = len(pdf_reader.pages)
    file_dir, file_name = os.path.split(input_pdf)
    file_base, file_ext = os.path.splitext(file_name)
    new_folder_path = os.path.join(file_dir, file_base)
    os.makedirs(new_folder_path, exist_ok=True)
    for start in range(0, total_pages, per_num):
        end = min(start + per_num, total_pages) 
        pdf_writer = PdfWriter()
        for i in range(start, end):
            pdf_writer.add_page(pdf_reader.pages[i])
        output_file_path = os.path.join(new_folder_path, f'{file_base}_{start}_{end}{file_ext}')
        with open(output_file_path, 'wb') as f:
            pdf_writer.write(f)
```


## 6. PDF 转成图片

按照本文第 2 部分的方式添加水印，很容易被一键去水印，比如 WPS 的会员功能。

如果要使得自己的水印变得更为隐蔽，最好是将 PDF 转为图片，然后在图片中添加水印。

如何将 PDF 转成图片？

这里我们采用 fitz 进行处理：

```
def pdf2imgs(input_pdf, png_path, zoom=200):
    doc = fitz.open(input_pdf)
    total = doc.page_count
    for pg in tqdm(range(total), total=total, desc='pdf2imgs'):
        page = doc[pg]
        zoom = int(zoom)  # 值越大，分辨率越高，文件越清晰
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        os.makedirs(png_path, exist_ok=True)
        pm.save(os.path.join(png_path, '%s.png' %(pg)))
    doc.close()
    return total
```

## 7. 图片转 PDF
接上一步，将加了水印的图片再合成为 PDF 文件。

```
def imgs2pdf(image_paths, output_path='1.pdf'):
    doc = fitz.open()
    for img in tqdm(image_paths, desc='imgs2pdf'):
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convert_to_pdf()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insert_pdf(imgpdf)
    doc.save(output_path)
    doc.close()
```

## 写在最后

本文带大家采用 Python 和相关库，自动化批量处理 PDF 文档，完美实现了类似 WPS 会员的高级功能，旨在帮助大家提供办公效率。

这些功能已足够我们解放双手了，还有未尽功能，欢迎评论区留言告诉我。

如果本文对你有帮助，欢迎**点赞收藏**备用。