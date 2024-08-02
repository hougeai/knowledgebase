
前几天和大家分享了：[全网爆火的AI语音合成工具-ChatTTS](https://blog.csdn.net/u010522887/article/details/139591713)。

有很多小伙伴反应模型下载还有点麻烦~

今天再给大家带来一款开源的语音合成 TTS 项目-EdgeTTS，相比ChatTTS，操作起来对小白更友好。

因为其底层是使用微软 Edge 的在线语音合成服务，所以**不需要下载任何模型，甚至连 api_key 都给你省了**，简直不要太良心~

关键是，除了支持普通话外，还支持很多地方口音(比如: **粤语、台湾口音、陕西话、辽宁东北话等**)，就凭这， 吊打 ChatTTS 有没有!

太香了，赶紧开始实操！

# EdgeTTS 简介
> GitHub 仓库地址：[https://github.com/rany2/edge-tts](https://github.com/rany2/edge-tts)

EdgeTTS 是一个文本转语音的开源项目，截至目前，在 GitHub 上已经斩获了 4k 的 Star，作者一直在更新，该项目核心就是调用微软 Edge 的在线语音合成服务，支持40多种语言，318种声音，中英文通吃，简直是我等 AI 应用开发者的福音。

![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/d3b5b85358944b80b7eb1f815cdffdc0.png)
# EdgeTTS 使用教程
## 1.安装环境
最基本的环境安装，只需要两个 pip 包：

```python
pip install edge-tts
pip install torchaudio
```
## 2. 命令行使用
安装好包后，命令行一键调用，主要有如下指令：
### 2.1 查看支持的音色
查看支持的所有音色：

```python
edge-tts  --list-voices
```

如果想查看支持的粤语 or 台湾语

```python
edge-tts  --list-voices| grep HK # TW
```
类似的，查看支持哪些地方方言：

```python
edge-tts  --list-voices |grep CN
Name: zh-CN-XiaoxiaoNeural
Name: zh-CN-XiaoyiNeural
Name: zh-CN-YunjianNeural
Name: zh-CN-YunxiNeural
Name: zh-CN-YunxiaNeural
Name: zh-CN-YunyangNeural
Name: zh-CN-liaoning-XiaobeiNeural
Name: zh-CN-shaanxi-XiaoniNeural
```
### 2.2 一键生成语音
不多说了，直接上代码：
```python
edge-tts --voice zh-HK-WanLungNeural \
--text "曾经有一份真诚的爱情放在我面前，我没有珍惜，等我失去的时候我才后悔莫及，人世间最痛苦的事莫过于此。\
如果上天能够给我一个再来一次的机会，我会对那个女孩子说三个字：我爱你。\
如果非要在这份爱上加上一个期限，我希望是……一万年" --write-media test.wav
```
速度超快，终端还会返回 SRT 格式的字幕文本：
![](https://axcvs2xtkbpq.objectstorage.ap-singapore-1.oci.customer-oci.com/n/axcvs2xtkbpq/b/bucket-20240802-0845/o/dfc619428d21478e823c74f64def2ab2.png)
### 2.3 更多参数使用
为了实现更个性化的语音，除了音色，还有以下参数可以调用：

**调整合成语音的语速--rate参数**
> -30%表示语速变慢30%，+30%表示语速增加30%。

```python
edge-tts  --rate=-30%  --voice  zh-HK-WanLungNeural  \
--text "xxx" --write-media test.mp3
```

**调整合成语音的音量--volume**
> 通过--volume参数来设置播放的语速快慢，-60%表示语速变慢60%，+60%表示语速增加60%。

```python
edge-tts --volume=-50%  --voice  zh-HK-WanLungNeural  \
--text "xxx" --write-media test.mp3
```

**调整合成语音的频率--pitch**
> 通过pitch参数来调整合成语音的频率，-50Hz表示降低频率50Hz，+50Hz则相反

```python
edge-tts --pitch=-50Hz  --voice  zh-HK-WanLungNeural  \
--text "xxx" --write-media test.mp3
```

## 3. python 代码调用
如果需要在python脚本中调用 EdgeTTS，来实现语音合成，也是没问题的，示例代码如下：

```python
import edge_tts

text = """曾经有一份真诚的爱情放在我面前，我没有珍惜，等我失去的时候我才后悔莫及，人世间最痛苦的事莫过于此。
如果上天能够给我一个再来一次的机会，我会对那个女孩子说三个字：我爱你。如果非要在这份爱上加上一个期限，我希望是……一万年"""

communicate = edge_tts.Communicate(text=text,
        voice="zh-HK-HiuGaaiNeural",
        rate='+0%',
        volume= '+0%',
        pitch= '+0Hz')

communicate.save_sync("test.wav")
```
# 写在最后
不得不说，AI 语音界真是人才辈出，除了 ChatTTS 之外，希望这款支持多种方言的TTS项目，在帮你打造个性化 AI 语音助手时，提供另外一种选择。
 
如果本文对你有帮助，欢迎 **点赞收藏** 备用！
