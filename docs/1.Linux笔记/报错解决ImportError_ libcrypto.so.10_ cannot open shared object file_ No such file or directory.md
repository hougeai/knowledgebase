# 原因分析
这是因为linux系统中ssl版本的问题，比如程序需要的是1.0版本，而系统中可能是1.1版本，所以需要重新安装open-ssl。

# 怎么解决
## 找到libcrypto所在位置
```bash
find /usr/ -name "libcrypto*" #比如我们这里发现是1.1版本
```
## 新建lib文件夹

```bash
mkdir ~/lib # 用户根目录下创建lib,用于存放依赖库，如果没有sudo权限，系统根目录下无法保存
cd ~/lib
```
## 下载源码包
这里下载所需要的1.0版本
```bash
wget https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz
tar -xzf openssl-1.0.2k.tar.gz
cd openssl-1.0.2k
```
## 编译安装

> make 和 make install的区别：
>  - ./config 或者 /configure：配置环境，建立Makefile文件
> - make：编译，就是把源码包编译成二进制可执行文件
> - make install：安装

```bash
./config -d shared --prefix=/home/aistudio/lib/ #配置环境，安装到指定目录
make  # 编译
echo $? # 检测是否编译成功，输出0说明成功
make install # 安装
echo $? # 检测是否安装成功，输出0说明成功
```
## 生成软链接

```bash
cd /home/aistudio/lib/ # 回到lib目录下
ln -s lib/libcrypto.so.1.0.0 libcrypto.so.10
ln -s lib/libssl.so.1.0.0 libssl.so.10
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/aistudio/lib/
```
至此，再重新运行你的程序，应该就没有报错了，继续愉快玩耍吧！
