# 专业 Skill 推荐：按当前问题选择

OPC Delivery 负责推进交付；需要某个领域的方法时，再选择相应的专业 Skill。`skills/` 已附带 30 项配套技能：下方 21 项主要推荐，加上 9 项 Agent 与 Python 配套能力。其中 27 项为本地快照，用户研究、原型验证与部署运维 3 项由本项目编写并附专用模板。表中的技能名称链接本包文件，作者链接保留上游来源。按问题查阅，不要求为一个任务加载所有分类。

## 如何选用

1. **先核对实际说明。** 读取下方链接的本包 `SKILL.md`，确认名称、适用范围及所需工具；只有涉及当前问题的项才继续读取其引用。包内快照已经可以按路径使用，不等于运行时为每项注册了独立入口。若选择本机其他版本，先查看本会话技能目录及其实际说明，并明确本次采用哪份。源目录名与 frontmatter 名称可能不同，例如上游 `react-best-practices` 目录中的名称是 `vercel-react-best-practices`。
2. **围绕当前阻塞点选择。** 通常先用一个主专业 Skill；另一项解决不同问题时再补充。专业方法服从当前用户目标、已有验收和项目约束，不因候选清单而引入新框架、第二套状态或无关重构。
3. **缺少必要能力时继续可做的部分。** 内置 Skill 仍可能需要当前环境没有的工具、网络或框架。先用本技能的阶段参考、项目工具或已安装的同类能力推进，说明覆盖边界。安装和外部操作按本次已有授权执行，未授权的全局安装、付费服务或框架迁移不会由推荐自动取得授权。
4. **把专业结论交回当前任务。** 给出改动或判断、验收方式和实际证据，写入已有主记录。无需为每项 Skill 再建计划或报告。

需要向用户说明选择时，可以简短地写：

> 当前问题是 React 请求串行，使用本包的 `skills/vercel-react-best-practices/SKILL.md` 检查数据依赖与请求瀑布。验证看同条件下的网络时序和页面行为；需要的浏览器工具不可用时，先沿现有调用链调查并说明未验证的部分。

## 1. UI/UX 设计

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [frontend-design](../skills/frontend-design/SKILL.md) · [Anthropic](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 新建页面或改版，需要确定视觉方向、字体、配色、布局与交互呈现 | 与产品和现有设计系统一致的界面；关键视口截图与主路径演示 |
| [web-design-guidelines](../skills/web-design-guidelines/SKILL.md) · [Vercel](https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md) | 已有 UI 需要检查键盘操作、焦点、表单、可访问性和 Web 交互规范 | 可定位到代码的发现、修复与操作验证；需要联网读取最新规则时说明实际取得的规则版本 |
| [prototype-validation](../skills/prototype-validation/SKILL.md) · 本项目 | 原型保真度、可用性任务、真人观察与迭代判断 | 原型范围、任务脚本、观察表、独立/受助/失败计数与证据；不把演示当付费验证 |

视觉设计、界面规范检查与用户研究解决不同问题。流程是否满足用户需求先回到 [需求判断](discovery.md)；已有品牌、设计稿和组件库作为设计输入。

## 2. 前端开发

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [vercel-react-best-practices](../skills/vercel-react-best-practices/SKILL.md) · [Vercel](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md) | React / Next.js 的数据获取、请求瀑布、渲染或包体积问题 | 对应路径的代码变化、构建与行为检查；性能结论附同条件下的测量 |
| [vercel-composition-patterns](../skills/vercel-composition-patterns/SKILL.md) · [Vercel](https://github.com/vercel-labs/agent-skills/blob/main/skills/composition-patterns/SKILL.md) | React 组件布尔参数膨胀，或需调整组件组合与复用 API | 使用方能表达的状态、组件接口变化及受影响页面回归 |

仅在相应技术栈和版本适用时采用。Vue、Svelte 或其他前端先找本环境的对应 Skill；不要为使用推荐项迁移技术栈。

## 3. 后端开发

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [python-fastapi](../skills/python-fastapi/SKILL.md) · [社区](https://github.com/martinffx/python-skills/blob/main/skills/python-fastapi/SKILL.md) | 已有 FastAPI 项目的校验、依赖、错误映射、鉴权或生命周期 | 与既有契约一致的实现、接口样例与正常/失败路径测试 |
| [java-springboot](../skills/java-springboot/SKILL.md) · [GitHub 社区集合](https://github.com/github/awesome-copilot/blob/main/skills/java-springboot/SKILL.md) | 已有 Spring Boot 项目的 DTO、服务、事务、配置与测试 | 既有分层内的实现及受影响模块验证 |
| [architecture-patterns](../skills/architecture-patterns/SKILL.md) · [社区](https://github.com/wshobson/agents/blob/main/plugins/backend-development/skills/architecture-patterns/SKILL.md) | 职责边界不清、层间循环依赖或业务逻辑与基础设施耦合，需要结构性判断 | 现有 owner 与依赖方向、必要改动及兼容与回归证据 |

普通接口修改从 [开发参考](development.md) 与项目框架能力开始。只有实际出现结构问题时才引入架构方法；项目的数据归属与契约真相源决定修改位置。

FastAPI 材料提到的 Python 专题也已附带：

| 配套 Skill | 何时读取 |
| --- | --- |
| [python-sqlalchemy](../skills/python-sqlalchemy/SKILL.md) | ORM 映射、查询、会话与事务边界 |
| [python-testing](../skills/python-testing/SKILL.md) | pytest、fixture、异步或数据库测试 |

## 4. Agent 开发

已有自研循环或其他 Agent 框架时，先读 [可靠性审查](reliability-review.md)，检查任务生命周期、Tools、副作用、恢复与资源边界。下列候选针对 LangChain 生态，只有项目已使用该生态或用户明确要求评估它时才选用。

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [ecosystem-primer](../skills/ecosystem-primer/SKILL.md) · [LangChain](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/ecosystem-primer/SKILL.md) | 需要在 LangChain / LangGraph / Deep Agents 之间确定适用层次；使用该生态时先读此入口 | 选择依据、现有约束与不确定项，再按其路由加载相关专业 Skill |
| [langchain-fundamentals](../skills/langchain-fundamentals/SKILL.md) · [LangChain](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/langchain-fundamentals/SKILL.md) | 实现 LangChain Agent、Tools 与 middleware | Tool 输入输出、错误与副作用边界，以及可复现的调用记录 |
| [langgraph-fundamentals](../skills/langgraph-fundamentals/SKILL.md) · [LangChain](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/langgraph-fundamentals/SKILL.md) | 实现 LangGraph 的状态、节点、分支、循环与流式执行 | 状态流转及终止条件的验证；恢复等能力继续按入口加载相应专题 |
| [deep-agents-core](../skills/deep-agents-core/SKILL.md) · [LangChain](https://github.com/langchain-ai/langchain-skills/blob/main/config/skills/deep-agents-core/SKILL.md) | 已选择 Deep Agents，需要配置 harness、规划、文件或委派能力 | 实际启用的能力、运行边界与任务验证；记忆等专题按需另读 |

不因“有长任务”就替换已有运行时。框架示例能运行只证明接通；任务质量、恢复与副作用需要各自的证据。

生态入口继续路由的专题也已附带，按当前问题读取：

| 配套 Skill | 何时读取 |
| --- | --- |
| [langchain-dependencies](../skills/langchain-dependencies/SKILL.md) | 包版本、安装与依赖管理 |
| [langchain-rag](../skills/langchain-rag/SKILL.md) | 文档加载、切分、向量检索与 RAG |
| [langchain-middleware](../skills/langchain-middleware/SKILL.md) | middleware、结构化输出与人工介入 |
| [langgraph-human-in-the-loop](../skills/langgraph-human-in-the-loop/SKILL.md) | 中断、审批与恢复输入 |
| [langgraph-persistence](../skills/langgraph-persistence/SKILL.md) | checkpoint、持久化、记忆与历史状态 |
| [deep-agents-memory](../skills/deep-agents-memory/SKILL.md) | 文件系统、存储后端与跨会话记忆 |
| [deep-agents-orchestration](../skills/deep-agents-orchestration/SKILL.md) | 子 Agent、规划与人工审批配置 |

## 5. 产品设计与分析

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [user-research](../skills/user-research/SKILL.md) · 本项目 | 需要规划访谈、识别用户分群、分析需求与相反证据 | 研究简报、中性提纲、证据账本与可支持的决定；样本边界和待验证项明确 |
| [market-research](../skills/market-research/SKILL.md) · [ECC 社区](https://github.com/affaan-m/ECC/blob/main/skills/market-research/SKILL.md) | 关键未知在市场、竞品、用户替代方案或供应商，需要外部研究支持取舍 | 可追溯来源、日期、事实与推断，以及会改变决策的结论 |
| [prd](../skills/prd/SKILL.md) · [GitHub 社区集合](https://github.com/github/awesome-copilot/blob/main/skills/prd/SKILL.md) | 用户要求 PRD，或复杂功能需要统一范围、用户故事、验收与风险 | 可执行的需求规格、待验证假设及验收条件 |

模糊想法先用 [需求判断](discovery.md) 找到关键未知；只有两次访谈时优先整理原始证据与最小验证。需要外部信息才做市场研究，需要规格才写 PRD；已有明确验收时直接实施。

## 6. Bug 修复

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [systematic-debugging](../skills/systematic-debugging/SKILL.md) · [Superpowers](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) | 错误、测试失败或异常行为的根因尚未证明 | 最小复现、调用链证据、根因与最小修复范围 |
| [test-driven-development](../skills/test-driven-development/SKILL.md) · [Superpowers](https://github.com/obra/superpowers/blob/main/skills/test-driven-development/SKILL.md) | 已明确要改变的行为，需要先建立失败测试再实现修复或功能 | 能在修复前失败、修复后通过的测试及相关回归 |

根因未知时先调查，再补最贴近故障域的能力。页面提示为空并不能证明错误源在前端。纯文案等低影响改动依 [开发参考](development.md) 和项目要求选择验证方式。

## 7. 工程基础

| 候选与来源 | 何时选择 | 交回的结果与证据 |
| --- | --- | --- |
| [using-git-worktrees](../skills/using-git-worktrees/SKILL.md) · [Superpowers](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/SKILL.md) | 两个功能需要隔离，或当前工作区已有不相关修改 | 已有或新建隔离工作区的路径、基准、分支与改动归属；先检查已有隔离 |
| [verification-before-completion](../skills/verification-before-completion/SKILL.md) · [Superpowers](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) | 即将声明修复、测试或交付完成 | 当前版本实际运行的验证、结果与覆盖边界 |
| [requesting-code-review](../skills/requesting-code-review/SKILL.md) · [Superpowers](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md) | 重要功能完成、复杂修复或合并前需要独立评审 | 明确的 diff、验收与风险、评审发现及处理结果；按环境与授权使用评审能力 |
| [deployment-operations](../skills/deployment-operations/SKILL.md) · 本项目 | 发布准备、渐进放量、监控值守、故障恢复或备份演练 | 同版本发布证据、应用/配置/schema/数据兼容判断、停止条件、恢复与交接手册 |

CI/CD、容器、数据库和部署优先复用项目现有入口；需要额外专题时按实际工具寻找对应 Skill。工作区隔离、评审和发布分别依当前任务的工具与授权推进。

## 清单之外与来源维护

本清单的上游源文件和声明范围于 **2026-10-22** 核对；27 项包内内容取自用户本机已安装的快照，可能与上游最新文件不同；新增 3 项为本项目编写，方法参考与核对日期列在各自 references 中，不标为上游导入。完整目录、来源、源文件与打包文件的 SHA-256 及本地调整见 [manifest.json](../skills/manifest.json)。所有原有参考文件与许可文件一起保留；Vercel 生成文档中的三处相对链接做了路径修正并记录。打包不代表所有 Skill 已做行为评测或兼容当前环境，来源身份不替代适用性判断。

未覆盖的技术栈先检索本会话技能目录；环境有技能发现工具时再用精确任务与技术栈查找，例如 `Vue accessibility`、`PostgreSQL migration`。推荐外部项前读取真实 `SKILL.md`，核对名称、范围、依赖和调用方式，给出可访问来源。找不到或无法核对时说明缺口并继续完成可做部分，不补造名称或安装状态。

维护此文件时重新核对选中项的源路径与说明，移除失效推荐或更正路径。保留少量能帮助当前决策的候选，避免复制外部技能全文或把安装排行当成质量结论。行为验证场景见 [evaluation.md](evaluation.md)。
