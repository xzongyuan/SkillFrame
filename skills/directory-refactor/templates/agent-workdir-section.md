## 工作目录

### 配置目录
- SOUL: `/root/.openclaw/workspace/agents/{agent_name}/SOUL.md`
- 项目清单: `/root/.openclaw/workspace/agents/{agent_name}/PROJECTS.md` (如有)
- TODO清单: `/root/.openclaw/workspace/agents/{agent_name}/TODO.md` (如有)

### 生成文件位置
| 文件类型 | 存放位置 | 说明 |
|:---|:---|:---|
| 配置文件 | `agents/{agent_name}/` | SOUL.md等 |
| 项目代码 | `projects/` | 代码文件 |
| 生成文档 | `docs/` 或 `agents/{agent_name}/docs/` | 文档 |

### 读取数据源
| 数据源 | 路径 | 用途 |
|:---|:---|:---|
| 系统配置 | `config/` | 读取配置 |
| 日志数据 | `data/logs/` | 分析日志 |

### 目录规范
- **禁止**在根目录生成文件
- **禁止**在 `agents/{agent_name}/` 下放代码文件
- 所有生成文件必须遵循 `docs/agent-directory-structure.md` 规范
