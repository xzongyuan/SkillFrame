# MEMORY.md - 跨会话共享记忆

## 2026-02-24 Git 仓库管理教训

### 问题
混淆了多个 GitHub 仓库的用途，差点把文件推送到错误的仓库。

### 正确的仓库映射

| 类型 | 仓库名 | 地址 | 用途 |
|-----|--------|------|------|
| **Skill** | SkillFrame | https://github.com/xzongyuan/SkillFrame.git | 只存放 Skill 文件 |
| **Agent/文档/记忆** | AgentSwarmVisualized | https://github.com/xzongyuan/AgentSwarmVisualized.git | Agent 系统、文档、记忆日志 |
| **任务系统** | TaskManagement | https://github.com/xzongyuan/TaskManagement.git | 任务管理前端代码 |

### SkillFrame 仓库结构
```
skillframe/
├── docs/           # 文档
├── scripts/        # 脚本
├── skills/         # skill 目录（只放这里）
│   └── insight-distiller/
│       └── SKILL.md
└── templates/      # 模板
```

### 推送前必须确认
1. **当前文件类型** → Skill / Agent文档 / 其他
2. **目标仓库** → 根据类型选择对应仓库
3. **远程 URL** → 执行 `git remote -v` 确认

### 教训
**不要假设仓库地址，必须显式确认！**
- 之前记住了 TaskManagement，但这次是 Skill 文件
- 不同文件类型对应不同仓库
- 推送前必须检查 `git remote -v`

### 自动化改进
以后推送时自动执行：
```bash
# 1. 识别文件类型
if [[ $file == *"/skills/"* ]]; then
    target="SkillFrame"
elif [[ $file == *"docs/agent"* ]] || [[ $file == *"data/memory"* ]]; then
    target="AgentSwarmVisualized"
else
    target="TaskManagement"
fi

# 2. 设置正确的远程
 git remote set-url origin https://xzongyuan:$TOKEN@github.com/xzongyuan/$target.git

# 3. 确认后再推送
git remote -v  # 显示当前远程
git push origin master
```

---

## 2026-02-24 观点管理最佳实践落地

### 机制设计
建立了渐进式观点沉淀机制：
```
触发条件 → 收集 → 发酵 → 固化
```

### 已创建的资产
1. **Skill**: `skills/insight-distiller/SKILL.md` → SkillFrame 仓库
2. **设计文档**: `docs/agent-system-design.md` → AgentSwarmVisualized 仓库
3. **实践记录**: `data/memory/2026-02-24.md` → AgentSwarmVisualized 仓库

### 关键设计
- 不过早固化，允许观点自然演化
- 低摩擦操作，标签 + 自动提醒
- 可追溯性，保留原始对话链接

---

*此文件用于跨会话共享记忆，所有 Main Agent 会话都应读取。*
