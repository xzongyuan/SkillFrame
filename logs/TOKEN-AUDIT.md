# Token 消费审计日志

**审计时间:** 2026-02-24 12:00:00 (Asia/Shanghai)  
**审计周期:** 今日活跃会话统计

---

## 今日会话概览

| Agent/会话 | 类型 | Token 消费 | 状态 |
|-----------|------|-----------|------|
| main (主会话) | 主会话 | 47,102 | ✅ 正常 |
| agent-status-monitor | Cron | 57,462 | ✅ 正常 |
| xiaozhi-claw-forum-insight | Cron | 44,279 | ✅ 正常 |
| daily-task-dashboard | Cron | 22,243 + 25,593 | ✅ 正常 |
| daily-security-audit | Cron | - | ✅ 正常 |
| daily-agent-health-check | Cron | 21,180 | ✅ 正常 |
| daily-github-backup | Cron | 24,890 | ✅ 正常 |
| daily-backup-to-feishu | Cron | 24,496 | ✅ 正常 |
| daily-agent-backup | Cron | 20,924 | ✅ 正常 |
| xiaozhi-log-check | Cron | 32,299 | ✅ 正常 |
| xiaot-task-monitor | Cron | 22,128 | ✅ 正常 |
| hourly-agent-monitor | Cron | 30,889 | ✅ 正常 |
| daily-agent-reflection | Cron | 29,570 | ✅ 正常 |
| vercel-deploy-check | Cron | 20,514 | ✅ 正常 |
| agent-growth-report | Cron | 39,785 | ✅ 正常 |
| xiaot-progress-monitor | Cron | 33,478 | ✅ 正常 |
| feishu 群聊 | 群聊 | 40,934 | ✅ 正常 |
| xiaot2 (子代理) | Subagent | 78,298 | ✅ 正常 |
| 其他子代理 | Subagent | 18,807 + 17,769 + 18,335 + 28,531 + 31,104 + 23,218 | ✅ 正常 |

---

## 消费阈值检查

| 阈值级别 | 标准 | 超标数量 |
|---------|------|---------|
| 🟡 警告 | > 500K tokens (~￥10) | 0 |
| 🟠 严重 | > 1M tokens (~￥20) | 0 |
| 🔴 危险 | > 2M tokens (~￥40) | 0 |

**检查结果:** ✅ 所有会话均在安全范围内

---

## 最高消费会话 TOP 5

| 排名 | 会话 | Token 消费 | 估算费用 |
|-----|------|-----------|---------|
| 1 | xiaot2 (子代理) | 78,298 | ~￥1.57 |
| 2 | agent-status-monitor | 57,462 | ~￥1.15 |
| 3 | main (主会话) | 47,102 | ~￥0.94 |
| 4 | xiaozhi-claw-forum-insight | 44,279 | ~￥0.89 |
| 5 | feishu 群聊 | 40,934 | ~￥0.82 |

---

## 审计结论

- **审计状态:** ✅ 通过
- **无超标会话**
- **所有 Agent 运行正常**
- **建议:** 继续保持监控

---

*日志由 token-audit-monitor 自动生成*
