前两天，搞了个微信 AI 小助理-`小爱(AI)`，爸妈玩的不亦乐乎。
- [零风险！零费用！我把AI接入微信群，爸妈玩嗨了，附教程（下）](https://zhuanlan.zhihu.com/p/718126892)

最近一直在迭代中，挖掘`小爱`的无限潜力:
- [链接丢给它，精华吐出来！微信AI小助理太强了，附完整提示词](https://zhuanlan.zhihu.com/p/718355186)
- [拥有一个能倾听你心声的「微信AI小助理」，是一种什么体验？](https://zhuanlan.zhihu.com/p/718748712)
- [小爱打工，你躺平！让「微信AI小助理」接管你的文件处理，一个字：爽！](https://zhuanlan.zhihu.com/p/718897171)
- [我把多模态大模型接入了「小爱」，痛快来一场「表情包斗图」！不服来战！](https://zhuanlan.zhihu.com/p/719007337)
- [我把「FLUX」接入了「小爱」，微信直接出图，告别一切绘画软件！](https://zhuanlan.zhihu.com/p/719226362)
- [告别信息焦虑，「小爱」携手「每日早报」，打造你的个性化新闻早餐！](https://zhuanlan.zhihu.com/p/719471465)

不过，机器人基于 web 端微信，大概一两天会掉线，很是闹挺！

能否在它掉线后，自动提醒我？

还有，用什么方式提醒我呢？

- 微信消息？它都下线了，咋给我发微信消息？

- QQ 邮件？可行！我们可以写个轮询任务，每隔一小时查看下接口状态，一旦发现下线，自动给我发邮件，类似下面这样：

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bb6a03a3c03d41998882611f3b4ae853.png)


今日分享，带大家实操：**如何自动给你的 QQ 邮箱发送邮件。**

> 注：其它邮箱的食用方式基本一致，因为微信端绑定了 QQ 邮箱，接收提醒更方便，故本文以 QQ 邮箱为例。

私以为，这个技能还有很多应用场景，而且实操也非常简单。此所谓：**一学就会，不学后悔**。哈哈，建议收藏~


## 1. 邮箱设置


首先，前往你的 QQ 邮箱，找到 “设置”=>“账号” 。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3520532eac6143d2a2ba7b79d2a38d7c.png)



拉到下面，找到 POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/fc53b40281c14cc0b9013118e699ed71.png)


然后，点击管理服务，会跳转到账号与安全页面，点击生成授权码以生成授权码，把`授权码`保存好，后面会用到。

## 2. 邮件发送接口实现
以 Python 为例：


### 2.1 通用接口

首先，引入邮件发送所需要的包（Python 自带，无需 pip 安装）：

```
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
```
然后，定义一个发送类，并实现发送邮件的通用接口：

```
class MailSender:
    def __init__(self, username='QQ 号', password='授权码'):
        self.username = username
        self.password = password
    def sendMail(self, msg):
        try:
            smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
            smtp.login(self.username, self.password) 
            smtp.sendmail(msg['From'], msg['To'], msg.as_string()) 
            smtp.quit()
        except Exception as e:  
            print(e)
```

### 2.2 发送纯文本

如果仅仅是发送纯文本，那么非常简单：

```
def sendText(self, text='邮件发送测试', title='SMTP 文本测试'):
    msg = MIMEText(text, 'plain', 'utf-8') # 邮件正文
    msg['From'] = self.username + '@qq.com' 
    msg['To'] = self.username + '@qq.com' 
    msg['Subject'] = title # 邮件标题
    self.sendMail(msg)
```


至此，本文开头的核心诉求就已经完成了，因为我们只需要把登录链接放到邮件中即可。

但是，除了纯文本，`smtplib` 还支持更复杂的消息内容。

### 2.3 发送 HTML

比如我们可以放入 `html` 文本，邮件中自动渲染：

```
def sendHtml(self, htmlContent, title='SMTP html测试'):
    msg = MIMEMultipart()
    msg['From'] = self.username + '@qq.com' 
    msg['To'] = self.username + '@qq.com' 
    msg['Subject'] = title # 邮件标题
    body = MIMEText(htmlContent, 'html', 'utf-8')
    msg.attach(body)
    self.sendMail(msg)
```

### 2.4 发送附件

当然，如果你需要在邮件中添加附件，而不仅仅是嵌入在 HTML 中，也是 OK 的，示例代码如下：
```
def sendMultiPart(self, text='',
                    att_src='data/xxx.csv',
                    img_src='data/xxx.jpg', 
                    title='SMTP html测试'):
      msg = MIMEMultipart()
      msg['From'] = self.username + '@qq.com' 
      msg['To'] = self.username + '@qq.com' 
      msg['Subject'] = title # 邮件标题
      # 写入html内容
      filename = img_src.split('/')[-1]
      htmlContent = '<html><head></head><body><p>'\
          + text + \
          '</p><img src="cid:'+filename+'"/>'\
          '</body></html>'
      body = MIMEText(htmlContent, 'html', 'utf-8')
      msg.attach(body)
      # 写入图片内容
      if os.path.exists(img_src):
          imgFile = MIMEImage(open(img_src, 'rb').read())
          imgFile['Content-ID'] = filename
          imgFile['Content-Disposition'] = 'attachment;filename="'+filename+'"'
          msg.attach(imgFile)
      # 写入附件内容
      if os.path.exists(att_src):
          attFile = MIMEText(open(att_src, 'r').read(), 'plain', 'utf-8')
          attFile['Content-Type'] = 'application/text'
          attFile['Content-Disposition'] = 'attachment;filename=%s' % (att_src.split('/')[-1])
          msg.attach(attFile)
      self.sendMail(msg)
```



### 2.5 邮件群发

群发？多调用几次接口不就好了。。。

当然没问题，不过你还可以：把接收者列表，采用 list 赋值给 `msg['To'] `:

```
msg['To'] = ['xx1@qq.com', 'xx2@xxx.edu.cn', 'xx3@gmail.com']
```


## 写在最后

本文带大家实操了`自动发邮件`的魔法，无论你是想监控 AI 助手的在线状态，还是要定时给朋友发生日祝福... 这个小技能都能派上用场。

感兴趣的朋友，赶紧去试试吧！

如果对你有帮助，不妨点个**免费的赞**和**收藏**备用。

--- 
为了方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

`小爱`也在群里，想进群体验的朋友，公众号后台「联系我」即可，拉你进群。

