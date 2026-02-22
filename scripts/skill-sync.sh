#!/bin/bash
# Skill同步脚本 - 将SkillFrame同步到OpenClaw

set -e

SKILLFRAME_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OPENCLAW_SKILLS_DIR="/root/.openclaw/workspace/skills"

echo "=== SkillFrame同步工具 ==="
echo ""

# 检查OpenClaw目录
if [ ! -d "$OPENCLAW_SKILLS_DIR" ]; then
    echo "错误: OpenClaw skills目录不存在: $OPENCLAW_SKILLS_DIR"
    exit 1
fi

# 显示菜单
echo "选择操作:"
echo "1) 同步所有Skill"
echo "2) 同步指定Skill"
echo "3) 查看差异"
echo "4) 退出"
echo ""
read -p "输入选项 (1-4): " choice

case $choice in
    1)
        echo "同步所有Skill..."
        for skill in "$SKILLFRAME_DIR"/skills/*/; do
            skill_name=$(basename "$skill")
            echo "  同步: $skill_name"
            rsync -av --delete "$skill" "$OPENCLAW_SKILLS_DIR/$skill_name/"
        done
        echo "同步完成!"
        ;;
    2)
        echo "可用Skill:"
        ls -1 "$SKILLFRAME_DIR"/skills/
        echo ""
        read -p "输入Skill名称: " skill_name
        if [ -d "$SKILLFRAME_DIR/skills/$skill_name" ]; then
            echo "同步: $skill_name"
            rsync -av --delete "$SKILLFRAME_DIR/skills/$skill_name/" "$OPENCLAW_SKILLS_DIR/$skill_name/"
            echo "同步完成!"
        else
            echo "错误: Skill不存在"
        fi
        ;;
    3)
        echo "查看差异..."
        for skill in "$SKILLFRAME_DIR"/skills/*/; do
            skill_name=$(basename "$skill")
            if [ -d "$OPENCLAW_SKILLS_DIR/$skill_name" ]; then
                echo ""
                echo "=== $skill_name ==="
                diff -r "$skill" "$OPENCLAW_SKILLS_DIR/$skill_name/" 2>/dev/null || true
            else
                echo ""
                echo "=== $skill_name (仅本地存在) ==="
            fi
        done
        ;;
    4)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选项"
        exit 1
        ;;
esac