# SkillFrame - 个人Skill仓库

> 基于OpenClaw的Skill管理系统
> 仓库地址: https://github.com/xzongyuan/SkillFrame

---

## 仓库结构

```
SkillFrame/
├── README.md                 # 本文件
├── skills/                   # Skill目录
│   ├── agent-directory/      # Agent目录服务
│   ├── agent-doppelganger/   # Agent分身通信
│   ├── agent-evaluation/     # Agent评估框架
│   ├── agent-team-orchestration/  # 多Agent编排
│   ├── ai-ppt-generator/     # AI PPT生成
│   ├── common/               # 通用工具
│   ├── directory-refactor/   # 目录重构工具
│   ├── evomap/               # EvoMap集成
│   ├── feishu-doc-manager/   # 飞书文档管理
│   ├── feishu-group-chat/    # 飞书群聊助手
│   ├── feishu-upload/        # 飞书文件上传
│   └── mineru/               # MinerU文档解析
├── templates/                # Skill模板
│   └── skill-template/       # 标准Skill模板
├── docs/                     # 文档
│   └── skill-design-spec-v1.md  # Skill设计规范
└── scripts/                  # 工具脚本
    └── skill-sync.sh         # Skill同步脚本
```

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/xzongyuan/SkillFrame.git
cd SkillFrame
```

### 2. 创建新Skill

```bash
# 基于模板创建
cp -r templates/skill-template skills/my-skill

# 编辑SKILL.md定义功能
vim skills/my-skill/SKILL.md

# 实现核心逻辑
vim skills/my-skill/src/index.js
```

### 3. 同步到OpenClaw

```bash
# 方式1: 使用同步脚本
./scripts/skill-sync.sh

# 方式2: 手动复制
cp -r skills/my-skill ~/.openclaw/workspace/skills/
```

### 完整开发流程

```
克隆仓库 → 创建Skill → 开发实现 → 测试验证 → 提交代码 → 同步使用
    ↑                                                    ↓
    └──────────────── 持续迭代更新 ←───────────────────────┘
```

---

## Skill清单

### Agent相关 (4个)

| Skill | 描述 | 状态 |
|:---|:---|:---:|
| **agent-directory** | Agent目录服务，发现和管理Agent | ✅ 可用 |
| **agent-doppelganger** | Agent分身通信，身份代理 | ✅ 可用 |
| **agent-evaluation** | Agent评估框架，测试和基准 | ✅ 可用 |
| **agent-team-orchestration** | 多Agent团队编排 | ✅ 可用 |

### 飞书集成 (4个)

| Skill | 描述 | 状态 |
|:---|:---|:---:|
| **feishu-doc-manager** | 飞书文档管理，Markdown渲染 | ✅ 可用 |
| **feishu-group-chat** | 飞书群聊助手，@提及支持 | ✅ 可用 |
| **feishu-upload** | 飞书文件上传 | ✅ 可用 |
| **common** | 通用飞书工具 | ✅ 可用 |

### 工具类 (4个)

| Skill | 描述 | 状态 |
|:---|:---|:---:|
| **ai-ppt-generator** | AI PPT生成 | ✅ 可用 |
| **directory-refactor** | 目录重构工具，项目迁移 | ✅ 可用 |
| **evomap** | EvoMap市场集成 | ✅ 可用 |
| **mineru** | MinerU文档解析(PDF/Word/PPT) | ✅ 可用 |

---

## 快速开始

### 安装Skill

```bash
# 克隆仓库
git clone https://github.com/xzongyuan/SkillFrame.git
cd SkillFrame

# 安装指定Skill到OpenClaw
cp -r skills/feishu-doc-manager /root/.openclaw/workspace/skills/
```

### 创建新Skill

```bash
# 使用模板
cp -r templates/skill-template skills/my-skill

# 编辑SKILL.md
vim skills/my-skill/SKILL.md

# 实现核心逻辑
vim skills/my-skill/src/index.js
```

---

## Skill设计规范

详见 [docs/skill-design-spec-v1.md](docs/skill-design-spec-v1.md)

### 核心原则

1. **需求驱动** - 先理解场景，再设计方案
2. **分层架构** - interface/core/adapters/config 分离
3. **多模式支持** - 配置驱动，非硬编码
4. **渐进式披露** - 信息分层，按需展示
5. **透明可观测** - 用户知道系统在做什么

---

## 同步到OpenClaw

```bash
# 运行同步脚本
./scripts/skill-sync.sh

# 或手动同步
cp -r skills/* /root/.openclaw/workspace/skills/
```

---

## 贡献指南

1. Fork本仓库
2. 创建新Skill或改进现有Skill
3. 确保符合skill-design-spec-v1.md规范
4. 提交Pull Request

---

## 许可证

MIT License