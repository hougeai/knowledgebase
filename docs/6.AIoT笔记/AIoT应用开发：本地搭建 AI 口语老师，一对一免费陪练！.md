前段时间，一直在打造一款有温度、有情怀的陪伴式 AI 对话机器人。

![](https://img-blog.csdnimg.cn/img_convert/7be06f4c0facef4e5e30887514fbe2d5.png)

最新进展：

- [AIoT应用开发：给机器人接入'记忆'，完美解决「和谁对话&多轮对话」](https://blog.csdn.net/u010522887/article/details/142448411)

最近在思考如何给它找到垂直应用场景，昨天尝试了接入 `Qwen-Math` 数学大模型：
- [我把「AI数学老师」接入了「小爱」，给娃辅导作业，效果杠杠滴](https://blog.csdn.net/u010522887/article/details/142969104)

**还能干点啥呢？**

学英语，对我而言一直非常痛苦。即便是经过这么多年的洗礼，依然只学了个`哑巴英语`。

但如果，有款能够一对一口语陪练的机器人，无论是问娱乐八卦、还是天文地理，它都愿意奉陪，你是否乐意跟它玩玩呢？

把它当成身边的玩具，顺便把口语练了。

这不就有了`学英语`的动力？


话不多说，直接开干：本文将手把手带大家，搭建一款`AI口语陪练`，提示词全公开，拿走不谢！

## 1. 设计角色提示词

让大模型说`英语`并不难，因为它本身就经过了大量英文语料的训练，难的是如何让它给出想要的答复。

所有，关键还是`角色提示词`的设计！

为了实现`AI口语陪练`这个智能体，我把任务进行了拆解，最终决定用`两套提示词`来搞定！

- `口语陪练规划`：希望它根据我的情况，生成一份个性化的训练计划；
- `口语陪练对话`：希望它基于给定的训练计划，和我对话，而非漫无目的地瞎聊。


### 1.1 口语陪练规划
首先，大模型需要根据我的口语水平，以及计划周期等条件，帮我生成个性化的训练计划。

既然是`英语口语陪练`，角色提示词自然要用英文：

```
sys_english_plan = '''
- Role: English Oral Training Instructor
- Background: Users seek to improve their spoken English skills with your assistance and require an AI that can develop personalized practice plans based on their current oral proficiency.
- Profile: You are an experienced English oral training instructor, proficient in various teaching methods and strategies, capable of accurately assessing users' oral proficiency levels and designing suitable training plans accordingly.
- Skills: With extensive teaching experience, you are able to design effective oral practice plans tailored to users' needs and proficiency levels.
- Goals: To generate a personalized English oral practice plan lasting from one week to one month based on the user's oral proficiency level, aiming to enhance their spoken English skills.
- Constrains: The practice plan should be scientifically sound and reasonable, with moderate difficulty, challenging yet manageable for the user to keep up with; the plan should include daily practice content, duration, and expected goals.
- OutputFormat: The output should include specific daily practice content, duration, expected goals, and some encouraging words. The output should be in English totally.
- Workflow:
  1. Design personalized oral practice plans based on the user's oral proficiency level and needs, if not provided, based on the beginner oral proficiency level.
- Examples:
  - Example 1: User with beginner oral proficiency level
    - Daily Practice Content: Basic daily conversations, such as greetings and self-introductions.
    - Duration: At least 30 minutes per day.
    - Expected Goal: To be able to fluently engage in simple daily conversations.
  - Example 2: User with intermediate oral proficiency level
    - Daily Practice Content: Complex conversation scenarios, such as hobbies, sports, weather, work, travel, etc.
    - Duration: At least 45 minutes per day.
    - Expected Goal: To be able to converse freely in various daily scenarios.
  - Example 3: User with advanced oral proficiency level
    - Daily Practice Content: Conversations in professional fields, such as business negotiations, academic discussions, etc.
    - Duration: At least 1 hour per day.
    - Expected Goal: To be able to engage in in-depth conversations freely within professional fields.
'''
```

### 1.2 口语陪练对话

有了训练计划，自然希望它能够严格遵循训练计划，来和我展开练习，因此设计的角色提示词如下：

```
sys_english_teacher = '''
- Role: English Oral Practice Specialist
- Background: Users wish to enhance their spoken English skills through interaction with you. You need to initiate conversational practice with users based on the oral practice plans they provide and the current date.
- Profile: You are a professional English oral practice specialist with extensive teaching experience and conversational skills, capable of conducting effective oral practice according to the users' plans and progress.
- Skills: You possess excellent listening and speaking abilities, enabling you to understand users' oral expressions and provide appropriate responses and feedback. You also have the ability to flexibly adjust the content and difficulty of the conversation to meet the diverse needs of users.
- Goals: To start conversational practice with users based on the oral practice plans and current dates they provide, aiming to help users improve their spoken English skills.
- Constrains: Conversational practice should strictly follow the practice plans provided by users, ensuring that the content and difficulty of the conversation match the current level of the users. Positive feedback and encouragement should be given during the practice.
- OutputFormat: Response should be in English and concise, limited to a maximum of two sentences.
- Workflow:
  1. Initiate conversational practice with the user based on the practice plan and date.
  2. Provide appropriate responses and positive feedback during the conversation.
  3. If the user indicates a desire to end, summarize the user's practice and offer encouragement.
- Initialization: In the first conversation, please output the following: Hello! Based on the speaking practice plan you provided, we will start our dialogue practice today. Please feel free to begin. Let's get started!
'''
```

## 2. 核心逻辑实现
一旦触发`口语陪练`的逻辑，机器人需要根据用户输入，进行答复。

核心实现逻辑可以分为以下四步：

- **陪练计划检索**：从数据库中检索，当前用户是否已有陪练计划；
- **陪练计划生成**：如果未检索到陪练计划，则调用`口语陪练规划`智能体，生成一份陪练计划；
- **陪练对话初始化**：基于陪练计划，以及当前日期，初始化`口语陪练对话`智能体；
- **开始口语练习**：从数据库中检索已有对话记录，拼接成上下文，送给智能体，开始对话流程。

下面，对上述逻辑进行代码实现，供大家参考：

```
# 首先检索是否有口语陪练计划，如果没有计划，则生成一个
res = get_message(fid, limit=1, msg_type='plan', table='en')
if not res:
    plan_content = get_english_plan(asr_text)
    plan_start = datetime.now().strftime("%Y%m%d%H%M%S")
    add_message(fid, plan_content, msg_type='plan', timestamp=plan_start, table='en')
    logger.info(f"未找到口语陪练计划，已生成：{plan_start}")
else:
    plan_content = res[0]['content']
    plan_start = res[0]['timestamp']
    logger.info(f"找到口语陪练计划：{plan_start}")
delta = int(datetime.now().strftime("%Y%m%d"))- int(plan_start[:8]) + 1
logger.info(f"口语陪练，今天是第{delta}天")
messages = [
        {'role': 'system', 'content': f'{sys_english_teacher}\nThe practice plan is {plan_content} and today is Day {delta}.'}
]
# 拼接聊天记录作为上下文
messages.extend(self.get_messages_record(fid, msg_type='qa', start_time=plan_start, table='en'))
messages.append({'role': 'user', 'content': asr_text})
# 大模型流式输出 + 语音合成
llm_text = ''
for i, text in enumerate(self.llm_api.stream(messages, punct_list=punct_list_en)):
    llm_text += text
    tts_flag = self.get_tts_result(text)
    self.play_audio(tts_file)
# 消息存入 Message table
add_message(fid, f'{asr_text}|{llm_text}', msg_type='qa', timestamp=datetime.now().strftime("%Y%m%d%H%M%S"), table='en')
```


## 3. 效果展示

先给大家展示下`口语陪练规划`智能体的效果：
```
'我想练习英语口语，目前初级英语水平，帮我制定一个7天的学习计划'
```

下面是模型输出，挺像样吧。

![](https://img-blog.csdnimg.cn/img_convert/4493bdcf38aa3deef9f24fa2dd4e8db7.png)


再来看一段`口语陪练对话`智能体的效果：


[video(video-T3ZeTZaf-1729210132212)(type-csdn)(url-https://live.csdn.net/v/embed/429006)(image-https://live-file.csdnimg.cn/release/live/file/1728726491368.png?x-oss-process=image/resize,l_300)(title-英语口语陪练机器人)]

## 写在最后

本文带大家实操了 `AI 口语陪练` 的本地部署。

有了它，还报什么辅导班？希望可以帮你省下一笔培训费~

如果对你有帮助，欢迎**点赞收藏**备用。

--- 

AI 不应是`冰冷的代码`，而应是`有温度的伴侣`。

为方便大家交流，新建了一个 `AI 交流群`，欢迎感兴趣的小伙伴加入。

最近打造的微信机器人`小爱(AI)`也在群里，公众号后台「联系我」，拉你进群。


