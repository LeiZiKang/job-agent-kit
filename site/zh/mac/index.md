# 在 Mac 上用起来是什么样｜job-agent-kit

网页：https://leizikang.github.io/job-agent-kit/zh/mac/

看看在 Mac 上使用 job-agent-kit 的一天：在 Claude Code 开工，子 Agent 分渠道搜岗，由你批准消息，用本地看板跟踪，再做每周复盘。所有窗口均为假数据演示。

> 对话为流程示意，公司与求职记录为虚构示例，不是实时账户活动。

## 1. 早晨：一句话开工。

```text
You › start the day
Read .agent-memory/handoff.md
$ python3 bin/jt.py status
```

Agent 读交接与跟踪器，提出三件优先事项：审阅 Fabrikam 的薪资回复、在准备面试前确认 Northwind 的雇佣关系、批准 Proseware 的申请草稿。真实会话需先刷新待办状态。随后手动检查一轮收件箱预览；打开未读聊天需批准。

## 2. 搜岗：三个渠道，一份候选清单。

主 Agent 给 LinkedIn、Indeed、公司 ATS 各分配一个只读 job-scout。每个子 Agent 返回 reports/scout/<date>-<channel>.json。主 Agent 复核完整职位描述，用 jt seen / jt company 查重后记录决定。子 Agent 不投递、不发消息。

使用 examples/tracker.json 候选的简化 JSON 示意：

```json
{"channel":"linkedin","source":"scout","shortlist":[{"company":"Alpine Ski House","role":"Senior React Engineer","verdict":"recommend"}]}
```

## 3. 由你批准：对象与原文。

T2 · 首次回复主动联系的招聘者。收件人：Example Co. 招聘团队，通过邮件。

> Example Co. 招聘团队，你们好。感谢联系我介绍前端工程师岗位。方便分享一下公司或客户、团队规模和工作安排吗？如果合适，我很乐意提供简历。

```text
Claude › 把这段原文发给这位收件人吗？
You › yes, send it
```

这是使用占位公司的模板示意，不包含个人经历声明。批准仅针对该对象与原文，核实送达后才能汇报已发送。也可在 outreach.md 中预先批准具体动作类型。

## 4. 跟踪：本地看板。

HTML 页面参照 python3 bin/jt.py demo 绘制了可滚动的 board.html 节选，包括待决策事项、指标、推荐、待确定候选及申请记录。数据全部来自 examples/tracker.json。

| 指标 | 示例数量 |
| --- | ---: |
| 申请记录（含草稿） | 8 |
| 等待回复 | 4 |
| 面试中状态 | 1 |
| 推荐 | 2 |
| 待确定 | 2 |
| 进行中 / 总记录 | 6 / 8 |

| Company | Role | Status |
| --- | --- | --- |
| Northwind | Senior Frontend Engineer | interviewing |
| Proseware | Senior Software Engineer | preparing |
| Litware | UI Engineer | submitted |
| Adatum | Staff Engineer | submitted |
| Fabrikam | Full-stack Engineer | submitted |
| Contoso Mobile | iOS Engineer | submitted |
| Tailspin Toys | Web Platform Engineer | rejected |
| Wingtip | Frontend Engineer | ghosted |

推荐：Alpine Ski House（Senior React Engineer）、Coho Winery（Frontend Lead）。待确定：Woodgrove、Lucerne。跟踪器命令只记账，不会投递或发消息。

## 5. 周五复盘：根据证据调整。

```text
$ python3 bin/jt.py funnel --by source
Source            Applied  Replied  Reply rate  Interviews  Rejected
(unrecorded)            8        0          0%           0         1
Total                   8        0          0%           0         1
```

演示数据：根据 examples/tracker.json 实际计算的输出。8 条记录含一条草稿。回复与面试为零表示里程碑字段未记录，不代表从未发生。source 是机会来源，platform 是投递平台。

1. 先补已知来源。8 条记录的来源都未填写，现在还不能给渠道排优先级。
2. 按证据补齐里程碑。Northwind 状态为面试中，但未记录面试日期；这里的零不代表没有面试。
3. 调整搜岗精力前，用 --since 比较观察时间相近的批次，再看 --by platform。下周五复查；本示例样本小且记录不全。

## 6. 保持更新。

```text
$ bin/update-check.sh
通知示意：发现新版本，尚未安装。
Claude › install it?
```

这不是实时版本检查。开会话时最多每周检查一次更新；Agent 解释变更，在你同意后才安装。个人规则保留在 CLAUDE.local.md。

## 快速开始

```sh
git clone https://github.com/LeiZiKang/job-agent-kit
cd job-agent-kit
claude
# then say: set me up
```

Agent 会访谈你并生成本地文件，无需手动编辑配置。跟踪器需要 Python 3.9+，工作流需要 Claude Code 或遵循 AGENTS.md 的 Agent。Codex 读取相同规则。

[GitHub](https://github.com/LeiZiKang/job-agent-kit) · [首页](https://leizikang.github.io/job-agent-kit/zh/) · [English](https://leizikang.github.io/job-agent-kit/mac/)
