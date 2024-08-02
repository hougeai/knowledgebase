
后台很多小伙伴反应，国内经常访问不了 GitHub，甚至无法 clone GitHub 上的项目和文件。

今天给大家分享一个超简单的方法，一行命令搞定。

说白了，就是给原始地址加一个镜像。

> 地址：[https://mirror.ghproxy.com/](https://mirror.ghproxy.com/)

具体而言：

## 1. 项目下载


```
# 原命令
git clone https://github.com/InternLM/InternLM.git

# 改为
git clone https://mirror.ghproxy.com/https://github.com/InternLM/InternLM.git
```


## 2. release文件下载

```
# 原命令
wget https://github.com/ngc660sec/NGCBot/releases/download/V2.1/WeChatSetup-3.9.10.27.exe
# 改为
wget https://mirror.ghproxy.com/https://github.com/ngc660sec/NGCBot/releases/download/V2.1/WeChatSetup-3.9.10.27.exe
```

## 3. raw文件下载

```
# 原命令
wget https://raw.githubusercontent.com/kubernetes/kubernetes/master/README.md -O README.md

# 改为
wget https://mirror.ghproxy.com/https://raw.githubusercontent.com/kubernetes/kubernetes/master/README.md-O README.md
```

如果本文对你有帮助，欢迎**点赞收藏**备用！
