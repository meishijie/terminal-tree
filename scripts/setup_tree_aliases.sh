#!/bin/bash
# 设置Tree命令的多个版本和别名

echo "🌲 设置 Tree 命令别名和版本..."

# 当前项目路径
PROJECT_PATH="/Volumes/meiMacMedia/app/monogames"

# 备份现有的shell配置
SHELL_CONFIG="$HOME/.zshrc"
if [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

echo "📝 备份当前配置..."
cp "$SHELL_CONFIG" "${SHELL_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"

# 移除现有的tree函数（如果存在）
echo "🧹 清理现有的tree配置..."
sed -i '' '/# Python Terminal Tree 应用/,/^$/d' "$SHELL_CONFIG"
sed -i '' '/tree() {/,/^}$/d' "$SHELL_CONFIG"

# 添加新的tree配置
echo "✨ 添加新的Tree配置..."
cat >> "$SHELL_CONFIG" << EOF

# ==========================================
# Python Terminal Tree 应用配置
# ==========================================

# 全功能版本tree命令
tree() {
    local target_path="\${1:-\$(pwd)}"

    # 验证路径
    if [[ ! -d "\$target_path" ]]; then
        echo "❌ 错误: 目录 '\$target_path' 不存在"
        return 1
    fi

    # 首先尝试全局安装版本
    if [[ -x "\$HOME/.local/bin/tree" ]]; then
        "\$HOME/.local/bin/tree" "\$target_path"
    else
        # 备用：使用项目本地版本
        if [[ -f "$PROJECT_PATH/test_app.py" ]]; then
            cd "$PROJECT_PATH"
            python test_app.py "\$target_path"
            cd - > /dev/null
        else
            echo "❌ Tree应用未找到。请检查安装或运行 ./install_simple_tree.sh"
            return 1
        fi
    fi
}

# 其他版本的别名
alias tree-full='cd "$PROJECT_PATH" && python test_app.py'
alias tree-compact='cd "$PROJECT_PATH" && python compact_tree.py'
alias tree-simple='cd "$PROJECT_PATH" && python simple_tree_app.py'
alias tree-minimal='cd "$PROJECT_PATH" && python minimal_tree.py'

# 传统tree命令（如果需要）
alias tree-brew='/opt/homebrew/bin/tree 2>/dev/null || /usr/bin/tree 2>/dev/null || echo "❌ 传统tree命令未找到"'

# 帮助命令
tree-help() {
    echo "🌲 Python Terminal Tree 使用指南"
    echo "================================="
    echo ""
    echo "主要命令:"
    echo "  tree [path]       - 启动全功能Tree应用"
    echo "  tree-full [path]  - 启动完整版（三面板布局）"
    echo "  tree-simple       - 启动简化版（双面板布局）"
    echo "  tree-compact      - 启动紧凑版（单面板布局）"
    echo "  tree-minimal      - 启动最简版"
    echo "  tree-brew         - 使用传统命令行tree"
    echo ""
    echo "应用内快捷键:"
    echo "  ↑/↓ - 上下导航    ←/→ - 展开/折叠"
    echo "  Enter - 进入      Backspace - 返回上级"
    echo "  g - 编辑路径      F5 - 刷新"
    echo "  Ctrl+H - 隐藏文件 Tab - 切换面板"
    echo "  q - 退出"
    echo ""
}

EOF

echo "✅ Tree配置已更新"

# 重新加载配置
source "$SHELL_CONFIG"

echo ""
echo "🎉 Tree命令设置完成！"
echo ""
echo "💡 可用命令:"
echo "  tree              - 主要Tree应用"
echo "  tree /path        - 在指定目录启动"
echo "  tree-full         - 完整版"
echo "  tree-compact      - 紧凑版"
echo "  tree-simple       - 简化版"
echo "  tree-minimal      - 最简版"
echo "  tree-help         - 显示帮助"
echo ""
echo "🔄 重新启动终端或运行: source $SHELL_CONFIG"