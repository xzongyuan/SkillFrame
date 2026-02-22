# 记忆系统 Skill

## 概述
为小知提供记忆存储与检索能力，支持短期/中期/长期/状态四类记忆。

## 版本
version: 1.0.0

## 作者
小S (Skill架构专家)

## 依赖
- python >= 3.8
- 无外部依赖（纯标准库）

## 接口定义

### store(content, category, agent, priority) -> str
存储记忆内容。

**参数:**
- `content` (str): 记忆内容
- `category` (str): 分类 - short(短期)/medium(中期)/long(长期)/state(状态)
- `agent` (str): 来源Agent名称
- `priority` (str): 优先级 - high/medium/low

**返回:**
- `memory_id` (str): 记忆唯一ID

### retrieve(query, category=None, limit=10) -> list
检索记忆。

**参数:**
- `query` (str): 检索关键词
- `category` (str, optional): 指定分类筛选
- `limit` (int): 返回数量限制

**返回:**
- `list[dict]`: 匹配的记忆列表，按相关性排序

### migrate() -> dict
迁移过期记忆。

**返回:**
- `dict`: 迁移统计信息

## 配置

```yaml
storage:
  base_path: "./data/memory"
  
categories:
  short:
    ttl_days: 1      # 1天后迁移到中期
  medium:
    ttl_days: 7      # 7天后迁移到长期
  long:
    ttl_days: 30     # 30天后归档
  state:
    ttl_days: -1     # 永久保存

retrieval:
  max_results: 10
  keyword_match_threshold: 0.5
```

## 使用示例

```python
from memory_system import store, retrieve, migrate

# 存储记忆
mid = store("用户喜欢喝咖啡", "long", "xiaozhi", "medium")

# 检索记忆
results = retrieve("咖啡", limit=5)

# 迁移过期记忆
stats = migrate()
```

## 文件结构

```
data/memory/
├── short/       # 短期记忆 (24h)
├── medium/      # 中期记忆 (7d)
├── long/        # 长期记忆 (30d)
├── state/       # 状态记忆 (永久)
└── archive/     # 归档记忆
```

## 记忆格式

每个记忆以JSON文件存储:

```json
{
  "id": "mem_abc123",
  "content": "记忆内容",
  "category": "short",
  "agent": "xiaozhi",
  "priority": "high",
  "created_at": "2026-02-19T07:14:00",
  "updated_at": "2026-02-19T07:14:00",
  "access_count": 0,
  "last_accessed": null,
  "keywords": ["关键词1", "关键词2"]
}
```
