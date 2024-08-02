​
> 摘要：新手小白入门AIGC开发，必须理论结合实践。本系列文章将结合Datawhale 11月份组织的《如何用免费GPU部署大模型》打卡活动，通过全身心体验，记录项目开发过程中遇到的一些问题和总结开发过程中的一些心得体会。
本文是基于项目文档来完成第2个任务：通过项目文档了解如何在趋动云上用免费GPU优化猫狗识别实践。

​​
## 任务是什么？
本次任务是一个经典的图像识别任务：通过训练一个二分类模型，将输入图像分为两类：猫和狗。

## 项目创建和调试
这部分在项目文档中已经有了非常详细的记录，这里简单记录下具体步骤，方便以后查看。

 - 在我的空间创建项目
 - 下载代码，并上传到我的项目中
 - 填写开发环境的初始化配置，这里选择了2GPU，但实际上这个任务一个GPU就足够了
 - 修改代码：因为原始代码在训练过程中没有打乱数据集，导致每次训练模型只见过一类样本，所以在训练代码44行将注释去掉。
 - 提交离线训练：
```python
python DogsVsCats.py --num_epochs 5 --data_dir $GEMINI_DATA_IN1/DogsVsCats --train_dir $GEMINI_DATA_OUT
```
 - 结果返回：训练成功后，5个epoch模型识别成功率就能达到87%了：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6c2e2ca33d329a5f888a978f9f1ce6a0.png)

 - 模型文件：同时在指定文件夹下，训练好的模型权重也保存了下来：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f9f791bdaa9db10adcb882fe84fbb795.png)
## 提交离线训练
上述步骤是调试代码是否有问题，如果训练没问题的话，就可以起一个训练任务，让平台调动资源对模型进行充分训练。具体步骤如下:

 - 提交训练任务
 - 配置和刚才的调试任务一样
 - 执行命令和刚才的调试任务一样
 - 启动命令：**注意**这时一定要把刚才的调试任务关掉，否则会因为个人的配额不足导致任务一直处于等待中。
 - 查看任务详情：可以发现3分钟就训练完成了，因为我只训练了5个epoch。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/511e4796b477df1c278e9f3784d78259.png)
**优势**：提交任务训练的优势在于，训练完成任务自动结束，系统会自动结算。
## 结果保存和下载
经过上一步的训练，成功后就可以把模型权重下载下来。

 - 查看结果：左侧导航栏查看结果
 - 导出模型
 - 创建一个共享模型

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/15184fadd4e9fc52e16d71c9d5210eae.png)

​
