> 摘要：新手小白入门AIGC开发，必须理论结合实践。本系列文章将结合Datawhale 11月份组织的《如何用免费GPU部署大模型》打卡活动，通过全身心体验，记录项目开发过程中遇到的一些问题和总结开发过程中的一些心得体会。
> 本文是基于[项目文档](https://nuly9zxzf1.feishu.cn/docx/HOmzdmST9oc43gxjTF0c7PAAnnb)来完成day1的任务，day1的任务是，通过项目文档了解如何在趋动云上创建项目并部署ChatGLM大语言模型。

## ChatGLM是什么？
用本次项目部署成功后，chatglm自己的回答来看：
我是一个人工智能助手，名为 ChatGLM3-6B。我是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型 GLM3-6B 开发的。我的任务是针对用户的问题和要求提供适当的答复和支持。由于我是一个计算机程序，所以我没有自我意识，也不能像人类一样感知世界。我只能通过分析我所学到的信息来回答问题。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/05229d9674271b68f9fc6505811454d3.png)

## 趋动云是什么？
> ```https://www.virtaicloud.com/```

用本次项目部署成功后，chatglm自己的回答来看：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/85605895282bad40024cfbea26709d9c.png)
## 项目创建和环境配置
这部分在项目文档中已经有了非常详细的记录，这里简单记录下具体步骤和遇到的问题以及相应的解决方法。
### 项目创建
按照项目文档中操作即可。
不过**资源配置**这里注意一定要使用B1.large，我一开始使用的B1.medium，对应的内存只有12G，加载chatglm3-6b还是会把内存打爆。
### 设置镜像源
注意设置pip所用的镜像源，否则后面安装包会出现找不到的问题。
```python
git config - -global url."https://gitclone.com/". insteadof https://
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
pip config set global.trusted-host mirrors.ustc.edu.cn
python -m pip install --upgrade pip
```
### 下载源代码

在国内访问github经常出问题，因此需要找到对应的解决方案，我的操作一般是：

 - 打开gitee
 - 新建仓库-import自github
 - 生成对应的gitee仓库

因为这次在gitee中已经存在chatglm3了，所以直接使用下面这个仓库即可：

```python
# git clone https://github.com/THUDM/ChatGLM3.git
git clone https://gitee.com/tomorrowsj/ChatGLM3.git
```

### 修改代码并运行
如果遇到pip安装的问题，需要回到**设置镜像源**部分检查，一定是这里出了问题。

#### **gradio方式：对应修改web_demo.py**

 1. 修改预训练模型的位置，如下所示，因为我们在配置镜像时已经下载到容器中了
 2. 修改launch部分代码。注意使用**share=True**会出现报错，跟这个版本的gradio有关，解决起来不复杂-根据提示操作即可，具体可参考[Gradio开放外部链接](https://blog.csdn.net/xxnnhcgdjy/article/details/132968705)，这里只展示项目文档中的使用方式。

```python
tokenizer = AutoTokenizer.from_pretrained("../../pretrain", trust_remote_code=True)
model = AutoModel.from_pretrained("../../pretrain", trust_remote_code=True).cuda()
demo.queue().launch(share=False, server_name='0.0.0.0', server_port=7000)
```
修改后，就可以通过如下代码起一个服务：

```python
python web_demo.py
```
注意此时要将7000端口在页面右侧**端口信息**处添加上去。添加后会得到外部访问的链接，比如我的是
```python
direct.virtaicloud.com:48801/
```
改成：

```python
http://direct.virtaicloud.com:48801/
```

此时如果在google chrome中输入会出现报错：
```WARNING:  Invalid HTTP request received.```
是因为端口默认配置是 http 协议，如果当前浏览器不支持 http，可更换浏览器尝试。
具体原因可参考[添加链接描述](https://blog.csdn.net/huangpb123/article/details/130535276)
更多描述在[平台的端口文档中](https://platform.virtaicloud.com/gemini/v1/gemini_doc/02-%E9%A1%B9%E7%9B%AE/04-%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83/11-%E7%AB%AF%E5%8F%A3%E4%BD%BF%E7%94%A8.html)可找到。
此时，我换成edge浏览器，成功搞定！
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ec7d57d4655183ac8cd46c9a01606965.png)



#### **streamlit方式：对应修改web_demo2.py**
相比gradio比较简单，只需要修改预训练权重的位置即可：

```python
model_path = "../../pretrain"
@st.cache_resource
def get_model():
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).cuda()
    # 多显卡支持,使用下面两行代替上面一行,将num_gpus改为你实际的显卡数量
    # from utils import load_model_on_gpus
    # model = load_model_on_gpus("THUDM/chatglm3-6b", num_gpus=2)
    model = model.eval()
    return tokenizer, model
```
运行如下代码：
```python
streamlit run web_demo2.py
```
终端得到：

```python
You can now view your Streamlit app in your browser.

  Network URL: http://10.244.3.204:8501
  External URL: http://106.13.99.55:8501
```

新增一个端口8501，和上面一样，打开外部链接，等待模型加载，后续就可以愉快和chatglm对话拉！
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/8ff1eb8b66542962ffa2e527d3709282.png)


