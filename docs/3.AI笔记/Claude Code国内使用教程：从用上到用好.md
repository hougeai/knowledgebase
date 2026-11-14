前段时间，分享的`OpenClaw`教程火了：

[永久免费 OpenClaw 部署和实战，7x24在线，手把手教程](https://zhuanlan.zhihu.com/p/2006309221654889869)

很多朋友，在感叹AI强大的同时，也想开发自己的产品。

确切地说，是**想用AI来开发自己的产品**！

此时，你一定听过，但一定不能绕过：`ClaudeCode`。

今日分享，

写给想体验 `ClaudeCode`的朋友：

一份从安装、配置到使用的完整指南，**全程免费**，国内可用！

全文9部分：

- 免费API申领
- `ClaudeCode`安装
- `MCP`是什么&怎么用
- `Hooks`是什么&怎么用
- `Skills`是什么&怎么用
- 如何让AI自我进化
- 如何让AI拥有永久记忆
- 如何提高AI的UI审美
- 如何规范AI的开发流程

## 1. 免费API申领

前文：[永久免费 OpenClaw 部署和实战，7x24在线](https://zhuanlan.zhihu.com/p/2006309221654889869)，带大家申领了`NVIDIA`的免费API，但目前只兼容 `OpenAI` 格式。

`Anthropic` 的 `Messages API` 与 `OpenAI` 的 `Chat Completions API`在结构上存在本质差异。

而`ClaudeCode`闭源，且只能接入`Anthropic` 的API。

本文，继续分享两款有免费额度的国内API平台，方便大家快速体验`ClaudeCode`。

### 1.1 硅基流动
> 注册：[https://cloud.siliconflow.cn/i/DrgxdqSF](https://cloud.siliconflow.cn/i/DrgxdqSF)，+16元免费额度。

兼容 OpenAI API 和 Anthropic API。

模型广场：[https://cloud.siliconflow.cn/me/models](https://cloud.siliconflow.cn/me/models)。推荐用`Pro/系列`：

![](https://i-blog.csdnimg.cn/img_convert/362365885862bc77c13449def4cc6104.png)

API文档：[https://docs.siliconflow.cn/cn/api-reference/chat-completions/messages](https://docs.siliconflow.cn/cn/api-reference/chat-completions/messages)
- `OPENAI_API_BASE`：[https://api.siliconflow.cn/v1](https://api.siliconflow.cn/v1) 兼容 OpenAI 接口（即 /chat/completions）
- `CLAUDE_API_BASE`：[https://api.siliconflow.cn/](https://api.siliconflow.cn/)    兼容 Anthropic 接口（即 /v1/messages）

### 1.2 七牛云

> 注册：[https://s.qiniu.com/YBVZ73](https://s.qiniu.com/YBVZ73)，+1000万Token免费额度。

兼容 OpenAI API 和 Anthropic API。

模型广场：[https://portal.qiniu.com/ai-inference/model](https://portal.qiniu.com/ai-inference/model)。

![](https://i-blog.csdnimg.cn/img_convert/ef49cd01fc10dbbc2a637034524c3a4e.jpeg)

使用邀请奖励：

![](https://i-blog.csdnimg.cn/img_convert/d6c22680b747a71804fceb4e67f2f5c2.png)

API文档：[https://apidocs.qnaigc.com/](https://apidocs.qnaigc.com/)
- `OPENAI_API_BASE`：[https://api.qnaigc.com/v1](https://api.qnaigc.com/v1) 
- `CLAUDE_API_BASE`：[https://api.qnaigc.com](https://api.qnaigc.com) 



## 2. ClaudeCode安装和配置

`ClaudeCode`可稳定运行在`windows / linux / mac`。

### 2.1 安装

前置条件：装好 node.js，其它没了。

```
# npm安装
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com

# 查看 claude code 版本
claude -V
2.1.74 (Claude Code)

# 启动看看
claude
```

这时启动 `claude`，如果遇到`登录失败`的问题：

![](https://i-blog.csdnimg.cn/img_convert/0023f9f6e7644fce208c1f1356dee063.png)

这是因为`claude`限制了国内用户访问。

怎么搞？

### 2.2 配置

上一步，会在根目录自动生成两个相关文件：

```
$ ls ~/.cl
.claude/      .claude.json
```

新建配置文件：

```
vim ~/.claude/settings.json
```

然后，填入模型相关信息：

- 硅基流动的模型配置示例：
```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xx",
    "ANTHROPIC_BASE_URL": "https://api.siliconflow.cn",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "Pro/MiniMaxAI/MiniMax-M2.5",
  },
  "includeCoAuthoredBy": false,
  "model": "Pro/MiniMaxAI/MiniMax-M2.5",
  "skipDangerousModePermissionPrompt": true
}
```
- 七牛云的模型配置示例：

```
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xx",
    "ANTHROPIC_BASE_URL": "https://api.qnaigc.com",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "minimax/minimax-m2.5"
  }
}
```

再次启动 `claude` 即可成功：

![](https://i-blog.csdnimg.cn/img_convert/d4f194d1f5e132bd2720194182c1f9f4.png)

### 2.3 对话

全局对话历史：`~/.claude/history.jsonl`；

项目级会话数据：`~/.claude/projects/`

![](https://i-blog.csdnimg.cn/img_convert/56f14ac4738160860680d2e3a21683b0.png)

```
# 查看历史会话列表
claude --resume 或 claude -r
# 从之前的会话继续（需要会话ID）
claude -r a9e7c777-52ce-41ba-8345-23459f9f28b6
# 继续当前项目的最近一次对话
claude --continue 或 claude -c
```

至此，你就可以和`ClaudeCode`畅快对话了。


当然，要想开启`ClaudeCode`的最强武力，绕不开以下几个核心概念：
- MCP
- Hooks
- Skills

## 3. MCP是什么&怎么用

早在2024年11月，Anthropic 发布 MCP 1.0 规范，开创 LLM 工具调用标准化先河。

关于MCP的原理，可参考笔者前文：

[搞不懂 MCP？那就动手搓一个](https://zhuanlan.zhihu.com/p/1912823317011888104)

### 3.1 MCP 配置

`ClaudeCode`中的 `MCP` 采用**分层配置**：

**全局配置:**

- 路径: `~/.claude.json` 

- 对所有`ClaudeCode`项目生效。通常用于配置通用的搜索引擎、个人 GitHub 权限等。

**项目配置:**

- 路径: 项目根目录下 `.mcp.json`

- 仅对当前项目生效。适合配置与项目强相关的工具，如特定数据库连接等。

**怎么配置？**

两种方式：
- 命令行指令
- 手动编辑 JSON

**方式 A：命令行配置**

使用内置命令可以自动处理语法并验证连接：

```
# 添加全局 MCP 服务器
claude mcp add github --scope user -- npx -y @modelcontextprotocol/server-github
# 添加当前项目的 MCP 服务器
claude mcp add sqlite --scope project -- npx -y @modelcontextprotocol/server-sqlite --db path/to/db
# 删除MCP
claude mcp remove xx
# 查看MCP详情
claude mcp get xx
# 列出所有MCP服务器
claude mcp list
```

注：`npx` 是 `npm` 的执行器：先检查本地 node_modules 有没有包；如果没有，它会自动下载到一个临时的缓存目录并直接运行。

此外，`ClaudeCode`也支持远程 MCP 服务器：

```
claude mcp add <名称> --scope user --transport sse <URL> --header "Authorization: Bearer YOUR_TOKEN"
```

**方式 B：手动编辑 JSON**

直接写入配置文件，格式如下：

```
{
  "mcpServers": {
    "my-tool": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"],
      "env": {
        "API_KEY": "your_secret_here"
      }
    }
  }
}
```

### 3.2 MCP 推荐

#### 3.2.1 全局MCP推荐

**1. Fetch (网页抓取)**

将网页内容转为 Markdown，方便 Claude 阅读 API 文档。

```
claude mcp add fetch --scope user -- uvx mcp-server-fetch
```
**注：这里采用Python 的 uvx安装**。`uv` 目前在 MCP 生态受到广泛推崇。Claude官方也在优先使用，因为它的依赖隔离做得比 npx 更好。

安装后：

![](https://i-blog.csdnimg.cn/img_convert/f5566a3a592ee4ec218965c2f5d66b0b.png)

![](https://i-blog.csdnimg.cn/img_convert/2388eae6322dffa3621d8f79a65e1a6e.png)


**2. Brave Search (实时联网)**

让 Claude 能够搜索最新的技术文档。
```
claude mcp add brave-search --scope user -- npx -y @modelcontextprotocol/server-brave-search
# 然后手动添加 env BRAVE_API_KEY
```

**3. GitHub (个人权限)**

用于跨项目搜索你的代码库、处理 Issue。

```
claude mcp add github --scope user -- npx -y @modelcontextprotocol/server-github
# 然后手动添加 env GITHUB_PERSONAL_ACCESS_TOKEN
```
如何获取 `GITHUB_PERSONAL_ACCESS_TOKEN`？
- 登录 Github，点击右上角头像 → Settings
- 左侧菜单 → Developer settings
- Personal access tokens → Tokens (classic)
- Generate new token (classic)
- 勾选权限：
  - ✅ repo（完整仓库访问）
  - ✅ workflow（管理Actions）
- 点击 Generate token
- 立即保存，后续不可查看


**4. Context7（技术文档）**

获取1000+流行框架的最新文档。

```
claude mcp add context7 --scope user -- npx -y @upstash/context7-mcp
```

安装后：

![](https://i-blog.csdnimg.cn/img_convert/c02852e4489db8043b3b2aceba5955df.png)


#### 3.2.2 项目MCP推荐

**1. SQLite (本地数据库调试)**

连接到当前项目的开发数据库：

```
claude mcp add sqlite --scope project -- uvx mcp-server-sqlite --db-path backend/app/data/db.sqlite3
```

**2. PostgreSQL (生产/测试库)**

连接到指定的数据库实例：

```
claude mcp add postgres --scope project -- npx -y @modelcontextprotocol/server-postgres postgresql://user:password@localhost:5432/my_project
```

**3. Memory (知识记忆)**

既可以全局（记录个人习惯），也可以项目级（记录业务逻辑）。

```
claude mcp add memory --scope project -- npx -y @modelcontextprotocol/server-memory
```

## 4. Hooks是什么&怎么用

### 4.1 Hooks原理
> 大白话：在特定环节，100%执行你的命令，实现完全可靠的自动化。

相比写提示词，`Hooks`的优势体现在：

| 维度 | 提示词方式 | Hooks 方式 | 优势 |
|:---------|:---------------------|:---------------------|:---------|
| **执行可靠性** | AI可能遗忘/跳过 | 100% 确定性执行 | Hooks 是系统级拦截，不依赖 AI「记得」 |
| **行为一致性** | 每次可能不同（受上下文/温度影响） | 每次完全相同 | 配置即契约，消除随机性 |
| **自动化程度** | 需要 AI 主动识别并执行 | 事件触发，无感执行 | 文件保存/命令执行前自动拦截，零人工干预 |
| **团队协作成本** | 每人都要重复提醒 AI | 配置一次，全员生效 | `.claude/hooks/` 纳入版本库，团队自动同步 |

举个例子：`我希望 claude 每次写完代码都能自动格式化`

```
PostToolUse

Hook触发：Claude写完代码(file_path="src/app.js")

Hook执行：运行 prettier --write src/app.js
```

常见的Hook类型有：

| Hook 类型 | 触发时机 | 典型用途 | 
|:----------|:---------|:---------|
| **UserPromptSubmit** | 用户输入提交后 | 提示词优化、敏感词过滤 | 
| **PreToolUse** | 工具调用前 | 权限校验、参数验证 | 
| **PostToolUse** | 工具调用后 | 格式修复、自动测试 | 
| **Notification** | 通知发送时 | 日志记录、桌面通知 |
| **SessionStart** | 会话开始时 | 环境初始化 | 
| **SessionEnd** | 会话结束时 | 清理临时文件 |

### 4.2 Hooks使用

Hooks使用非常简单，在`~/.claude`目录下新建`hooks`文件夹，然后在`settings.json`配置文件中，填入对应字段即可：

![](https://i-blog.csdnimg.cn/img_convert/c63875e9a7c5a83832dd299f6a608293.png)


## 5. Skills是什么&怎么用

### 5.1 Skills原理
> 一句话：Anthropic推出的一套标准，让Al能够使用各种专业技能，无需重复输入提示词。

Skills 本质上是将最佳实践代码化和文件化。

将高频、复杂、关键的交互逻辑沉淀为 Skills，实现从人治到法治的转变。

![](https://i-blog.csdnimg.cn/img_convert/468e78f897748802304ebd58e4b0d139.png)

在`claude code`中，`skills`通常存在于两个位置：
- 全局skills：~/.claude/skills
- 项目skills：.claude/skills

### 5.2 Skill的文件结构
每个技能其实就是一个文件夹。

根据复杂程度，通常可包含：

```
- SKILL.md //技能说明文件
- scripts/ //可执行脚本
- assets/ //资源
- references/ //参考文档
```

我们以官方的`docx`技能为例：

![](https://i-blog.csdnimg.cn/img_convert/02344458db43fc1b69dc0db797f2d6eb.png)

`SKILL.md` 是每个技能的核心，它包含两个关键部分。
- **元数据**：YAML格式，在文件开头，`name` 是技能的名字，`description` 是技能的描述
- **指令内容**：就是精心设计的提示词，用于指导AI怎么做。


### 5.3 Skill安装的4种方式

**方式1：复制粘贴（最简单）**

对于简单的`skill`，把`skill`包放到`.claude/skills/`文件夹下即可。


**方式2：从技能市场安装**

在`claude code`中，技能市场是通过插件形式安装的。

比如，先安装claude官方技能市场：

```
/plugin marketplace add anthropics/skills
```

然后，安装指定skill：

```
/plugin
# 或者手动install
/plugin install document-skills@anthropic-agent-skills
```

安装完成，可在`setting.json`中看到：

```
"enabledPlugins": {
    "document-skills@anthropic-agent-skills": true
  }
```

重启后，上述技能即可被加载。


**方式3：Skill CLI安装**
> [https://skills.sh/](https://skills.sh/)

`Vercel` 出品的命令行工具，一行命令安装任意开源`skills`：

```
# 格式
npx skills add <owner/repo>
# 比如：安装 vercel 官方的所有skills
npx skills add vercel-labs/agent-skills
# 比如：安装指定的skill
npx skills add vercel-labs/agent-skills --skill frontend-design
# 如果访问github失败，也可下载到本地后安装
npx skills add ./agent-skills --skill frontend-design
```

安装成功后，会保存到`~/.agent/skills/`，然后建立软链接到`~/.claude/skills/`。

**方式4：其它**

还有更多开源skill项目，通常会有特定的安装方式。

比如，用于去AI味、提升`UI`审美的`UI/UX Pro Max`：

```
npm install -g uipro-cli
uipro init --ai claude # 会自动安装到项目的.claude/skills/
```
下面，推荐实践中常用的几个 Skill。

## 6. 如何让AI自我进化

### 6.1 Claudeception简介

> [https://github.com/blader/Claudeception](https://github.com/blader/Claudeception)

`Claudeception`是一个自动学习技能：

- 每次发送消息或会话结束，`ClaudeCode` 评估当前任务是否有可提取的经验
- 如果有（比如解决了隐藏的 bug、学会了特定项目模式），它会提取出新 skill，下次遇到类似问题时自动激活

以 SKILL.md 格式存储，位置在：
- 用户级：`~/.claude/skills/[skill-name]/SKILL.md`
- 项目级：`.claude/skills/[skill-name]/SKILL.md`

### 6.2 Claudeception使用

首先安装，直接下载后copy:

```
git clone https://github.com/blader/Claudeception.git ~/.claude/skills/claudeception
```

`Claudeception` 有三种触发方式：
- 自动触发 - 当检测到有价值的知识时自动激活
- 手动触发 - 输入 /claudeception 命令
- Hook 触发 - SessionEnd 时提醒你评估

**配置激活Hook**（可选）

配置Hook，可确保每次会话都判断是否有可提取的知识。

```
mkdir -p ~/.claude/hooks
cp ~/.claude/skills/claudeception/scripts/claudeception-activator.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/claudeception-activator.sh
```

然后，在 `~/.claude/settings.json` 里加上hook配置：

```
"hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/claudeception-activator.sh"
          }
        ]
      }
    ]
  }
```

**注意**："UserPromptSubmit" 会在每次发送消息都触发，会增加耗时和Token消耗。


## 7. 如何让AI拥有永久记忆
> [https://github.com/thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)

`Claude` 每次新会话都是全新开始。`Claude-Mem` 能够跨会话保留项目上下文、技术决策和调试经验。

核心亮点：
-  3层检索工作流，先索引后详情，节省 10 倍 Token
- 支持监控面板，`http://localhost:37777` 实时查看记忆流

安装方式如下：
```
/plugin marketplace add thedotmack/claude-mem
/plugin install claude-mem
# 会自动注册插件钩子
```

首次运行后，配置文件自动写入：

```
~/.claude-mem/settings.json
```


## 8. 如何提高AI的UI审美

除了claude官方的`front-design`，在笔者看来，目前去AI味最强：
- `UI/UX Pro Max`

安装方式如下：
```
npm install -g uipro-cli
uipro init --ai claude # 会自动安装到项目的.claude/skills/
```

## 9. 如何规范AI的开发流程

我们知道，一套完整的开发流程至少包括：
- 需求分析
- 架构设计
- 技术选型
- 开发测试

![](https://i-blog.csdnimg.cn/img_convert/98d89f13ae250837c7d17a85059f108b.png)

如果你想：拥有一套完整的`应用开发流程`，让AI像专业程序员一样工作?

那么，强烈推荐三个`规范驱动开发`的技能库：

- **偏向规范**：制定规范和管理变更
  - Spec-Kit
  - OpenSpec
- **偏向执行**：强制执行和审查流程
  - Superpowers
  
简单理解：

![](https://i-blog.csdnimg.cn/img_convert/21bb51c0c647c9ba38154ee96373b422.png)

怎么选？

![](https://i-blog.csdnimg.cn/img_convert/78f35f11284f4b2487ec131efa095ffd.png)

二者的工作流略有区别：

- `Spec-Kit`：分阶段严格流程（适合新项目）

- `OpenSpec`：轻量循环迭代（适合存量项目）

至于 `Superpowers`，非企业级/大型项目，可以先不考虑。


下面，分别介绍这三个工具，按需取用。

### 9.1 `Spec-Kit`
> [https://github.com/github/spec-kit](https://github.com/github/spec-kit)

安装：

```
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init . --ai claude  # 会自动初始化到当前项目
```

`claude code`中使用：
```
1. /speckit.constitution → 定义项目治理原则
2. /speckit.specify     → 创建功能规范（spec.md）
3. /speckit.clarify    → 需求澄清（可选）
4. /speckit.plan       → 技术方案设计（plan.md + contracts/）
5. /speckit.analyze    → 交叉一致性校验（可选）
6. /speckit.tasks      → 拆解实施任务（tasks.md）
7. /speckit.implement  → 执行编码 + 测试
```

### 9.2 `OpenSpec`
> [https://github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)

安装：

```
npm install -g @fission-ai/openspec@latest
openspec init # 会自动初始化到当前项目
```
初始化后，项目根目录会多出两个文件夹：

![](https://i-blog.csdnimg.cn/img_convert/fb45e9af25f6757c7d263ac1790e1bb9.png)

`claude code`中使用：

```
/opsx:propose "需求描述"
  ↓
├─ 生成 changes/xxx/
│  ├─ proposal.md（为什么做）
│  ├─ specs/（需求场景）
│  └─ tasks.md（实施清单）
  ↓
/opsx:apply "xx"
  ↓
├─ AI 执行 tasks.md
├─ 生成代码 + 测试
  ↓
/opsx:archive "xx"
  ↓
├─ 变更归档至 changes/archive/
├─ 知识沉淀至 specs/（单一真相源）

# 举个例子
# 1.生成规范
/opsx:propose "生成后端接口"
# 2.规范完成，开始写代码：AI会按照tasks.md中的任务列表逐一实现,并标记完成状态。
/openspec:apply add-python-fastapi-backend
# 3.代码写完，归档这次变更
/openspec:archive add-python-fastapi-backend
```

终端命令：

```
openspec list                        # 查看所有变更
openspec validate add-python-fastapi-backend    # 验证格式是否正确
openspec show add-python-fastapi-backend        # 查看详细内容
```

**举个例子：**

先提需求：

![](https://i-blog.csdnimg.cn/img_convert/0fa5e789cb04535804a198a3a7f20b29.png)

![](https://i-blog.csdnimg.cn/img_convert/313b238a085907b1c5d41f2045cc5fde.png)

再来讨论：

![](https://i-blog.csdnimg.cn/img_convert/ba9a8b630d28572a8667219da8516802.png)

开始执行：

![](https://i-blog.csdnimg.cn/img_convert/09d5e41420d9aa6c6486d5cb17fdf411.png)

代码有问题，缝缝补补，再来一轮：

![](https://i-blog.csdnimg.cn/img_convert/294ae212004c6345de5bb2a67ad16941.png)

什么时候该 `archive`？

![](https://i-blog.csdnimg.cn/img_convert/e9559d357b07ec0a95123be51108c042.png)



### 9.3 `Superpowers`
> [https://github.com/obra/superpowers](https://github.com/obra/superpowers)

安装：

```
# 先装市场
/plugin marketplace add obra/superpowers-marketplace
# 再从市场安装skill
/plugin install superpowers@superpowers-marketplace
```

`claude code`中使用：

```
/superpowers:brainstorm 通过和用户交互来不断改进设计
/superpowers:write-plan 创建实现方案
/superpowers:execute-plan 批量执行方案
```
### 9.4 实操建议
看到这里，你会发现，这些技能库功能有重叠啊！

所以，切忌无脑都装，易导致冲突。

**友情提醒：**
- **简单项目**：啥也别装，这些都要额外消耗大量Token，性价比不高
- **复杂项目**：先从 `OpenSpec` 开始（轻量），如果发现代码质量不稳定，再在编码环节引入 `Superpowers`。


## 写在最后

本文分享了`ClaudeCode 安装和使用`的完整指南。

Agent 元年，我们不得不面对一个现实：

你可以`不用动手写代码`，但一定要`想清楚做什么`。

希望本文能带你踏上`ClaudeCode`的体验之旅。

如果对你有帮助，不妨**点赞收藏**备用。
