前两天，有位粉丝朋友，在本地部署大模型时，在安装`flash_attn`遇到了很多问题，比如：

```
"flash_attn" module. while I tried to install flash_attn, It mentioned " RuntimeError: FlashAttention is only supported on CUDA 11 and above".
```

Linux、显卡、nvidia、CUDA/CUDNN、Pytorch、TensorFlow、PaddlePaddle，还有各种依赖库。

各种版本兼容，让很多朋友在学习 AI 的过程中，倒在了`配置环境`的路上。

今日分享，将系统梳理上述概念之间的依赖关系，以及如何安装，希望给遇到类似问题的小伙伴，一点点帮助。

## 1. 显卡和驱动

跑大模型，自然免不了 Nvidia 家的显卡。

所以，第一步需要查看显卡类型。

通常来说，你的系统镜像出厂时可能已经装好 Nvidia 驱动，因此输入 `nvidia-smi`，即可看到显卡类型。

重点需要关注的有下方三个红色框选：

![](https://img-blog.csdnimg.cn/img_convert/3b7777efee73f909c5b0a34538a47861.png)

最下方就是你的显卡型号，左上角是当前的显卡驱动版本，右上角是当前显卡驱动**最高支持**的 CUDA 版本（向下兼容），**但并不代表环境中**的 CUDA 版本！！！

所以，当你发现 CUDA 版本出问题时，记得来这里看看：**右上角红框的数字是多少？**

如果太低，意味着要更新显卡驱动了！

因为每个 CUDA 版本都有特定的最低驱动程序版本要求，比如 CUDA 12.0 驱动版本至少为 510.xxx。

**怎么更新？**

当前显卡能够支持的最高驱动版本，**在哪查看**？

前往 NVIDIA 官网：[https://www.nvidia.com/en-us/drivers/](https://www.nvidia.com/en-us/drivers/)

拿 RTX 3090 举例，点击 Find:

![](https://img-blog.csdnimg.cn/img_convert/006081ab8047d2352599e8da2e89f942.jpeg)



![](https://img-blog.csdnimg.cn/img_convert/6ac743f103f7ea685c49c6cf074b3d9a.png)


进入驱动下载页：[https://www.nvidia.com/en-us/drivers/details/233004/](https://www.nvidia.com/en-us/drivers/details/233004/)

![](https://img-blog.csdnimg.cn/img_convert/08e01cd838f616eaeedf526f27945b45.png)

下载成功后，你会得到一个类似 `xxx.run` 的文件，然后打开一个终端，输入：

```
# 添加可执行权限
chmod +x NVIDIA-Linux-x86_64-510.xxx.run

# 在安装过程中跳过对 X 服务器的检查，跳过对 Nouveau 驱动程序的检查，不安装与 OpenGL 相关的文件
sudo ./NVIDIA-Linux-x86_64-xxx.run -no-x-check -no-nouveau-check -no-opengl-files
```

进入可视化安装界面，一路 Yes 就可以了。


最后，一定记得重启机器，才能生效！

```
sudo reboot
```

重启后，再来试试`nvidia-smi`，驱动版本是不是已经更新了？

这时，再来安装最新版的 cuda 就没问题了。

## 2. CUDA/CuDNN
CUDA 是啥？

CuDNN 是啥？

nvcc 又是啥？

傻傻分不清啊~

大白话来讲：

- **CUDA**（Compute Unified Device Architecture）是由 NVIDIA 开发的并行计算库，旨在充分发挥 GPU 的并行计算能力，实现计算加速。

- **CuDNN**（CUDA Deep Neural Network library）*建立在 CUDA 之上*，提供了一系列针对CNN/RNN等模型中算子的高效实现，比如卷积、池化、激活函数等。（通常，**CUDA**和**CuDNN**需要搭配使用）


- **nvcc** 则是 CUDA 的编译器。

有同学说我在本地执行`nvcc -V`，提示找不到这个指令啊。

对啊，说明你在本地没安装 cuda，哪来的编译器呢？

那我要一顿操作，先下载并安装 cuda 么？

**推荐你不用**，因为你安装 cuda，大概率是用 Pytorch 等深度学习库，需要依赖它。

而当你安装不同版本的 Pytorch，你会发现它要求的 CUDA/CuDNN 版本还不一样。

所以，我们这一部分，不需进行任何操作，等你用到不同版本深度学习库时，再来安装对应版本的 **CUDA**和**CuDNN** 即可！

接着往下看！

### 2.1 Pytorch 下安装

Pytorch 非常友好，因为它会自动根据你的当前环境，安装对应版本的**CUDA**和**CuDNN**。

所以，如果你的项目依赖 Pytorch，压根无需手动安装**CUDA**和**CuDNN**。

最优雅的方式是，新建一个虚拟环境，一键安装指定版本的 torch 即可，比如：

```
conda env create -n torchenv python==3.8
conda activate torchenv
pip install torch==2.0.1
```

装完后，如何在代码中查看，版本是否正确呢？

```
import torch
print(torch.__version__) # 查看torch版本
print(torch.cuda.is_available()) # 查看cuda是否安装
print(torch.backends.cudnn.is_available()) # 查看cudnn是否安装
print(torch.version.cuda) # 打印cuda的版本
print(torch.backends.cudnn.version()) # 打印cudnn的版本
# 输出
2.0.1+cu117
True
True
11.7
8500
```

**装在哪了呢？**

当在虚拟环境中使用 pip 安装带有CUDA支持的PyTorch时，CUDA和cudnn相关的库通常会被安装在虚拟环境的lib目录下。例如：

```
/home/xx/miniconda3/envs/torchenv/lib/python3.8/site-packages/nvidia/cuda_runtime/lib/
/home/xx/miniconda3/envs/torchenv/lib/python3.8/site-packages/nvidia/cudnn/lib/
```

**怎么找到的？**

```
find /home/xx/miniconda3/envs/torchenv/lib/ -name libcuda*
```

### 2.2 PaddlePaddle 下安装

如果项目依赖 PaddlePaddle，这里会有点小坑。

如果用 pip 安装，需要额外手动安装 cuda 和 cudnn：

```
# 需指定是否用 GPU 版本
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
```

**所以，推荐用 conda 安装：**

```
# 会自动安装cuda11.7和cudnn8.4
conda install paddlepaddle-gpu==2.6.0 cudatoolkit=11.7 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/ -c conda-forge
```

如果运行后，提示找不到 cudnn，需要在环境变量中加上 lib：

```
export LD_LIBRARY_PATH=/home/xx/miniconda3/envs/paddle/lib:$LD_LIBRARY_PATH
```

最后，来检查下是否安装成功：

```
import paddle
paddle.utils.run_check()
```

如果在 Paddle 中使用多 GPU，还要安装 nccl2：

```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install libnccl2 libnccl-dev
```

PS：整体来看，你想用 PaddlePaddle，配置环境会麻烦很多。

## 3. 依赖库-以flash-attn为例

看到这里，你的本地环境基础搭建，基本已经 OK 了。

还有最后一关，那就是依赖 cuda 版本的各种依赖库。

比如，本地跑大模型，一定绕不过的 `flash_attn`。

如果你在 pip 安装一直无法成功：

```
# --no-build-isolation 意味着构建过程将使用当前环境中已安装的包，而不是创建一个新的隔离环境
pip install flash-attn --no-build-isolation
```

遇到了本文开头的报错，可是环境中的 cuda 版本没问题啊？

这是因为它只去你的 /usr/local 去执行 nvcc，结果发现 cuda 版本不对。

所以，最好在你的 conda 环境中，装上 nvcc 编译器：

```
conda install cuda-nvcc
```

当然，这时你可能还会遇到网络的问题，导致安装失败！

怎么搞？

直接去官方仓库，看看有没有 Releases 包？

比如 `flash_attn` 的官方仓库，就提供了各种版本的 whl 包:
[https://github.com/Dao-AILab/flash-attention/releases](https://github.com/Dao-AILab/flash-attention/releases)

截至发文，最新版是 2.6.3，**根据你的 torch 版本，python 版本**，选择对应的文件，下载到本地： 
![](https://img-blog.csdnimg.cn/img_convert/330d692af6f06f8af5ff545f328502aa.png)


然后，一键安装：

```
pip install flash_attn-2.6.3+cu118torch2.0cxx11abiFALSE-cp310-cp310-linux_x86_64.whl
```

whl 包安装，适用于解决网络不通的问题，如果安装失败，一定是版本没对应上，再回头仔细检查下吧。

## 写在最后

洋洋洒洒数千字，把`AI 环境配置`的各种问题捋了一遍。不到之处，欢迎评论区留言，我来更新。

如果对你有帮助，欢迎**点赞收藏**备用。


