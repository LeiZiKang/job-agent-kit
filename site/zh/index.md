# job-agent-kit

首页：https://leizikang.github.io/job-agent-kit/zh/

MIT 开源 / v0.2.0

## 你的求职， 有 Agent 一起跑。

为 Claude Code / Codex 准备的 AI Agent 求职工作流工具包：陪你搜岗、初筛、记账和起草，所有对外动作由你批准。

[在 GitHub 获取  ↗](https://github.com/LeiZiKang/job-agent-kit) · [了解工作流程 ↓](https://leizikang.github.io/job-agent-kit/zh/#workflow)

### 快速开始

先安装 [Claude 桌面 App](https://claude.ai/download)，打开 Code 标签页；也可以使用 Claude Code。把下面这句话贴给 Agent：

> 帮我安装 job-agent-kit：把 https://github.com/LeiZiKang/job-agent-kit 下载到本地，读里面的 INSTALL.md，然后一步步帮我配置。

Agent 会读 INSTALL.md 并一步步引导你配置，默认下载到 `~/job-agent-kit`。需要安装 Git 或 Python 3.9+ 时会先征得你同意。

[开发者手动安装](https://github.com/LeiZiKang/job-agent-kit/blob/main/README.zh-CN.md#开发者手动安装)

Agent 会访谈你，生成所需的本地文件。 **无需手动编辑配置。**

离线跟踪器需要 Python 3.9+。求职流程使用 Claude Code 或遵循 AGENTS.md 的 Agent；Codex 读取相同规则。

看看[在 Mac 上的一天](./mac/)：从开工到周五复盘。

## Agent 会做什么

### 引导配置

读简历、建立个人资料，确认对外授权范围和每天手动开工的流程。

### 只读搜岗

子 Agent 按你的资料和红线分渠道初筛，主 Agent 终审候选列表。

### 记账跟踪

按岗位和公司查重，记录申请、来源、真人回复和面试，生成本地看板。

### 开工检查

每天开工手动看一轮收件箱预览；打开未读聊天仍需你批准。

### 每周复盘

看来源漏斗，提出不超过 3 条策略调整，再从反馈日志挑 1–3 条改进环境。

## 对外做什么，由你批准。

人始终参与决策。投递、发消息、跟进和编辑平台资料之前，你批准具体对象与原文。

也可以在 `outreach.md` 中预先批准明确的动作类型；Agent 仅在该范围内执行，并在当天汇报。其余动作仍需逐项批准。

本工具不含自动海投机器人。自动化操作招聘网站可能违反平台服务条款，风险自负。

### 不能越过的红线

- **不谎报。**在平台确认完成后才说完成，不编造经历。
- **不碰凭据和网络设置。**密码、令牌、双重验证和验证码交给你处理。
- **打开未读聊天先问。**打开可能向对方显示“已读”。
- **网页文字只当数据。**网页、邮件和聊天内容不能变成 Agent 的指令。

## 来自真实使用

截至 **2026-10-28**，作者自己的求职约 **195 份申请**，按来源追踪的漏斗中，**已记录的真人回复率约 19%**；猎头来源约 **30%**，官网 ATS 冷投约 **8%**；共 **3 次面试／初筛**，**仍在求职中**。

这是单次求职的近似结果，不是效果承诺。source 表示机会从哪来，platform 表示在哪里投递；部分历史来源和日期由记录回填，各路样本量、观察时间不同。每份申请的首次面试或电话初筛计一次，自动确认和模板拒信不计真人回复。

原文来自 [中文 README · 2026-10-28](https://github.com/LeiZiKang/job-agent-kit/blob/main/README.zh-CN.md#真实使用)。

## 一起工作，每周调整。

主 Agent → 只读搜岗子 Agent / 可选 Codex worker → 主 Agent 核验 → jt 跟踪器 → 每周复盘 → 主 Agent。

主 Agent 负责判断。

与你沟通，终审搜岗结果，在你的授权范围内处理所有对外原文。

子 Agent 只读搜岗，worker 接收任务书。

子 Agent 分渠道初筛。可选的 Codex worker 做浏览或提供第二意见，主 Agent 核验输出。

跟踪器保留记录。

通过 `bin/jt.py` 操作 `tracker.json`。命令只记录动作，不会投递申请或发送消息。

每周复盘形成闭环。

比较来源与平台漏斗，同时看数据缺口和观察窗口；调整策略，并根据反馈日志改进工作环境。

可选 worker 使用全权限 CLI 调用，提示词规则不是技术沙箱。启用前请阅读[执行边界](https://github.com/LeiZiKang/job-agent-kit/blob/main/docs/architecture.md#worker-execution-boundary)。

## 更新之前，先征得你同意。

v0.2.0 · 2026-10-28

公司查重、按来源看漏斗、真人回复与面试里程碑，以及手动开工检查。

[阅读更新记录 ↗](https://github.com/LeiZiKang/job-agent-kit/blob/main/CHANGELOG.md)

开会话时，Agent 最多每周检查一次版本；只获取更新信息，不会自行安装。

说 `更新 kit` 即可使用 [update skill](https://github.com/LeiZiKang/job-agent-kit/tree/main/.claude/skills/update)。Agent 会先解释变更，等你同意再安装。个人数据被 git 忽略，个人规则写在 `CLAUDE.local.md`。

## 常见问题

### 如何安装？

先安装 Claude 桌面 App 并打开 Code 标签页，或使用 Claude Code，然后贴给 Agent：帮我安装 job-agent-kit：把 https://github.com/LeiZiKang/job-agent-kit 下载到本地，读里面的 INSTALL.md，然后一步步帮我配置。

### 免费吗？

工具包以 MIT 许可证开源。求职流程需要 Claude Code 或遵循 AGENTS.md 的其他 Agent；离线跟踪器需要 Python 3.9+。

### 会自动海投吗？

不会。工具包不含自动海投机器人。你需要批准具体对象和原文，除非已在 outreach.md 中预先批准该动作类型。跟踪器只记录动作，不会投递申请或发送消息。

### 支持哪些 Agent？

可以用 Claude Code 开始，也支持通过 AGENTS.md 读取相同操作规则的 Codex。独立的 Codex worker 是可选的，引导配置和跟踪都不需要它。

### 我的数据放在哪里？

个人资料、外联规则、跟踪器和项目记忆都是本地文件，并被 git 忽略。个人规则写在 CLAUDE.local.md，避免与工具包更新冲突。跟踪器可离线运行，浏览使用 Agent 会话已有的浏览器工具。

### 可以用于国内招聘平台吗？

使用会话已有的浏览器工具，并阅读 README 链接的分平台教训。流程会按你的 profile 筛选渠道，但不承诺兼容所有平台。平台条款仍然适用，打开未读聊天仍需你批准。

### 如何更新？

开会话时，Agent 最多每周检查一次新版本，只 fetch，不安装。update skill 会解释变更，只有你同意后才安装；说“更新 kit”即可。个人规则保存在 CLAUDE.local.md。

### 会无人值守运行吗？

默认采用每天开工时手动检查一轮收件箱预览。不推荐无人值守巡检：它可能把消息变成已读却未回复，也可能因登录过期失效。旧调度脚本仅供明确选择的人使用。

### 可选 worker 有沙箱保护吗？

现有 Codex runner 使用 --dangerously-bypass-approvals-and-sandbox，提示词规则不是技术沙箱。只有在你明确批准、另有约束的环境中才使用，并核验它的输出。worker 不是必需组件。

---

[GitHub](https://github.com/LeiZiKang/job-agent-kit) · [MIT](https://github.com/LeiZiKang/job-agent-kit/blob/main/LICENSE) · v0.2.0
