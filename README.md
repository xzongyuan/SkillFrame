# SkillFrame

Anthropic兼容的Skill系统 - 让Agent能力可复用、可沉淀、可进化

## 项目定位

SkillFrame是一个与Anthropic Skills规范兼容的Skill管理系统，专为OpenClaw多Agent系统设计。它实现了三层渐进披露、自动Skill检测、代码沙箱执行等核心能力。

## 核心特性

- ✅ **Anthropic兼容** - 遵循官方Skill规范，100%兼容
- ✅ **三层渐进披露** - Token效率优化，初始仅~100 tokens
- ✅ **自动Skill检测** - 智能匹配最合适的Skill
- ✅ **代码沙箱执行** - Docker隔离，安全执行脚本
- ✅ **轻量部署** - 纯文件+插件，无服务进程
- ✅ **深度集成** - 与OpenClaw Gateway无缝集成

## 架构设计

```
SkillFrame/
├── skill-manager/          # Skill管理核心
│   ├── scanner.py          # 扫描skills目录
│   ├── indexer.py          # 构建索引
│   └── registry.py         # 注册管理
├── context-manager/        # 上下文管理
│   ├── loader.py           # 三层加载
│   ├── cache.py            # 缓存管理
│   └── optimizer.py        # Token优化
├── code-sandbox/           # 代码执行
│   ├── executor.py         # 脚本执行
│   ├── security.py         # 安全隔离
│   └── monitor.py          # 监控日志
└── gateway-plugin/         # OpenClaw集成
    ├── api.py              # API接口
    └── websocket.py        # 实时推送
```

## 快速开始

### 安装

```bash
git clone https://github.com/xzongyuan/SkillFrame.git
cd SkillFrame
pip install -r requirements.txt
```

### 配置

```bash
# 配置OpenClaw Gateway插件
cp config.example.yaml config.yaml
# 编辑config.yaml
```

### 创建第一个Skill

```bash
mkdir -p skills/my-skill
cat > skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: 我的第一个Skill
version: 1.0.0
author: xiaos
tools: [bash, read]
---

# 使用说明

## 执行流程
1. 读取输入文件
2. 处理数据
3. 输出结果
EOF
```

## Skill格式

```yaml
---
name: skill-name                    # Skill名称（64字符内）
description: 一句话描述            # 描述（1024字符内）
version: 1.0.0                      # 版本
author: xiaos                       # 作者
tools: [bash, read, write]          # 允许的工具
---

# Skill手册（Markdown格式）

## 使用场景
什么时候使用这个Skill...

## 执行流程
1. 步骤一
2. 步骤二
3. 步骤三

## 错误处理
如何处理异常...
```

## 与竞品对比

| 特性 | SkillFrame | Anthropic | MCP | OpenAI |
|:---|:---:|:---:|:---:|:---:|
| 渐进披露 | ✅ | ✅ | ❌ | ❌ |
| 自动检测 | ✅ | ✅ | ❌ | ❌ |
| Token效率 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| 部署复杂度 | 低 | 低 | 高 | 中 |
| 外部连接 | 预留 | ❌ | ✅ | ✅ |

## 开发计划

- [x] 架构设计
- [ ] Phase 1: Skill Manager
- [ ] Phase 2: Context Manager
- [ ] Phase 3: Code Sandbox
- [ ] Phase 4: Gateway集成
- [ ] Phase 5: 测试优化

## 贡献

欢迎贡献！请阅读[贡献指南](CONTRIBUTING.md)。

## 许可证

MIT License

---

*SkillFrame - 让Skill成为Agent的超能力*
