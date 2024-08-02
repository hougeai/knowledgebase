
最近用 Pytorch 训模型的过程中，发现总是训练几轮后，出现显存爆炸 out-of-memory 的问题，询问了 ChatGPT、查找了各种文档。。。

在此记录这次 debug 之旅，希望对有类似问题的小伙伴有一点点帮助。

# 问题描述：

训练过程中，网络结构做了一些调整，forward 函数增加了部分计算过程，突然发现 16G 显存不够用了。

用 nvidia-smi 观察显存变化，发现显存一直在有规律地增加，直到 out-of-memory。

# 解决思路：
## 尝试思路1：
计算 loss 的过程中是否使用了 item() 取值，比如：

```
train_loss += loss.item()
```

发现我不存在这个问题，因为 loss 是最后汇总计算的。

## 尝试思路2：
训练主程序中添加两行下面的代码，实测发现并没有用。
```
torch.backends.cudnn.enabled = True
torch.backends.cudnn.benchmark = True
```

这两行代码是干啥的？

大白话：设置为 True，意味着 cuDNN 会自动寻找最适合当前配置的高效算法，来获得最佳运行效率。这两行通常一起是哦那个

所以：
- 如果网络的输入数据在尺度或类型上变化不大，设置 `torch.backends.cudnn.benchmark = True` 可以增加运行效率；
- 如果网络的输入数据在每次迭代都变化，比如多尺度训练，会导致 cnDNN 每次都会去寻找一遍最优配置，**这样反而会降低运行效率**。


## 尝试思路3：
及时删除临时变量和清空显存的 cache，例如在每轮训练后添加：
```
torch.cuda.empty_cache()
```
依旧没有解决显存持续增长的问题，而且如果频繁使用 `torch.cuda.empty_cache()`，会显著增加模型训练时长。

## 尝试思路4：
排查显存增加的代码位置，既然是增加了部分代码导致的显存增加，那么问题肯定出现在这部分代码中。

为此，可以逐段输出显存占用量，确定问题点在哪。

举个例子：

```
print("训练前:{}".format(torch.cuda.memory_allocated(0)))
train_epoch(model,data)
print("训练后:{}".format(torch.cuda.memory_allocated(0)))
eval(model,data)
print("评估后:{}".format(torch.cuda.memory_allocated(0)))
```

## 最终方案：
最终发现的问题是：我在模型中增加了 `register_buffer`：

```
self.register_buffer("positives", torch.randn(1, 256))
self.register_buffer("negatives", torch.randn(256, self.num_negatives))
```

但 **register_buffer** 注册的是非参数的 Tensor，它只是被保存在模型的状态字典中，并不会进行梯度计算啊。

为了验证这一点，还打印出来验证了下：

```
# for name, param in model.named_parameters():
for name, param in model.named_buffers():
    print(name, param.shape, param.requires_grad)

# 输出如下：
positives torch.Size([1, 256]) False
negatives torch.Size([256, 20480]) False
```

但是这个 `buffer` 却是导致显存不断增加的罪魁祸首。

为此，赶紧把和 `buffer` 相关的操作放在 **torch.no_grad()** 上下文中，问题解决！

```
@torch.no_grad()
def dequeue_samples(self, positives, negatives):
    if positives.shape[0] > 0:
        self.positives = 0.99*self.positives + 0.01*positives.mean(0, keepdim=True)
    self.negatives[:, self.ptr:self.ptr+negatives.shape[1]] = F.normalize(negatives, dim=0)

with torch.no_grad():
    keys = F.normalize(self.positives.clone().detach(), dim=1).expand(cur_positives.shape[0], -1)
    negs = self.negatives.clone().detach()
```

# 结论：

如果是训练过程中显存不断增加，问题大概率出现在 forward 过程中，可以通过`尝试思路4`逐步排查出问题点所在，把不需要梯度计算的操作放在 **torch.no_grad()** 上下文中。

如果本文对你有帮助，欢迎**点赞收藏**备用！
