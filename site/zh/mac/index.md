# 在桌面应用中求职的一天｜job-agent-kit

网页：https://leizikang.github.io/job-agent-kit/zh/mac/

在 Mac 的桌面应用界面中看看 job-agent-kit 的一天：对话开工、只读搜岗、批准消息、预览本地看板与每周复盘。虚构数据的界面示意，不是截图。

> 桌面应用界面示意，不是截图。应用更新后界面可能不同。对话、公司、会话名与求职记录均为虚构示例，不是实时账户活动。

六个场景共用固定深色的四栏应用窗口：项目与会话侧栏、看板或 JSON 预览、对话与决策卡、任务与环境信息栏。窄屏依次隐藏右信息栏和预览；手机只显示顶栏与对话，跟踪场景只显示看板。按钮均为静态示意。看板与漏斗标注演示数据。

## 1. 早晨：一句话开工。

```text
你 › 开始今天的工作
读取 .agent-memory/handoff.md
运行 jt status → python3 bin/jt.py status
```

智能体读交接与跟踪器，提出三件优先事项：审阅 Fabrikam 的薪资回复、在准备面试前确认 Northwind 的雇佣关系、批准 Proseware 的申请草稿。真实会话需先刷新待办状态。随后手动检查一轮收件箱预览；打开未读聊天需批准。

## 2. 搜岗：三个渠道，一份候选清单。

主智能体给 LinkedIn、Indeed、公司招聘系统各分配一个只读 job-scout。每个子智能体返回 reports/scout/<date>-<channel>.json。主智能体复核完整职位描述，用 jt seen / jt company 查重后记录决定。子智能体不投递、不发消息。

使用 examples/tracker.json 候选的简化 JSON 示意：

```json
{"channel":"linkedin","source":"scout","shortlist":[{"company":"Alpine Ski House","role":"高级 React 工程师","verdict":"recommend"}]}
```

## 3. 由你批准：对象与原文。

T2 · 首次回复主动联系的招聘者。收件人：Example Co. 招聘团队，通过邮件。

> Example Co. 招聘团队，你们好。感谢联系我介绍前端工程师岗位。方便分享一下公司或客户、团队规模和工作安排吗？如果合适，我很乐意提供简历。

```text
决策卡 › 把这段原文发给这位收件人吗？
主按钮 › 可以，发送（示意，尚未点击）
```

这是使用占位公司的模板示意，不包含个人经历声明。批准仅针对该对象与原文，核实送达后才能汇报已发送。也可在 outreach.md 中预先批准具体动作类型。

## 4. 跟踪：本地看板。

HTML 页面在加宽的预览面板中展示可滚动看板：统计卡、接下来、转化漏斗、推荐、待确定候选及全部申请记录。数据全部来自 examples/tracker.json。

| 指标 | 示例数量 |
| --- | ---: |
| 申请记录（含草稿） | 8 |
| 已记录回复 | 3 |
| 已记录面试 | 1 |
| 等待回复 | 2 |
| 面试中状态 | 1 |
| 推荐 | 2 |
| 待确定 | 2 |
| 进行中 / 总记录 | 6 / 8 |

| 公司 | 岗位 | 状态 |
| --- | --- | --- |
| Northwind | 高级前端工程师 | 面试中 |
| Proseware | 高级软件工程师 | 草稿准备中 |
| Litware | 界面工程师 | 已投递 |
| Adatum | 资深工程师 | 已投递 |
| Fabrikam | 全栈工程师 | 已投递 |
| Contoso Mobile | iOS 工程师 | 已投递 |
| Tailspin Toys | 网页平台工程师 | 已拒绝 |
| Wingtip | 前端工程师 | 无回复归档 |

推荐：Alpine Ski House（高级 React 工程师）、Coho Winery（前端负责人）。待确定：Woodgrove、Lucerne。跟踪器命令只记账，不会投递或发消息。

## 5. 周五复盘：根据证据调整。

```text
python3 bin/jt.py funnel --by source
来源              记录  回复  回复率  面试  拒绝
搜岗  4  0  0%  0  1
招聘者  2  2  100%  1  0
内推  1  1  100%  0  0
自投  1  0  0%  0  0
合计  8  3  38%  1  1
```

演示数据，非效果宣称；样本很小。8 条记录含 1 条草稿，3 条回复、1 条面试。回复率 37.5%（命令行取整为 38%），面试占记录 12.5%，回复到面试为 33.3%。来源与投递平台不同。

1. 继续跟进招聘者来源。2 条已投递记录均有回复，1 条进入面试；样本仅 2 条。
2. 复核搜岗匹配度与草稿。4 条搜岗记录含 1 条未投递草稿，已记录回复为 0；先审阅草稿和岗位匹配度。
3. 比较观察时间相近的批次。用 --since 和 --by platform 复核；内推 1 条有回复、自投 1 条无回复，下周五再评估。

## 6. 保持更新。

```text
运行 update-check.sh → bin/update-check.sh
通知示意：发现新版本，尚未安装。
决策卡 › 安装 v0.x 吗？（占位版本，非实时发布）
```

这不是实时版本检查。开会话时最多每周检查一次更新；智能体解释变更，在你同意后才安装。个人规则保留在 CLAUDE.local.md。

## 快速开始

先安装 [Claude 桌面应用](https://claude.ai/download)，打开 Code 标签页；也可以使用 Claude Code。把下面这句话贴给智能体：

> 帮我安装 job-agent-kit：把 https://github.com/LeiZiKang/job-agent-kit 下载到本地，读里面的 INSTALL.md，然后一步步帮我配置。

智能体会读 INSTALL.md 并一步步引导你配置，默认下载到 `~/job-agent-kit`。需要安装 Git 或 Python 3.9+ 时会先征得你同意。

[开发者手动安装](https://github.com/LeiZiKang/job-agent-kit/blob/main/README.zh-CN.md#开发者手动安装)

智能体会访谈你并生成本地文件，无需手动编辑配置。跟踪器需要 Python 3.9+，工作流需要 Claude Code 或遵循 AGENTS.md 的智能体。Codex 读取相同规则。

[GitHub](https://github.com/LeiZiKang/job-agent-kit) · [首页](https://leizikang.github.io/job-agent-kit/zh/) · [英文](https://leizikang.github.io/job-agent-kit/mac/)
