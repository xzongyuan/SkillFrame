---
name: skill-template
description: |
  Skill创建模板，用于快速创建新Skill
version: 1.0.0
author: OpenClaw
tags: [template, skill-development]
---

# Skill Template

## 功能概述

这是一个Skill创建模板，帮助你快速创建符合规范的Skill。

### 适用场景

| 场景 | 说明 |
|:---|:---|
| 创建新Skill | 基于模板快速启动 |
| 学习Skill结构 | 理解最佳实践 |

## 输入/输出

### 输入

```json
{
  "type": "object",
  "properties": {
    "skillName": { "type": "string", "description": "Skill名称" },
    "description": { "type": "string", "description": "Skill描述" }
  }
}
```

### 输出

```json
{
  "type": "object",
  "properties": {
    "path": { "type": "string", "description": "创建的Skill路径" },
    "files": { "type": "array", "description": "创建的文件列表" }
  }
}
```

## 快速开始

### 方式1: 使用SkillFrame仓库（推荐）

```bash
# 1. 克隆SkillFrame仓库
git clone https://github.com/xzongyuan/SkillFrame.git
cd SkillFrame

# 2. 基于模板创建新Skill
cp -r templates/skill-template skills/my-skill

# 3. 编辑SKILL.md定义你的Skill
vim skills/my-skill/SKILL.md

# 4. 实现核心逻辑
vim skills/my-skill/src/index.js

# 5. 同步到OpenClaw
./scripts/skill-sync.sh
```

### 方式2: 手动创建

```bash
# 复制模板到OpenClaw skills目录
cp -r templates/skill-template ~/.openclaw/workspace/skills/my-skill

# 编辑并开发
vim ~/.openclaw/workspace/skills/my-skill/SKILL.md
```

### 方式3: 通过对话创建

```
你: 帮我创建一个名为xxx的Skill，用于...
→ 我会基于模板自动创建并配置
```

## 设计决策

### 为什么这样设计

1. **标准化**: 统一Skill结构，便于维护
2. **可扩展**: 分层架构，易于扩展
3. **可测试**: 分离关注点，便于单元测试

## 演进路线

- v1.1: 添加更多示例
- v1.2: 添加CLI工具