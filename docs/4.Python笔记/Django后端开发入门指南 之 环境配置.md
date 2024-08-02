> 摘要：入门后端开发，必须理论结合实践。本系列文章将结合Datawhale 10月份的打卡活动，通过全身心体验，记录项目开发过程中遇到的一些问题和总结开发过程中的一些心得体会。

## 如何快速访问github
由于种种原因，国内很难访问github，我是通过将GitHub上的仓库import到gitee进行解决
## 安装python虚拟环境
在windows下使用virtualenv：如果发现无法activate，可以参考这篇文章加以解决：[link](https://blog.csdn.net/weixin_44548098/article/details/129944030)

## 搭建项目
- 新建文件夹，命名为erp
- 新建apps文件夹用于存放app
- 建立app-erp_test:
- django-admin startapp erp_test
- 配置settings.py文件，将新安装的app包导入
- 运行项目：python manage.py runserver，在浏览器中输入http://127.0.0.1:8000/就可以看到项目成功运行
