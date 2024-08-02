# 前言
上次分享[【飞桨AI实战】交通灯检测：手把手带你入门PaddleDetection，从训练到部署](https://blog.csdn.net/u010522887/article/details/136863553)，我们以交通灯检测为案例，带着大家从0到1完成了检测任务的模型训练评估和推理部署全流程，了解了 PaddleDetection 为核心的常用组件的具体使用方法。

在此基础上，本篇将继续带领大家完成一个前后端分离的应用开发，最终实现的效果如下图所示，希望能为有类似项目需求的同学提供一点帮助。


![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ea7f5c12feac9557712340e145ba0a49.png)

代码地址：https://gitee.com/liuwei16/flask-paddle-demo

# 项目目标
- 基于 PaddleDetection 组件完成一个人脸口罩检测任务的模型训练；
- 基于 ONNX 完成模型转换和推理部署；
- 基于 Flask 搭建一个前后端分离的项目。

# 项目实战
## 1 PaddleDetection完成模型训练
如何完成 PaddleDetection 的安装等环境配置，可跳转到[【飞桨AI实战】交通灯检测：手把手带你入门PaddleDetection，从训练到部署](https://blog.csdn.net/u010522887/article/details/136863553)查看。

这里主要介绍下我们采用的数据集，以及选用的模型。
### 1.1 数据集准备
这次我们选用的数据集包含两类图像：未带口罩的和带口罩的人脸图像。在 AI Studio 项目中添加数据集时，搜索 face_mask ，选择第一个即可。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b7567142f184c500d8d3a2c158dbf540.png)
打开项目后，首先需要将数据解压出来，然后划分训练集/验证集。

step1: 解压数据集
```
cd data
unzip data226320/face_mask.zip
```
step2: 划分训练集/验证集：我们按照 4:1 划分

```
python generate_voc_dataset.py
# 其中generate_voc_dataset.py中的代码如下：
import os
import xml.etree.ElementTree as ET

root_dir = '/home/aistudio/data/face_mask'
anno_dir = os.path.join(root_dir, 'Annotations')
image_dir = os.path.join(root_dir, 'JPEGImages')

# get train/valid data
image_files = os.listdir(image_dir)
val_files = image_files[::5]
train_files = [f for f in image_files if f not in val_files]
with open(os.path.join(root_dir, 'train.txt'), 'w') as f:
    for ifile in train_files:
        afile = ifile.replace('.jpg', '.xml')
        f.write(f'JPEGImages/{ifile} Annotations/{afile}\n')
print('train ready')

with open(os.path.join(root_dir, 'val.txt'), 'w') as f:
    for ifile in val_files:
        afile = ifile.replace('.jpg', '.xml')
        f.write(f'JPEGImages/{ifile} Annotations/{afile}\n')
print('valid ready')
```
step3: 新建数据集配置文件
> 这里假设您的 PaddleDetection 已经下载到本地
```
cd PaddleDetection/
# 复制一份数据集的config并进行修改
cp configs/datasets/roadsign_voc.yml configs/datasets/facemask_voc.yml
# 修改其中的文件位置，如下所示：
metric: VOC
map_type: integral
num_classes: 2

TrainDataset:
  name: VOCDataSet
  dataset_dir: /home/aistudio/data/face_mask
  anno_path: train.txt
  label_list: leable.txt
  data_fields: ['image', 'gt_bbox', 'gt_class', 'difficult']

EvalDataset:
  name: VOCDataSet
  dataset_dir: /home/aistudio/data/face_mask
  anno_path: val.txt
  label_list: label_list.txt
  data_fields: ['image', 'gt_bbox', 'gt_class', 'difficult']

TestDataset:
  name: VOCDataSet
  dataset_dir: /home/aistudio/data/face_mask
  anno_path: val.txt
  label_list: label_list.txt
```
### 1.2 模型训练
这次我们选用百度自研的 picodet 轻量级模型，同样我们先要复制一份有关模型的配置文件，并进行修改：

```
cp configs/picodet/picodet_xs_416_coco_lcnet.yml configs/picodet/picodet_xs_416_facemask.yml
# 修改其中的数据集配置为我们刚新建的数据集配置文件：
_BASE_: [
  '../datasets/facemask_voc.yml',
  ...
]
# 由于本次任务比较简单，还可以减少训练的轮数：
epoch: 30
snapshot_epoch: 5
```
接下来就可以开启训练了：

```
python tools/train.py -c configs/picodet/picodet_xs_416_facemask.yml --eval
```
训练成功后，可以在终端查看训练过程，loss下降说明没问题，我这里只训了 15 个 epoch 就可以了，测试发现效果还可以。接下来我们需要将训练得到的最好模型转成部署需要的 inference 格式。

```
python tools/export_model.py -c configs/picodet/picodet_xs_416_facemask.yml --output_dir=output/inference_model -o weights=output/14
```
成功后，会在 `output/inference_model/picodet_xs_416_facemask/` 下生成 inference 格式的模型文件，如下所示：

```
output/inference_model/picodet_xs_416_facemask/
|-- infer_cfg.yml
|-- model.pdiparams
|-- model.pdiparams.info
|-- model.pdmodel
```


## 2 基于 ONNX 完成模型转换和推理部署

上篇[【飞桨AI实战】交通灯检测：手把手带你入门PaddleDetection，从训练到部署](https://blog.csdn.net/u010522887/article/details/136863553)我们分享了多种部署方式，这里我们采用 ONNX 来完成模型转换和推理部署。

**step1: ONNX模型导出**

```
# 将部署模型转为ONNX格式
pip install paddle2onnx
# cd到inference模型路径
cd output/inference_model/picodet_xs_416_facemask
paddle2onnx --model_dir ./ --model_filename model.pdmodel --params_filename model.pdiparams --opset_version 11 --save_file picoxs.onnx
```
导出后在当前目录生成 picoxs.onnx 模型文件。

**step2: onnxruntime模型推理**

```
pip install onnxruntime
# 执行推理，找张图像测试了看看吧
python deploy/third_engine/onnx/infer.py --infer_cfg output/inference_mode
l/picodet_xs_416_facemask/infer_cfg.yml --onnx_file output/inference_model/picodet_xs_416_facemask/picoxs.onnx --image_file ~/data/face_mask/JPEGImages/test_00001329.jpg
```
推理结果中的数字分别表示：类别 置信度得分 左上角坐标xy 右下角坐标xy。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/4be8d139ff563a0c8778eb68d7e367dc.png)

## 3 基于 Flask 搭建一个前后端分离的项目
> 参考示例代码：https://gitee.com/liuwei16/flask-paddle-demo

Flask 是一个非常小的 Python Web 框架，被称为微型框架；为了简单搭建一个应用，你不需要了解 Flask 的所有技术细节，你只需要将任务拆解为：
- 如何调用 ONNX 模型得到推理结果；
- 如何搭建一个界面，显示推理结果。

可以先将上面的示例代码git clone到本地，然后安装好依赖项：

```
pip install requirements.txt
```
**step 1: 实现调用 ONNX 模型的接口**

首先将模型文件和配置文件存放在`models`文件下：
```
models/
├── infer_cfg.yml
└── picoxs.onnx
```
然后编写接口函数，这里主要参考了`PaddleDetection/deploy/third_engine/onnx/infer.py`的具体写法，接口函数的位置在：
```
backend/
├── __init__.py
├── paddle_inference.py
└── preprocess.py
```
其中`predict`函数实现了读取数据的两种方式：一是读取本地图片，而是读取二进制文件，其中前者用于本地测试，后者用于线上调用。编成成功后，可以先在本地测试一下：

```
if __name__ == "__main__":
    detector = PicoDetector()
    img_path = 'images/test_mask.jpg'
    result = detector.predict(img_path)
    print(result)
    with open(img_path, 'rb') as f:
        img_bin = f.read()
    result = detector.predict(img_bin=img_bin)
    print(result)
```
**step 2: 搭建界面 可视化结果**

界面的核心逻辑在根目录的`index.html`中，其中依赖的 css 和 js 文件分别在`css`和`js`文件夹下，通过`python -m http.server`就可以起一个 web 服务（默认在8000端口），渲染`index.html`。

为了使得`index.html`中能够调用预测函数，一种最简单的方式是：基于 flask 写一个接口函数，然后后端通过 ajax 来发送一个请求，取回推理结果，在前端展示就可以了。

基于 flask 实现的接口函数在 `app.py`中：

```
detector = PicoDetector()

@app.route('/api/', methods=["POST"])
def main_interface():
    response = request.get_json(force=True)
    data_str = response['image']
    base64_str = re.sub('^data:image/.+;base64,', '', data_str)
    image = base64.b64decode(base64_str)
    results = detector.predict(img_bin=image)
    print(results)
    return jsonify(results)
```
后端的 ajax 请求代码在`js/index.js`中：
```
function communicate(img_base64_url) {
  $.ajax({
    url: URL,
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({"image": img_base64_url}),
    dataType: "json"
  }).done(function(response_data) {
      drawResult(response_data.results);
  });
}
```
更多实现细节，可参考代码仓库。

**step 3: 服务启动**
运行如下脚本启动服务：
```bash
sh test.sh
```
其中`test.sh`的内容如下：
```
python3 app.py & # 启动 flask app 并放到后台运行，准备推理函数的接口
python3 -m http.server # 启动 web 服务，渲染 index.html
```
如果发现 5000 端口被占用了，可以通过如下命令查看是被哪个进程占用了，然后 kill 掉再重新启动服务：

```
netstat -ntlp
kill 29403
```

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6f9d34bceb1ebb0f6dbc9fb9cbcde65d.png)

服务启动成功后，可以发现 web 服务在本地的 8000 端口，而 flask app的服务在 5000 端口，所以我们在本地游览器中输入 localhost:8000 就可以看到文章开头的界面了。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/fce174aaca971cd168f2e764524ee4ff.png)

# 总结
在掌握PaddleDetection完成模型训练和推理部署的基础上，本文带领大家从零开始构建一个人脸口罩检测的前后端分离的Flask应用。首先，我们采用PaddleDetection训练得到了人脸口罩检测模型，然后基于 ONNX 完成了模型推理，最后基于Flask框架搭建了一个前后端分离的Web应用，包括如何实现模型推理的后端接口、如何搭建前端界面，以及启动和运行整个服务。

本系列的后续文章将沿袭这一思路，继续分享更多采用Paddle深度学习框架服务更多产业应用的案例。




