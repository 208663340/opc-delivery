# 专业交接离线对照

全部输入为合成材料；没有生产账号、真实客户、联网或真实发布。执行者不读 rubric、旧输出或改动设计。H02 各版本使用 5 个新上下文，H01/H03 各一次。

准备每个重复的独立快照：

```bash
python3 evals/handoffs/prepare.py <skill-root> <new-destination>
```

固定执行提示（仅替换 arm 和 case）：

> 执行独立离线任务。先读 `{arm}/{case}/task.json`，用户请求在 request，原始材料在 `{arm}/{case}/project`。指定技能为 `{arm}/skill/SKILL.md`，引用按需读取。仅可读本案例和指定技能快照，仅用本地文件/命令工具；写操作遵守 allowed_actions，另可保存 `{arm}/{case}/response.md` 和 `{arm}/{case}/trace.json`。不联网、不委派、不读其他案例/评分表/其他技能。不向真实用户发问；必要选择写入回复并完成独立部分，不虚构答复。最多 20 次工具调用。完成后将原始最终回复保存 response.md；trace.json 自报读取文件、运行命令和结果，不将其称为完整工具审计。最后报告保存位置。

保存 response.txt、trace.json、实际修改、独立比较的 changes.json 与初始文件哈希。路径中的临时目录仅为历史记录，不要求继续存在。隔离依赖指令与独立目录，不是 OS 级访问隔离。

H02 的事件命令返回 3，H03 检查返回 1，均为预设业务观察。prepare.py 不复制评分表和历史结果。两臂使用同一模型配置、工具边界与预算；旧版为 0.5.0，不包含新增参考。记录未测量项和防回归结果，不把五次局部观察解释成普遍改善。
