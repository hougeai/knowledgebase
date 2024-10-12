
你以为刷到的短视频都是真人出镜？

其实，换脸、数字人技术早已走向了商业化。

之前大部分的换脸模型，都需要大量样本进行训练，技术门槛非常高！

今天看到一个开源项目-ReHiFace-S，支持一键实时换脸的开源项目，只需一张人脸照片，即可将视频中的人脸，替换为你想要的人物形象。

话不多说，上实操！

## 1. 项目简介
> 项目地址：[https://github.com/GuijiAI/ReHiFace-S](https://github.com/GuijiAI/ReHiFace-S)

ReHiFace-S（Real Time High-Fidelity Faceswap）是由硅基智能开发的，实时高保真的换脸算法。

实时换脸功能，是开源数字人生成的底层能力。

有哪些亮点？

1. **实时处理**：在 NVIDIA GTX 1080Ti 显卡上，即可实现实时换脸。（*当然 CPU 也能跑，只要速度你能忍。。。*）
2. **零样本推断**：无需训练数据即可进行有效推断。
3. **高保真度**：换脸效果逼真，能够生成高质量的面部图像。
4. **支持 ONNX 和实时摄像头模式**：便于与其他模型或应用集成。
5. **超分辨率与色彩转换**：提升图像质量，增强视觉效果。
6. **更好的 Xseg 模型**：用于面部分割，提升换脸精度。

## 2. 项目实战
### 2.1 环境准备
要运行此项目，建议使用以下环境配置：
- Python >= 3.9（推荐使用 Anaconda 或 Miniconda）
- PyTorch >= 1.13
- CUDA 11.7
- 操作系统：Linux Ubuntu 20.04

1. 克隆代码库并准备环境：
  ```bash
  conda create --name faceswap python=3.9
  conda activate faceswap
  pip install -r requirements.txt
  ```
2. 下载预训练模型权重，并将其放入 `./pretrain_models` 文件夹中。


### 2.2 本地测试
先使用默认示例图片和视频跑下看看：

```bash
CUDA_VISIBLE_DEVICES='0' python inference.py
```
也可以通过指定 `--src_img_path` 和 `--video_path` 参数来更改输入。

```
CUDA_VISIBLE_DEVICES='0' python inference.py --src_img_path --video_path
```

如果要在摄像头中进行实时换脸：
```bash
CUDA_VISIBLE_DEVICES='0' python inference_cam.py
```
注意：支持在直播中更换源面孔。

如果遇到 onnxruntime 报错：

```
onnxruntime::Provider& onnxruntime::ProviderLibrary::Get() [ONNXRuntimeError] : 1 : FAIL : Failed to load library libonnxruntime_providers_cuda.so with error: libonnxruntime_providers_cuda.so: cannot open shared object file: No such file or directory
```

比如上面这个，首先找到 "libonnxruntime_providers_cuda.so" 的安装位置：

```
find / -name "libonnxruntime_providers_cuda.so" 2>/dev/null
```
然后把它添加到环境变量中，

```
export LD_LIBRARY_PATH=/path/to/onnxruntime/lib:$LD_LIBRARY_PATH
```


### 2.3 Web 应用
项目还提供了 Gradio 搭建的应用，可以通过以下命令一键运行：
```bash
python app.py
```
界面非常简洁，输入你想要换的人脸图像，和原始视频，提交即可！

![](https://img-blog.csdnimg.cn/img_convert/41f781811ef5b804157784229542d668.png)

注意：确保你的 onnxruntime 跑在 GPU 上，否则 CPU 跑就。。。

最后，展示下实测效果（CSDN无法支持gif）：
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/315afe9cb66d4b368b13df8e9d9c3a8d.png)
## 结论
ReHiFace-S 是一个功能强大且灵活的换脸工具，其实时处理能力和高保真的换脸效果，为数字人应用提供了新的可能性。

基于 ReHiFace-S ，硅基智能的数字人：[https://github.com/GuijiAI/duix.ai](https://github.com/GuijiAI/duix.ai)，也已开源。

支持 Android 和 IOS 终端一键部署，开发者可自行接入大模型（LLM）、语音识别（ASR）、语音合成（TTS），实现数字人实时交互。

有机会实操后，再和大家分享！

如果本文对你有帮助，不妨点个**免费的赞**和**收藏**备用。

有任何问题欢迎通过公众号找到我，一起打怪升级。


