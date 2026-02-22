# Skill创建模板

## 快速开始（推荐方式）

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

## 完整开发流程

```
┌─────────────────────────────────────────────────────────────┐
│  1. 创建  →  2. 开发  →  3. 测试  →  4. 发布  →  5. 同步    │
│                                                             │
│  cp模板    编辑代码    运行测试    push到    同步到         │
│           实现功能    验证功能    SkillFrame  OpenClaw     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

```
skills/{skill-name}/
├── SKILL.md              # Skill定义（必须）
├── README.md             # 使用文档
├── package.json          # 依赖（如有）
├── src/                  # 源码
│   ├── index.js          # 入口
│   ├── core/             # 核心逻辑
│   └── utils/            # 工具函数
├── config/               # 配置模板
│   └── default.json
├── examples/             # 使用示例
│   └── example-1.md
└── tests/                # 测试
    └── test-1.js
```

## SKILL.md 模板

```markdown
---
name: skill-name
description: |
  一句话描述Skill功能
version: 1.0.0
author: your-name
tags: [tag1, tag2]
---

# {Skill名称}

## 功能概述

### 适用场景

| 场景 | 说明 |
|:---|:---|
| 场景A | 描述 |
| 场景B | 描述 |

### 多模式支持

| 模式 | 用途 | 配置 |
|:---|:---|:---|
| mode-a | 场景A | `{ mode: "a" }` |
| mode-b | 场景B | `{ mode: "b" }` |

## 输入/输出

### 输入

```json
{
  "type": "object",
  "properties": {
    "param1": { "type": "string", "description": "参数1" }
  }
}
```

### 输出

```json
{
  "type": "object",
  "properties": {
    "result": { "type": "string", "description": "结果" }
  }
}
```

## 使用示例

### 示例1: 基础用法

```javascript
// 调用示例
```

### 示例2: 高级用法

```javascript
// 复杂场景
```

## 设计决策

### 为什么这样设计

1. **决策1**: 原因...
2. **决策2**: 原因...

### 已知限制

- 限制1: 说明...
- 限制2: 说明...

## 演进路线

- v1.1: 计划功能
- v2.0: 重大更新
```

## 设计原则

1. **需求驱动** - 先理解场景，再设计方案
2. **分层架构** - interface/core/adapters/config 分离
3. **多模式支持** - 配置驱动，非硬编码
4. **渐进式披露** - 信息分层，按需展示
5. **透明可观测** - 用户知道系统在做什么

## 目录结构

```
skills/{skill-name}/
├── SKILL.md              # Skill定义（必须）
├── README.md             # 使用文档
├── package.json          # 依赖（如有）
├── src/                  # 源码
│   ├── index.js          # 入口
│   ├── core/             # 核心逻辑
│   └── utils/            # 工具函数
├── config/               # 配置模板
│   └── default.json
├── examples/             # 使用示例
│   └── example-1.md
└── tests/                # 测试
    └── test-1.js
```

## SKILL.md 模板

```markdown
---
name: skill-name
description: |
  一句话描述Skill功能
version: 1.0.0
author: your-name
tags: [tag1, tag2]
---

# {Skill名称}

## 功能概述

### 适用场景

| 场景 | 说明 |
|:---|:---|
| 场景A | 描述 |
| 场景B | 描述 |

### 多模式支持

| 模式 | 用途 | 配置 |
|:---|:---|:---|
| mode-a | 场景A | `{ mode: "a" }` |
| mode-b | 场景B | `{ mode: "b" }` |

## 输入/输出

### 输入

```json
{
  "type": "object",
  "properties": {
    "param1": { "type": "string", "description": "参数1" }
  }
}
```

### 输出

```json
{
  "type": "object",
  "properties": {
    "result": { "type": "string", "description": "结果" }
  }
}
```

## 使用示例

### 示例1: 基础用法

```javascript
// 调用示例
```

### 示例2: 高级用法

```javascript
// 复杂场景
```

## 设计决策

### 为什么这样设计

1. **决策1**: 原因...
2. **决策2**: 原因...

### 已知限制

- 限制1: 说明...
- 限制2: 说明...

## 演进路线

- v1.1: 计划功能
- v2.0: 重大更新
```

## 设计原则

1. **需求驱动** - 先理解场景，再设计方案
2. **分层架构** - interface/core/adapters/config 分离
3. **多模式支持** - 配置驱动，非硬编码
4. **渐进式披露** - 信息分层，按需展示
5. **透明可观测** - 用户知道系统在做什么