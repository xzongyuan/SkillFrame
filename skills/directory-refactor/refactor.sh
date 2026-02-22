#!/bin/bash
# Directory Refactor Skill 入口脚本

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${1:-$(pwd)}"
COMMAND="${2:-help}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
Directory Refactor Skill - 全自动目录重构工具

用法:
    ./refactor.sh <workspace> <command> [options]

命令:
    analyze         分析目录结构
    plan            生成重构计划
    execute         执行重构
    verify          验证重构结果
    rollback        回滚重构
    test            运行测试
    help            显示帮助

示例:
    # 分析当前目录
    ./refactor.sh . analyze

    # 执行重构
    ./refactor.sh /root/.openclaw/workspace execute

    # 回滚
    ./refactor.sh /root/.openclaw/workspace rollback --timestamp 20260221-235500

EOF
}

cmd_analyze() {
    log_info "分析目录结构: $WORKSPACE"
    python3 "$SKILL_DIR/lib/refactor.py" --workspace "$WORKSPACE" --analyze
}

cmd_execute() {
    log_info "执行目录重构: $WORKSPACE"
    
    # 预检
    log_info "预检中..."
    if [ ! -d "$WORKSPACE/.git" ]; then
        log_warn "工作空间不是Git仓库，无法回滚"
    fi
    
    # 执行
    python3 "$SKILL_DIR/lib/refactor.py" --workspace "$WORKSPACE" --execute
    
    log_info "重构完成"
}

cmd_test() {
    log_info "运行测试..."
    cd "$SKILL_DIR"
    python3 -m pytest tests/ -v
}

# 主逻辑
case "$COMMAND" in
    analyze)
        cmd_analyze
        ;;
    execute)
        cmd_execute
        ;;
    test)
        cmd_test
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "未知命令: $COMMAND"
        show_help
        exit 1
        ;;
esac
