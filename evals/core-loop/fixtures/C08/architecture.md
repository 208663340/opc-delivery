# 现有实现

前端 Vue，Python 自研循环；不使用 LangChain/LangGraph。run_id/action_id 由调度层提供且恢复时保持。恢复会重新执行未完成 action。工具在共享存储创建记录，当前没有 action_id 唯一约束。无浏览器连接，无安装授权。
