# Directory Refactor Skill

全自动 workspace 目录结构重构工具。

## 快速开始

```bash
# 进入 Skill 目录
cd skills/directory-refactor

# 分析目录结构
./refactor.sh /root/.openclaw/workspace analyze

# 执行重构
./refactor.sh /root/.openclaw/workspace execute

# 运行测试
./refactor.sh /root/.openclaw/workspace test
```

## 目录结构

```
directory-refactor/
├── SKILL.md                    # Skill 定义
├── refactor.sh                 # 入口脚本
├── lib/
│   └── refactor.py            # 核心算法
├── rules/
│   └── directory-spec.json    # 目录规范
├── templates/
│   ├── agent-workdir-section.md
│   └── agent-principles-section.md
└── tests/
    └── test_refactor.py       # 单元测试
```

## 核心算法

### 1. 数据完整性保证
- SHA256 校验，迁移前后 bit 级一致
- 自动备份，支持回滚

### 2. MD 增量更新
- 章节级替换，其他内容完全保留
- 智能合并，不破坏原有格式

### 3. 脚本路径替换
- 只替换字符串字面量
- 替换后强制语法检查

## 配置

编辑 `rules/directory-spec.json` 自定义规范。

## 测试

```bash
# 运行所有测试
python3 -m pytest tests/ -v

# 测试特定功能
python3 -m pytest tests/test_refactor.py::TestIntegrityCheck -v
```

## 许可证

MIT
