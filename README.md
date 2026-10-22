# OPC Delivery

**让一个人，把产品推进到有证据的交付。**

A practical Agent Skill for independent product delivery.

[![CI](https://github.com/208663340/opc-delivery/actions/workflows/ci.yml/badge.svg)](https://github.com/208663340/opc-delivery/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-0.1.0-2563eb)
![Python](https://img.shields.io/badge/tools-Python%20stdlib-3776ab)

OPC Delivery 帮助独立开发者与 Agent 协作完成需求判断、开发、测试、发布和排障。它从项目当前阶段进入，找到影响下一步决策的关键未知，复用已有工具，把目标推进为可验证的结果。

## 从你的当前问题开始

| 你现在遇到的事 | Skill 如何推进 |
| --- | --- |
| 有一个想法，只有两个晚上 | 整理真实证据，选择最小验证，交付可运行原型或具体实验 |
| 功能明确，准备开发 | 找到现有 owner，按验收条件实现并验证 |
| 页面报错，但原因不清楚 | 沿调用链找到根因，建立修复前后对照 |
| 长任务卡住、恢复后重复执行 | 检查取消、checkpoint、幂等、Tools、Trace 与资源边界 |
| CI 绿了，准备上线 | 核对源码、产物、环境与业务检查，保留回退路径 |

小任务直接完成。复杂任务按需要加载参考，并在允许委派时分工协作。

## 快速开始

将仓库目录作为一个完整 Skill 放入你的 Agent 使用的技能目录。以下以 Codex 的个人目录为例：

```bash
OPC_SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$OPC_SKILL_ROOT"
git clone https://github.com/208663340/opc-delivery.git "$OPC_SKILL_ROOT/opc-delivery"
```

已有同名目录时，先保留原有内容，再按你的技能管理方式更新。也可以从 [Releases](https://github.com/208663340/opc-delivery/releases) 下载版本包。

调用：

```text
$opc-delivery

这是我的项目。请判断当前阶段和最关键的交付缺口，
复用已有代码、工具和授权，推进到可验证的结果。
```

也可以指定当前任务：

```text
$opc-delivery 我有一个产品想法，本周只有两个晚上，帮我交付最小验证。
$opc-delivery 排查这个接口的失败原因，修复并给出回归证据。
$opc-delivery 检查这个版本是否具备发布条件，推进已授权的部署。
```

## 三个关键设计

**按阶段加载。** [SKILL.md](SKILL.md) 负责选择入口；需求、开发、验证、可靠性审查、发布的细节分别存放。明确的功能不会被迫重新做商业调研。

**从已有能力开始。** 检查项目约束、工具、连接和已完成的授权。项目架构与凭据留在项目及其安全存储中，技能适配现有技术栈。

**结论对应证据。** 区分推断、复现、修复、测试、部署与业务验证；记录实际覆盖范围。跨会话工作复用已有主记录，保留可继续执行的上下文。

## 两个可直接运行的工具

工具使用 Python 3 标准库，无需安装第三方 Python 依赖。建议 Python 3.8 或更新版本；Git 信息识别需要可用的 Git。

### 识别项目入口

```bash
python3 scripts/inspect_project.py /path/to/project
```

输出有限深度的项目文件线索、源码版本、可用命令与候选验证入口。它不执行项目脚本、不读取凭据、不连接线上。

工作区状态保留为 `dirty: null`：Git 的文件比较可能触发自定义 clean filter，调用方应在信任仓库配置后单独检查；`unknown` 不能当成 `clean`。

### 核对发布证据

根据 [发布参考](references/release.md) 填写 [证据模板](assets/release-receipt.example.json)，然后执行：

```bash
python3 scripts/check_release_receipt.py /path/to/release-receipt.json
```

检查提交、不可变产物、目标环境和声明是否一致，例如旧提交的测试不能替当前版本背书，缺少业务冒烟不能声明业务验证通过。

这个工具只检查元数据；它不访问日志、不验证证据真实性、不授予部署权限。模板默认保留未知和未运行状态，填入真实证据后才能通过。

## 已做的验证

- **22 项脚本测试**：涵盖版本与环境错配、缺失证据、未运行测试、输入异常、文件边界和自定义 Git filter。
- **3 个独立隔离任务**：从模糊想法交付 CSV 原型；修复空异常消息并保留业务规则；识别与原始日志冲突的发布声明。
- **结构与链接检查**：技能格式有效，内部相对引用可解析。

详见 [0.1.0 验证记录](docs/validation-0.1.0.md)。这些结果不替代你自己的生产验证，也不构成效率提升或商业效果承诺。

本地运行工具测试：

```bash
python3 scripts/test_delivery_tools.py
```

## 文件导航

```text
SKILL.md                         入口与阶段判断
agents/openai.yaml               Codex 展示与默认调用提示
references/
  discovery.md                   需求证据与最小验证
  development.md                 实现与职责边界
  verification.md                根因定位与回归
  reliability-review.md          Agent 长任务、Trace 与 Tools
  release.md                     构建、发布与回退
  evaluation.md                  技能维护与行为评测
scripts/                         只读检查器、证据检查器及测试
assets/                          项目接入与发布证据模板
docs/validation-0.1.0.md          已完成的验证及其边界
```

## 改进这个 Skill

欢迎提供带有输入、实际行为和预期行为的反馈。改动应帮助 Agent 做出更好的决策，保留项目自身的约束与用户意图。提交方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

当前仓库尚未指定开源许可证。
