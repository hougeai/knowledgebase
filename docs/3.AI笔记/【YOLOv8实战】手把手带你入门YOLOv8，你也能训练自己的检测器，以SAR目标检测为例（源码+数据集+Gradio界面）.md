

💡💡💡**本文摘要：基于YOLOv8的SAR图像目标检测系统，覆盖数据制作、数据可视化、模型训练/评估/推理/部署全流程，最后通过 Gradio 界面进行展示。**


# 0 写在前面
上篇分享[【飞浆AI实战】交通灯检测：手把手带你入门PaddleDetection，从训练到部署](https://blog.csdn.net/u010522887/article/details/136863553)，我们以交通灯检测为案例，带着大家从0到1完成了检测任务的模型训练评估和推理部署全流程。
本次分享将带领大家熟练掌握 YOLOv8 的使用，并根据自己的任务训练一个特定场景的检测器，本文将重点讲解 YOLOv8 训练框架中数据集的格式、配置文件等细节，让小白少走弯路，跟着走就能轻松训练好自己的检测器，并基于 Gradio 搭建一个简单的应用。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/b9f567cf7514afe0f9b4e58c09c61b76.png)

# 1 环境准备
首先我们先要准备好本地 Python 环境，有关 Windows 和 Linux 下如何配置虚拟环境，可参考笔者之前的分享：
- [【7天Python入门系列】Day1：环境准备-Conda和VS code安装](https://blog.csdn.net/u010522887/article/details/136969406)
- [【保姆级教程】Windows上安装Linux子系统，搞台虚拟机玩玩](https://zhuanlan.zhihu.com/p/689560472)
我们以建议一个 Python=3.8 的 conda 虚拟环境为例，终端指令如下：

```
conda create -n sar python=3.8
conda activate sar
```

在本地新建好虚拟环境之后,就可以把 YOLOv8 装上了。官方提供了两种下载安装方式：
- 方式1：pip 源安装

```
# 方式1：pip源安装
pip install ultralytics
# 如果要使用最新版，可以采用如下方式
pip install git+https://github.com/ultralytics/ultralytics.git@main
```
- 方式2：源码安装（推荐）

```
git clone https://github.com/ultralytics/ultralytics
cd ultralytics
pip install -e .
```
推荐大家采用源码安装，这样可以用上项目的最新更新。安装后的位置位于你的虚拟环境位置中，比如我的就在：`/home/xxx/miniconda3/envs/sar/lib/python3.8/site-packages`.

# 2 YOLOv8 初体验
这里主要是参考了 YOLOv8 的[官方文档](https://docs.ultralytics.com/)，文档结构非常清晰，不过是英文的，对小白来说不太友好，这里笔者将其中开发中最常用的功能摘出来给大家做一个梳理，按照这个流程走，你就能快速训好你的检测器。
## 2.1 模型训练
YOLOv8 做了非常好的封装，基本在 10 行代码以内就能完成模型训练、评估、推理和导出等常用功能。
我们以加载 YOLOv8 的最小版本 yolov8n 为例：
```
from ultralytics import YOLO
model = YOLO('yolov8n.yaml') # 会调用ultralytics/cfg/models/v8/yolov8.yaml 并加载 scale='n'
model = YOLO('yolov8n.pt') # 会加载预训练模型，如果没有 默认下载到当前目录
```
接下来调用 `model.train()` 函数开始进行模型训练：

```
results = model.train(data='coco128.yaml', batch=4, epochs=1)
```
`model.train()` 函数中的参数说明如下：
- data='coco128.yaml'，数据集配置文件，默认在`ultralytics/cfg/datasets/coco128.yaml`，其中的数据集会默认下载到 `../datasets/coco128/`
- batch=4， 指定 batchsize 大小
- device=[0, 1]， 指定 gpu 设备
- resume=True，恢复训练，会自动从 .pt 文件中加载
- 更多训练参数的默认设置，可参考[官方文档 Train](https://docs.ultralytics.com/modes/train/#resuming-interrupted-trainings)
训练结束后的模型权重结果保存在当前目录下 `runs/detect/train`：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/fc03ccb4f2d4692f6169ab18f4fcbf18.png)

## 2.2 模型评估
模型评估同样只需要一行代码，调用 `model.val()` 函数:

```
# 加载模型参数文件
model = YOLO('runs/detect/train/weights/best.pt')
# 指定评估数据集 data='coco8.yaml'
results = model.val()
```
`model.val()` 函数中的更多参数说明可参考[官方文档 Val](https://docs.ultralytics.com/modes/val/#example-validation-with-arguments)。

评估结果保存在当前目录下 `runs/detect/val`：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/158b5558e6dd0926c502cd83d16255e5.png)


## 2.3 模型推理
模型推理同样只需要一行代码，不过输出结果中内容较为丰富，这是因为 YOLOv8 不仅只能完成检测这一任务，这里我们将 results 中的结果打印出来看看，加深对输出结果的认识。

```
from ultralytics import YOLO
model = YOLO('runs/detect/train/weights/best.pt')
# results = model('https://ultralytics.com/images/bus.jpg')
results = model('bus.jpg')
for result in results:
    boxes = result.boxes  # 目标检测框
    masks = result.masks  # 实例分割结果，这里没有
    keypoints = result.keypoints  # 关键点检测结果，这里没有
    probs = result.probs  # 目标框对应的置信度得分
    result.show()  # display to screen
    result.save(filename='result.jpg')  # save to disk
```
模型推理函数中的更多参数说明可参考[官方文档 Predict](https://docs.ultralytics.com/modes/predict/#key-features-of-predict-mode)。

## 2.4 模型导出
模型导出同样只需要一行代码，调用 `model.export()` 函数，模型导出类型有`'onnx', 'torchscript', 'tensorflow'，paddle`等常见类型。

导出前需要先按照 ONNX 包：`pip install onnx`，然后执行如下脚本：
```
from ultralytics import YOLO
model = YOLO('runs/detect/train/weights/best.pt')
# Export the model to ONNX format
success = model.export(format='onnx')
```
导出后 .onnx 文件会保存在同级目录下，比如 `runs/detect/train/weights/best.onnx`

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/ccda75c0245bc6f4104f94183cbdb961.png)

模型导出函数中的更多参数说明可参考[官方文档 Export](https://docs.ultralytics.com/modes/export/#key-features-of-export-mode)。

如果要评估不同导出方式的性能和耗时对比，同样可以在一行指令内完成：
- 首先是在 GPU 上的推理：

```
from ultralytics.utils.benchmarks import benchmark
benchmark(model='runs/detect/train/weights/best.pt', data='coco8.yaml', imgsz=640, half=False, device=0)
```
过程中如果缺少依赖的包，会自动下载安装，比如 `'onnxruntime-gpu' 'nvidia-tensorrt' ‘tensorflow’`，比如在我的 `NVIDIA GeForce RTX 2050` 4G 显卡上的测试结果如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/3b9ce67a206a0f376767d6d6626c2d1b.png)

可以看到转成 ONNX 推理速度还是快很多的。
- 再测试下 CPU 下的推理：

```
from ultralytics.utils.benchmarks import benchmark
benchmark(model='runs/detect/train/weights/best.pt', data='coco8.yaml', imgsz=640, half=False)
```

过程中如果缺少依赖的包，会自动下载安装，比如 `'onnxruntime'`，测试结果如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/a1a75fa2dbfd31b3797a53c5418e67f2.png)

## 2.5 更多...
YOLOv8 更多支持的检测模型可在[官方文档 Model](https://docs.ultralytics.com/models/)找到。在本地项目中：
- 对应的配置文件在：`ultralytics/cfg/models/`
- 对应的代码在：`ultralytics/models/`

同样，更多支持的数据集可在[官方文档 Datasets](https://docs.ultralytics.com/datasets/)找到。在本地项目中：
- 对应的配置文件在：`ultralytics/cfg/datasets/`
- 对应的代码在：`ultralytics/data/`

# 3 训练自己的检测器
这一部分开始，让我们动手在自己的数据集上训练一个 YOLOv8 检测器吧。项目源码我放在了[这里](https://download.csdn.net/download/u010522887/89117086)，供有需要的同学参考。
## 3.1 数据集准备
YOLOv8 对数据集的格式要求以及目录结构和我们之前所了解的 COCO 和 VOC 都不同，比如官方提供的 coco8 数据集的目录示例如下：

```
├── images
│   ├── train
│   │   ├── 000000000009.jpg
│   └── val
│       ├── 000000000036.jpg
└── labels
    ├── train
    │   ├── 000000000009.txt
    ├── val
    │   ├── 000000000036.txt

```

总结而言，为 YOLOv8 创建数据集共可以分为以下三步：
- 创建 .yaml 配置文件，可以参考 coco128.yaml
- 创建标签文件：每张图片对应一个 .txt，如果没有目标，则不需要 .txt; 要求：
  - 每行一个目标
  - 格式 class x_center y_center width height
  - 其中 class 从0开始，坐标是归一化的 (from 0 to 1)
- 组织数据集文件夹，格式如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/57452fb194162e456e1bf3ca39151c48.png)
下面我将以一个 SAR图像舰船目标检测数据集 为例，带领大家走一遍数据集制作的过程。

如果你在本地没有数据，我已经将数据集上传到 [AI Studio 平台](https://aistudio.baidu.com/datasetdetail/264241)了，直接下载到本地即可。
## 3.2 创建标签文件&组织数据集文件夹
接下来我们需要进行数据转换，转换成 YOLOv8 指定的格式，代码我放在了项目源码根目录下`convert_labels.py`，具体实现逻辑如下：

```
import os
import json
import shutil
import cv2
import numpy as np
from collections import defaultdict
from ultralytics.utils import LOGGER, TQDM

# Create dataset directory
orig_dir = '../../datasets/ssdd'
save_dir = '../../datasets/ssdd_yolo'
for p in f'{save_dir}/labels', f'{save_dir}/images':
    os.makedirs(p, exist_ok=True)

for json_file in ['train.json', 'val.json']:
    lname = json_file.split('.')[0]
    img_dir = f'{save_dir}/images/{lname}'
    os.makedirs(img_dir, exist_ok=True)
    fn = f'{save_dir}/labels/{lname}'
    os.makedirs(fn, exist_ok=True)
    with open(f'{orig_dir}/{json_file}') as f:
        data = json.load(f)
    images = {f'{x["id"]:d}': x for x in data["images"]}
    imgToAnns = defaultdict(list)
    for ann in data["annotations"]:
        imgToAnns[ann["image_id"]].append(ann)
    image_txt = []
    # Write labels file
    for img_id, anns in TQDM(imgToAnns.items(), desc=f"Annotations {json_file}"):
        img = images[f"{img_id:d}"]
        h, w = img["height"], img["width"]
        f = img["file_name"]
        shutil.copy(f'{orig_dir}/JPEGImages/{f}', f'{img_dir}/{f}')
        bboxes = []
        for ann in anns:
            box = np.array(ann["bbox"], dtype=np.float64)
            box[:2] += box[2:] / 2  # xy top-left corner to center
            box[[0, 2]] /= w  # normalize x
            box[[1, 3]] /= h  # normalize y
            if box[2] <= 0 or box[3] <= 0:  # if w <= 0 and h <= 0
                continue
            cls = ann["category_id"] - 1
            box = [cls] + box.tolist()
            if box not in bboxes:
                bboxes.append(box)
        with open(f'{fn}/{f[:-3]}txt', 'a') as file:
            for i in range(len(bboxes)):
                line = ' '.join([str(n) for n in bboxes[i]])
                file.write(line + "\n")

LOGGER.info(f"COCO data converted successfully.\nResults saved to {save_dir}")
```
转换完成后，我们还可以打印一张结果出来看看，确保自己转换的标签是没问题的，测试脚本如下：

```
# check converted annos
img_path = f'{save_dir}/images/train/000031.jpg'
txt_path = f'{save_dir}/labels/train/000031.txt'
lines = open(txt_path, 'r').read().splitlines()
img = cv2.imread(img_path)
ih, iw = img.shape[:2]
for line in lines:
    c, x, y, w, h = [float(i) for i in line.split(' ')]
    x1, y1 = int((x-w/2)*iw), int((y-h/2)*ih)
    x2, y2 = int((x+w/2)*iw), int((y+h/2)*ih)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0))
cv2.imwrite('0.jpg', img)
```
测试结果如下，说明我们转换的没问题，接下来就可以放心开始模型训练了。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/1c30b8fab08f1d7c1c5f1550006b57da.png)
## 3.3 创建 ssdd.yaml 数据集配置文件
配置文件中主要是指定自己数据集所在的位置，例如我们刚刚生成的数据保存在`../../datasets/ssdd_yolo`目录下。
```
# ssdd.yaml
path: ../../datasets/ssdd_yolo # dataset root dir
train: images/train # train images (relative to 'path') 
val:  images/val # val images (relative to 'path')
test: images/val 

# Classes
names:
  0: ship
download: |
```
## 3.4 数据集上传 ultralytics.hub (可选)
此外，我们还可以将自己的数据集上传到 ultralytics.hub ，分享给更多的社区小伙伴。
在正式上传之前，需要先在本地检查一下数据集是否符合标准。

压缩指令如下：
```
cd ~/datasets/
zip -r -o ssdd_yolo.zip ssdd_yolo/
```
得到压缩包后，执行如下脚本，进行数据集检查：

```
from ultralytics.hub import check_dataset
check_dataset('../../datasets/ssdd_yolo.zip')
```
出现如下结果，说明数据集符合标准，可以进行上传了。
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/c4a289e76b0260823bd158a0d0b60053.png)

进入 [ultralytics.hub](https://hub.ultralytics.com/signin) 后需要先注册一个账号，然后点击右上角的 Upload 开始上传。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/6488a6d053ef0e776ff35c97ae24e88f.png)

数据集右上侧 三个点 -> Share，将数据集公开，就可以生成数据集的[分享链接](https://hub.ultralytics.com/datasets/mMUhIhAB4MXoZE265X9U)。点击数据集，可以看到有关数据集的统计数据，例如在 Train 中共有2009个舰船目标。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/18a90aba65fe2049a74e290cb03a756c.png)
## 3.5 模型训练
上述准备工作做好后，就可以一键开启模型训练了，代码放在项目源码根目录下`train.py`:

```
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model.train(data='ultralytics/cfg/datasets/ssdd.yaml', batch=4, epochs=10)
```
这里我根据自己的 GPU 显存选择了batchsize=4，大家可以根据自己的显存大小进行调整，以免显存溢出：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/f62c632ed5bc96a6e981ce88485d26f9.png)

训练结果展示：训练了 10 个 epoch，mAP50 = 0.956，结果 OK，接下来就是部署成应用了。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/25c7c4de61b49cd24e3c23957c4d2ef8.png)

# 4 模型部署和应用搭建
## 4.1 ONNX 模型转换
考虑到 ONNX 模型的通用性，这里选择 ONNX 模型进行部署。首先将训好的模型转换成 ONNX 格式：
```
from ultralytics import YOLO
model = YOLO('runs/detect/train2/weights/best.pt')
success = model.export(format='onnx')
```
## 4.2 编写推理函数
需要先安装 `onnxruntime` 包。如果上面已经跑过 benchmark 测试了，那么 `onnxruntime` 已经安装好了。推理函数放在项目源码根目录下`demo.py`，供大家参考。
```
import cv2
import time
import numpy as np
import onnxruntime
import gradio as gr
from ultralytics.utils.ops import xywh2xyxy

class_names = ['ship']
colors = np.random.uniform(0, 255, size=(len(class_names), 3))

def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou

def nms(boxes, scores, iou_threshold):
    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]

        # print(keep_indices.shape, sorted_indices.shape)
        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes

def multiclass_nms(boxes, scores, class_ids, iou_threshold):

    unique_class_ids = np.unique(class_ids)

    keep_boxes = []
    for class_id in unique_class_ids:
        class_indices = np.where(class_ids == class_id)[0]
        class_boxes = boxes[class_indices,:]
        class_scores = scores[class_indices]

        class_keep_boxes = nms(class_boxes, class_scores, iou_threshold)
        keep_boxes.extend(class_indices[class_keep_boxes])

    return keep_boxes

def draw_detections(image, boxes, scores, class_ids, mask_alpha=0.3):
    det_img = image.copy()

    img_height, img_width = image.shape[:2]
    font_size = min([img_height, img_width]) * 0.0006
    text_thickness = int(min([img_height, img_width]) * 0.001)

    det_img = draw_masks(det_img, boxes, class_ids, mask_alpha)

    # Draw bounding boxes and labels of detections
    for class_id, box, score in zip(class_ids, boxes, scores):
        color = colors[class_id]

        draw_box(det_img, box, color)

        label = class_names[class_id]
        caption = f'{label} {int(score * 100)}%'
        draw_text(det_img, caption, box, color, font_size, text_thickness)

    return det_img

def detections_dog(image, boxes, scores, class_ids, mask_alpha=0.3):
    det_img = image.copy()

    img_height, img_width = image.shape[:2]
    font_size = min([img_height, img_width]) * 0.0006
    text_thickness = int(min([img_height, img_width]) * 0.001)

    # det_img = draw_masks(det_img, boxes, class_ids, mask_alpha)

    # Draw bounding boxes and labels of detections

    for class_id, box, score in zip(class_ids, boxes, scores):

        color = colors[class_id]

        draw_box(det_img, box, color)
        label = class_names[class_id]
        caption = f'{label} {int(score * 100)}%'
        draw_text(det_img, caption, box, color, font_size, text_thickness)

    return det_img

def draw_box( image, box, color=(0, 0, 255), thickness=2):
    x1, y1, x2, y2 = box.astype(int)
    return cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

def draw_text(image, text, box, color=(0, 0, 255), font_size=0.001, text_thickness=2):
    x1, y1, x2, y2 = box.astype(int)
    (tw, th), _ = cv2.getTextSize(text=text, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=font_size, thickness=text_thickness)
    th = int(th * 1.2)

    cv2.rectangle(image, (x1, y1),
                  (x1 + tw, y1 - th), color, -1)

    return cv2.putText(image, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), text_thickness, cv2.LINE_AA)

def draw_masks(image: np.ndarray, boxes: np.ndarray, classes: np.ndarray, mask_alpha: float = 0.3) -> np.ndarray:
    mask_img = image.copy()

    # Draw bounding boxes and labels of detections
    for box, class_id in zip(boxes, classes):
        color = colors[class_id]

        x1, y1, x2, y2 = box.astype(int)

        # Draw fill rectangle in mask image
        cv2.rectangle(mask_img, (x1, y1), (x2, y2), color, -1)

    return cv2.addWeighted(mask_img, mask_alpha, image, 1 - mask_alpha, 0)

class YOLOV8Det:
    def __init__(self, path, conf_thre=0.5, iou_thre=0.5):
        self.conf_threshold = conf_thre
        self.iou_threshold = iou_thre

        # Initialize model
        self.initialize_model(path)

    def __call__(self, image):
        return self.detect_objects(image)

    def initialize_model(self, path):
        self.session = onnxruntime.InferenceSession(path,providers=onnxruntime.get_available_providers())
        # Get model info
        self.get_input_details()
        self.get_output_details()


    def detect_objects(self, image):
        input_tensor = self.prepare_input(image)

        # Perform inference on the image
        outputs = self.inference(input_tensor)

        self.boxes, self.scores, self.class_ids = self.process_output(outputs)

        return self.boxes, self.scores, self.class_ids

    def prepare_input(self, image):
        self.img_height, self.img_width = image.shape[:2]

        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize input image
        input_img = cv2.resize(input_img, (self.input_width, self.input_height))

        # Scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)

        return input_tensor


    def inference(self, input_tensor):
        start = time.perf_counter()
        outputs = self.session.run(self.output_names, {self.input_names[0]: input_tensor})

        # print(f"Inference time: {(time.perf_counter() - start)*1000:.2f} ms")
        return outputs

    def process_output(self, output):
        predictions = np.squeeze(output[0]).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_threshold, :]
        scores = scores[scores > self.conf_threshold]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        indices = multiclass_nms(boxes, scores, class_ids, self.iou_threshold)

        return boxes[indices], scores[indices], class_ids[indices]

    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        return boxes

    def rescale_boxes(self, boxes):

        # Rescale boxes to original image dimensions
        input_shape = np.array([self.input_width, self.input_height, self.input_width, self.input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])
        return boxes

    def draw_detections(self, image, draw_scores=True, mask_alpha=0.4):

        return detections_dog(image, self.boxes, self.scores,
                               self.class_ids, mask_alpha)

    def get_input_details(self):
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]

    def get_output_details(self):
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]
```
接下来，让我们用 Gradio 写一个前端界面，简单搭建一个应用吧：
> 注意要先安装 gradio：`pip install gradio`
```
def predict_image(img, conf_thre, iou_thre):
    predictor = YOLOV8Det('runs/detect/train2/weights/best.onnx', conf_thre, iou_thre)
    predictor(img)
    out = predictor.draw_detections(img)
    return out

demo = gr.Interface(
    fn=predict_image,
    inputs=[
        gr.Image(label="Upload Image"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU threshold")
    ],
    outputs=gr.Image(label="Result"),
    title="Ultralytics Gradio",
    description="Upload images for inference. The Ultralytics YOLOv8n model is used by default.",
    examples=[
        ["../../datasets/ssdd_yolo/images/train/000031.jpg", 0.25, 0.45],
    ]
)

demo.launch()
```
可视化结果如下：

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/8d2bcfc639a940eabd1412e24ba42fcb.png)

# 5 总结
至此，我们完成了 YOLOv8 的一个实战任务，了解了它的数据集组成形式和标签格式，并根据自己的任务训练一个特定场景的检测模型，搭建了一款基于 Gradio 的前端应用。感兴趣的小伙伴赶紧用自己的数据集炼丹吧。

