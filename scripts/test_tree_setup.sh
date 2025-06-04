#!/bin/bash
# 测试Tree命令设置

echo "🧪 测试 Python Tree 命令设置"
echo "============================="

# 获取脚本所在目录的父目录作为项目路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="$(dirname "$SCRIPT_DIR")"

# 检查项目目录
echo "1. 检查项目目录..."
if [[ -d "$PROJECT_PATH" ]]; then
    echo "   ✅ 项目目录存在: $PROJECT_PATH"
else
    echo "   ❌ 项目目录不存在: $PROJECT_PATH"
    exit 1
fi

# 检查Python应用文件
echo "2. 检查应用文件..."
apps=(
    "run.py:主启动脚本"
    "examples/compact_tree.py:紧凑版应用"
    "examples/simple_tree_app.py:简化版应用"
)

for app_info in "${apps[@]}"; do
    IFS=':' read -r app_file app_desc <<< "$app_info"
    if [[ -f "$PROJECT_PATH/$app_file" ]]; then
        echo "   ✅ $app_desc ($app_file)"
    else
        echo "   ❌ $app_desc ($app_file) - 缺失"
    fi
done

# 检查全局安装
echo "3. 检查全局tree命令..."
if [[ -x "$HOME/.local/bin/tree" ]]; then
    echo "   ✅ 全局tree命令已安装: $HOME/.local/bin/tree"
else
    echo "   ⚠️  全局tree命令未安装，将使用本地版本"
fi

# 检查Python依赖
echo "4. 检查Python依赖..."
cd "$PROJECT_PATH"
if python -c "import textual, rich" 2>/dev/null; then
    echo "   ✅ Python依赖已安装 (textual, rich)"
else
    echo "   ❌ Python依赖缺失"
    echo "   💡 请运行: pip install textual rich"
    exit 1
fi

# 检查shell配置
echo "5. 检查shell配置..."
SHELL_CONFIG="$HOME/.zshrc"
if [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
fi

if grep -q "Python Terminal Tree" "$SHELL_CONFIG" 2>/dev/null; then
    echo "   ✅ Shell配置包含Tree设置"
else
    echo "   ⚠️  Shell配置可能需要更新"
    echo "   💡 请运行: ./setup_tree_aliases.sh"
fi

echo ""
echo "🚀 测试命令（请在新终端中测试）:"
echo "   tree              # 启动Tree应用"
echo "   tree /tmp         # 浏览/tmp目录"
echo "   tree-compact      # 紧凑版"
echo "   tree-help         # 显示帮助"

echo ""
echo "📋 手动测试步骤:"
echo "1. 打开新终端"
echo "2. 运行: tree"
echo "3. 使用快捷键: ↑↓←→, Enter, q"

echo ""
echo "✅ 测试完成！" 