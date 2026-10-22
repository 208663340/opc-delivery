# OPC Delivery

**让一个人，把产品推进到有证据的交付。**

A practical Agent Skill for independent product delivery.

[![CI](https://github.com/208663340/opc-delivery/actions/workflows/ci.yml/badge.svg)](https://github.com/208663340/opc-delivery/actions/workflows/ci.yml)
![Version](https://img.shields.io/badge/version-0.3.0-2563eb)
![Node](https://img.shields.io/badge/installer-Node.js%20%E2%89%A520-339933)
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

### 用 npm 安装

需要 Node.js 20 或更新版本。当前可以从 GitHub 安装 CLI，然后安装技能包：

```bash
npm install -g github:208663340/opc-delivery
opc-delivery install
```

默认将主 Skill 和全部 30 项配套能力放入 `${CODEX_HOME:-~/.codex}/skills/opc-delivery`。需要其他 Agent 的技能目录或项目内安装时，使用 `--dir` 指定技能根目录：

```bash
opc-delivery install --dir .agents/skills
opc-delivery install --dir .agents/skills --dry-run
opc-delivery list
```

目录已存在时默认退出并保留内容。确认要更新时运行 `opc-delivery install --force`；旧目录会完整保存在同一技能根目录下的 `.opc-delivery-backup-*`，成功后输出备份位置。`--dry-run` 不写入任何文件。

npm 的包安装阶段只安装 CLI；写入技能目录由显式的 `opc-delivery install` 执行。包内没有第三方 Node 依赖，也不在安装阶段执行 Python 工具。

本版本发布到 npm registry 后，还可使用：

```bash
npx opc-delivery install
# 或全局安装 CLI 后使用：
npm install -g opc-delivery
opc-delivery install
```

发布前可从源码生成并安装本地 tarball：

```bash
npm pack
npm install -g ./opc-delivery-0.3.0.tgz
opc-delivery install --dry-run
```

### 直接复制 Skill

也可以将仓库目录作为一个完整 Skill 放入你的 Agent 使用的技能目录。以下以 Codex 的个人目录为例：

```bash
OPC_SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$OPC_SKILL_ROOT"
git clone https://github.com/208663340/opc-delivery.git "$OPC_SKILL_ROOT/opc-delivery"
```

已有同名目录时，先保留原有内容，再按你的技能管理方式更新。也可以从 [Releases](https://github.com/208663340/opc-delivery/releases) 下载版本包。

仓库中已附带 30 项配套 Skill：27 项从本机技能库收录，保留各自的规则、参考和已有许可文件；另有 3 项本项目编写的用户研究、原型验证与部署运维技能及其模板。完整克隆本仓库即可一起取得，OPC Delivery 会沿推荐表的本地路径按需读取。它们不需要为了被读取而再次联网下载；部分专业任务所需的浏览器、外部文档或框架依赖仍按实际环境使用。

这些内置目录由 OPC Delivery 按路径路由，各 Agent 对嵌套 Skill 的发现方式可能不同。需要单独安装某项时，可将 `skills/<名称>/` 完整放入所用 Agent 的技能目录，先保留已有同名内容。

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

## 按当前问题补充专业 Skill

内置 [专业 Skill 推荐](references/skill-recommendations.md)，覆盖 UI/UX 设计、前端开发、后端开发、Agent 开发、产品设计与分析、Bug 修复和工程基础。21 项主要推荐和 9 项 Agent / Python 配套能力均已收录到 `skills/`，表中技能名称直接打开本地 `SKILL.md`，并保留上游来源、选择时机与应交回的验证证据。

例如，视觉改版可参考 `frontend-design`，React 请求瀑布可参考 `vercel-react-best-practices`，根因未知时可参考 `systematic-debugging`。Agent 专题按项目实际框架选择；自研循环先走现有可靠性审查。完整名单与来源以推荐参考为准。

新增三项可直接使用的专业能力：

| Skill | 适用问题与配套材料 |
| --- | --- |
| [user-research](skills/user-research/SKILL.md) | 用户分群、访谈与需求证据；附研究简报、中性提纲方法与证据记录模板 |
| [prototype-validation](skills/prototype-validation/SKILL.md) | 原型范围、任务测试与迭代；附主持方法、观察表、结果计数与复测模板 |
| [deployment-operations](skills/deployment-operations/SKILL.md) | 发布、监控值守与恢复；附兼容性检查、告警与发布/恢复/交接手册 |

先读取选中项的实际说明，再按需加载其规则和参考；专业结果回到当前任务的验收与证据记录。目录、来源、文件校验值及打包调整见 [技能来源与文件清单](skills/manifest.json)。

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
- **专业 Skill 推荐增量验证**：核对 18 项候选的源文件；完成一次旧版检索对照与两个更新后的隔离任务，详见 [推荐能力验证记录](docs/validation-skill-recommendations.md)。
- **本地 Skill 收录验证**：27 项、140 个原有文件；核对入口、目录完整性与 SHA-256，验证内部链接可解析。仅修正一份生成文档中的三处相对链接，详见同一验证记录。
- **0.2.0 npm 安装器验证**：Node 20 / 26 的 11 项测试通过，覆盖预览、备份更新、路径及安装边界；实际 `npm pack` 后离线安装 tarball 并执行 CLI，详见 [0.2.0 npm 验证记录](docs/validation-npm-0.2.0.md)。

- **0.3.0 三项专业能力验证**：同输入的旧版检索对照与三项新版独立案例通过；30 项、150 个技能文件哈希一致，Node 20 / 26 的 12 项安装测试、22 项 Python 测试与 npm 发布预演通过，详见 [专业能力验证记录](docs/validation-specialists-0.3.0.md)。未执行真实用户研究或生产运维。

详见 [0.1.0 验证记录](docs/validation-0.1.0.md)。这些结果不替代你自己的生产验证，也不构成效率提升或商业效果承诺。

本地运行工具测试：

```bash
python3 scripts/test_delivery_tools.py
npm test
```

## 文件导航

```text
SKILL.md                         入口与阶段判断
package.json                     npm 包元数据、CLI 入口与发布文件清单
bin/opc-delivery.mjs              零依赖 CLI：install、list、help、version
test/                            CLI 文件系统与真实 npm tarball 安装验证
agents/openai.yaml               Codex 展示与默认调用提示
references/
  discovery.md                   需求证据与最小验证
  development.md                 实现与职责边界
  verification.md                根因定位与回归
  reliability-review.md          Agent 长任务、Trace 与 Tools
  release.md                     构建、发布与回退
  skill-recommendations.md        七个领域的可选 Skill、来源与选用条件
  evaluation.md                  技能维护与行为评测
scripts/                         只读检查器、证据检查器及测试
assets/                          项目接入与发布证据模板
skills/                          30 项配套技能及其方法、模板、参考与已有许可文件
  manifest.json                  来源、源文件与打包校验值、本地调整
docs/validation-0.1.0.md          已完成的验证及其边界
docs/validation-skill-recommendations.md  推荐能力增量验证
docs/validation-npm-0.2.0.md      npm CLI、打包与安装验证
docs/validation-specialists-0.3.0.md  三项专业能力的对照与安装验证
```

## 改进这个 Skill

欢迎提供带有输入、实际行为和预期行为的反馈。改动应帮助 Agent 做出更好的决策，保留项目自身的约束与用户意图。提交方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

当前仓库尚未指定开源许可证。

npm 元数据中的 `UNLICENSED` 保留这一现状；配套 Skill 中的原有许可文件随包保留。
