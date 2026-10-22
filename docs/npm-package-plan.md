# npm 安装包实施记录

目标：将现有完整 Skill 包装为零依赖 npm CLI，保留 27 项配套技能及原有 Python 工具。

约定：包名 `opc-delivery`，版本 `0.2.0`，Node.js >= 20。`opc-delivery install` 默认安装到 `${CODEX_HOME:-~/.codex}/skills/opc-delivery`；`--dir` 指定技能根目录，`--dry-run` 不写文件，`--force` 先保留旧目录再替换。`list` 展示附带技能，`--help` 和 `--version` 不安装。

## 实施与验证

1. `test/cli.test.mjs` 先用真实 CLI 子进程和临时文件系统验证完整安装、默认目录、自定义路径、预览、重复安装与更新、错误参数和符号链接边界；观察缺少实现时失败。
2. `package.json` 定义 `bin` 与明确发布文件清单；`bin/opc-delivery.mjs` 只使用 Node 标准库。安装先复制到临时目录，成功后重命名；覆盖前备份，失败时保留原安装。
3. `test/package.test.mjs` 通过真实 `npm pack` 产出 tarball，验证其中内容，并用 `npm install --global --prefix` 安装后运行 CLI，确认 npm 的安装阶段不会自动改写技能目录。
4. CI 加入 Node CLI、打包安装测试，保留 Python 测试与文档链接检查。README 提供 npm、GitHub 与本地 tarball 的明确使用方法，区分“包可安装”和“已经发布”。

发布不作为测试副作用。当前 npm registry 没有同名包，本机没有 npm 登录；完成 tarball 验证后再处理发布所需登录。
