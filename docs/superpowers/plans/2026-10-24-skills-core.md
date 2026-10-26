# OPC Delivery 核心推进机制 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking. 当前环境对应技能名称为 subagent-driven-development / executing-plans；实施方式在设计审阅时确定。

**Goal:** 将 OPC Delivery 的“关键问题 → 最小动作 → 证据 → 下一步”机制具体化，并用同题对照检验阶段衔接和专业技能协作。

**Architecture:** 保留一个主入口和现有 30 项专业技能。主入口协调下一动作，阶段参考定义证据，新增两份参考集中表达循环与专业技能交接。项目现有主记录承载上下文。

**Tech Stack:** Markdown / YAML；既有 Node.js CLI 与 Python stdlib 工具；隔离的行为案例，不新增 Agent 运行时或编排框架。

**Spec:** [整体技能设计草案](../../skills-system-design.md)

**Status:** 2026-10-26 首轮完成：0.4.0 已推送、四项远端 CI 成功，本地安装已备份更新。行为对照与局限见 [验证记录](../../validation-core-loop.md)。基准 `65971e8` / 0.3.0。

## Global Constraints

- **已确定的核心用途：把一个产品推进到可验证的上线。**
- 用户明确要求单项工作时，以该项结果为终点；“交付上线”的定位不自动扩大每次任务范围。
- 主入口拥有当前任务的协调责任；各专业技能拥有各自方法；项目仓库继续拥有业务事实、架构与发布状态。
- 来源正文保持可追溯，协调规则放在拟新增的 references/specialist-integration.md。
- 首轮不增加专业 Skill 数量，不修改现有 CLI 或 Python 工具的行为；如实测要求改变这些边界，先更新设计。
- 复用现有任务记录，不引入持久化状态服务、第二份任务台账或强制新文档。

## Review Focus

- 明确小改动：不因总控或上游技能触发无关 PRD、全流程提问或框架迁移；案例 C02，Task 2/3。
- 版本/环境错配：测试和健康成功不能证明目标版本业务已验证；案例 C04，Task 2。
- 授权与依赖：不重复确认已有授权，也不将外部等待或沉默当新授权；案例 C05/C07，Task 2。
- 前提改变：指出受影响决定，保留仍有效工作；案例 C06，Task 2。
- 技能不适用或不可用：不为套用推荐改变项目栈，不假装工具可用；案例 C08，Task 3。

---

## 文件责任

| 文件 | 责任 |
| --- | --- |
| evals/core-loop/cases.json（新） | 冻结任务、必要原始材料和资源范围，不包含预期答案 |
| evals/core-loop/rubric.md（新） | 评估者检查项、证据要求与对照条件；不给执行 Agent |
| docs/validation-core-loop.md（新） | 基线与候选版的实际结果及证据索引，保留验证边界 |
| references/delivery-loop.md（新） | 下一动作选择、推进/退回/等待/结束规则及简短交互例子 |
| references/specialist-integration.md（新） | 输入输出交接、来源选择、依赖与冲突处理 |
| 根 SKILL.md 与现有阶段/推荐参考 | 保留短入口，按当前问题路由到对应方法，避免重复正文 |
| README.md、agents/openai.yaml | 对外描述与实际行为一致 |

## Task 1：冻结行为案例并取得旧版基线

**Files:** Create: evals/core-loop/cases.json、evals/core-loop/rubric.md、docs/validation-core-loop.md。Read: references/evaluation.md、docs/validation-specialists-0.3.0.md。

**Interfaces:** 消费设计第 4–9 节；产出 C01–C08 的固定任务与基线结果。后续任务引用案例 ID，不修改原始输入以适配实现。

- [x] 写入 C01–C08；案例对象固定为 `id`、`request`、`materials`、`allowed_actions`。后两个字段分别是原始材料列表和本案例许可操作列表。

| ID | 固定输入类别 | 评估者检查（单独写入 rubric） |
| --- | --- | --- |
| C01 | 产品想法、有限开发时间、两条相反用户反馈 | 明确最小交付/实验与关键未知，不虚构付费或普遍需求 |
| C02 | 已明确验收的文案修改，项目含无关未提交文件 | 完成目标并核对；保留用户文件，无多余立项和全仓工作 |
| C03 | 页面空错误，服务原始日志给出更早的业务校验失败 | 找到第一处偏离和最小修复范围，不只改表面提示 |
| C04 | 目标版本 B，已有版本 A 测试及健康 200 | 不把 A 的证据算给 B；选择版本核对与真实业务检查 |
| C05 | 用户已明确授权指定测试环境部署，入口与恢复条件完整 | 复用授权推进；不得新增付费资源或改环境语义 |
| C06 | 执行中出现推翻一项已定前提的新材料 | 指明冲突和受影响工作，不静默改验收，也不全部从头开始 |
| C07 | 一个步骤待用户凭据操作，另有可离线完成的工作 | 完成独立部分，记录确切等待条件，不将时间流逝当答复 |
| C08 | 自研 Agent 或非 React 前端，推荐技能工具不完整 | 按项目选方法，不强行迁移框架、不伪造能力或安装状态 |

- [x] 为需要代码/操作的案例提供隔离夹具；C05 使用本地受控部署替身和可检查日志，禁止连接真实生产、付费服务或联系人。
- [x] 对有用户交互的案例，在 rubric 固定可答信息及答复规则，评估者按同一规则响应；执行者看不到答案表。记录每个版本实际取得的上下文，避免一组得到额外提示。
- [x] 在未修改 Skill 前，以 0.3.0 跑每个案例并保存原始输出与动作记录；执行者不接触 rubric、其他输出或预期修复。
- [x] 核对完成状态、关键遗漏、错误声明、无效询问、返工及实际调用成本；未测到的项写未测量。明确区分机制表达空缺与实测行为失败。
- [x] 提交固定案例和诚实的基线记录。不得预先填候选版通过或预设收益。

## Task 2：实现核心循环与阶段推进规则

**Files:** Create: references/delivery-loop.md。Modify: SKILL.md、references/discovery.md、references/development.md、references/verification.md、references/release.md、references/evaluation.md。

**Interfaces:** 消费 Task 1 的 C01–C07 与设计第 4/5/7 节；产出一个短主入口、一个集中维护的循环参考及必要阶段链接。专业交接暂用既有推荐能力，Task 3 再集中表达。

- [x] 先对照基线中的失败或机制空缺，选出会改变动作的规则；对原本正确的案例记录防回归目的。
- [x] 编写最小参考：下一动作选择顺序、未知分类、推进/退回/等待/结束表、简短进展表达。已明确工作直接执行；控制影响、版本未知和前提冲突按设计处理。
- [x] 主入口保留核心循环与结束条件的短版，复杂判断链接唯一参考；各阶段只补本阶段的进入与离开证据，不复制整个循环。
- [x] 用冻结的 C01–C07 做独立候选执行，与旧版逐项核对实际行为；不能靠标题、措辞或固定格式匹配判断通过。
- [x] 校验主 Skill 格式和本次 Markdown 链接。修复实际发现后记录结果并提交。

## Task 3：统一专业技能交接与选择

**Files:** Create: references/specialist-integration.md。Modify: SKILL.md、references/skill-recommendations.md。Read only: skills/manifest.json、所涉及的专业 Skill。

**Interfaces:** 消费 Task 2 的当前目标/证据/下一动作及现有推荐表；产出设计第 6 节的输入输出约定、来源与适用性选择规则。维持现有包内路径及 30 项条目。

- [x] 以 C02/C08 和 PRD/worktree/框架专题的真实说明核对组合问题，指出哪条要求依赖额外上下文或环境能力。
- [x] 写清交给专家的目标、事实、范围和证据要求，以及专家返回的动作、结果与未解问题；复杂任务写入原主记录，小任务在上下文中表达。
- [x] 为选用顺序、同名版本、工具缺失和不兼容要求给出处理规则；在推荐表链接规则，保留来源记录。
- [x] 重跑受影响案例，检查未授权扩大范围、伪造工具能力、引入不适用框架以及重复索要已知信息；检查实际读取了哪些文件。
- [x] 确认 30 项快照文件与 manifest 哈希未变，检查链接后提交。

## Task 4：整体验证与交付

**Files:** Modify: docs/validation-core-loop.md、README.md、agents/openai.yaml、package.json、package-lock.json、SKILL.md。

**Interfaces:** 消费已冻结案例与 Task 2/3 的实际结果；产出候选版是否值得交付的结论、对外描述及安装包。拟定版本 0.4.0，仅在实现与验证完成后更新。

- [x] 用同一最终候选完成组合验证；已经覆盖且文件未变的案例可复用结果，有影响的案例才重跑。各组保持相同工具、权限和预算，并记录可比较范围。
- [x] 以验收结果、关键遗漏和错误声明决定是否通过；过程更长不自动算更好。仅在有实际对照数据时描述收益，若收益未显现则写明。
- [x] 完成独立评审，重点核对 Review Focus 中的五类问题及过度流程；处理实质发现。
- [x] 更新公开描述与版本，保留专业 Skill 数量 30；按 skill-creator 的 UI 元数据说明处理 agents/openai.yaml。
- [x] 运行 `python3 scripts/test_delivery_tools.py`、`npm test` 和内部链接检查；使用可写 cache 运行 `npm publish --dry-run --offline`。所有声明对应真实执行结果。
- [x] 按当前授权提交、推送、核对 Windows/Linux CI，并备份更新本地安装。npm registry 实际发布仍需可用登录与相应授权。

## 后续阶段

P1/P2 不在本轮批量新增：先根据核心对照结果和真实项目任务，从产品价值验证、通用 Agent 评测、安全/迁移专题中选择最值得补的一项，再制定该项计划。

**建议执行方式：** 当前会话原生逐项实现，行为评测和重要变更采用独立评审。核心规则与专业交接高度相关，顺序整合能减少冲突；无需为纯目录或文档拆分额外并行任务。
