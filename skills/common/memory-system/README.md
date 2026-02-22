# 记忆系统 Skill

为小知提供记忆存储与检索能力，支持短期/中期/长期/状态四类记忆。

## 快速开始

```python
# 方法1: 直接使用存储/检索接口
from scripts.store import store
from scripts.retrieve import retrieve

mid = store("用户喜欢喝咖啡", "long", "xiaozhi", "medium")
results = retrieve("咖啡", limit=5)

# 方法2: 使用小忆Agent
from scripts.xiaoyi import remember, recall

mid = remember("用户喜欢喝咖啡", "xiaozhi", "high")
results = recall("咖啡", limit=5)
```

## 目录结构

```
skills/common/memory-system/
├── SKILL.md              # Skill定义
├── scripts/
│   ├── store.py          # 存储接口
│   ├── retrieve.py       # 检索接口
│   ├── migrate.py        # 迁移接口
│   └── xiaoyi.py         # 小忆Agent核心
├── config.yaml           # 配置文件
└── README.md             # 使用文档
```

## 记忆分类

| 分类 | TTL | 说明 |
|------|-----|------|
| short | 1天 | 短期记忆，临时信息 |
| medium | 7天 | 中期记忆，近期信息 |
| long | 30天 | 长期记忆，重要信息 |
| state | 永久 | 状态记忆，用户偏好等 |

## 接口说明

### store(content, category, agent, priority) -> str
存储记忆，返回记忆ID。

### retrieve(query, category=None, limit=10) -> list
检索记忆，返回匹配的记忆列表。

### migrate() -> dict
迁移过期记忆，返回迁移统计。

## 数据存储

记忆数据存储在 `./data/memory/` 目录下：

```
data/memory/
├── short/       # 短期记忆
├── medium/      # 中期记忆
├── long/        # 长期记忆
├── state/       # 状态记忆
└── archive/     # 归档记忆
```

## 小忆Agent

小忆Agent提供智能记忆管理：

- **自动分类**: 根据内容自动选择存储分类
- **智能检索**: 基于关键词匹配和相关性排序
- **记忆整合**: 自动迁移过期记忆
- **记忆摘要**: 生成记忆统计和摘要

```python
from scripts.xiaoyi import remember, recall, consolidate, summarize

# 智能存储（自动分类）
mid = remember("用户喜欢喝拿铁", "xiaozhi", "high")

# 智能检索
results = recall("咖啡")

# 整合记忆
stats = consolidate()

# 生成摘要
summary = summarize()
```

## 配置

编辑 `config.yaml` 修改配置：

```yaml
storage:
  base_path: "./data/memory"

categories:
  short:
    ttl_days: 1
  medium:
    ttl_days: 7
  long:
    ttl_days: 30
  state:
    ttl_days: -1  # 永久
```

## 测试

```bash
cd skills/common/memory-system

# 测试存储
python3 scripts/store.py

# 测试检索
python3 scripts/retrieve.py

# 测试迁移
python3 scripts/migrate.py

# 测试小忆Agent
python3 scripts/xiaoyi.py
```

## 与小知集成

小知可以通过以下方式调用记忆系统：

```python
import sys
sys.path.insert(0, "./skills/common/memory-system")

from scripts.xiaoyi import remember, recall

# 在对话中存储关键信息
remember("用户提到喜欢蓝色", "xiaozhi", "medium")

# 在回复前检索相关记忆
memories = recall("用户 喜欢")
# 将记忆融入回复...
```

## 作者

小S (Skill架构专家)
