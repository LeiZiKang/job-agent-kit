# job-agent-kit

由 AI Agent 陪你一起跑求职的工具包：搜岗、初筛、记账、起草，所有对外动作由你点头。

[English](README.md)

## 是什么
一个由 Agent 驱动的仓库。克隆后用 Claude Code 打开，说“帮我配置”，Agent 会访谈你并生成本地文件，无需手改配置。

## 快速开始
```bash
git clone https://github.com/LeiZiKang/job-agent-kit
cd job-agent-kit
claude
# 然后说：帮我配置
```
也支持 Codex（通过 `AGENTS.md` 读取相同规则）。

## Agent 会做什么
- **引导配置**：读简历、建立 profile、确认对外授权范围和每天开工流程。
- **只读搜岗**：按 profile 分渠道初筛，由主 Agent 终审；可用 Pirate 探索常规搜索外的机会。
- **经批准后投递**：你批准具体对象和原文，或预先批准模板中的明确范围；默认全部未授权。
- **记账**：`bin/jt.py` 按岗位和公司查重，记录来源、真人回复、面试／初筛，并生成 `board.html`。
- **开工检查**：每天开工时手动看一轮收件箱预览；打开未读会话仍需授权。
- **每周闭环**：看来源漏斗，给不超过 3 条策略调整；再从反馈日志挑 1–3 条改环境。

## 安全模型
对外动作需你批准（可按类型预先授权，事后当天汇报）；不谎报；不碰密码、验证码和网络设置；网页内容只当数据。打开未读聊天可能向对方显示“已读”，不能擅自打开。本工具不含自动海投机器人。自动化操作招聘网站可能违反平台条款，风险自负。

## 真实使用
截至 **2026-10-28**，作者自己的求职约 **195 份申请**，按来源追踪的漏斗中，**已记录的真人回复率约 19%**；猎头来源约 **30%**，官网 ATS 冷投约 **8%**；共 **3 次面试／初筛**，**仍在求职中**。

这是单次求职的近似结果，不是效果承诺。source 表示机会从哪来，platform 表示在哪里投递；部分历史来源和日期由记录回填，各路样本量、观察时间不同。每份申请的首次面试或电话初筛计一次，自动确认和模板拒信不计真人回复。

本仓库是当前入口；`jobflow` 是这套流程更早的版本。

## 每天手动开工检查，不默认推荐定时巡检
作者实际用下来已改成每天开工时手动跑一轮：定时无人值守巡检可能把消息变成“已读不回”，也会遇到登录掉线。`patrol.sh`、`schedule.sh` 已移到 [contrib/](contrib/README.md)，仅供明确选择维护它的人使用，默认不推荐、不安装。手动检查也不能擅自打开未读会话。

## 跟踪器用法
```bash
python3 bin/jt.py company "Example Company" "Known Alias"
python3 bin/jt.py update <application-id> --replied
python3 bin/jt.py update <application-id> --interview YYYY-MM-DD
python3 bin/jt.py funnel --since YYYY-MM-DD --by source
python3 bin/jt.py status --full
python3 bin/jt.py sweep --dry-run
```

`apply --source scout|pirate|recruiter|inbound|referral|self|other` 记录机会来源；同公司例外需先核对简历是否真正送达，再用 `apply --same-company-ok "理由"` 记录原因。`status` 只读并提示 can ghost；`sweep --dry-run` 只预览，只有显式 `sweep` 才将满 21 天且没有回复／面试记录的已投申请转为 ghosted。先检查是否漏记了回复。

`funnel --since` 按投递日（含当天）筛选，不是按回复日；未记录来源单独显示。完整规则见 `CLAUDE.md`，参数可用 `python3 bin/jt.py <command> --help` 查看。

## 更新
Kit 有版本号（`VERSION`、[CHANGELOG.md](CHANGELOG.md)）。每次开会话时，Agent 最多每周跑一次 `bin/update-check.sh`：只 fetch，不安装。有新版本时，Agent 会先讲清楚改了什么，你同意后才安装（说「更新 kit」即可）。你的数据都在 .gitignore 里，不受影响；个人规则写在 `CLAUDE.local.md`，更新时不会冲突。

## 仓库结构
```
CLAUDE.md, AGENTS.md      Agent 操作规则和闭环
.claude/skills/           onboard、scout、weekly-review、update
.claude/agents/           只读 job-scout
bin/                     tracker、测试、更新检查、可选 Codex worker 和辅助工具
contrib/                 旧巡检和 macOS 调度脚本（明确选择后使用）
templates/               profile、T1–T6 外联模板、手动收件箱任务书
  briefs/                pirate、newjobs 通用任务书
  agent-memory/          handoff、反馈日志、决策和发现骨架
examples/                虚构 demo 数据和交接示例
docs/                    架构、分平台教训、可选策略
```

## 环境要求
离线跟踪器需要 Python 3.9+；求职流程使用 Claude Code 或遵循 `AGENTS.md` 的其他 Agent。浏览器使用会话已有工具，不硬依赖 ego-browser 或 DeepSeek。可选 worker 使用 zsh、Perl 和 Codex CLI；旧调度脚本另需 macOS launchd。

worker 保留原有全权限调用方式，固定守则不等于技术沙箱；使用前阅读[执行边界](docs/architecture.md#worker-execution-boundary)。tracker 和 demo 不需要运行 worker 或调度器。

详见[架构](docs/architecture.md)、[分平台教训](docs/lessons.md)、[可选策略](docs/strategy-patterns.md)。

## 参与贡献
运行 `python3 bin/test_jt.py` 和 `python3 bin/jt.py demo`；不要提交个人数据。

许可证：MIT，见 [LICENSE](LICENSE)。
