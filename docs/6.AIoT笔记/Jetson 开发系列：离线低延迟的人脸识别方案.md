最近，在 Jetson 上探索构建**离线、低延迟**的智能对话助手，欢迎感兴趣的朋友一起交流。


上篇调研了`语音识别和语音合成`解决方案。
- [Jetson 开发系列：离线低延迟的语音解决方案](https://blog.csdn.net/u010522887/article/details/142814654)

本篇继续探索`人脸识别`的离线部署方案。


## 1. CompreFace

关于 CompreFace 的优势和使用方法，之前出过一篇教程：[手把手搭建免费的人脸识别系统，支持REST API](https://zhuanlan.zhihu.com/p/710781082)。

CompreFace 是一套开源的人脸识别解决方案，功能包括：人脸识别、人脸验证、人脸检测、人脸关键点检测、面具检测、头部姿势检测、年龄和性别识别等。

遗憾的是，它依赖 AVX 指令集，因此 arm 架构的板子上无法部署，只好放弃。

你可以在终端使用如下命令试试看：
```
lscpu | grep avx
```

## 2. face_recognition
> 项目地址：[https://github.com/ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)

号称世界上最简单的人脸识别库，底层依赖[dlib](http://dlib.net/files/)。

如果需要使用 GPU 推理，由于 Jetson cuda的 bug，需要重新编译 dlib，详情可参考[作者的博客](https://medium.com/@ageitgey/build-a-hardware-based-face-recognition-system-for-150-with-the-nvidia-jetson-nano-and-python-a25cb8c891fd)。


一键安装：

```
pip install face_recognition
```


使用也非常简单，比如：

**人脸检测：**


```
import face_recognition
image = face_recognition.load_image_file("your_file.jpg")
face_locations = face_recognition.face_locations(image)
```

**人脸识别：**

```
known_image = face_recognition.load_image_file("biden.jpg")
unknown_image = face_recognition.load_image_file("unknown.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
```

唯一的缺陷是：没有检测框的得分，难以实现后处理。

## 3. Insightface

> 项目地址：[https://github.com/deepinsight/insightface](https://github.com/deepinsight/insightface)

Insightface 是一个强大的开源人脸识别项目，涵盖了各种人脸相关的应用。

一键安装：

```
pip install insightface
```
insightface 从 0.2 版本开始，推理后端从 MXNet 切换到了 onnxruntime。

不过在 Jetson 上，只支持 CPU 推理，无法使用 onnxruntime-gpu 推理。

如果需要使用使用 GPU，需要自行编译，但要确保 onnxruntime-gpu, cuda, cudnn 三者的版本对应，否则会报错。**PS：这个坑，有趟过的小伙伴欢迎交流啊。😊**

不过，倒是可以用 tensorrt 对 ONNX 模型进行推理加速，我们下篇再聊。

本篇，我们暂且先使用 CPU 来跑跑看：

```
import cv2
import numpy as np
from insightface.app import FaceAnalysis
app = FaceAnalysis(name='buffalo_sc')
app.prepare(ctx_id=0, det_size=(640, 640))
img = cv2.imread('data/images/1.png')[:, :, ::-1]
faces = app.get(img)
print(len(faces))
```
[官网](https://github.com/deepinsight/insightface/tree/master/python-package)提供了模型列表，示例代码中用的是小模型。

返回的结果中有哪些字段：

```
dict_keys(['bbox', 'kps', 'det_score', 'embedding'])
```

其中，返回的 embedding 是没有归一化的，记得在保存到向量库之前进行归一化处理：

```
feature = np.array(face['embedding'])[None, :]
feature = feature / np.linalg.norm(feature, axis=1, keepdims=True)
```

(640, 640)的图像推理耗时怎么样？

同一张图像，分别测三次：

**'buffalo_sc'模型**：没有人脸矫正和属性预测

```
0 Time taken: 0.40
1 Time taken: 0.39
2 Time taken: 0.39
```
**'buffalo_s'模型**：加上人脸矫正和属性预测

```
0 Time taken: 1.51
1 Time taken: 1.50
2 Time taken: 1.50
```

因此，为了兼顾推理速度，只好选择阉割版的**buffalo_sc**。

## 写在最后

本文为离线低延迟的人脸识别，提供了几种解决思路，更多方案，欢迎评论区交流。

如果对你有帮助，不妨**点赞收藏**备用。

--- 

为方便大家交流，新建了一个 `AI 交流群`，欢迎对`AIoT`、`AI工具`、`AI自媒体`等感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。






