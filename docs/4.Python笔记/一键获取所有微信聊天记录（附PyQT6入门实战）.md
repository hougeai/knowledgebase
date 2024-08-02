
想导出微信聊天记录，发现很多都要收费，我想着「这破功能还得收费？」，于是决定自己搞一个。

话接上篇：[微信聊天记录导出为电脑文件实操教程（附代码）](https://blog.csdn.net/u010522887/article/details/139795722)

后台有小伙伴反应，能不能搞个图形界面？方便分享给朋友一起用。

经过半天的摸索，终于搞出来一个还有点糙的工具，免费分享给大家。

本篇主要记录工具制作过程和使用方法，只需要工具的小伙伴，直接拉到文末自取~

# 1 界面搭建-PyQT
## 1.1 环境准备
用 Python 写的脚本程序，如何制作一个可视化界面呢？

选择有很多，比如 Python 的标准GUI库 Tkinter, 不过可以实现的功能比较简单。

考虑到后续可能还需要做的更复杂，所以决定选择主流的 PyQT 框架。

在 Python 中，PyQt 和 PySide 都是基于Qt框架的两个库，它们提供了丰富的控件和功能来创建复杂的GUI应用程序。

实在没弄明白，为啥同一个东西需要搞出不同的名称来？

选框架，当然是选最新且最稳定的了，主流的 PyQt 是 PyQt5，后来发现最新已经是第6版了，不过是 PySide6，相比 PyQt，使用了更宽松的许可证（LGPL）。

PySide6 提供了与PyQt相似的功能和API。PySide6的优点在于它基于Qt 6，具有高性能、丰富的组件库和强大的设计工具。同时，PySide6还提供了对触摸输入的支持，适用于开发触摸型的软件。

PySide6 和 PyQt5 的用法非常类似，如果熟悉 PyQt5 开发的小伙伴，上手 PySide6 将非常容易。举个最简单的例子，你就明白了：

```python
# from PySide6 import QtWidgets
from PyQt5 import QtWidgets
```

综上，直接上 PySide6，pip 一键安装，非常方便：

```python
pip install pyside6
```
## 1.2. 熟悉组件

PyQt 中最基础的组件就是这个 QtWidgets，由于我们这个工具主要就是一个窗口，所以直接一个类搞定.

新建一个文件 - `main.py`。 初始化 `MainWindow` 类时，把软件名称和 Logo 图像先放上去：

```python
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("微信信息提取工具")
        self.setWindowIcon(QtGui.QIcon('data/logo.png'))
        self.setupUI()
```
接下来，我们来编写 `setupUI()` 函数，把 UI 界面搭出来。

搭界面，首先需要布局，这时需要用到 PyQt 中的布局组件，这个工具我主要用到了两种布局组件：
-  QBoxLayout 盒子布局
- QFormLayout 表单布局

最简单的，将布局分成上下两个部分：

```python
def setupUI(self):        
   main_layout = QtWidgets.QVBoxLayout()
   self_groupbox = self.create_self_groupbox()
   chat_groupbox = self.create_chat_groupbox()
   self_groupbox.setStyleSheet(style)
   chat_groupbox.setStyleSheet(style)

   main_layout.addWidget(self_groupbox)
   main_layout.addWidget(chat_groupbox)
   bottom_text = QtWidgets.QLabel("by 公众号：猴哥的AI知识库")
   bottom_text.setAlignment(QtCore.Qt.AlignRight)
   main_layout.addWidget(bottom_text)
   self.setLayout(main_layout)
```

这时又发现，界面实在太丑了，能不能把样式美化一下？

查了写资料，发现 PyQt 中有一个 QSS 的概念，类似网页布局中的 CSS，熟悉 CSS 语法的同学，很容易看懂 QSS 。举一个例子，比如我要修改按钮的样式，可以在 style 中直接定义：

```python
style = """
QPushButton {
    background-color: #4CAF50;  /* 按钮背景色 */
    color: white;               /* 按钮文字颜色 */
    border: 1px solid #4CAF50; /* 按钮边框 */
    border-radius: 10px;       /* 按钮边框圆角 */
    padding: 1px;              /* 按钮内边距 */
}
QPushButton:hover {
    background-color: #45a049;  /* 鼠标悬停时的背景色 */
}
QPushButton:pressed {
    background-color: #397d35;  /* 按钮被按下时的背景色 */
}
"""
```

基于上面这些内容，一个粗糙的界面雏形就出来了：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/2e3664b8a80c4537a485de7db808914e.png)
## 1.3. 封装功能

骨架搭建起来后，接下来需要为它装入灵魂！

说白了，就是把想要实现的具体功能编写成函数，然后和 对应的按钮 实现通信。

每个一个功能对应一个函数，比如我这里主要是四个功能：![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/e26f8a5da5374da19a67329f0ac4e21b.png)
# 2. 工具打包-PyInstall
用 Python 写的脚本程序，如何制作成windows上的可执行文件，让其他人也能用上？

PyInstaller 是比较主流的一个工具，它可以将Python脚本和所有依赖项打包成一个可执行文件。

使用PyInstaller的基本步骤如下：

## 2.1 安装
Python 环境下安装 PyInstaller ，很简单：
```python
pip install pyinstaller
```
## 2.2 打包
然后，命令行使用 PyInstaller 创建可执行文件：

```python
pyinstaller --onefile main.py
```

注意：--onefile 选项会创建单个的exe文件，包含所有必需的文件。

如果创建失败，可以采用如下命令，重新打包：

```python
pyinstaller --onefile --clean main.py
```
注意，打包这里很容易报错，比如我在打包到下面这一步时报错：

```python
File "D:\miniconda3\envs\wechat\lib\dis.py", line 292, in _get_const_info
    argval = const_list[const_index]
IndexError: tuple index out of range
```
一开始还以为是 `matplotlib` 等相关的依赖出现问题，但发现不能根本解决问题。找了很久，终于在 pyinstall 官方仓库中找到一条解决方案：

修改这里报错的 "D:\miniconda3\envs\wechat\lib\dis.py" 文件，找到_unpack_opargs函数，在倒数第二行中添加 extended_arg = 0，修改后的代码如下：

```python
def _unpack_opargs(code):
    extended_arg = 0
    for i in range(0, len(code), 2):
        op = code[i]
        if op >= HAVE_ARGUMENT:
            arg = code[i+1] | extended_arg
            extended_arg = (arg << 8) if op == EXTENDED_ARG else 0
        else:
            arg = None
            extended_arg = 0  # +
        yield (i, op, arg)
```

打包成功后，在你的当前目录下会多出一个文件夹 `dist`，里面有 `main.exe`，搞定！ 

可以分享出去了~
# 3. 工具使用教程
下面介绍下我们制作的 `微信信息提取工具`。

双击 `main.exe` 打开后，会自动打开一个终端，后台输出的信息会显示在终端。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b57fadec9794403aa2f426b08af62671.png)

主要功能包含两个部分：
## 3.1 个人信息提取
首先确保微信电脑端已经打开。

然后，点击 `提取个人信息` 按钮，会将你的个人账号信息显示在右侧。同时，在你本地目录 `output` 文件夹下会多出一个文件`self_info.json`，保存的是你个人账号信息。

点击`更新数据库`，将你的微信数据库进行解码，控制台输出导出过程，稍等片刻，成功后，文本框中有提示~
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ee67df06d21f4a60a5fbf180632c5553.png)
## 3.2 聊天信息提取
首先需要将你账号中的所有联系人信息先提取出来，并保存到本地。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/8b4248acac68420ba7cc5e133112d86e.png)

如上图所示，点击 `联系人信息提取`，右侧会给出保存路径，此时在你本地目录 `output` 文件夹下会多出一个文件`contact.json`，是一个列表，保存了所有联系人和群聊的基本信息。（如果提取失败，软件重启一下）
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b2d3263a88b04cb9a942a6f089b80c91.png)
最后，选择输出类型（txt or json），输入你想要查找的 昵称 或者 备注名，然后点击 `聊天记录提取` ，就可以一键提取出和该联系人的所有聊天记录。

# 写在最后
目前界面还比较糙，想要用 PyQT 搭建一个功能复杂且界面美观的应用，需要学的东西还是挺多的。

为了方便有需要的同学下载，我把打包后的软件上传到了网盘，公众号【**猴哥的AI知识库**】后台回复 **微信信息提取工具**， 直接领取免安装软件包～

如果本文对你有帮助，欢迎**点赞收藏**备用！
