# 一、项目出发点

AI Studio为我们提供了免费的GPU资源，当我们在NoteBook环境中把代码调试成功后，通常一个训练任务耗时较长，而Notebook离线运行有时长限制，一不小心就容易被kill掉。

如何解决这一问题？

后台任务帮到你！有关什么是后台任务，以及如何起一个后台任务，官方已经出了[相关教程](https://aistudio.baidu.com/projectdetail/1173726)。

本次分享将基于笔者的一个任务需求-SAR图像目标检测，带领大家从0到1跑通一个检测任务的后台训练，希望能为有类似需求的同学提供一点帮助。

# 二、Notebook离线调试
## 数据集准备
> 这一步是为模型训练做好准备

数据集获取有两种方式：
- 在[AI Studio平台-数据集](https://aistudio.baidu.com/my/dataset)中搜索是否有自己需要的数据集；
- 如果是自己收集的数据，首先需要制作成为VOC 或者 COCO 格式的数据，这里笔者已经把一个SAR图像目标检测数据集SSDD制作好了，然后上传到了AI Studio平台[SSDD遥感SAR目标检测数据集-COCO格式](https://aistudio.baidu.com/datasetdetail/264241)

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/1cabe8557ccdd0e2d5e8c4c8b91455e5.png)


## 新建Notebook任务
新建一个Notebook任务，
AI Studio平台注册账号后，点击创建项目-选择NoteBook任务，然后添加上一步的数据集，参考下图操作（注意数据集选用[SSDD遥感SAR目标检测数据集-COCO格式](https://aistudio.baidu.com/datasetdetail/264241)），完成项目创建。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ed2c9edf9addcecf8de4a9e1acc0f880.png)

## 环境准备
本次任务我们将采用PaddleDetection框架完成训练任务，为此需要先将PaddleDetection下载到本地:
```
git clone https://github.com/PaddlePaddle/PaddleDetection.git
# 如果下载失败，换成gitee源
git clone https://gitee.com/PaddlePaddle/PaddleDetection.git
```
安装环境依赖：
```
cd PaddleDetection
pip install -r requirements.txt
# 编译安装paddledet
python setup.py install
```
测试是否安装成功：
```
python ppdet/modeling/tests/test_architectures.py
```
如果出现下图，说明安装成功：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/0b5d1ac535dd8e21ebbcad39115ccf40.png)

## 准备任务调试
为了完成训练任务，我们需要准备两个配置文件：
- 数据集配置文件
```
在`PaddleDetection/configs/datasets`中新建coco_detection_ssdd.yml
其中写入：
metric: COCO
num_classes: 1

TrainDataset:
  name: COCODataSet
  image_dir: JPEGImages
  anno_path: train.json
  dataset_dir: /home/aistudio/datasets/ssdd/
  data_fields: ['image', 'gt_bbox', 'gt_class', 'is_crowd']

EvalDataset:
  name: COCODataSet
  image_dir: JPEGImages
  anno_path: val.json
  dataset_dir: /home/aistudio/datasets/ssdd/
  allow_empty: true

TestDataset:
  name: ImageFolder
  anno_path: val.json # also support txt (like VOC's label_list.txt)
  dataset_dir: /home/aistudio/datasets/ssdd/ # if set, anno_path will be 'dataset_dir/anno_path'
```
- 模型配置文件
> 选择一个检测模型，这里我们以选用picodet为例，在`PaddleDetection/configs/picodet/`中找到`picodet_l_640_coco_lcnet.yml`并复制一份，命名为`picodet_l_640_ssdd_lcnet.yml`，修改其中对应的数据集配置文件即可：

```
_BASE_: [
  '../datasets/coco_detection_ssdd.yml',
  ...
]
```

这时就可以开启训练任务了：

```
# 注意：这里需要使用GPU环境，cpu环境训练跑不起来
# --eval 代表训练时在验证集上测试训练效果
python tools/train.py -c configs/picodet/picodet_l_640_ssdd_lcnet.yml --eval
```
如果没问题的话，可以看到训练日志，接下来就可以创建后台任务，将这一训练放到后台去跑了。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3041ca4cf84b54cb18468ddf9e55a694.png)


# 三、后台任务创建
## 主文件准备
后台任务对上传文件数量和大小都有限制，为此我们不能将dataset和PaddleDetection都上传，这时就需要我们在NoteBook中手动下载需要的数据，并进行必要的操作完成环境准备。这里我们以新建`main.ipynb`为例，在cell中写入如下代码，主要分为以下几个步骤：
- 解压数据
```
!mkdir -p /home/aistudio/datasets/
!unzip -qo /home/aistudio/data/data264241/ssdd.zip -d /home/aistudio/datasets/
```
- 环境配置
```
!git clone https://gitee.com/PaddlePaddle/PaddleDetection.git
%cd PaddleDetection/
!pip install -r requirements.txt
!python setup.py install
!python ppdet/modeling/tests/test_architectures.py
```
- 开启训练
> 注意：这里需要将上一步中新建的配置文件`coco_detection_ssdd.yml`和`picodet_l_640_ssdd_lcnet.yml`放到下载的PaddleDetection文件夹中
```
!cp /home/aistudio/coco_detection_ssdd.yml /home/aistudio//configs/datasets/
!cp /home/aistudio/picodet_l_640_ssdd_lcnet.yml /home/aistudio/PaddleDetection/configs/picodet/
!python tools/train.py -c configs/picodet/picodet_l_640_ssdd_lcnet.yml --eval
```
## 版本构建
创建后台任务之前，需要我们将用到的代码新建一个版本，比如这里我们只需要上传三份代码：
- `main.ipynb`
- `coco_detection_ssdd.yml`
- `picodet_l_640_ssdd_lcnet.yml`

点击项目栏左侧 **版本**->版本管理+ ，参考下图勾选需要的文件，点击生成版本即可：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3e22114df8a13c0c4e97a9b63ee3a38a.png)

## 任务构建
完成项目版本创建后，就可以创建后台任务了，点击项目栏左侧 **任务**->后台任务+，如下图所示，选择刚刚构建的项目版本，并指定执行文件`main.ipynb`：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d64a379ca5045923a7b04ffdbc856f5f.png)

点击下一步，就可以看到任务状态已经改变了：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/865826b51412e368bc77fb000504d5e7.png)

当状态变更为`运行中`，可以在右侧`查看日志`，如果有报错，需要对应排除掉bug后再重新按照上述流程提交任务。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3323bb73350ebe9c9b32262432735687.png)

如果运行成功，可以看到如下日志，这里显示大约40min后任务会完成：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b34a22bd1d6eb874a7260120fd34300a.png)

## 下载输出
训练完成后，可以到任务后台`下载输出`，里面保留有训练好的模型权重，便于后续进行模型测试和部署推理。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/0065738d47fc35d2919ab45f8c1b5b79.png)

# 四、模型预测推理
下载下来的模型权重文件位于`PaddleDetection\output\picodet_l_640_ssdd_lcnet`，将得到的模型参数文件，上传到我们的项目文件夹中，通过如下代码我们在验证集上评估一下：

```
python tools/eval.py -c configs/picodet/picodet_l_640_ssdd_lcnet.yml -o weights=output/model_final.pdparams
```
`PicoDet`通过100个epoch的训练，在验证集上的mAP@0.5达到了0.965，这个结果已经比很多Paper中报告的结果要好了，***感兴趣的同学可以把它当成你的baseline，继续开始你的炼丹之旅吧！***
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/1669590c761e18121572f6152f959b8a.png)
此外，我们还可以打印一张预测结果出来看看：

```
python tools/infer.py -c configs/picodet/picodet_l_640_ssdd_lcnet.yml -o weights=output/model_final.pdparams --infer_img=../datasets/ssdd/JPEGImages/000031.jpg
# 输出结果保存在：Detection bbox results save in output/000031.jpg
```
让我们打开预测结果看看：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ad21c0c4fc78610f647b7750d4ddd8c4.png)
# 五、模型压缩和推理部署
此外，我们还可以将训练得到的模型进一步压缩，以及转换成部署需要的模型，分别在服务端和手机端进行部署，这部分的具体流程可以参考笔者之前撰写的文档：

[【飞桨AI实战】Yolo交通灯检测：手把手带你入门PaddleDetection，从训练到部署](https://zhuanlan.zhihu.com/p/687805616)

[【飞桨AI实战】桃子分类系统部署：手把手带你入门PaddleClas全家桶](https://zhuanlan.zhihu.com/p/685561416)

# 六、总结
- 本项目通过计算机视觉领域中最基础的任务之目标检测，带领大家熟悉如何启动一个AI Studio后台任务，来完成自己的训练任务。
- 案例选自地球科学领域，有现实场景应用需求，本系列的后续文章将沿袭这一思路，继续分享更多采用Paddle深度学习框架服务更多产业应用的案例。
