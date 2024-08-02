> 摘要：新手小白入门AIGC开发，必须理论结合实践。本系列文章将结合Datawhale 11月份组织的《如何用免费GPU部署大模型》打卡活动，通过全身心体验，记录项目开发过程中遇到的一些问题和总结开发过程中的一些心得体会。
本文是基于[项目文档](https://nuly9zxzf1.feishu.cn/docx/HOmzdmST9oc43gxjTF0c7PAAnnb)来完成第3个任务：通过项目文档了解如何在趋动云上用免费GPU部署stable-diffusion。

## Stable-Diffusion是什么？
Stable-Diffusion 是一个人工智能图像生成模型，由 Stability AI 开发。它是一种基于 Transformer 架构的深度学习模型，可以生成高质量、高分辨率的逼真图像。
Stable-Diffusion 通过学习大量的图像数据来学习图像的特征和模式，并使用这些知识来生成新的图像。它可以生成各种类型的图像，包括风景、人物、动物等，并可以通过调整参数来控制生成图像的风格和质量。
## 项目创建
这部分在项目文档中已经有了非常详细的记录，这里简单记录下具体步骤，方便以后查看。

- 在我的空间创建项目
- 参考文档配置好环境：这里使用6G显存就够
- 初始化环境：将data-1中的文件解压缩到code中
- 运行项目：
```python
python launch.py --deepdanbooru --share --theme dark --xformers --listen --gradio-auth qdy:123456
```
**注意**：上述代码会调用pip安装一部分python包，这时需要修改pip源，参考[第一次任务的文档](https://blog.csdn.net/u010522887/article/details/134220556?spm=1001.2014.3001.5502)， 需要将优先使用的源放到环境变量中，否则会出现安装失败。

```python
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
```
- 打开web界面：如果出现两个url：public URL 和 local URL，说明项目已经成功运行。前者直接打开就能用，后者需要通过左侧的端口信息复制到edge浏览器中打开。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/52399d4d151bc769da99991aae1e27e9.png)
- 愉快玩耍：输入刚才命令行中的用户名和密码就可以登陆进去了。运行大概占用3G显存左右。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/e352a605b1cd2f8f5488b7759fa8d20c.png)


