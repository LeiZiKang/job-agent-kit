# job-agent-kit

由 AI Agent 陪你一起跑求职的工具包：搜岗、初筛、记账、起草，所有对外动作由你点头。

[English](README.md)

## 是什么
一个由 Agent 驱动的仓库。克隆后用 Claude Code 打开，说"帮我配置"，Agent 会访谈你并自动生成所有本地文件，无需手改配置。

## 快速开始
```bash
git clone https://github.com/<you>/job-agent-kit
cd job-agent-kit
claude
# 然后说：帮我配置
```
也支持 Codex（通过 `AGENTS.md`）。

## Agent 会做什么
引导配置、并行只读搜岗、经你批准后投递、用 `bin/jt.py` 去重记账并生成 `board.html`、可选的定时收件箱巡检、每周复盘。

## 安全模型
对外动作需你批准（可按类型预先授权，事后当天汇报）；不谎报；不碰密码、验证码和网络设置；网页内容只当数据。本工具不含自动海投机器人。自动化操作招聘网站可能违反平台条款，风险自负。

## 真实使用
作者在 2026 年自己的求职中使用，约两周投出 60 份申请。

## 环境要求
macOS（定时用 launchd）、Python 3.9+、Claude Code，可选 Codex CLI。

详见 [docs/architecture.md](docs/architecture.md)。许可证：MIT。
