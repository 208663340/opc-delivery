# npm 安装包 0.2.0 — 验证记录

验证日期：2026-10-22（Asia/Shanghai）。记录源码、打包与隔离安装证据；不代表 npm registry 已发布。

## 已验证

- `npm test`：11 项测试通过。使用真实 CLI 子进程和临时文件系统，覆盖完整安装、空格路径、`CODEX_HOME`、预览、已有目录保护、备份更新、错误参数、符号链接和源码路径重叠。
- tarball 端到端测试：实际 `npm pack`，离线安装到独立消费项目，执行 npm 生成的 CLI 入口，再检查主 Skill、27 项配套能力、规则、参考与许可文件。npm 安装阶段没有写技能目录。
- Node 20.20.2 与 Node 26.5.0：相同 11 项测试均通过。
- `npm publish --dry-run --offline`：通过，执行真实 `prepublishOnly` 测试流程并检查发布清单；未向 registry 发布。
- `python3 scripts/test_delivery_tools.py`：22 项测试通过。
- 主 Skill 格式与内部相对链接：通过；27 项第三方快照的文件校验值保持不变。
- 独立复核：全局 tarball 安装和全局 CLI 执行成功；另外检查默认用户目录与注入最终重命名失败后的恢复，未发现新的可复现缺陷。

发布预演与 `npm exec --package` 会向子进程注入 npm 配置；打包测试隔离这些父进程设置，确保测试中的 tarball 和消费项目安装仍真实执行。

## 范围与发布状态

CLI 仅使用 Node 标准库。发布包包含明确列出的技能资源和 CLI，排除测试目录、开发依赖与生成的 tarball；`--force` 在替换前保留整个旧安装目录，输出备份位置。

CI 覆盖 Ubuntu Node 20 / 24 和 Windows Node 24。Windows 运行结果以对应 GitHub Actions 为准；本机没有声称执行 Windows 测试。

目前 registry 没有同名公开包，本机 npm 检查返回 `ENEEDAUTH`。GitHub 来源和本地 tarball 可作为 npm 安装输入；短命令 `npx opc-delivery install` 需要先完成 npm 登录与正式发布。仓库未指定开源许可，npm 元数据采用 `UNLICENSED`，不改变已有许可状态。
