---
name: directory-refactor
description: 全自动目录重构工具，支持项目迁移、Agent配置更新、路径修复，保证数据完整性
version: 1.0.0
author: main
tools: [bash, read, write, edit, exec]
---

# Directory Refactor Skill

全自动 workspace 目录结构重构工具。

## 核心特性

- ✅ **数据零变更** - SHA256 完整性校验
- ✅ **MD 增量更新** - 智能章节合并
- ✅ **脚本纯路径替换** - 只改字符串字面量
- ✅ **原子性保证** - 事务日志，自动回滚
- ✅ **全自动执行** - 无需人工干预

## 使用方法

```bash
# 分析目录结构
claw run directory-refactor --analyze

# 预览重构计划
claw run directory-refactor --plan --dry-run

# 执行重构
claw run directory-refactor --execute

# 查看报告
claw run directory-refactor --report
```

## 执行流程

1. **扫描分析** - 识别需要迁移的文件
2. **生成计划** - 制定迁移、更新、修复清单
3. **预检** - 磁盘、权限、Git 状态检查
4. **备份** - 创建完整备份和回滚脚本
5. **执行** - 原子操作，每步校验
6. **验证** - 完整性、语法、功能验证
7. **提交** - Git 分批次提交

## 算法保证

- 文件迁移：SHA256 校验，bit 级一致
- MD 更新：章节级替换，其他内容保留
- 脚本修复：只替换字符串字面量，语法检查

## 异常处理

- 完整性失败：自动回滚，重试
- 语法错误：回滚，标记人工处理
- 权限不足：尝试 sudo 或跳过
- 磁盘满：立即停止，报告

## 配置

```yaml
# rules/directory-spec.yaml
structure:
  projects:
    path: "projects/"
    pattern: "^[a-z0-9-]+$"
  agents:
    path: "agents/"
    required_files: ["SOUL.md"]
```

## 测试

```bash
# 运行测试
claw test directory-refactor

# 测试特定场景
claw test directory-refactor --scenario migrate-project
claw test directory-refactor --scenario update-md
claw test directory-refactor --scenario fix-paths
```

## 许可证

MIT
