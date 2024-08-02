# 原因分析
这是因为linux系统中没有安装tensorrt。
## 什么是tensorrt
- 一句话：TensorRT是用于NVIDIA各种GPU的一个模型推理框架，支持C++和Python。Pytorch或者Paddle框架训好的模型，可以转为TensorRT的格式，再用TensorRT去运行，可以提升NVIDIA-GPU上的运行速度。
- CUDA，CUDNN 和 TensoRT 之间的关系
  - cuda 是 NVIDIA-GPU 进行并行计算的框架
  - cudnn 是 NVIDIA-GPU 进行神经网络训练和推理的加速库，cudnn 会将神经网络的计算进行优化，再通过 cuda 调用 gpu 进行运算
  - tensorrt 和 cudnn 类似，不过只支持模型推理

# 怎么解决
## 方式一
> 查看cuda cudnn版本并到官网下载对应tensorrt版本

```bash
# 查看cuda cudnn版本
nvcc -V
ls -l /usr/local/ | grep cuda
dpkg -l | grep libcudnn
find /usr/ -name "cudnn*" # 找到cudnn.h的位置
cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2 # 打印cudnn版本
#define CUDNN_MAJOR 8
#define CUDNN_MINOR 9
#define CUDNN_PATCHLEVEL 6

# 综上，我的cuda版本是11.8，cudnn版本是8.9.6
# 官网下载对应的tensorrt版本并安装
https://developer.nvidia.cn/tensorrt
```
## 方式二（推荐）
> 直接pip安装

```bash
pip install tensorrt # 默认会安装8.6.1，所以还是找不到libnvinfer.so.7。目前pip安装已找不到版本7

# 找到你的python环境安装包位置，并cd进去
# 为了让程序能找到libnvinfer.so.8，这里新建了软链接，并在环境变量中新增安装位置
cd /home/aistudio/envs/py38/lib/python3.8/site-packages/tensorrt_libs
ln -s libnvinfer.so.8 libnvinfer.so.7
ln -s libnvinfer_plugin.so.8 libnvinfer_plugin.so.7
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/aistudio/envs/py38/lib/python3.8/site-packages/tensorrt_libs
```

