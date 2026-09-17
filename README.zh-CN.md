<div align="center">

# Vibe Coding 狗屎检测器

### 你的 Vibe Coding 项目到底是工程，还是一坨狗屎？

**如果删除所有聊天记录，一个不了解背景的工程师还能理解、修改、验证、发布和恢复这个项目吗？**

[![CI](https://github.com/dulanjy/vibe-coding-shit-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/dulanjy/vibe-coding-shit-detector/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/dulanjy/vibe-coding-shit-detector)](https://github.com/dulanjy/vibe-coding-shit-detector/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) · [示例报告](examples/audit-report.sample.md) · [评分方法](references/scoring-model.md) · [更新记录](CHANGELOG.md)

</div>

---

> `v0.3.0` 起由 `software-engineering-health-audit` 更名。旧 GitHub 地址会自动跳转，但已安装的 Skill 应重新安装，并改用 `$vibe-coding-shit-detector` 调用。

**Vibe Coding 狗屎检测器**专门审计 AI 生成、快速拼接或持续打补丁形成的代码库。它会告诉你：这个项目是可维护的软件、尚可控制的 Vibe Slop，还是一坨无法接手的工程狗屎，并给出可复核的仓库证据。

名字很直接，审计不会乱骂。它不评价代码“看起来漂不漂亮”，而是检查项目的实际责任、生命周期和复杂度，是否有足够的工程约束支撑。

它将四类结论严格分开：

| 结论 | 回答的问题 |
|---|---|
| **Engineering Health** | 十项工程能力成熟到什么程度？ |
| **Vibe Slop Risk** | 项目责任与治理能力之间有多大错配？ |
| **Evidence Confidence** | 审计结论得到了多少可靠证据支持？ |
| **Production Readiness** | 当前发布责任是未评估、阻断、有条件还是就绪？ |

安全、数据、验证和恢复相关的 Critical Gate 可以覆盖平均分。

## 30 秒开始

使用 Agent Skills CLI 安装：

```bash
npx skills add dulanjy/vibe-coding-shit-detector \
  --skill vibe-coding-shit-detector -g -a codex -y
```

然后对 Agent 说：

```text
使用 $vibe-coding-shit-detector 判断当前 Vibe Coding 项目到底是可维护工程还是一坨狗屎。
生成 audit-report.md 和 audit-result.json，不要修改项目源代码。
```

也可以直接克隆：

```powershell
git clone https://github.com/dulanjy/vibe-coding-shit-detector.git `
  "$env:USERPROFILE\.codex\skills\vibe-coding-shit-detector"
```

## 它与普通代码质量评分的区别

| 常见误判 | 本 Skill 的处理方式 |
|---|---|
| 测试少，所以项目差 | 追踪关键业务不变量是否有可执行证据 |
| README 写了规则，所以规则成立 | 区分文档、代码约束和自动化强制 |
| 看不到部署配置，所以没有恢复能力 | 标记 `UNKNOWN` 并降低置信度 |
| 总分高，所以可以发布 | 最后应用 Critical Gate |
| `utils` 很大，所以架构差 | 只有证明责任混乱或有害耦合才形成 Finding |
| 原型缺少生产设施，所以扣分 | 先判断项目类型、阶段和关键性 |

## 两个核心实测

1. **Repository Amnesia Test**：仅保留仓库、Schema、基础设施和文档，新接手者能否完成理解、运行、验证、发布与恢复？
2. **Controlled Change Test**：只读推演一个普通变更，检查状态所有者、影响边界、未知依赖、验证与回滚路径。

默认输出：

- `audit-report.md`：适合人阅读；
- `audit-result.json`：符合内置 JSON Schema，适合自动处理。

可查看[虚构项目示例报告](examples/audit-report.sample.md)及其[机器可读结果](examples/audit-result.sample.json)。

## 只读安全边界

默认模式为 `AUDIT_ONLY`：

- 可以读取仓库、Git 历史、CI、配置、测试和文档；
- 不自动修复、重构、补依赖、改数据库、改基础设施、提交或发布；
- 不尝试使用发现的凭证，也不主动利用疑似授权绕过；
- 不在报告中暴露密钥内容；
- 不可访问的证据记为 `UNKNOWN`，不会偷换成失败。

修复应作为一个单独获得授权的任务执行。

## 可选只读工具

```bash
# 只读取路径与文件元数据，不读取文件内容
python scripts/repository_inventory.py /path/to/repository

# 汇总 Git 热点与共同变更候选，不读取提交说明或文件内容
python scripts/git_change_coupling.py /path/to/repository --max-commits 300
```

两项脚本都只依赖 Python 标准库。它们提供调查线索，不会自动生成 Finding。

## 当前边界

`0.2` 版是一套证据可追溯的审计框架，不是通用静态分析器，也不是经过认证的生产就绪标准。评分权重和阈值已显式化，但在用于组织级排名前，仍需使用不同类型的真实仓库和独立评审者进行校准。

## 参与改进

最有价值的反馈包括：误报、漏报、`UNKNOWN` 处理错误、相同证据得到不稳定评分，以及首要建议无法验收。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT](LICENSE)
