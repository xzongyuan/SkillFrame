# Skill设计规范 v1.0

## 设计原则（融合经验）

### 1. 需求驱动设计

**经验来源**: 任务系统数据同步方案设计

```
用户真实需求
    ↓
场景分析（多PC？内网？团队协作？）
    ↓
模式识别（Git同步/本地/混合）
    ↓
方案设计
```

**原则**: 不预设技术方案，先理解场景

### 2. 分层架构

**经验来源**: Auto Agent Routing设计

```
Skill/
├── interface/          # 接口层 - 对外契约
│   ├── input.schema    # 输入定义
│   └── output.schema   # 输出定义
├── core/               # 核心层 - 业务逻辑
│   ├── analyzer.js     # 分析器
│   ├── matcher.js      # 匹配器
│   └── executor.js     # 执行器
├── adapters/           # 适配层 - 外部集成
│   ├── git.adapter.js
│   └── local.adapter.js
└── config/             # 配置层
    ├── sync-config.json
    └── mode-config.json
```

**原则**: 分离关注点，便于扩展和测试

### 3. 多模式支持

**经验来源**: 数据同步的三种模式设计

```javascript
// 配置驱动，非硬编码
const modes = {
  git: { syncTasks: true, syncSettings: true },
  local: { syncTasks: false, syncSettings: false },
  hybrid: { syncTasks: true, syncSettings: false }
};

// 运行时选择
const currentMode = config.mode;
const adapter = adapters[currentMode];
```

**原则**: 一个Skill支持多种使用模式

### 4. 渐进式披露

**经验来源**: 汇报格式规范设计

```
启动时: 展示调度方案
执行中: 进度更新（如并发）
完成时: 详细结果
```

**原则**: 信息分层，按需展示

### 5. 透明可观测

**经验来源**: Agent并发处理可视化

```
📋 任务分析 → 类型/领域/复杂度
🤖 Agent调度 → 谁负责什么
⏳ 执行进度 → 实时百分比
✅ 完成汇报 → 耗时/产出
```

**原则**: 用户知道系统在做什么

---

## Skill创建模板

### 目录结构

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

### SKILL.md 模板

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

---

## 最佳实践

### DO

- ✅ 从场景出发，不预设方案
- ✅ 支持多模式，适应不同环境
- ✅ 分层架构，便于扩展
- ✅ 透明汇报，用户知情
- ✅ 渐进式功能，从简单开始

### DON'T

- ❌ 一上来就追求通用
- ❌ 硬编码特定环境假设
- ❌ 黑盒操作，用户不知道在做什么
- ❌ 过度设计，增加复杂度

---

## 与OpenClaw SkillCreator对比

| 维度 | OpenClaw SkillCreator | 本规范 |
|:---|:---|:---|
| 设计起点 | 技术能力 | 用户场景 |
| 架构 | 单层 | 分层 |
| 模式 | 单一 | 多模式 |
| 可观测 | 基础 | 透明汇报 |
| 演进 | 版本迭代 | 渐进式 |

**融合点**:
- 采用 SkillCreator 的目录结构标准
- 加入场景驱动和多模式设计
- 强化透明汇报和渐进式披露

---

*规范版本: v1.0*
*创建时间: 2026-02-22*
*融合经验: 数据同步方案 + Auto Agent Routing + OpenClaw SkillCreator*
