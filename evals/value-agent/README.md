# 第二阶段离线案例

开发者评测材料，全部合成。评分表不交给执行者。先冻结本目录，再取得旧版输出；每个版本、每个案例均启用新上下文。

准备：`python3 evals/value-agent/prepare.py <skill-root> <new-destination>`。不允许目标目录已存在；不会复制评分表或历史结果到执行者目录。独立目录与读取边界由指令约束，未声明操作系统级隔离。

固定提示（仅替换路径）：

> 执行独立离线任务。先读 `{arm}/{id}/task.json` 的用户请求和许可范围，材料在 `{arm}/{id}/project`；指定 Skill 是 `{arm}/skill/SKILL.md`，按需读取其引用。仅可读本案例和该技能快照，写操作遵守 allowed_actions，并可保存 `{arm}/{id}/response.md` 和 `{arm}/{id}/trace.json`。只用本地文件/命令工具，不联网、不委派、不读取其他案例/评分表/其他技能。最多 24 次工具调用。没有真人答复，必要选择写进输出并完成独立部分，不向真实用户提问、不虚构回答。完成后把原始最终回复写 response.md，trace.json 自报实际读取文件、命令和结果；它不是完整工具审计。报告保存位置。

对原始回复使用 .txt 后缀存档，保留文本中的历史路径；实际变更另存并记录哈希。对照不声称真实用户价值、真实 Agent 性能或统计稳定性。结果见 [第二阶段验证记录](../../docs/validation-value-agent-0.5.0.md)。

结果分为 baseline（0.4.0，四例）、product-candidate（先完成产品材料，P01/P02）、agent-candidate（集成 0.5.0，A01/A02）。各目录的 initial-hashes.json 记录实际初始快照；不能把产品中间快照冒称最终全包版本。产品方法四文件在最终集成中未再修改。原始响应保留历史路径，不要求这些临时路径继续存在。

归档的 changed/ 是 A02 在获准 evals/ 内新增的真实文件；与 fixtures/A02 合并可复查现有 dry-run。response.txt 和 trace.json 为执行者输出，changes.json 为评估者独立比较的文件哈希。评分表末尾保留评审勘误，原冻结文本不被覆盖。
