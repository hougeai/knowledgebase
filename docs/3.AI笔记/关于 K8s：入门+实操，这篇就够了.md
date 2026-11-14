这是一篇关于 `Kubernetes(简称K8s)` 的**科普+实操**文！

前文，分享了`小智AI服务端`的完整解决方案：

[低至1.5元/天，小智AI服务端，完整解决方案，高可用+可扩展](https://zhuanlan.zhihu.com/p/1937478173907452319)

服务部署在 Sealos 上，很多小伙伴对`低成本`感兴趣，让单独开一篇`sealos`的教程。

`sealos`是啥？

一套基于 K8s 的云操作系统，屏蔽掉 K8s 的复杂性，数据库、网站、对象存储，在 Sealos 里都是一个“应用”。你只需像在手机应用商店一样，点点鼠标，就能把这些服务部署到云上，而不用关心背后复杂的 K8s 配置。

> 注册体验：[https://bja.sealos.run/?uid=QDGJoX2_Qp](https://bja.sealos.run/?uid=QDGJoX2_Qp)

思来想去，要讲 `sealos`，就得对`K8s`的基本概念有所了解，否则文章就成了大杂烩，读者获得感不强。

因此，本文，尝试带大家以实操的方式来理解 `K8s`。

云原生工具，光看没用，自己搭个环境体验一番，亲测方可得真知。

`K8s`亦如此！

## 1. 云原生：从 “有云” 到 “用好”

笔者认为，把`K8s`放到云原生的发展历史中，能更好地理解`为什么是现在这个样子`！

### 1.1 什么是云原生

云原生 = `云计算基础设施` + `应用工具链`

如果从 `应用工具链` 看，其核心特征有：
- **容器化**：应用及依赖被打包成镜像，运行在容器，保证环境一致性；
- **微服务**：应用拆分为独立部署的微服务，单独迭代、故障隔离；
- **动态编排**：通过工具自动管理容器的部署、扩缩容、自愈；
- **持续交付**：结合 CI/CD 工具，实现代码提交到上线的自动化；
- **声明式配置**：通过 “描述目标状态” 而非 “步骤” 来管理系统。

### 1.2 早期云计算：有云但效率低

早在 2006 年， AWS 推出 EC2（虚拟机服务），标志着 IaaS（基础设施即服务）兴起。

买物理服务器，真麻烦，租用云厂商的虚拟机，真香！

但此时的应用还是`传统架构`=单体应用+手动部署，无法动态扩缩容。

到这里，尽管实现了`把应用搬到了云上`，但效率很低。

怎么解决？

### 1.3 容器技术的突破：Docker

早期容器技术（如 Linux LXC），操作复杂，难以普及。

2013 年 `Docker` 开源。

成功解决了应用部署的核心痛点：`在我电脑上能跑啊！`

但只能在我电脑上跑，咋办？

Docker 的解决方案：`容器+镜像`实现`一次打包，到处运行`。

- **镜像**（Image）：应用及其依赖的 “快照”，相当于一个 “只读模板”，无论在开发、测试还是生产环境，完全一致；
- **容器**（Container）：镜像的 “运行实例”，基于宿主机内核（非独立 OS），体积小（MB 级）、启动快（秒级），且通过隔离技术（如 Linux Namespace）保证应用间互不干扰。

通过 `镜像 + 容器` 的简化设计， Docker 成了容器化的事实标准。

从此，云原生有了基础工具。

### 1.4 编排工具的竞争：K8s

小网站，`Docker` 容器足矣，手动运维就 OK。

实际场景中，一个应用，拆分成多个微服务，每个服务还有多个实例，成百上千个容器，你怎么管？

此外，还有更多新问题：
- 如何自动在多台服务器上分配容器（负载均衡）？
- 某个容器崩溃了，如何自动重启（自愈）？
- 流量激增时，如何自动增加容器数量（扩缩容）？
- 如何管理容器间的网络通信（服务发现）？

**容器编排工具**应运而生！

2014 年，Google 开源了 `K8s`。

同期还有 Docker Swarm 等竞争对手，但 `K8s` 凭借强大的功能和生态，逐渐成为**容器编排**的事实标准。

比如“这个服务要 3 个实例”，`K8s` 的解决方案：
- 容器调度：根据服务器资源（CPU / 内存）分配容器；
- 自愈：检测到容器故障时，自动在健康节点重启容器；
- 扩缩容：根据流量或自定义规则，自动增加 / 减少容器数量；
- 服务发现与负载均衡：为容器分配统一访问地址，自动分发请求；
- 滚动更新：更新应用时，逐个替换旧容器，避免服务中断

---
总结来说：`Docker` 让容器 `能跑`，而 `K8s` 让容器 `规模化、稳定地跑`。

要做到以上几点，离不开 `K8s` 中的几个核心概念！

## 2. K8s 基本概念

用`小区`来打个比方：

- Namespace：小区的南区/北区（对应 K8s 中测试区、生产区，互不干扰）。
- Master：物业中心（管理所有楼栋）。
- Node：楼盘里的某一栋楼（实际服务器）。
- Pod：住人的房间（容器住的地方，共享水电等基础设施）。
- Deployment：物业经理（确保始终有足够的人手，随时替换请假的人）。
- Service：门口保安（提供稳定地址，帮你指路）。

### 2.1 Namespace 
Namespace 负责把不同的资源（Pod、Service、Deployment 等）分类存放。

相当于在整个 K8s 集群上，建立相互隔离的几个`子集群`。

比如创建一个`测试环境`的 Namespace，再创建一个`生产环境`的 Namespace，互不干扰。

### 2.2 Master

K8s 的“大脑”，负责整个集群的管理。

有几个重要角色：
- **API Server**：对外沟通的窗口，所有指令都经过它。
- **Scheduler**：调度员，决定新的 Pod 应该放在哪个 Node 上。
- **Controller Manager**：管家，确保集群状态符合预期（比如 Pod 坏了，自动再创建一个）。
- **etcd**：一个小数据库，记录整个集群的状态信息。

### 2.3 Node

工作节点，就是一台实际的服务器（物理机或虚拟机）。

每个 Node 上根据自身资源(cpu/内存)，可以运行很多 Pod。


### 2.4 Pod

K8s 里的最小部署单位，住在 Node 里面，你可以把它当成一个“小房间”，里面可以住一个或多个容器（通常是一个）。

Pod 里的容器共享网络、存储，彼此通信特别方便。

### 2.5 Deployment

> 负责管理 Pod 的“副本数量”和“版本更新”。

假设网站有 3 个 Pod 同时运行，Deployment 会确保：

- 如果某个 Pod 挂了，自动再建一个。
- 如果想更新网站，Deployment 会先更新一个 Pod，再更新下一个，确保网站一直可用。

Deployment 就像一个项目经理，确保始终有 3 个员工（Pod）干活，有人请假（Pod 挂了），立即再招一个；想换一批新员工（更新网站），也会一个个换，不影响工作进程。

### 2.6 Service
> 负责服务发现与负载均衡。

**服务发现**：给一组 Pod 提供一个稳定的“门牌号”（IP 地址和端口），用户访问这个门牌号就行，不管后面 Pod 怎么变，用户都感知不到。

**负载均衡**：自动把用户的请求平均分给后面的多个 Pod。

--- 

当然，关于 K8s，还有很多概念，光看没用，实操中再去理解吧~

下文，我们通过动手搭建一套 K8s 集群，来加深理解。

## 3. K8s 集群部署体验

> 注：以下操作，只需一台装好 `Linux` 的虚拟机。

### 3.1 安装 `kubectl`

`kubectl` 是 K8s 官方的命令行工具，是操作 K8s 集群的 “遥控器”。

因此，本地要先安装好 `kubectl` 。

```
# linux下直接下载二进制文件 - 57.3M
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

如果下载慢，到官方仓库下载：[https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.33.md#v1333](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.33.md#v1333)

测试一下:

```
kubectl version --client
# 输出：
Client Version: v1.33.3
Kustomize Version: v5.6.0
```

接下来，连接到 `K8s` 集群，怎么连？
- 根据配置文件（~/.kube/config）连！

比如，我要连接到 `sealos` 上的集群，配置文件在这里：

![](https://i-blog.csdnimg.cn/img_convert/34a48fa1e83e3e855f92cd6b5e72980d.png)

把它 copy 到`~/.kube/config`就 OK 了！

来试试几个最常用的命令吧：

```
kubectl get nodes # 查看集群节点，可能没有这个权限
kubectl get pods # 查看当前命名空间的Pod
kubectl get deployments
kubectl get services
```

### 3.2 安装 `helm`

Helm 是 K8s 的「apt / yum」，一键安装、卸载应用的包管理器。


```
# linux下安装
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version   # 看到 v3.x.x 即成功
```

如果下载慢，可以到官方仓库下载：[https://github.com/helm/helm/releases/latest](https://github.com/helm/helm/releases/latest)

Helm 安装好之后，同样是通过`~/.kube/config`和 K8s 集群通信。

快速体验：

```
helm install my-mysql bitnami/mysql   # 一键装个 MySQL
kubectl get pods                      # 集群里已出现 MySQL Pod
helm uninstall my-mysql               # 一键卸载
```

其中`bitnami/mysql`就是 mysql 安装包，把各种依赖都打包好了。

---

当然，为了更好地体验 `K8s`，最好是自己搭建一个集群！


### 3.3 搭建`K8s`集群的三种方式

要搭建一个`K8s`集群，有哪些方式？

**方式一：手动部署（劝退）**

手动操作每个节点，逐一安装组件（kube-apiserver、kube-controller-manager、kube-scheduler、kubelet、kube-proxy 等），并配置证书、网络等。

**痛点**：步骤繁琐、易出错

为此，`sealos` 等半自动化工具应运而生~

**方式二：半自动化工具（推荐）**

1. Kubernetes 官方提供的集群部署工具
- 需安装容器运行时
- 需至少 2 台服务器，1 台控制平面 + 1 台节点


2. Sealos
- 无需安装 Docker/containerd，会自动安装；
- 支持单节点集群；
- 安装工具开源，web 控制台需购买 License；

3. Rainbond
- 和 Sealos 类似
- 安装工具和控制台均开源；

就笔者体验来看，Sealos/Rainbond 等工具的优势，在于抽象层的降维设计，它把 K8s 复杂的控制器、资源对象封装在底层，让开发者点鼠标就能部署应用，完全不用记 `Pod/Service/Ingress` 这些概念。

**方式三：容器化部署（适合测试）**

Sealos/Rainbond 等工具面向的是生产环境，需要一台全新的服务器。

如果我们只是想了解学习，可以考虑`容器化部署`的方式搭建`K8s`集群。

只需一台装好 Docker 的机器，通过容器模拟多节点集群，轻量且隔离性好。

下面，我们就用 `kind（Kubernetes IN Docker）`这款开源工具，拉起一个 `K8s`集群。

### 3.4 kind 创建集群

**step 1: 安装kind**
```
# 下载安装
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/
kind --version  # 输出 kind version 0.20.0 即成功
```
**step 2: 创建集群**

```
# 自动拉取 kind 镜像（包含 Kubernetes 组件），并启动 Docker 容器作为集群的 master节点
kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.27.3) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:kubectl cluster-info --context kind-kind
# 查看当前存在的 kind 集群名称
kind get clusters
# 查看集群节点（kind 集群默认只有一个master节点）
kubectl get nodes
```

**step 3: 创建Deployment**

注：这一步会在 master 节点中拉取应用的镜像，因为现在 k8s 运行在docker容器中，所以无法识别本的镜像，需要将本地镜像先加载到 kind 集群：

```
# kind load docker-image 命令会将你本地 Docker 中的镜像，复制到 kind 集群的所有节点容器（如 kind-control-plane）的内部镜像存储中
kind load docker-image node:22-slim --name <集群name>
```

然后，开始创建：
```
kubectl create deployment node --image=node:22-slim
```

看看实例有没有起来呢：

```
kubectl get pods
NAME                    READY   STATUS             RESTARTS      AGE
node-54fb46689f-552gr   0/1     CrashLoopBackOff   4 (34s ago)   117s
```

失败了，因为我们选用的 node 基础镜像没有运行命令，k8s 根据默认的重启策略（Always），自动重启容器。但多次重启仍失败，触发了退避机制（CrashLoopBackOff），逐渐延长重启间隔。

所以，`kubectl create deployment` 只适合快速部署 “开箱即用” 的镜像。

如果要加启动命令，最好是写一份配置文件：
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node
spec:
  replicas: 1
  selector:
    matchLabels:
      app: node
  template:
    metadata:
      labels:
        app: node
    spec:
      containers:
      - name: node
        image: node:22-slim
        command: ["sleep"]  # 启动命令
        args: ["infinity"]  # 命令参数
```


再来创建：

```
kubectl apply -f deployment.yaml
```

这就是你在 `sealos` 中的看到的 `deployment.yaml`:

![](https://i-blog.csdnimg.cn/img_convert/74f2da194cd3b1835b3bf30aaabbd47d.png)

**step 4: 查看实例**

```
# 查看 Deployment（确保期望的 Pod 数量运行）
kubectl get deployments
kubectl delete deployment node # 删除后pod也没了
# 查看 Pod（应用的实际运行实例，被 Deployment 管理）, Pod 实际运行在节点容器（kind-control-plane）内部的容器运行时（containerd）中
kubectl get pods
# 如果显示镜像拉取失败,查看日志 
kubectl describe pod node-76478fbd9f-2npqk
```

### 3.5 可视化管理工具

`K8s Dashboard` 是官方提供的 Web 界面工具。

**step 1: 一键部署**

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

上述命令，会新建一个新的命名空间：`kubernetes-dashboard`，其中创建所需的 Deployment、Service 等资源。

```
# 查看命名空间下的资源
kubectl get all -n kubernetes-dashboard
# 查看所有命名空间
kubectl get namespaces or kubectl get ns
```

如果镜像拉取失败，修改为阿里云的镜像：

```
kubectl set image deployment/dashboard-metrics-scraper \
  dashboard-metrics-scraper=registry.cn-hangzhou.aliyuncs.com/google_containers/metrics-scraper:v1.0.8 -n kubernetes-dashboard
kubectl set image deployment/kubernetes-dashboard \
  kubernetes-dashboard=registry.cn-hangzhou.aliyuncs.com/google_containers/dashboard:v2.7.0 -n kubernetes-dashboard
```

**step 2: 创建访问 Dashboard 的管理员账号**

创建一个配置文件（dashboard-admin.yaml），内容如下：

```
# 1. 服务账号
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dashboard-admin
  namespace: kubernetes-dashboard
---
# 2. 与服务账号绑定的 Secret（明确关联）
apiVersion: v1
kind: Secret
metadata:
  name: dashboard-admin-secret
  namespace: kubernetes-dashboard
  annotations:
    # 关键：指定绑定的服务账号名称
    kubernetes.io/service-account.name: "dashboard-admin"
type: kubernetes.io/service-account-token
---
# 3. 角色绑定（授权）
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: dashboard-admin-binding
subjects:
- kind: ServiceAccount
  name: dashboard-admin
  namespace: kubernetes-dashboard
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

然后运行：

```
kubectl apply -f dashboard-admin.yaml
# 强制关联 Secret 到服务账号
kubectl patch serviceaccount dashboard-admin -n kubernetes-dashboard -p '{"secrets": [{"name": "dashboard-admin-secret"}]}'
# 查看服务账号（ServiceAccount）是否存在
kubectl get sa -n kubernetes-dashboard dashboard-admin
```

**step 3: 获取登录令牌**

```
kubectl get secret dashboard-admin-secret -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 --decode && echo
```

**step 4: 查看 Dashboard 的 Pod 状态**

```
kubectl get pods -n kubernetes-dashboard
```

**step 5: 启动访问代理**

```
 kubectl proxy
```

Dashboard 默认仅集群内部可访问，因此需要暴露本地访问：默认是8001端口：

```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

打开上述链接，输入登录令牌，即可查看集群资源：

![](https://i-blog.csdnimg.cn/img_convert/db409f3e7ac495bcefe09b5adcdc85dd.png)

我们只部署了一个节点，这里可以看到节点的可用资源：

![](https://i-blog.csdnimg.cn/img_convert/f75c0f3349bba371784e3d9fba49d116.png)

## 写在最后

本文分享了一条`从 0 到 1 体验 K8s`的极简路径，有了这番体感，云原生的大门就打开了。

如果对你有帮助，不妨**点赞收藏**备用。
